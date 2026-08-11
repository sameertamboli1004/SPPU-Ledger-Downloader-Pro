import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QHBoxLayout,
    QWidget,
)

from ui.navigation import NavigationPanel
from ui.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SPPU Ledger Downloader Pro")
        self.resize(1100, 700)

        # Main container
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Navigation panel
        self.navigation = NavigationPanel()
        self.navigation.page_selected.connect(self.page_selected)

        main_layout.addWidget(self.navigation)

        # Main content area
        self.dashboard = Dashboard()
        main_layout.addWidget(self.dashboard, 1)

        self.setCentralWidget(central_widget)

        # Status bar
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def page_selected(self, page_name):
        if page_name == "dashboard":
            self.dashboard.show()


def main():
    app = QApplication(sys.argv)

    style_path = "src/sppu_ledger/resources/style.qss"

    try:
        with open(style_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"Warning: stylesheet not found: {style_path}")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()