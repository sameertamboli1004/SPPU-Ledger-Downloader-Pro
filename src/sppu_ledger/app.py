import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SPPU Ledger Downloader Pro")
        self.resize(900, 600)

        label = QLabel("SPPU Ledger Downloader Pro")
        label.setStyleSheet("font-size: 24px;")

        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()