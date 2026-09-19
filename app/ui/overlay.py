from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PySide6.QtCore import Qt, QThread, Signal, QPoint
from app.ai.client import ask_ai
import pyautogui
import pyperclip
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

        self.setStyleSheet("""
    QWidget {
        background-color: #0B1120;
        color: #E5E7EB;
        font-family: "Segoe UI";
    }

    QLineEdit {
        background-color: #111827;
        color: #F9FAFB;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
    }

    QPushButton {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 9px 14px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton:disabled {
        background-color: #374151;
        color: #9CA3AF;
    }
""")

        self.setup_ui()
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

        super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

        super().mouseMoveEvent(event)

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

        self.copy_button = QPushButton("Copy Answer")
        self.copy_button.clicked.connect(self.copy_answer)
        self.copy_button.setEnabled(False)



        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setPlaceholderText(
            "Your answer will appear here..."
        )

        self.answer_box.setStyleSheet("""
            QTextEdit {
                background-color: #111827;
                color: #E5E7EB;
                border: 1px solid #374151;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                selection-background-color: #374151;
            }
            
            QScrollBar:vertical {
                background: #111827;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #374151;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.question_input)
        layout.addWidget(self.ask_button)
        layout.addWidget(self.insert_button)
        layout.addWidget(self.copy_button)
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
        self.copy_button.setEnabled(True)

    def handle_ai_error(self, error):
        self.answer_box.setPlainText(
            f"Error:\n\n{error}"
        )
        self.ask_button.setEnabled(True)
        self.insert_button.setEnabled(False)
        self.copy_button.setEnabled(False)

    def insert_answer(self):
        answer = self.answer_box.toPlainText().strip()

        if not answer or answer == "Thinking...":
            return

        pyperclip.copy(answer)

        self.hide()

        pyautogui.hotkey("ctrl", "v")

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.question_input.setFocus()

    def copy_answer(self):
        answer = self.answer_box.toPlainText().strip()

        if not answer or answer == "Thinking...":
            return

        pyperclip.copy(answer)
    