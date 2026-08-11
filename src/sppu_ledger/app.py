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
        self.content_label = QLabel(
            "Welcome to SPPU Ledger Downloader Pro"
        )
        self.content_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                padding: 30px;
            }
        """)

        main_layout.addWidget(self.content_label, 1)

        self.setCentralWidget(central_widget)

        # Status bar
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def page_selected(self, page_name):
        self.content_label.setText(
            f"Selected: {page_name.replace('_', ' ').title()}"
        )


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