from libbiomedit.lib.secret import Secret

from .model import AppData, ConfigProxy
from ..core import gpg, crypt
from ..core.error import UserError
from .component import (
    LineEdit,
    grid_layout,
    GridLayoutCell,
    NormalMessageBox,
    show_warning,
    warning_callback,
)

from .parallel import run_thread
from .pyside import QtWidgets, QtCore, QtGui, open_window


class KeyGenDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data
        self.setWindowTitle("Generate new key pair")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.text_name_full = LineEdit()
        self.text_name_extra = LineEdit()
        self.text_email = LineEdit()
        self.text_pass = LineEdit()
        self.text_pass_repeat = LineEdit()
        self.toggle_password_visibility(False)

        re_email = QtCore.QRegularExpression(r"[^@]+@[^@]+\.[^@]+")
        self.text_email.setValidator(QtGui.QRegularExpressionValidator(re_email))

        self.btn_run = QtWidgets.QPushButton("Generate key")
        self.btn_run.setDefault(True)
        self.btn_run.clicked.connect(self.create_private_key)  # type: ignore
        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)  # type: ignore
        btn_show_pass = QtWidgets.QPushButton("Show")
        btn_show_pass.setCheckable(True)
        btn_show_pass.clicked.connect(self.toggle_password_visibility)  # type: ignore

        self.setLayout(
            grid_layout(
                (QtWidgets.QLabel("Full name"), self.text_name_full),
                (
                    QtWidgets.QLabel("(optional) institution/project"),
                    self.text_name_extra,
                ),
                (QtWidgets.QLabel("Institutional email"), self.text_email),
                (QtWidgets.QLabel("Password"), self.text_pass),
                (
                    QtWidgets.QLabel("Password (repeat)"),
                    self.text_pass_repeat,
                    btn_show_pass,
                ),
                (btn_cancel, self.btn_run),
                (
                    GridLayoutCell(
                        QtWidgets.QLabel("Key generation can take a few minutes"),
                        span=3,
                    ),
                ),
            )
        )

    def toggle_password_visibility(self, show: bool) -> None:
        mode = QtWidgets.QLineEdit.Normal if show else QtWidgets.QLineEdit.Password
        self.text_pass.setEchoMode(mode)
        self.text_pass_repeat.setEchoMode(mode)

    def clear_form(self) -> None:
        self.text_name_full.clear()
        self.text_name_extra.clear()
        self.text_email.clear()
        self.text_pass.clear()
        self.text_pass_repeat.clear()

    def post_key_creation(self, key: gpg.Key) -> None:
        msg = NormalMessageBox(self.parentWidget(), "GPG Key Generation")
        try:
            revocation_cert = crypt.create_revocation_certificate(
                key.fingerprint,
                self.text_pass.text(),
                self.config.gpg_store,
            )
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(
                revocation_cert_creation_successful_text.format(
                    self.config.dcc_portal_url
                )
            )
            msg.setDetailedText(revocation_cert.decode())
            # Programmatically click the "Show Details..." button so that the
            # certificate is shown by default.
            click_show_details(msgbox=msg)

        except UserError:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                revocation_cert_creation_failed_text.format(
                    self.config.dcc_portal_url, key.fingerprint
                )
            )
        finally:
            open_window(msg)
            self.clear_form()
            self.app_data.update_private_keys()
            self.app_data.update_public_keys()
            self.close()

    @property
    def config(self) -> ConfigProxy:
        return self.app_data.config

    def create_private_key(self) -> None:
        self.btn_run.setEnabled(False)
        name_full = self.text_name_full.text().strip()
        name_extra = self.text_name_extra.text().strip()
        if name_extra:
            if not name_extra.startswith("(") and not name_extra.endswith(")"):
                name_extra = f"({name_extra})"
            name_full = name_full + " " + name_extra
        if self.text_pass.text() != self.text_pass_repeat.text():
            show_warning(
                "GPG Key Generation Error",
                "Password and repeated password do not match.",
                self,
            )
            self.btn_run.setEnabled(True)
            return

        run_thread(
            crypt.create_key,
            f_kwargs=dict(
                full_name=name_full,
                email=self.text_email.text(),
                pwd=Secret(self.text_pass.text()),
                gpg_store=self.config.gpg_store,
            ),
            forward_errors=warning_callback("GPG Key Generation Error"),
            report_config=self.config,
            signals=dict(
                result=self.post_key_creation,
                finished=lambda: self.btn_run.setEnabled(True),
            ),
        )


def click_show_details(msgbox: QtWidgets.QMessageBox) -> None:
    for button in msgbox.buttons():
        if msgbox.buttonRole(button) is QtWidgets.QMessageBox.ButtonRole.ActionRole:
            button.click()


post_key_creation_text = """Your new key has been successfully generated.

Upload your public key to the keyserver by selecting it in the Public keys list and clicking on the upload button.

To get your key approved, please [connect to the portal]({0}/keys).

"""

revocation_cert_creation_successful_text = (
    post_key_creation_text
    + """Additionally, a [revocation certificate](https://sett.rtfd.io/en/stable/key_management.html?#revocation-certificates)
has been issued. Please store the revocation certificate below in a safe location.
"""
)

revocation_cert_creation_failed_text = (
    post_key_creation_text
    + """However, it was not possible to create a revocation certificate for it.
Please execute the following command to create the certificate:
```
gpg --gen-revoke {1}
```"""
)
