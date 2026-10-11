
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)


class PermissionDialog(QDialog):

    def __init__(
        self,
        parent,
        purpose,
        category,
        content,
        destination="Not connected — privacy test only",
    ):
        super().__init__(parent)

        self.setWindowTitle("Jarvis Privacy Permission")
        self.setMinimumSize(520, 460)

        self.approved = False

        layout = QVBoxLayout(self)

        title = QLabel("🔐 Jarvis Privacy Permission")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        layout.addWidget(title)

        warning = QLabel(
            "Review the information below before deciding. "
            "Approval applies only to this request."
        )
        warning.setWordWrap(True)
        layout.addWidget(warning)

        destination_label = QLabel(
            "Destination: " + destination
        )
        destination_label.setWordWrap(True)
        destination_label.setStyleSheet(
            "font-weight: bold; padding: 5px;"
        )
        layout.addWidget(destination_label)

        purpose_label = QLabel("Purpose: " + purpose)
        purpose_label.setWordWrap(True)
        layout.addWidget(purpose_label)

        category_label = QLabel("Data category: " + category)
        category_label.setWordWrap(True)
        layout.addWidget(category_label)

        layout.addWidget(
            QLabel("Exact information proposed for sharing:")
        )

        preview = QTextEdit()
        preview.setReadOnly(True)
        preview.setPlainText(content)
        layout.addWidget(preview)

        note = QLabel(
            "Passwords, private keys, and authentication tokens "
            "must never be sent to an AI model. Automatic secret "
            "detection is not perfect. Review the information "
            "carefully before approving."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #c0392b;")
        layout.addWidget(note)

        test_notice = QLabel(
            "Current status: No AI model is connected. "
            "This permission test sends no data to a model."
        )
        test_notice.setWordWrap(True)
        layout.addWidget(test_notice)

        buttons = QHBoxLayout()

        deny_button = QPushButton("Deny")
        allow_button = QPushButton("Allow Once")

        buttons.addWidget(deny_button)
        buttons.addWidget(allow_button)

        layout.addLayout(buttons)

        deny_button.clicked.connect(self.deny)
        allow_button.clicked.connect(self.allow)

    def deny(self):
        self.approved = False
        self.reject()

    def allow(self):
        self.approved = True
        self.accept()