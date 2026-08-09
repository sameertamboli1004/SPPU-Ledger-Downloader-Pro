from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
)


class NavigationPanel(QFrame):
    page_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumWidth(60)
        self.setMaximumWidth(220)

        layout = QVBoxLayout(self)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.clicked.connect(self.toggle)

        layout.addWidget(self.toggle_button)

        self.buttons = []

        self.add_navigation_button("Dashboard", "dashboard", layout)
        self.add_navigation_button("Download Ledger", "download", layout)
        self.add_navigation_button("Download History", "history", layout)
        self.add_navigation_button("Settings", "settings", layout)

        layout.addStretch()

        self.expanded = True

    def add_navigation_button(self, text, page_name, layout):
        button = QPushButton(text)
        button.setFixedHeight(42)
        button.clicked.connect(
            lambda: self.page_selected.emit(page_name)
        )

        self.buttons.append(button)
        layout.addWidget(button)

    def toggle(self):
        self.expanded = not self.expanded

        if self.expanded:
            self.setMaximumWidth(220)

            self.toggle_button.setText("☰")

            for button in self.buttons:
                button.show()

        else:
            self.setMaximumWidth(60)

            self.toggle_button.setText("☰")

            for button in self.buttons:
                button.hide()