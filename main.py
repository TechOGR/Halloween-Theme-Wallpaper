import os
from flask import (
    Flask,
    json,
)
from os import (
    path,
    getcwd
)
from pyautogui import (
    hotkey
)
from threading import Thread
from module.url_programs import Programs
from module.router import rutas
from module.getAdmin import run_as_admin
from PyQt5.QtGui import (
    QFont,
    QPixmap,
    QPainter,
    QFontDatabase,
    QColor
)
from PyQt5.QtWidgets import (
    QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QTableWidget, 
    QTableWidgetItem, QApplication, QHeaderView, QDialog, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QRect,
    QPoint
)

import socket
import sys
import pyqrcode


# Clase Principal
class Main:
    def __init__(self):
        self.full_path = getcwd()
        self.path_template = path.join(getcwd(), "template")
        self.path_static = path.join(getcwd(), "static")
        print(self.full_path, self.path_template, self.path_static)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.hilo_ = Thread(target=self.wait_for_fear)
        self.hilo_.daemon = True
        self.hilo_.start()
        
        self.app = Flask(__name__, static_folder=self.path_static, template_folder=self.path_template)
        self.nombre_programa = ""
        
        self.instance_programs = Programs()
        
        # Inicia las rutas web
        self.routes()
        
    def init_server(self, directions):
        self.app.run("localhost", 6780)
        
    def routes(self):
        rutas(self.app, self.nombre_programa, self.instance_programs, self.full_path)
        
    def wait_for_fear(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((ip, 5000))
        print(f"***********SERVER LISTENING ON {ip}:5000")
        self.sock.listen(2)
        
        while True:
            conn, addr = self.sock.accept()
            print(f"CLIENTE CONECTADO: {addr[0]} : {str(addr[1])}")
            data = conn.recv(1024).decode("utf-8").strip()
            print(f"Datos recibidos: {data}")
            
            if len(data) <= 0 or data is None:
                print("ERRROROROOROR")
            elif data.endswith("Activar"):
                open(path.join(self.full_path, "archivo.txt"), "w").write(data[2:])
                hotkey("win", "m")
            else:
                print("No pues GG")
            
                
class CustomWindow(QWidget):
    def __init__(self, full_path):
        super().__init__()
        self.full_path = full_path
        # Configuración de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 700)
        self.old_position = None

        self.wall_image = QPixmap("static/img/wallpaper.png")
        
        # Fondo del contenedor principal
        self.main_container = QWidget(self)
        self.main_container.setGeometry(0, 0, 500, 700)
        self.main_container.setStyleSheet("background-color: #333; border-radius: 10px;")
        self.main_instance = Main()

        # Botones de cerrar y minimizar
        self.create_control_buttons()

        # Botón de iniciar y detener servidor
        self.create_start_stop_buttons()

        # Cuatro botones principales
        self.create_action_buttons()

        # Eventos de mouse para arrastrar la ventana
        self.main_container.mousePressEvent = self.mouse_press
        self.main_container.mouseMoveEvent = self.mouse_move
        
        data_font_id = QFontDatabase().addApplicationFont("static/fonts/BloodyHell.otf")
        font_bloody = QFontDatabase().applicationFontFamilies(data_font_id)[0]
        font = QFont(font_bloody,90,2,True)
        
        shadow_effect_label = QGraphicsDropShadowEffect()
        shadow_effect_label.setBlurRadius(20)
        shadow_effect_label.setOffset(0, 0) 
        shadow_effect_label.setColor(Qt.white)
        
        self.label_text_welcome = QLabel("Halloween",self)
        self.label_text_welcome.setFont(font)
        self.label_text_welcome.setGeometry(50, 85, 420, 200)
        self.label_text_welcome.setGraphicsEffect(shadow_effect_label)
        self.label_text_welcome.setObjectName("label_text_welcome")
        self.label_text_welcome.setStyleSheet(
            """
                #label_text_welcome {
                    color: black;
                }
                #label_text_welcome:hover {
                    color: white;
                }
            """
        )
        self.label_text_welcome.show()
        
        self.qr_label = QLabel(self)
        self.qr_label.setGeometry(150, 340, 200, 200)
        self.qr_label.setVisible(False)
        
        self.selected_files = {}
        
        self.side_menu = QWidget(self)
        self.side_menu.setGeometry(500, 50, 200, 640)  # Inicia fuera de la vista
        self.side_menu.setStyleSheet("""
            background-color: #666;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        """)
        
        # Layout de la barra lateral
        self.side_layout = QVBoxLayout()
        self.side_layout.setContentsMargins(20, 20, 20, 20)  # Márgenes internos
        self.side_layout.setSpacing(15)  # Espaciado entre botones
        self.label_Title = QLabel("Opciones",self)
        self.label_Title.setGeometry(150, 160, 200, 40)
        self.label_Title.setStyleSheet("font-size: 19px; font-weight: bold; color: white;")
        self.label_Title.setAlignment(Qt.Alignment(Qt.AlignmentFlag.AlignCenter))
        self.side_layout.addWidget(self.label_Title)
        self.side_layout.addWidget(self.exe_button)
        self.side_layout.addWidget(self.list_button)
        self.side_layout.addWidget(self.help_button)
        self.side_menu.setLayout(self.side_layout)
        
        self.toggle_button = QPushButton("≡", self)
        self.toggle_button.setGeometry(450, 10, 40, 40)  # Ubicado cerca del borde derecho
        self.toggle_button.setFont(QFont("Arial", 14))
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                border: none;
                color: white;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #fff;
                color: black;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_menu)

        self.menu_visible = False  # Estado del menú
        
        self.server_thread = None
        
        
    def painEvent(self, event):
        painer = QPainter(self.main_container)
        painer.drawPixmap(self.main_container.rect(), self.wall_image)

    def toggle_menu(self):
        if self.menu_visible:
            # Ocultar el menú
            self.animate_menu(500)
        else:
            # Mostrar el menú
            self.animate_menu(300)
        self.menu_visible = not self.menu_visible

    def animate_menu(self, end_position):
        self.animation = QPropertyAnimation(self.side_menu, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.side_menu.geometry())
        self.animation.setEndValue(QRect(end_position, 50, 200, 640))
        self.animation.start()

    def create_control_buttons(self):
        # Botón rojo de cerrar (X)
        close_button = QPushButton("X", self)
        close_button.setGeometry(20, 20, 30, 30)
        close_button.setStyleSheet("font-size: 14px;background-color: white; color: #000; border-radius: 15px;")
        close_button.clicked.connect(self.close)

        # Botón amarillo de minimizar (-)
        minimize_button = QPushButton("-", self)
        minimize_button.setGeometry(60, 20, 30, 30)
        minimize_button.setStyleSheet("font-size: 18px;background-color: black; color: #fff; border-radius: 15px;")
        minimize_button.clicked.connect(self.showMinimized)
        
        shadow_effect_close = QGraphicsDropShadowEffect()
        shadow_effect_close.setBlurRadius(20)
        shadow_effect_close.setOffset(0, 0)
        shadow_effect_close.setColor(Qt.white)
        
        shadow_effect_minimze = QGraphicsDropShadowEffect()
        shadow_effect_minimze.setBlurRadius(20)
        shadow_effect_minimze.setOffset(0, 0)
        shadow_effect_minimze.setColor(Qt.black)
        
        minimize_button.setGraphicsEffect(shadow_effect_minimze)
        close_button.setGraphicsEffect(shadow_effect_close)

    def create_start_stop_buttons(self):
        # Botón de iniciar servidor
        start_button = QPushButton("Iniciar", self)
        start_button.setGeometry(150, 600, 100, 40)
        start_button.setStyleSheet("font-style: bold;background-color: white; color: black; border-radius: 10px; font-size: 15px;")
        start_button.clicked.connect(self.start_server)

        # Botón de detener servidor
        stop_button = QPushButton("Detener", self)
        stop_button.setGeometry(260, 600, 100, 40)
        stop_button.setStyleSheet("font-style: bold;background-color: black; color: white; border-radius: 10px;font-size: 15px;")
        stop_button.clicked.connect(self.stop_server)
        
        shadow_effect_stop = QGraphicsDropShadowEffect()
        shadow_effect_stop.setBlurRadius(20)
        shadow_effect_stop.setOffset(0,0) 
        shadow_effect_stop.setColor(Qt.black)
        
        shadow_effect_start = QGraphicsDropShadowEffect()
        shadow_effect_start.setBlurRadius(20)
        shadow_effect_start.setOffset(0,0)
        shadow_effect_start.setColor(Qt.white)
        
        stop_button.setGraphicsEffect(shadow_effect_stop)
        start_button.setGraphicsEffect(shadow_effect_start)

    def create_action_buttons(self):
        
        style_buttons = """
        QPushButton {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #555;
            color: white;
            font-size: 13px;
        }
        """
        
        # Primer botón: Buscar archivo .exe
        self.exe_button = QPushButton("Buscar EXE", self)
        self.exe_button.setGeometry(150, 100, 200, 40)
        self.exe_button.setStyleSheet(style_buttons)
        self.exe_button.clicked.connect(self.select_file)
        

        # Segundo botón: Lista de programas seleccionados
        self.list_button = QPushButton("Ver Lista", self)
        self.list_button.setGeometry(150, 160, 200, 40)
        self.list_button.setStyleSheet(style_buttons)
        self.list_button.clicked.connect(self.view_program_list)

        # Tercer botón: Mostrar ayuda
        self.help_button = QPushButton("Mostrar Ayuda", self)
        self.help_button.setGeometry(150, 220, 200, 40)
        self.help_button.setStyleSheet(style_buttons)
        self.help_button.clicked.connect(self.show_help)

        # Cuarto botón: Mostrar código QR
        self.qr_button = QPushButton("Mostrar Código QR", self)
        self.qr_button.setGeometry(150, 280, 200, 40)
        self.qr_button.setStyleSheet(style_buttons)
        self.qr_button.clicked.connect(self.show_qr_code)
        
        shadow_effect_qr_button = QGraphicsDropShadowEffect()
        shadow_effect_qr_button.setBlurRadius(20)
        shadow_effect_qr_button.setOffset(0,0)
        shadow_effect_qr_button.setColor(QColor(90,90,90))
        
        self.qr_button.setGraphicsEffect(shadow_effect_qr_button)

    # Función para abrir diálogo de archivos
    def select_file(self):
               
        file, _ = QFileDialog.getOpenFileName(self,"Select the FIle that you'll open", "D:/Programas", "*.exe")
        print(file)
        name_file = os.path.basename(file)[:-4]
        path_file = os.path.abspath(file)
        
        print(path_file, name_file)
        # if not path.exists("./esto.json"):
        #     file_name = path.basename(file)
        #     self.selected_files[file_name] = file
        #     with open("./esto.json", "w") as f:
        #         f.write("")
        #         json.dump(self.selected_files, f)
        #         f.close()
        # else:
        #     if file:
        #         file_name = path.basename(file)
        #         self.selected_files[file_name] = file
        #         json_loaded = ""
        #         with open("./esto.json", "r") as f_json:
        #             json_loaded = json.load(f_json)
        #             f_json.close()
        #         print(json_loaded)
                    
        #         print(f"Archivo seleccionado: {file}")
        #         print(f"Archivos seleccionados hasta ahora: {self.selected_files}")

    # Función para ver lista de programas seleccionados
    def view_program_list(self):
        # Crear una nueva ventana para mostrar la tabla
        self.program_window = QWidget()
        self.program_window.setWindowFlags(Qt.FramelessWindowHint)
        self.program_window.setAttribute(Qt.WA_TranslucentBackground)
        self.program_window.setWindowTitle("Programas Seleccionados")
        self.program_window.setGeometry(600, 300, 500, 400)
        
        def closebutton():
            self.program_window.setVisible(False)
        
        self.button_close = QPushButton("x",self.program_window)
        self.button_close.setGeometry(0, 0, 50,50)
        self.button_close.setText("X")
        self.button_close.setStyleSheet("background-color: #3E3E3E; color: black; border-radius: 10px;")
        self.button_close.clicked.connect(closebutton)


        # Crear la tabla
        table = QTableWidget(self.program_window)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Nombre del Archivo", "Ruta del Archivo"])
        table.setRowCount(len(self.selected_files))
        
        # Agregar los archivos seleccionados a la tabla
        for row, (name, path) in enumerate(self.selected_files.items()):
            item_name = QTableWidgetItem(name)
            item_name.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            table.setItem(row, 0, item_name)
            
            item_path = QTableWidgetItem(path)
            item_path.setFlags(Qt.ItemIsEnabled)
            table.setItem(row, 1, item_path)

        # Configuración de la tabla
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: none;
            }
            QHeaderView::section {
                background-color: #007BFF;
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

        # Layout de la ventana de programas
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.program_window.setLayout(layout)
        self.program_window.show()

    # Función para mostrar ayuda
    def show_help(self):
        # Mostrar ayuda en un diálogo profesional
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda")
        help_dialog.setFixedSize(400, 300)

        label = QLabel("Esta es la sección de ayuda. Aquí puedes encontrar información sobre cómo utilizar la aplicación.", help_dialog)
        label.setWordWrap(True)
        label.setStyleSheet("color: #FFFFFF; font-size: 16px; padding: 20px;")

        layout = QVBoxLayout()
        layout.addWidget(label)

        help_dialog.setLayout(layout)
        help_dialog.setStyleSheet("background-color: #2E2E2E; border-radius: 10px;")
        help_dialog.exec_()

    # Función para mostrar código QR con la dirección IP
    def show_qr_code(self):
        ip = socket.gethostbyname(socket.gethostname())
        qr = pyqrcode.create(f"{ip}:5000", error="H")
        qr.png(
            "static/img/qr_code.png",
            scale=8,
            quiet_zone=0,
            background=(222,222,222,0)
        )

        pixmap = QPixmap("static/img/qr_code.png")
        self.qr_label.setPixmap(pixmap)
        self.qr_label.setVisible(True)
        self.qr_label.show()

    # Eventos de mouse para mover la ventana
    def mouse_press(self, event):
        self.old_position = event.globalPos()

    def mouse_move(self, event):
        delta = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()

    # Funciones para iniciar y detener el servidor
    def start_server(self):
        mein = Main()
        ip = socket.gethostbyname(socket.gethostname())
        if self.server_thread is None or not self.server_thread.is_alive():
            self.server_thread = Thread(target=self.main_instance.init_server, args=[ip])
            self.server_thread.daemon = True
            self.server_thread.start()
            print("Servidor iniciado")

    def stop_server(self):
        self.server_thread.stop()
        print("Servidor detenido")

def getFullPath() -> str:
    return os.getcwd()

if __name__ == "__main__":
    # run_as_admin()
    app = QApplication(sys.argv)
    window = CustomWindow(getFullPath())
    window.show()
    sys.exit(app.exec_())

