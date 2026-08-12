import sys

from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QStackedWidget,
    QWidget,
)

from ui.dashboard import Dashboard
from ui.ledger_downloader import LedgerDownloader
from ui.navigation import NavigationPanel
from ui.placeholder_page import PlaceholderPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "SPPU Ledger Downloader Pro"
        )
        self.resize(1200, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(
            central_widget
        )
        main_layout.setContentsMargins(
            0, 0, 0, 0
        )
        main_layout.setSpacing(0)

        # Navigation
        self.navigation = NavigationPanel()
        main_layout.addWidget(
            self.navigation
        )

        # Page container
        self.pages = QStackedWidget()
        self.pages.setObjectName(
            "pageContainer"
        )

        main_layout.addWidget(
            self.pages,
            1,
        )

        # Main pages
        self.dashboard = Dashboard()

        self.downloader_page = (
            LedgerDownloader()
        )

        self.history_page = PlaceholderPage(
            "Download History",
            "Downloaded ledger records and activity history will appear here.",
        )

        self.settings_page = PlaceholderPage(
            "Settings",
            "Application and download settings will be configured here.",
        )

        self.about_page = PlaceholderPage(
            "About",
            "SPPU Ledger Downloader Pro.",
        )

        # Add pages
        self.pages.addWidget(
            self.dashboard
        )
        self.pages.addWidget(
            self.downloader_page
        )
        self.pages.addWidget(
            self.history_page
        )
        self.pages.addWidget(
            self.settings_page
        )
        self.pages.addWidget(
            self.about_page
        )

        # Navigation events
        self.navigation.page_selected.connect(
            self.show_page
        )

        self.navigation.toggle_requested.connect(
            self.toggle_navigation
        )

        # Initial page
        self.pages.setCurrentWidget(
            self.dashboard
        )

    def show_page(self, page_name):
        pages = {
            "dashboard": self.dashboard,
            "downloader": self.downloader_page,
            "history": self.history_page,
            "settings": self.settings_page,
            "about": self.about_page,
        }

        page = pages.get(page_name)

        if page is not None:
            self.pages.setCurrentWidget(page)

    def toggle_navigation(self):
        self.navigation.set_expanded(
            not self.navigation.expanded
        )


def load_stylesheet():
    stylesheet_path = (
        Path(__file__).parent
        / "resources"
        / "style.qss"
    )

    if stylesheet_path.exists():
        return stylesheet_path.read_text(
            encoding="utf-8"
        )

    return ""


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(
        load_stylesheet()
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()