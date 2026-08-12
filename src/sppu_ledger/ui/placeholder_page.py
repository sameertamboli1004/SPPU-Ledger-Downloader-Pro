from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class PlaceholderPage(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")

        description_label = QLabel(description)
        description_label.setObjectName("pageSubtitle")
        description_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(description_label)

        layout.addStretch()