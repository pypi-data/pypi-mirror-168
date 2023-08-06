import html
import logging
import warnings
from pathlib import Path
from typing import (
    Any,
    Callable,
    Iterator,
    Sequence,
    Tuple,
    cast,
)

from sett.core.error import UserError
from .component import (
    GridLayoutCell,
    SelectionAction,
    ToolBar,
    grid_layout,
    warning_callback,
    NormalMessageBox,
)
from .key_generation_dialog import KeyGenDialog
from .keys_download_dialog import KeyDownloadDialog
from .model import AppData, KeyValueListModel
from .parallel import run_thread
from .pyside import QAction, QtCore, QtWidgets, open_window
from .theme import Action, IconRepainterWidget
from ..core import crypt, gpg
from ..workflows import upload_keys as upload_keys_workflow


class KeysTab(IconRepainterWidget):
    def __init__(self, parent: QtWidgets.QMainWindow, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data

        self.text_panel = QtWidgets.QTextEdit()
        self.text_panel.setReadOnly(True)

        self.priv_keys_view = QtWidgets.QListView()
        self.priv_keys_view.setModel(self.app_data.priv_keys_model)
        self.priv_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            self._update_display
        )

        self.pub_keys_view = QtWidgets.QListView()
        self.pub_keys_view.setModel(self.app_data.pub_keys_model)
        self.pub_keys_view.selectionModel().currentChanged.connect(self._update_display)  # type: ignore
        self.pub_keys_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        # When item is selected in the public/private key list, clear
        # the selection in the other list.
        self.priv_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            lambda: self.pub_keys_view.selectionModel().clear()
        )
        self.pub_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            lambda: self.priv_keys_view.selectionModel().clear()
        )

        action_generate_key = Action(
            ":icon/feather/plus-square.png",
            "Generate new private/public key",
            self,
        )
        action_generate_key.triggered.connect(  # type: ignore
            lambda: KeyGenDialog(parent=self, app_data=app_data).show()
        )
        action_refresh_keys = Action(
            ":icon/feather/refresh-cw.png",
            "Refresh keys from the local keyring",
            self,
        )

        def refresh_keys() -> None:
            self.app_data.update_private_keys()
            self.app_data.update_public_keys()
            self.update_display_selected_pub_key()

        action_refresh_keys.triggered.connect(refresh_keys)  # type: ignore

        toolbar = ToolBar("Key management", self)
        toolbar.addAction(action_generate_key)
        toolbar.addSeparator()
        for action in self.create_public_keys_actions():
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(action_refresh_keys)

        self.setLayout(
            grid_layout(
                (GridLayoutCell(toolbar, span=2),),
                (QtWidgets.QLabel("Private keys"), QtWidgets.QLabel("Public keys")),
                (self.priv_keys_view, self.pub_keys_view),
                (GridLayoutCell(self.text_panel, span=2),),
            )
        )

    def key_to_html(self, key: gpg.Key) -> str:
        """Represent a PGP key as an HTML string"""

        # Add key info (user ID, key ID, fingerprint, signatures).
        content = ["<table>"]
        rows = [
            ("User ID", html.escape(str(key.uids[0]))),
            ("Key ID", key.key_id),
            ("Key fingerprint", key.fingerprint),
            ("Key length", key.key_length),
        ]
        for k, v in rows:
            content.append(f"<tr><th>{k}</th><td>{v}</td></tr>")

        content.append("<tr><th>Signatures</th><td>")
        content.append(
            "<br>".join(
                [
                    f"{html.escape(str(sig.issuer_uid))} {sig.issuer_key_id} "
                    f"{sig.signature_class}"
                    for sig in key.valid_signatures
                ]
            )
        )
        content.append("</td></tr>")

        # Add key validation info: display whether a key is approved or not.
        content.append("</table>")
        if key.key_type == gpg.KeyType.public:
            if self.app_data.config.offline:
                content.append(
                    '<p class="info">Key approval cannot be verified in '
                    "offline mode.</p>"
                )
            elif not self.app_data.config.verify_key_approval:
                content.append(
                    '<p class="info">Key approval cannot be verified because '
                    "approval verification is disabled in your config file.</p>"
                )
            else:
                # Make a call to portal API to check if the key is approved.
                try:
                    self.app_data.config.portal_api.verify_key_approval(
                        fingerprints=(key.fingerprint,)
                    )
                    content.append('<p class="safe">This key is approved.</p>')
                except RuntimeError as e:
                    # Note: changing "<email>" to "[email]" in the error message
                    # as the text between "< >" is not rendered.
                    error_msg = str(e).replace("<", "[").replace(">", "]")
                    if "not approved" in error_msg:
                        content.append(
                            '<p class="danger">This key is not approved. '
                            f"{error_msg}</p>"
                        )
                    else:
                        content.append(
                            '<p class="info">Key approval could not be '
                            f"verified: {error_msg}</p>"
                        )
        else:
            content.append(
                "<p>This is a private key. Private keys are not subject to "
                "approval.</p>"
            )
        return "".join(content)

    @staticmethod
    def key_to_text(key: gpg.Key) -> str:
        uid = key.uids[0]
        return f"{uid.email} ({key.key_id})"

    def create_public_keys_actions(self) -> Iterator[QAction]:
        selection_model = self.pub_keys_view.selectionModel()

        def offline_action(action: QAction) -> QAction:
            """Force disable button in offline mode."""
            orig = action.text()

            def listener() -> None:
                offline = self.app_data.config.offline
                action.setText(
                    orig + (" (NOT available in offline mode)" if offline else "")
                )
                if isinstance(action, SelectionAction):
                    action.enable_selection(not offline)
                else:
                    action.setEnabled(not offline)

            self.app_data.config.add_listener("offline", listener)
            return action

        # Create a dict of actions (functions) to associate to each
        # action button of the GUI.
        # The reason to create a dict object before looping over it is so
        # that mypy gets the correct typing information (for some reason
        # SelectionAction is not recognized as a subtype of QAction).
        functions_by_action: Sequence[Tuple[QAction, Callable[..., Any]]] = (
            (
                offline_action(
                    Action(
                        ":icon/feather/download-cloud.png",
                        "Download keys from the keyserver",
                        self,
                    )
                ),
                lambda: KeyDownloadDialog(parent=self, app_data=self.app_data).show(),
            ),
            (
                offline_action(
                    SelectionAction(
                        ":icon/feather/upload-cloud.png",
                        "Upload selected keys to the keyserver",
                        self,
                        selection_model=selection_model,
                    )
                ),
                self.upload_key,
            ),
            (
                offline_action(
                    SelectionAction(
                        ":icon/feather/rotate-cw.png",
                        "Update selected keys from the keyserver",
                        self,
                        selection_model=selection_model,
                    )
                ),
                self.update_keys,
            ),
            (
                SelectionAction(
                    ":icon/feather/trash-2.png",
                    "Delete selected keys from your computer",
                    self,
                    selection_model=selection_model,
                ),
                self.delete_keys,
            ),
            (
                Action(
                    ":icon/feather/file-plus.png",
                    "Import key from file",
                    self,
                ),
                self.import_key,
            ),
        )
        for action, fn in functions_by_action:
            action.triggered.connect(fn)  # type: ignore
            yield action

    def get_selected_keys(self) -> Tuple[gpg.Key, ...]:
        """Returns the gpg.Key objects corresponding to the keys currently
        selected in the GUI.
        """
        # Note: it's probably possible to get rid of the cast() here.
        selected_keys = (
            cast(KeyValueListModel, index.model()).get_value(index)
            for index in self.pub_keys_view.selectedIndexes()
        )
        return tuple(selected_keys)

    def update_keys(self) -> None:
        """Update/refresh selected keys from the keyserver."""
        show_ok = ok_message(
            "Updated keys",
            ("Keys have been successfully updated.",),
            parent=self.parentWidget(),
        )
        keys_to_update = self.get_selected_keys()
        if keys_to_update:

            def on_result() -> None:
                self.app_data.update_public_keys()
                self.update_display_selected_pub_key()
                show_ok()

            run_thread(
                crypt.download_keys,
                f_kwargs=dict(
                    key_identifiers=[key.fingerprint for key in keys_to_update],
                    keyserver=self.app_data.config.keyserver_url,
                    gpg_store=self.app_data.config.gpg_store,
                ),
                report_config=self.app_data.config,
                forward_errors=warning_callback("GPG key update error"),
                signals=dict(result=on_result),
            )

    def import_key(self) -> None:
        """Import a GPG key from a local file."""
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select GPG key file", str(Path.home())
        )[0]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG public key import")
        try:
            if path:
                with open(path, encoding="utf-8") as fin:
                    key_data = fin.read()
                crypt.import_keys(key_data, self.app_data.config.gpg_store)
                self.app_data.update_public_keys()
                self.update_display_selected_pub_key()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Key has been imported.")
                open_window(msg)
        except (UnicodeDecodeError, UserError) as e:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(format(e))
            open_window(msg)

    def delete_keys(self) -> None:
        """Delete the selected public keys from the user's local keyring. Only
        public keys with no associated private key can be deleted.
        """
        msg = NormalMessageBox(self.parentWidget(), "Delete public key")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        msg_warn = NormalMessageBox(self.parentWidget(), "GPG key deletion error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        priv_keys = self.app_data.config.gpg_store.list_sec_keys()

        keys_to_delete = self.get_selected_keys()
        msg.set_text_list(
            (
                "Do you really want to delete the following public key(s)?",
                "<br />".join([self.key_to_text(key) for key in keys_to_delete]),
            )
        )
        if open_window(msg) == QtWidgets.QMessageBox.Ok:
            for key in keys_to_delete:
                if any(k for k in priv_keys if key.fingerprint == k.fingerprint):
                    msg_warn.set_text_list(
                        (
                            "Unable to delete key:",
                            f"{KeysTab.key_to_text(key)}",
                            "Deleting private keys (and by extension public keys "
                            "with an associated private key) is not supported by "
                            "this application. Please use an external software  "
                            "such as GnuPG (Linux, MacOS) or Kleopatra (Windows).",
                        )
                    )
                    open_window(msg_warn)
                    continue
                try:
                    crypt.delete_pub_keys(
                        [key.fingerprint], self.app_data.config.gpg_store
                    )
                    self.pub_keys_view.selectionModel().clearSelection()
                except UserError as e:
                    msg_warn.setText(format(e))
                    open_window(msg_warn)
                self.text_panel.clear()
        self.app_data.update_public_keys()

    def upload_key(self) -> None:
        """Uploads selected keys to keyserver specified in the user's config file."""
        key_send_message_box = NormalMessageBox(self.parentWidget(), "Send public key")
        cb = QtWidgets.QCheckBox(
            "Associate the key(s) with your identity (email).", key_send_message_box
        )
        cb.setToolTip(
            "The identity association/verification is done via email "
            "and handled by the keyserver."
            "<p>It only makes sense to verify keys you actually own.</p>"
        )
        cb.setChecked(True)
        key_send_message_box.setCheckBox(cb)
        key_send_message_box.setIcon(QtWidgets.QMessageBox.Question)
        key_send_message_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        show_ok = ok_message(
            "Send public key",
            ("Key has been successfully uploaded to the keyserver.",),
            self.parentWidget(),
        )

        keys_to_upload = self.get_selected_keys()
        key_send_message_box.set_text_list(
            (
                "Do you want to upload selected key(s) to the key server?",
                "<br />".join([self.key_to_text(key) for key in keys_to_upload]),
            )
        )
        if open_window(key_send_message_box) == QtWidgets.QMessageBox.Ok:
            for key in keys_to_upload:
                if (
                    verify_key_length(self.parentWidget(), key)
                    == QtWidgets.QMessageBox.Ok
                ):
                    run_thread(
                        upload_keys_workflow.upload_keys,
                        f_kwargs=dict(
                            fingerprints=[key.fingerprint],
                            verify_key=cb.isChecked(),
                            config=self.app_data.config,
                        ),
                        capture_loggers=(upload_keys_workflow.logger,),
                        report_config=self.app_data.config,
                        forward_errors=warning_callback("GPG key upload error"),
                        signals=dict(
                            result=lambda _: show_ok(),
                        ),
                    )

    def _update_display(self, index: QtCore.QModelIndex) -> None:
        """Display key info summary in GUI text panel."""
        style = (
            "<style>"
            "th {text-align: left; padding: 0 20px 5px 0;}"
            ".danger { color: red;}"
            ".safe { color: green;}"
            "</style>"
        )
        if index.isValid():
            try:
                # Note: it's probably possible to get rid of the cast() here.
                self.text_panel.setHtml(
                    style
                    + self.key_to_html(
                        cast(KeyValueListModel, index.model()).get_value(index)
                    )
                )
            except IndexError:
                self.text_panel.setHtml("")

    def update_display_selected_pub_key(self) -> None:
        """Refresh the displayed key info of the currently selected public keys."""
        self._update_display(self.pub_keys_view.selectionModel().currentIndex())


def ok_message(
    title: str, msg: Tuple[str, ...], parent: QtWidgets.QWidget
) -> Callable[[], Any]:
    msg_ok = NormalMessageBox(parent, title)
    msg_ok.setIcon(QtWidgets.QMessageBox.Information)
    msg_ok.set_text_list(msg)
    return lambda: open_window(msg_ok)


def verify_key_length(
    parent: QtWidgets.QWidget,
    key: gpg.Key,
) -> int:
    """Verifies length and type of given key.
    If some warning or error has been caught up, then an additional popup (asking for user interaction)
    will be displayed. If this is NOT the case, we simply return `QtWidgets.QMessageBox.Ok`
    (meaning everything is fine).
    """
    msg = NormalMessageBox(parent, "Key length verification")
    try:
        with warnings.catch_warnings(record=True) as warns:
            crypt.verify_key_length(key)
            if len(warns) > 0:
                logging.warning(warns[-1].message)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStandardButtons(
                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
                )
                msg.setText(str(warns[-1].message))
    except UserError as exc:
        logging.error(str(exc))
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(str(exc))
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
    return open_window(msg) if len(msg.text()) else int(QtWidgets.QMessageBox.Ok)
