from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel
)

from PySide6.QtCore import Qt

from core.assistant import Jarvis


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.jarvis = Jarvis()

        self.setWindowTitle("Jarvis")
        self.setMinimumSize(800, 600)

        self.create_interface()

    def create_interface(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

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

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input_box.returnPressed.connect(
            self.send_message
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