import json
from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QVBoxLayout,
    QFileIconProvider,
    QPushButton
)
from PyQt5.QtCore import (
    Qt,
    QFileInfo,
    QPropertyAnimation,
    QRect,
    QSize
)
from PyQt5.QtGui import (
    QFont,
    QColor,
    QPainter,
    QBrush,
    QPen,
    QRegion
)
import os

class ListItems(QWidget):
    
    def __init__(self, data, fullPath):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.fullPathConfig = fullPath  # Ruta al archivo de configuración JSON
        self.setWindowTitle("Programas Seleccionados")
        self.setGeometry(600, 300, 500, 450)  # Tamaño ajustado para incluir el botón
        self.setupUI(data)
        
    def setupUI(self, dataJson):
        # Crear la tabla
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Route"])
        self.table.setRowCount(len(dataJson))
        self.table.verticalHeader().setVisible(False)
        
        font = QFont("Monospace", 12, 3)
        icon_provider = QFileIconProvider()
        
        # Agregar los datos a la tabla
        for row, (name, path) in enumerate(dataJson.items()):
            item_name = QTableWidgetItem(name)
            item_name.setFont(font)
            item_name.setForeground(QColor("#FFFFFF"))

            # Agregar el ícono del .exe
            if icon := self.get_exe_icon(icon_provider, path):
                item_name.setIcon(icon)
            
            item_name.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_name)
            
            item_path = QTableWidgetItem(path)
            item_path.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 1, item_path)

        # Configuración de la tabla
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2B2B2B;
                color: #FFFFFF;
                border: 1px solid #3E3E3E;
                gridline-color: #555;
            }
            QHeaderView::section {
                background-color: #000;
                color: #FFFFFF;
                font-weight: bold;
                border: none;
                height: 30px;
            }
            QTableWidget::item {
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #17A2B8;
            }
        """)

        # Crear el botón "Actualizar"
        update_button = QPushButton("Save Config", self)
        update_button.setFont(QFont("Arial", 12))
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #005c61;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        update_button.clicked.connect(self.save_data_to_json)

        # Layout de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(update_button)
        self.setLayout(layout)

    def get_exe_icon(self, icon_provider, path):
        """Extrae el ícono del archivo usando QFileIconProvider."""
        if os.path.exists(path):
            file_info = QFileInfo(path)  # Crear un objeto QFileInfo
            return icon_provider.icon(file_info)  # Pasar QFileInfo para obtener el ícono
        return None

    def save_data_to_json(self):
        """Guardar los datos de la tabla en un archivo JSON."""
        data = {}
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text()
            path = self.table.item(row, 1).text()
            data[name] = path

        try:
            with open(self.fullPathConfig, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception:
            print("ERROR 3 Al guardar json")
        print(f"Datos guardados en {self.fullPathConfig}")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rounded_rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(QColor(43, 43, 43)))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(rounded_rect, 15, 15)
