from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QFrame,
)

from services.sppu_portal import (
    SppuPortalService,
)


class PortalWorker(QObject):
    """
    Runs Playwright in its own Qt thread so that the
    application UI remains responsive.
    """

    status = Signal(str)

    connected = Signal(list, list)

    branches_loaded = Signal(list)

    download_completed = Signal(str)

    error = Signal(str)

    finished = Signal()

    def __init__(self):
        super().__init__()

        self.service = None

    # -----------------------------------------------------
    # Connect
    # -----------------------------------------------------

    @Slot()
    def connect_to_sppu(self):

        try:
            self.service = SppuPortalService()

            periods, courses = (
                self.service.connect(
                    self.status.emit
                )
            )

            self.connected.emit(
                periods,
                courses
            )

        except Exception as exc:

            self.error.emit(
                str(exc)
            )

    # -----------------------------------------------------
    # Branches
    # -----------------------------------------------------

    @Slot(str)
    def load_branches(self, course_value):

        try:

            if self.service is None:
                raise RuntimeError(
                    "Connect to SPPU first."
                )

            branches = (
                self.service.get_branches(
                    course_value
                )
            )

            self.branches_loaded.emit(
                branches
            )

        except Exception as exc:

            self.error.emit(
                str(exc)
            )

    # -----------------------------------------------------
    # Download
    # -----------------------------------------------------

    @Slot(str, str, str)
    def download(
        self,
        exam_period,
        course_value,
        branch_value,
    ):

        try:

            if self.service is None:
                raise RuntimeError(
                    "Connect to SPPU first."
                )

            filename = (
                self.service.download_ledger(
                    exam_period,
                    course_value,
                    branch_value,
                    self.status.emit,
                )
            )

            self.download_completed.emit(
                filename
            )

        except Exception as exc:

            self.error.emit(
                str(exc)
            )

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    @Slot()
    def close(self):

        try:

            if self.service is not None:
                self.service.close()

        finally:

            self.finished.emit()


class LedgerDownloader(QFrame):

    # Signals sent to worker thread.
    request_connect = Signal()
    request_branches = Signal(str)
    request_download = Signal(str, str, str)
    request_close = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.connected_to_sppu = False

        self._build_ui()
        self._start_worker()

    # =====================================================
    # UI
    # =====================================================

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        layout.setSpacing(18)

        # -------------------------------------------------
        # Heading
        # -------------------------------------------------

        title = QLabel(
            "Ledger Downloader"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Download the Engineering Ledger directly "
            "from the SPPU College portal."
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -------------------------------------------------
        # Configuration
        # -------------------------------------------------

        config_group = QGroupBox(
            "SPPU Ledger Configuration"
        )

        form = QFormLayout(
            config_group
        )

        form.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        # Exam Period
        self.exam_period_combo = (
            QComboBox()
        )

        self.exam_period_combo.addItem(
            "Connect to SPPU first",
            None,
        )

        self.exam_period_combo.setEnabled(
            False
        )

        form.addRow(
            "Exam Period",
            self.exam_period_combo,
        )

        # Course / Level
        self.course_combo = (
            QComboBox()
        )

        self.course_combo.addItem(
            "Connect to SPPU first",
            None,
        )

        self.course_combo.setEnabled(
            False
        )

        form.addRow(
            "Course / Level",
            self.course_combo,
        )

        # Branch
        self.branch_combo = (
            QComboBox()
        )

        self.branch_combo.addItem(
            "Select Course / Level first",
            None,
        )

        self.branch_combo.setEnabled(
            False
        )

        form.addRow(
            "Branch",
            self.branch_combo,
        )

        layout.addWidget(
            config_group
        )

        # -------------------------------------------------
        # Connect
        # -------------------------------------------------

        self.connect_button = QPushButton(
            "Connect to SPPU"
        )

        self.connect_button.setObjectName(
            "primaryButton"
        )

        self.connect_button.setMinimumHeight(
            44
        )

        self.connect_button.clicked.connect(
            self._connect_to_sppu
        )

        layout.addWidget(
            self.connect_button
        )

        # -------------------------------------------------
        # Download
        # -------------------------------------------------

        self.download_button = QPushButton(
            "Download Ledger"
        )

        self.download_button.setObjectName(
            "primaryButton"
        )

        self.download_button.setMinimumHeight(
            44
        )

        self.download_button.setEnabled(
            False
        )

        self.download_button.clicked.connect(
            self._download_ledger
        )

        layout.addWidget(
            self.download_button
        )

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        progress_group = QGroupBox(
            "Progress"
        )

        progress_layout = QVBoxLayout(
            progress_group
        )

        progress_layout.setContentsMargins(
            20,
            15,
            20,
            15,
        )

        self.progress_bar = (
            QProgressBar()
        )

        self.progress_bar.setRange(
            0,
            100,
        )

        self.progress_bar.setValue(
            0
        )

        progress_layout.addWidget(
            self.progress_bar
        )

        layout.addWidget(
            progress_group
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        status_group = QGroupBox(
            "Status"
        )

        status_layout = QVBoxLayout(
            status_group
        )

        status_layout.setContentsMargins(
            20,
            15,
            20,
            15,
        )

        self.status_label = QLabel(
            "Not connected to SPPU."
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        self.status_label.setWordWrap(
            True
        )

        status_layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            status_group
        )

        layout.addStretch()

        # -------------------------------------------------
        # UI signals
        # -------------------------------------------------

        self.course_combo.currentIndexChanged.connect(
            self._course_changed
        )

    # =====================================================
    # Worker thread
    # =====================================================

    def _start_worker(self):

        self.worker_thread = QThread(
            self
        )

        self.worker = PortalWorker()

        self.worker.moveToThread(
            self.worker_thread
        )

        # Requests
        self.request_connect.connect(
            self.worker.connect_to_sppu
        )

        self.request_branches.connect(
            self.worker.load_branches
        )

        self.request_download.connect(
            self.worker.download
        )

        self.request_close.connect(
            self.worker.close
        )

        # Results
        self.worker.status.connect(
            self._set_status
        )

        self.worker.connected.connect(
            self._portal_connected
        )

        self.worker.branches_loaded.connect(
            self._branches_loaded
        )

        self.worker.download_completed.connect(
            self._download_completed
        )

        self.worker.error.connect(
            self._worker_error
        )

        self.worker_thread.start()

    # =====================================================
    # Connect
    # =====================================================

    def _connect_to_sppu(self):

        if self.connected_to_sppu:
            return

        self.connect_button.setEnabled(
            False
        )

        self.progress_bar.setValue(
            5
        )

        self._set_status(
            "Opening SPPU login..."
        )

        self.request_connect.emit()

    # =====================================================
    # Portal connected
    # =====================================================

    @Slot(list, list)
    def _portal_connected(
        self,
        periods,
        courses,
    ):

        self.connected_to_sppu = True

        # ---------------------------------------------
        # Exam Period
        # ---------------------------------------------

        self.exam_period_combo.clear()

        self.exam_period_combo.addItem(
            "Select exam period",
            None,
        )

        for item in periods:

            self.exam_period_combo.addItem(
                item["text"],
                item["value"],
            )

        self.exam_period_combo.setEnabled(
            True
        )

        # ---------------------------------------------
        # Course / Level
        # ---------------------------------------------

        self.course_combo.clear()

        self.course_combo.addItem(
            "Select course / level",
            None,
        )

        for item in courses:

            self.course_combo.addItem(
                item["text"],
                item["value"],
            )

        self.course_combo.setEnabled(
            True
        )

        # ---------------------------------------------
        # Branch
        # ---------------------------------------------

        self.branch_combo.clear()

        self.branch_combo.addItem(
            "Select course / level first",
            None,
        )

        self.branch_combo.setEnabled(
            False
        )

        self.connect_button.setText(
            "Connected to SPPU"
        )

        self.progress_bar.setValue(
            30
        )

        self._set_status(
            "Connected to SPPU. "
            "Select Exam Period and Course / Level."
        )

    # =====================================================
    # Course changed
    # =====================================================

    def _course_changed(self, index):

        if not self.connected_to_sppu:
            return

        course_value = (
            self.course_combo.itemData(index)
        )

        self.branch_combo.clear()

        if not course_value:

            self.branch_combo.addItem(
                "Select course / level first",
                None,
            )

            self.branch_combo.setEnabled(
                False
            )

            self.download_button.setEnabled(
                False
            )

            return

        self.branch_combo.addItem(
            "Loading branches...",
            None,
        )

        self.branch_combo.setEnabled(
            False
        )

        self.download_button.setEnabled(
            False
        )

        self.progress_bar.setValue(
            40
        )

        self._set_status(
            "Loading branches from SPPU..."
        )

        self.request_branches.emit(
            str(course_value)
        )

    # =====================================================
    # Branches loaded
    # =====================================================

    @Slot(list)
    def _branches_loaded(
        self,
        branches,
    ):

        self.branch_combo.clear()

        self.branch_combo.addItem(
            "Select branch",
            None,
        )

        for item in branches:

            self.branch_combo.addItem(
                item["text"],
                item["value"],
            )

        self.branch_combo.setEnabled(
            True
        )

        self.progress_bar.setValue(
            50
        )

        self._set_status(
            f"{len(branches)} branch options loaded."
        )

    # =====================================================
    # Download
    # =====================================================

    def _download_ledger(self):

        exam_period = (
            self.exam_period_combo.currentData()
        )

        course_value = (
            self.course_combo.currentData()
        )

        branch_value = (
            self.branch_combo.currentData()
        )

        if not exam_period:

            QMessageBox.warning(
                self,
                "Exam Period Required",
                "Please select an Exam Period.",
            )

            return

        if not course_value:

            QMessageBox.warning(
                self,
                "Course / Level Required",
                "Please select a Course / Level.",
            )

            return

        if not branch_value:

            QMessageBox.warning(
                self,
                "Branch Required",
                "Please select a Branch.",
            )

            return

        self.download_button.setEnabled(
            False
        )

        self.connect_button.setEnabled(
            False
        )

        self.progress_bar.setValue(
            60
        )

        self._set_status(
            "Preparing ledger download..."
        )

        self.request_download.emit(
            str(exam_period),
            str(course_value),
            str(branch_value),
        )

    # =====================================================
    # Download completed
    # =====================================================

    @Slot(str)
    def _download_completed(
        self,
        filename,
    ):

        self.progress_bar.setValue(
            100
        )

        self.download_button.setEnabled(
            True
        )

        self._set_status(
            f"Ledger downloaded successfully:\n"
            f"{filename}"
        )

        QMessageBox.information(
            self,
            "Download Complete",
            "The SPPU ledger was downloaded successfully.\n\n"
            f"File:\n{filename}",
        )

    # =====================================================
    # Status
    # =====================================================

    @Slot(str)
    def _set_status(self, message):

        self.status_label.setText(
            message
        )

    # =====================================================
    # Errors
    # =====================================================

    @Slot(str)
    def _worker_error(self, message):

        self.progress_bar.setValue(
            0
        )

        self.connect_button.setEnabled(
            True
        )

        self.download_button.setEnabled(
            self.connected_to_sppu
        )

        self._set_status(
            f"Error: {message}"
        )

        QMessageBox.critical(
            self,
            "SPPU Error",
            message,
        )

    # =====================================================
    # Close
    # =====================================================

    def closeEvent(self, event):

        try:

            self.request_close.emit()

            self.worker_thread.quit()

            self.worker_thread.wait(
                5000
            )

        except Exception:
            pass

        event.accept()