from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class Dashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Dashboard")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel(
            "Welcome to SPPU Ledger Downloader Pro"
        )
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #64748b;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()