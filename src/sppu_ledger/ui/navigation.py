from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class NavigationPanel(QFrame):
    page_selected = Signal(str)
    toggle_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("navigationPanel")
        self.expanded = True

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(6)

        # Header
        header = QHBoxLayout()
        header.setSpacing(8)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setObjectName("navToggle")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.clicked.connect(self.toggle_requested.emit)

        self.logo_label = QLabel("SPPU Ledger")
        self.logo_label.setObjectName("navLogo")

        header.addWidget(self.toggle_button)
        header.addWidget(self.logo_label)

        layout.addLayout(header)

        # Navigation buttons
        self.buttons = {}

        pages = [
            ("dashboard", "Dashboard"),
            ("downloader", "Ledger Downloader"),
            ("history", "Download History"),
            ("settings", "Settings"),
            ("about", "About"),
        ]

        for page_id, title in pages:
            button = QPushButton(title)
            button.setObjectName("navButton")
            button.setMinimumHeight(42)

            button.clicked.connect(
                lambda checked=False, page=page_id:
                self.page_selected.emit(page)
            )

            self.buttons[page_id] = button
            layout.addWidget(button)

        layout.addStretch()

        self.setFixedWidth(230)

    def set_expanded(self, expanded):
        self.expanded = expanded

        if expanded:
            self.setFixedWidth(230)
            self.logo_label.show()

            for page_id, button in self.buttons.items():
                button.setText(self._button_title(page_id))

        else:
            self.setFixedWidth(65)
            self.logo_label.hide()

            symbols = {
                "dashboard": "⌂",
                "downloader": "↓",
                "history": "↶",
                "settings": "⚙",
                "about": "ⓘ",
            }

            for page_id, button in self.buttons.items():
                button.setText(symbols[page_id])

    @staticmethod
    def _button_title(page_id):
        titles = {
            "dashboard": "Dashboard",
            "downloader": "Ledger Downloader",
            "history": "Download History",
            "settings": "Settings",
            "about": "About",
        }

        return titles[page_id]