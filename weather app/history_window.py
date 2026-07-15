
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QHeaderView,
    QMessageBox,
)

import database

COLUMNS = ["City", "Country", "Temp (°C)", "Humidity (%)",
           "Description", "Wind (m/s)", "Sunrise", "Sunset", "Searched At"]


class HistoryWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search History")
        self.resize(760, 420)
        self._build_ui()
        self.load_history()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Previously Searched Cities")
        title.setStyleSheet("font-size:20px; font-weight:700; color:#1a1a1a;")
        layout.addWidget(title)

        self.table = QTableWidget(0, len(COLUMNS), self)
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        button_row = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.clear_button = QPushButton("Clear History")
        self.close_button = QPushButton("Close")

        self.refresh_button.clicked.connect(self.load_history)
        self.clear_button.clicked.connect(self.clear_history)
        self.close_button.clicked.connect(self.close)

        button_row.addWidget(self.refresh_button)
        button_row.addWidget(self.clear_button)
        button_row.addStretch()
        button_row.addWidget(self.close_button)
        layout.addLayout(button_row)

        self.setStyleSheet("""
            QDialog { background-color:#ffffff; }
            QLabel { font-family: Calibri; }
            QTableWidget {
                font-family: Calibri;
                font-size: 13px;
                gridline-color:#e0e2ea;
            }
            QHeaderView::section {
                background-color:#5a7dfa;
                color:white;
                font-weight:bold;
                padding:6px;
                border:none;
            }
            QPushButton {
                font-family: Calibri;
                font-size: 13px;
                padding:6px 14px;
                border-radius:6px;
                background-color:#5a7dfa;
                color:white;
            }
            QPushButton:hover { background-color:#7593ff; }
        """)

    def load_history(self):
        """Query SQLite and populate the table with search history."""
        records = database.get_history(limit=100)
        self.table.setRowCount(0)

        for row_index, record in enumerate(records):
            self.table.insertRow(row_index)
            values = [
                record["city"],
                record["country"] or "-",
                f"{record['temperature']:.1f}" if record["temperature"] is not None else "-",
                str(record["humidity"]) if record["humidity"] is not None else "-",
                (record["description"] or "-").title(),
                f"{record['wind_speed']}" if record["wind_speed"] is not None else "-",
                record["sunrise"] or "-",
                record["sunset"] or "-",
                record["searched_at"],
            ]
            for col_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

    def clear_history(self):
        confirm = QMessageBox.question(
            self, "Clear History",
            "Delete all saved search history? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            database.clear_history()
            self.load_history()
