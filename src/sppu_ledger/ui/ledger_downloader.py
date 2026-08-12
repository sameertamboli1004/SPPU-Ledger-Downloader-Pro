from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class LedgerDownloader(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Page heading
        title = QLabel("Ledger Downloader")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Configure the SPPU ledger download before starting."
        )
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Configuration group
        config_group = QGroupBox("SPPU Ledger Configuration")
        config_group.setObjectName("configGroup")

        form = QFormLayout(config_group)
        form.setContentsMargins(20, 20, 20, 20)
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        # University
        self.university_combo = QComboBox()
        self.university_combo.addItem("SPPU")

        form.addRow("University / Portal", self.university_combo)

        # Academic year
        self.academic_year_combo = QComboBox()
        self.academic_year_combo.addItems(
            [
                "2025-26",
                "2024-25",
                "2023-24",
            ]
        )

        form.addRow("Academic Year", self.academic_year_combo)

        # Examination
        self.examination_combo = QComboBox()
        self.examination_combo.addItem(
            "Select examination"
        )

        form.addRow("Examination", self.examination_combo)

        # Ledger type
        self.ledger_type_combo = QComboBox()
        self.ledger_type_combo.addItem(
            "Select ledger type"
        )

        form.addRow("Ledger Type", self.ledger_type_combo)

        layout.addWidget(config_group)

        # Download button
        self.download_button = QPushButton(
            "Start Download"
        )
        self.download_button.setObjectName(
            "primaryButton"
        )
        self.download_button.setMinimumHeight(44)

        self.download_button.clicked.connect(
            self.start_download
        )

        layout.addWidget(self.download_button)

        # Status section
        status_group = QGroupBox("Status")
        status_group.setObjectName("statusGroup")

        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(
            20, 15, 20, 15
        )

        self.status_label = QLabel(
            "Ready to download"
        )
        self.status_label.setObjectName(
            "statusLabel"
        )

        status_layout.addWidget(self.status_label)

        layout.addWidget(status_group)

        layout.addStretch()

    def start_download(self):
        self.status_label.setText(
            "Download function will be connected to the SPPU service."
        )