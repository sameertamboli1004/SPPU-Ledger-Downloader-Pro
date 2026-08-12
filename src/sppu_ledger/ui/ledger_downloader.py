from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QFormLayout,
    QGroupBox,
    QLabel,
    QProgressBar,
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

        # -------------------------------------------------
        # SPPU Ledger Configuration
        # -------------------------------------------------
        config_group = QGroupBox(
            "SPPU Ledger Configuration"
        )
        config_group.setObjectName("configGroup")

        form = QFormLayout(config_group)
        form.setContentsMargins(20, 20, 20, 20)
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        # University / Portal
        self.university_combo = QComboBox()
        self.university_combo.addItem("SPPU")
        self.university_combo.setEnabled(False)

        form.addRow(
            "University / Portal",
            self.university_combo,
        )

        # Academic Year
        self.academic_year_combo = QComboBox()
        self.academic_year_combo.addItems(
            [
                "2025-26",
                "2024-25",
                "2023-24",
            ]
        )

        form.addRow(
            "Academic Year",
            self.academic_year_combo,
        )

        # Exam Session / Period
        self.session_combo = QComboBox()

        self.session_combo.addItem(
            "Select session / period"
        )

        # Session / period options will be
        # populated dynamically from the SPPU portal.
        self.session_combo.setEnabled(False)

        form.addRow(
            "Exam Session / Period",
            self.session_combo,
        )

        layout.addWidget(config_group)

        # -------------------------------------------------
        # Download Button
        # -------------------------------------------------
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

        layout.addWidget(
            self.download_button
        )

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------
        progress_group = QGroupBox("Progress")
        progress_group.setObjectName(
            "statusGroup"
        )

        progress_layout = QVBoxLayout(
            progress_group
        )
        progress_layout.setContentsMargins(
            20, 15, 20, 15
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        progress_layout.addWidget(
            self.progress_bar
        )

        layout.addWidget(
            progress_group
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------
        status_group = QGroupBox("Status")
        status_group.setObjectName(
            "statusGroup"
        )

        status_layout = QVBoxLayout(
            status_group
        )
        status_layout.setContentsMargins(
            20, 15, 20, 15
        )

        self.status_label = QLabel(
            "Ready to download"
        )
        self.status_label.setObjectName(
            "statusLabel"
        )

        status_layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            status_group
        )

        layout.addStretch()

    def start_download(self):
        academic_year = (
            self.academic_year_combo.currentText()
        )

        session = (
            self.session_combo.currentText()
        )

        if session == "Select session / period":
            self.status_label.setText(
                "Please select an exam session / period."
            )
            return

        self.download_button.setEnabled(False)

        self.status_label.setText(
            f"Preparing SPPU Ledger download — "
            f"{academic_year}, {session}"
        )

        self.progress_bar.setValue(10)

        # Actual SPPU portal downloader service
        # will be connected here.

        self.progress_bar.setValue(100)

        self.status_label.setText(
            "Download service is ready to be connected."
        )

        self.download_button.setEnabled(True)