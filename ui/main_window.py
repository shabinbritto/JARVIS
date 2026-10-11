
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QDialog,
    QMessageBox,
)

from PySide6.QtCore import Qt

from core.assistant import Jarvis
from security.privacy_shield import (
    PrivacyShield,
    PrivacyRequest,
)
from security.permission_dialog import PermissionDialog
from security.message_classifier import MessageClassifier


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.jarvis = Jarvis()
        self.privacy_shield = PrivacyShield()
        self.message_classifier = MessageClassifier()

        self.setWindowTitle("Jarvis")
        self.setMinimumSize(800, 600)

        self.create_interface()

    def create_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title = QLabel("🤖 JARVIS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 15px;
        """)
        main_layout.addWidget(title)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
        """)
        main_layout.addWidget(self.chat_area)

        bottom_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText(
            "Ask Jarvis something..."
        )
        self.input_box.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
        """)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            font-size: 16px;
            padding: 12px 20px;
        """)

        bottom_layout.addWidget(self.input_box)
        bottom_layout.addWidget(self.send_button)
        main_layout.addLayout(bottom_layout)

        self.privacy_test_button = QPushButton(
            "Test Privacy Permission"
        )

        self.ai_test_button = QPushButton(
            "Ask AI (Privacy Test)"
        )

        main_layout.addWidget(self.privacy_test_button)
        main_layout.addWidget(self.ai_test_button)

        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        self.privacy_test_button.clicked.connect(
            self.test_privacy_permission
        )

        self.ai_test_button.clicked.connect(
            self.test_ai_permission_flow
        )

        self.chat_area.append(
            "<b>Jarvis:</b> Hello! I'm Jarvis. "
            "How can I help you?"
        )

    def send_message(self):
        user_input = self.input_box.text().strip()

        if not user_input:
            return

        self.chat_area.append(
            f"<b>You:</b> {user_input}"
        )

        response = self.jarvis.process(user_input)

        self.chat_area.append(
            f"<b>Jarvis:</b> {response}"
        )

        self.input_box.clear()
        self.input_box.setFocus()

    def request_ai_permission(
        self,
        purpose,
        category,
        content,
    ):
        classification = self.message_classifier.classify(content)

        if classification.category == "credentials":
            return self.privacy_shield.create_request(
                purpose,
                "credentials",
                content,
            )

        request = self.privacy_shield.create_request(
            purpose,
            category,
            content,
        )

        if not isinstance(request, PrivacyRequest):
            return request

        dialog = PermissionDialog(
            self,
            purpose,
            category,
            request.content,
            destination="Not connected — local privacy test only",
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.privacy_shield.cancel_request(request)

            return self.privacy_shield.prepare_for_ai(request)

        token = self.privacy_shield._approve_once(request)

        if token is None:
            self.privacy_shield.cancel_request(request)

            return self.privacy_shield.prepare_for_ai(request)

        return self.privacy_shield.prepare_for_ai(
            request,
            token,
        )

    def test_privacy_permission(self):
        result = self.request_ai_permission(
            purpose="Testing the privacy permission system",
            category="study",
            content="My exam is Monday",
        )

        if result.allowed:
            QMessageBox.information(
                self,
                "Privacy Test",
                "Permission approved for this request.\n\n"
                "No data was sent to an AI model.",
            )
        else:
            QMessageBox.information(
                self,
                "Privacy Test",
                "Request blocked.\n\n" + result.reason,
            )

    def test_ai_permission_flow(self):
        result = self.request_ai_permission(
            purpose="Test an AI-generated study plan",
            category="study",
            content="My exam is Monday",
        )

        if not result.allowed:
            self.chat_area.append(
                "<b>Jarvis:</b> AI test blocked. "
                + result.reason
            )
            return

        ai_result = self.jarvis.ai_gateway.ask(
            "Create a study plan.",
            contains_personal_data=True,
            personal_data_result=result,
        )

        self.chat_area.append(
            "<b>Jarvis:</b> " + ai_result.reason
        )


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

