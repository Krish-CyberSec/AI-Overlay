from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Qt, QThread, Signal
from app.ai.client import ask_ai
import pyautogui
class AIWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question

    def run(self):
        try:
            answer = ask_ai(self.question)
            self.finished.emit(answer)

        except Exception as error:
            self.error.emit(str(error))
class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Overlay")
        self.resize(600, 350)

        self.setWindowFlag(
            Qt.WindowType.WindowStaysOnTopHint,
            True,
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("AI Overlay")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        subtitle = QLabel("Ask your question")

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Type your question..."
        )

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.handle_question)
        self.insert_button = QPushButton("Insert Answer")
        self.insert_button.clicked.connect(self.insert_answer)
        self.insert_button.setEnabled(False)

        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setPlaceholderText(
            "Response will appear here..."
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.question_input)
        layout.addWidget(self.ask_button)
        layout.addWidget(self.insert_button)
        layout.addWidget(self.answer_box)
        self.setLayout(layout)

    def handle_question(self):
        question = self.question_input.text().strip()

        if not question:
            self.answer_box.setPlainText(
                "Please enter a question."
            )
            return

        self.answer_box.setPlainText("Thinking...")
        self.ask_button.setEnabled(False)

        self.worker = AIWorker(question)

        self.worker.finished.connect(self.handle_ai_response)
        self.worker.error.connect(self.handle_ai_error)

        self.worker.start()
    def handle_ai_response(self, answer):
        self.answer_box.setPlainText(answer)
        self.ask_button.setEnabled(True)
        self.insert_button.setEnabled(True)


    def handle_ai_error(self, error):
        self.answer_box.setPlainText(
            f"Error:\n\n{error}"
        )
        self.ask_button.setEnabled(True)
        self.insert_button.setEnabled(False)

    def insert_answer(self):
        answer = self.answer_box.toPlainText().strip()

        if not answer or answer == "Thinking...":
            return

        self.hide()

        pyautogui.write(
            answer,
            interval=0.01,
        )
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.question_input.setFocus()
    