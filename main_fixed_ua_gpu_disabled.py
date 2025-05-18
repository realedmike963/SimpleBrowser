import sys
import os

import glob
import configparser
import logging
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar,
    QLineEdit, QWidget, QVBoxLayout, QInputDialog
)
from PyQt6.QtGui import QPalette, QColor, QAction  # QAction を QtGui からインポート
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl

CONFIG_FILE = "setting.ini"
LOG_FILE = "browser.log"

def build_chromium_flags(config):
    flags = []
    if config.getboolean("Browser", "disable_gpu", fallback=False):
        flags.append("--disable-gpu")
    if config.getboolean("Browser", "disable_software_rasterizer", fallback=False):
        flags.append("--disable-software-rasterizer")
    if config.getboolean("Browser", "enable_logging", fallback=False):
        flags.append("--enable-logging")
    return " ".join(flags)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = self.load_settings()
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = build_chromium_flags(self.config)

        self.prepare_log_directory()

        logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

        self.setWindowTitle("Simple Browser (PyQt6)")
        self.setGeometry(100, 100, 1280, 800)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(self.config.get("Browser", "user_agent"))

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(self.config.get("Browser", "homepage")))

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        back_btn = QAction("戻る", self)
        back_btn.triggered.connect(self.web_view.back)
        toolbar.addAction(back_btn)

        forward_btn = QAction("進む", self)
        forward_btn.triggered.connect(self.web_view.forward)
        toolbar.addAction(forward_btn)

        reload_btn = QAction("リロード", self)
        reload_btn.triggered.connect(self.web_view.reload)
        toolbar.addAction(reload_btn)

        home_btn = QAction("ホーム", self)
        home_btn.triggered.connect(lambda: self.web_view.setUrl(QUrl(self.config.get("Browser", "homepage"))))
        toolbar.addAction(home_btn)

        search_btn = QAction("検索", self)
        search_btn.triggered.connect(self.search_text)
        toolbar.addAction(search_btn)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        layout.addWidget(self.url_bar)
        layout.addWidget(self.web_view)

        self.setCentralWidget(central_widget)

        self.web_view.urlChanged.connect(self.update_url_bar_and_log)

        if self.config.getboolean("Browser", "dark_mode", fallback=False):
            self.enable_dark_mode()

    def load_settings(self):
        config = configparser.ConfigParser()
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config.read_file(f)
        except FileNotFoundError:
            config["Browser"] = {
                "homepage": "http://127.0.0.1:7860/",
                "dark_mode": "false",
                "user_agent": "SimpleBrowser/1.0",
                "disable_gpu": "true",
                "disable_software_rasterizer": "true",
                "enable_logging": "false"
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                config.write(f)
        return config

    def prepare_log_directory(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        cutoff_date = datetime.now() - timedelta(days=365)
        for filepath in glob.glob(os.path.join(log_dir, "access_*.log")):
            try:
                date_str = os.path.basename(filepath)[7:15]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                if file_date < cutoff_date:
                    os.remove(filepath)
                    logging.info(f"Old log deleted: {filepath}")
            except Exception as e:
                logging.warning(f"Failed to process log file {filepath}: {e}")

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.web_view.setUrl(QUrl(url))

    def update_url_bar_and_log(self, qurl):
        url = qurl.toString()
        self.url_bar.setText(url)
        logging.info(f"Visited: {url}")

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        logfile = os.path.join("logs", f"access_{now.strftime('%Y%m%d')}.log")
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {url}\n")

    def search_text(self):
        text, ok = QInputDialog.getText(self, "ページ内検索", "検索語句:")
        if ok and text:
            self.web_view.findText("", QWebEngineView.FindFlag(0))  # clear previous
            self.web_view.findText(text)

    def enable_dark_mode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        QApplication.instance().setPalette(dark_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
