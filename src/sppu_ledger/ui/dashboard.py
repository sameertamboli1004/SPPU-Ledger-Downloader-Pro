from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from ui.stat_card import StatCard


class Dashboard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Welcome to SPPU Ledger Downloader Pro"
        )
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.downloads_card = StatCard("Downloads")
        self.ledgers_card = StatCard("Ledgers")
        self.errors_card = StatCard("Errors")

        cards_layout.addWidget(self.downloads_card)
        cards_layout.addWidget(self.ledgers_card)
        cards_layout.addWidget(self.errors_card)

        layout.addLayout(cards_layout)

        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("sectionTitle")

        activity_label = QLabel("No activity yet")
        activity_label.setObjectName("activityPlaceholder")

        layout.addWidget(activity_title)
        layout.addWidget(activity_label)

        layout.addStretch()