from typing import cast

from . import keys_tab
from .component import LineEdit, grid_layout, warning_callback
from .model import AppData, ConfigProxy
from .parallel import run_thread
from .pyside import QtWidgets, QtCore
from ..core import crypt


class KeyDownloadDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data
        self.setWindowTitle("Download public keys from keyserver")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.key_identifier = LineEdit()
        self.btn_download = QtWidgets.QPushButton("Download")
        self.btn_download.clicked.connect(self.download)  # type: ignore
        self.btn_download.setEnabled(False)

        self.key_identifier.textChanged.connect(  # type: ignore
            lambda text: self.btn_download.setEnabled(bool(text))
        )

        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)  # type: ignore

        self.setLayout(
            grid_layout(
                (
                    QtWidgets.QLabel(
                        "Enter an identifier (fingerprint, key ID or email)"
                    ),
                ),
                (self.key_identifier, self.btn_download),
                (None, btn_box),
            )
        )

    @property
    def config(self) -> ConfigProxy:
        return self.app_data.config

    def download(self) -> None:
        """Download key identified by given input to user's local keyring."""

        key_identifier = self.key_identifier.text()

        def on_result() -> None:
            self.app_data.update_public_keys()
            cast(
                keys_tab.KeysTab, self.parentWidget()
            ).update_display_selected_pub_key()
            try:
                key = crypt.search_pub_key(
                    key_identifier, self.config.gpg_store, sigs=False
                )
                keys_tab.ok_message(
                    "Download key",
                    (
                        "Following public key has been downloaded from the keyserver:",
                        f"{key.uids[0].email} ({key.fingerprint})",
                        "Please verify that the fingerprint is correct (otherwise delete the key).",
                    ),
                    self.parentWidget(),
                )()
            except crypt.UnpackError:
                # No (new) key has been downloaded resp. no single key could be found for given
                # key identifier.
                pass
            self.btn_download.setEnabled(True)
            self.close()

        self.btn_download.setEnabled(False)
        run_thread(
            crypt.download_keys,
            f_kwargs=dict(
                key_identifiers=[self.key_identifier.text()],
                keyserver=self.config.keyserver_url,
                gpg_store=self.config.gpg_store,
            ),
            report_config=self.config,
            forward_errors=warning_callback("GPG key search error"),
            signals=dict(
                result=on_result,
            ),
        )
