"""
main_Government.py - Government-Styled Main Menu (PyQt5)
Professional entry point for the Document Generator System
Enhanced with backup, validation, and error handling
Modern UI with PyQt5 (Qt 5) - 32-bit compatible
"""
import json
import os
import sys

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QPixmap
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog, QFrame, QGridLayout,
                                QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton,
                                QVBoxLayout, QWidget)

from helpers.resource_path import get_logo_path

# Import FormDeleteItem - wrapped in try/except for PyInstaller compatibility
try:
    from modules.Form_DeleteItem import FormDeleteItem
except ImportError:
    FormDeleteItem = None

# Import enhancement systems
try:
    from helpers.backup_manager import BackupManager, BackupManagerGUI
    from helpers.error_handler import get_error_handler
    from helpers.performance_optimizer import get_optimizer
    from helpers.template_validator import TemplateValidator
except ImportError as e:
    print(f"Warning: Some enhancement modules not available: {e}")
    BackupManager = None
    BackupManagerGUI = None
    get_error_handler = None
    get_optimizer = None
    TemplateValidator = None


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Pengurusan Dokumen Kastam - Menu Utama")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Government colors
        self.colors = {
            'primary': '#003366',
            'secondary': '#004080',
            'accent': '#006699',
            'bg_main': '#F5F5F5',
            'bg_white': '#FFFFFF',
            'text_dark': '#1a1a1a',
            'text_light': '#FFFFFF',
            'border': '#FFFFFF',
            'button_primary': '#003366',
            'button_success': '#2E7D32',
            'button_danger': '#C62828',
            'button_hover': '#004d99'
        }
        
        # ✨ Initialize enhancement systems
        self.backup_manager = BackupManager() if BackupManager else None
        self.error_handler = get_error_handler() if get_error_handler else None
        self.optimizer = get_optimizer() if get_optimizer else None
        self.validator = TemplateValidator() if TemplateValidator else None
        
        # Start daily backup scheduler
        if self.backup_manager:
            self.backup_manager.schedule_daily_backup()
            if self.error_handler:
                self.error_handler.log_info("Daily backup scheduler started", "System")
        
        # Preload common templates for performance
        if self.optimizer:
            try:
                self.optimizer.preload_common_templates()
                if self.error_handler:
                    self.error_handler.log_info("Common templates preloaded", "Performance")
            except Exception as e:
                if self.error_handler:
                    self.error_handler.log_warning(f"Template preload failed: {e}", "Performance")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create interface
        self.create_header(main_layout)
        self.create_main_content(main_layout)
        self.create_footer(main_layout)
        
        # Center window
        self.center_window()
    
    def create_header(self, parent_layout):
        """Create professional government header"""
        # Top banner
        header_frame = QFrame()
        header_frame.setFixedHeight(140)
        header_frame.setStyleSheet(f"background-color: {self.colors['primary']};")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Logo section (left)
        logo_widget = QWidget()
        logo_widget.setStyleSheet(f"background-color: {self.colors['primary']};")
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(30, 20, 30, 20)
        
        try:
            # Load logo with transparency support
            logo_image = Image.open(get_logo_path())
            
            # Convert to RGBA if not already
            if logo_image.mode != 'RGBA':
                logo_image = logo_image.convert('RGBA')
            
            # Resize with high quality
            logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
            
            # Create a background image with the same color as the frame
            background_color = self.colors['primary']  # '#003366'
            bg_rgb = tuple(int(background_color[i:i+2], 16) for i in (1, 3, 5))
            
            # Create a new RGBA image with the background color
            background = Image.new('RGBA', logo_image.size, bg_rgb + (255,))
            
            # Composite the logo onto the background using alpha compositing
            if logo_image.mode == 'RGBA':
                logo_image = Image.alpha_composite(background, logo_image)
                logo_image = logo_image.convert('RGB')
            
            # Convert PIL Image to QPixmap
            from io import BytesIO
            buf = BytesIO()
            logo_image.save(buf, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            
            logo_label = QLabel()
            logo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setStyleSheet(f"background-color: {self.colors['primary']};")
            logo_layout.addWidget(logo_label)
        except Exception as e:
            # Fallback if logo not found
            logo_label = QLabel("🇲🇾")
            logo_label.setStyleSheet(f"background-color: {self.colors['primary']}; color: white; font-size: 70px;")
            logo_layout.addWidget(logo_label)
        
        header_layout.addWidget(logo_widget)
        
        # Title section (center)
        title_widget = QWidget()
        title_widget.setStyleSheet(f"background-color: {self.colors['primary']};")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignCenter)
        
        # Main title
        title_main = QLabel("JABATAN KASTAM DIRAJA MALAYSIA")
        title_main.setStyleSheet(f"background-color: {self.colors['primary']}; color: white; font-size: 22px; font-weight: bold;")
        title_main.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_main)
        
        # Subtitle
        title_sub = QLabel("Royal Malaysian Customs Department")
        title_sub.setStyleSheet(f"background-color: {self.colors['primary']}; color: #E0E0E0; font-size: 13px; font-style: italic;")
        title_sub.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_sub)
        
        # System name
        system_name = QLabel("Sistem Pengurusan Dokumen Automatik")
        system_name.setStyleSheet(f"background-color: {self.colors['primary']}; color: white; font-size: 16px; font-weight: bold;")
        system_name.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(system_name)
        
        # Department info
        dept_info = QLabel("Bahagian Penguatkuasaan • Cawangan Johor Bahru")
        dept_info.setStyleSheet(f"background-color: {self.colors['primary']}; color: #B0B0B0; font-size: 11px;")
        dept_info.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(dept_info)
        
        header_layout.addWidget(title_widget, stretch=1)
        
        # Right side buttons
        right_buttons_widget = QWidget()
        right_buttons_widget.setStyleSheet(f"background-color: {self.colors['primary']};")
        right_buttons_layout = QHBoxLayout(right_buttons_widget)
        right_buttons_layout.setContentsMargins(20, 20, 20, 20)
        right_buttons_layout.setSpacing(5)
        
        btn_history = QPushButton("📋 SEJARAH")
        btn_history.setStyleSheet(f"""
            QPushButton {{
                background-color: #1976D2;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                min-width: 140px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: #1565C0;
            }}
        """)
        btn_history.clicked.connect(self.open_history)
        right_buttons_layout.addWidget(btn_history)
        
        if BackupManagerGUI:
            btn_backup = QPushButton("💾 BACKUP")
            btn_backup.setStyleSheet(f"""
                QPushButton {{
                    background-color: #666666;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                    min-width: 140px;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: #555555;
                }}
            """)
            btn_backup.clicked.connect(self.open_backup_manager)
            right_buttons_layout.addWidget(btn_backup)
        
        header_layout.addWidget(right_buttons_widget)
        
        parent_layout.addWidget(header_frame)
        
        # Separator line
        separator = QFrame()
        separator.setFixedHeight(3)
        separator.setStyleSheet(f"background-color: {self.colors['accent']};")
        parent_layout.addWidget(separator)
    
    def create_main_content(self, parent_layout):
        """Create main menu content"""
        # Main container
        main_container = QWidget()
        main_container.setStyleSheet(f"background-color: {self.colors['bg_main']};")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(30)
        
        # Welcome card
        welcome_card = QFrame()
        welcome_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        welcome_layout = QVBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(25, 20, 25, 20)
        
        welcome_title = QLabel("Selamat Datang")
        welcome_title.setStyleSheet(f"color: {self.colors['primary']}; font-size: 20px; font-weight: bold;")
        welcome_layout.addWidget(welcome_title)
        
        welcome_text = QLabel("Sila pilih modul yang anda ingin gunakan:")
        welcome_text.setStyleSheet(f"color: {self.colors['text_dark']}; font-size: 14px;")
        welcome_layout.addWidget(welcome_text)
        
        main_layout.addWidget(welcome_card)
        
        # Modules section
        modules_widget = QWidget()
        modules_widget.setStyleSheet(f"background-color: {self.colors['bg_main']};")
        modules_layout = QGridLayout(modules_widget)
        modules_layout.setSpacing(10)
        
        # Module cards
        self.create_module_card(
            modules_layout,
            "📋 Pengurusan Pelupusan & Lain-lain",
            "Sistem untuk pengurusan dokumen pelupusan barang",
            "• Surat kelulusan pelupusan\n• Dokumen pemusnahan\n• Pilih template terus",
            self.open_form2,
            row=0,
            column=0
        )
        
        self.create_module_card(
            modules_layout,
            "📊 Jadual Data",
            "Sistem pengurusan data barang-barang untuk permohonan AMES",
            "• Senarai barang pedagang\n• Senarai barang pengilang\n• borang 3D\n• Lampiran dokumen",
            self.open_form3,
            row=1,
            column=0
        )
        
        self.create_module_card(
            modules_layout,
            "🗑 Pemadaman Item AMES",
            "Urus permohonan penambahan/pemadaman item dalam senarai AMES dengan jejak warna.",
            "• Tambah/Padam item berwarna\n• Simpan ke PDF/DOCX\n• Rekod ke pangkalan data",
            self.open_form4,
            row=0,
            column=1
        )
        
        self.create_module_card(
            modules_layout,
            "📝 Pendaftaran Sign Up",
            "Sistem untuk pendaftaran dan pengurusan Sign Up A,B,C",
            "• Borang pendaftaran Sign Up\n• Pengurusan maklumat pendaftaran\n• Simpan ke pangkalan data",
            self.open_signup_form,
            row=1,
            column=1
        )
        
        self.create_module_card(
            modules_layout,
            "🔍 Template Scanner & Validator",
            "Scan template baru dan check jika input fields mencukupi",
            "• Scan placeholders dalam template\n• Check completeness\n• Suggest missing fields\n• Validate sebelum generate",
            self.open_template_scanner,
            row=2,
            column=0
        )
        
        main_layout.addWidget(modules_widget, stretch=1)
        parent_layout.addWidget(main_container, stretch=1)
    
    def create_module_card(self, parent_layout, title, description, features, command, row, column=0):
        """Create a professional module card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        
        # Left side - Info
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignTop)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {self.colors['primary']}; font-size: 16px; font-weight: bold;")
        title_label.setWordWrap(True)
        left_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {self.colors['text_dark']}; font-size: 13px;")
        desc_label.setWordWrap(True)
        left_layout.addWidget(desc_label)
        
        features_label = QLabel(features)
        features_label.setStyleSheet(f"color: {self.colors['text_dark']}; font-size: 11px;")
        features_label.setWordWrap(True)
        left_layout.addWidget(features_label)
        
        card_layout.addWidget(left_widget, stretch=1)
        
        # Right side - Button
        btn = QPushButton("BUKA MODUL")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['button_primary']};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                min-width: 170px;
                min-height: 70px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['button_hover']};
            }}
        """)
        btn.clicked.connect(command)
        card_layout.addWidget(btn)
        
        parent_layout.addWidget(card, row, column)
    
    def create_footer(self, parent_layout):
        """Create footer section"""
        footer_container = QWidget()
        footer_container.setStyleSheet(f"background-color: {self.colors['bg_main']};")
        footer_layout = QVBoxLayout(footer_container)
        footer_layout.setContentsMargins(60, 0, 60, 30)
        footer_layout.setAlignment(Qt.AlignCenter)
        
        btn_exit = QPushButton("✕ KELUAR DARI SISTEM")
        btn_exit.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['button_danger']};
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                min-width: 280px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #B71C1C;
            }}
        """)
        btn_exit.clicked.connect(self.exit_application)
        footer_layout.addWidget(btn_exit)
        
        parent_layout.addWidget(footer_container)
        
        # Copyright info
        copyright_frame = QFrame()
        copyright_frame.setFixedHeight(40)
        copyright_frame.setStyleSheet(f"background-color: {self.colors['primary']};")
        copyright_layout = QVBoxLayout(copyright_frame)
        copyright_layout.setAlignment(Qt.AlignCenter)
        
        copyright_text = QLabel("© 2025 Jabatan Kastam Diraja Malaysia. Semua hak terpelihara. | Versi 1.0")
        copyright_text.setStyleSheet(f"background-color: {self.colors['primary']}; color: #B0B0B0; font-size: 10px;")
        copyright_text.setAlignment(Qt.AlignCenter)
        copyright_layout.addWidget(copyright_text)
        
        parent_layout.addWidget(copyright_frame)
    
    def center_window(self):
        """Center window on screen"""
        frame_geometry = self.frameGeometry()
        # Get screen geometry (compatible with PySide2)
        try:
            screen = QApplication.primaryScreen()
            if screen:
                screen_geometry = screen.availableGeometry()
            else:
                # Fallback for older PySide2 versions
                from PyQt5.QtWidgets import QDesktopWidget
                desktop = QDesktopWidget()
                screen_geometry = desktop.availableGeometry(desktop.primaryScreen())
        except:
            # Fallback method
            from PyQt5.QtWidgets import QDesktopWidget
            desktop = QDesktopWidget()
            screen_geometry = desktop.availableGeometry(desktop.primaryScreen())
        
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        self.raise_()
        self.activateWindow()
    
    def open_history(self):
        """Open universal history viewer"""
        try:
            from helpers.UniversalHistoryViewer_PyQt5 import UniversalHistoryViewer
            history_dialog = UniversalHistoryViewer(self)
            history_dialog.exec_()
            # Show main window again when dialog closes
            self.show()
            self.raise_()
            self.activateWindow()
        except ImportError as e:
            QMessageBox.critical(self, "Ralat",
                               f"Tidak dapat membuka modul:\n{e}\n\n"
                               "Pastikan fail UniversalHistoryViewer_PyQt5.py wujud.")
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Tidak dapat membuka sejarah: {e}")
    
    def open_backup_manager(self):
        """Open backup manager GUI"""
        if BackupManagerGUI:
            try:
                # Note: BackupManagerGUI needs to be migrated to PySide2
                QMessageBox.information(self, "Info", "Backup Manager akan dibuka (perlu migrasi ke PySide2)")
            except Exception as e:
                if self.error_handler:
                    self.error_handler.handle_error(e, "Opening Backup Manager", show_user=True)
                else:
                    QMessageBox.critical(self, "Error", f"Failed to open Backup Manager:\n{e}")
        else:
            QMessageBox.warning(self, "Not Available", "Backup Manager module not available")
    
    def open_form2(self):
        """Open Form2 directly with template selector"""
        try:
            from modules.form2_Government_PyQt5 import Form2
            self.hide()
            form2_dialog = Form2(self)
            form2_dialog.exec_()
            self.show()
            self.raise_()
            self.activateWindow()
        except ImportError as e:
            QMessageBox.critical(self, "Ralat",
                               f"Tidak dapat membuka modul:\n{e}\n\n"
                               "Pastikan fail form2_Government_PyQt5.py wujud.")
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Ralat: {e}")
            import traceback
            traceback.print_exc()
    
    def open_form3(self):
        """Open Form3 (AMES table)"""
        try:
            from modules.Form3_Government_PySide2 import Form3
            form3_dialog = Form3(self)
            result = form3_dialog.exec_()
            # Show main window again when Form3 closes
            self.show()
            self.raise_()
            self.activateWindow()
        except ImportError as e:
            QMessageBox.critical(self, "Ralat",
                               f"Tidak dapat membuka modul:\n{e}\n\n"
                               "Pastikan fail Form3_Government_PyQt5.py wujud.")
    
    def open_form4(self):
        """Open Form4 (Delete Item AMES)"""
        try:
            # Try PyQt5 version first, fallback to Tkinter version
            try:
                from modules.Form_DeleteItem_PyQt5 import FormDeleteItem
                form4_dialog = FormDeleteItem(self)
                result = form4_dialog.exec_()
                # Show main window again when form closes
                self.show()
                self.raise_()
                self.activateWindow()
            except ImportError:
                # Fallback to Tkinter version
                if FormDeleteItem is None:
                    from modules.Form_DeleteItem import FormDeleteItem
                QMessageBox.information(self, "Info", 
                    "Form_DeleteItem masih menggunakan Tkinter.\n"
                    "Versi PyQt5 sedang dalam pembangunan.")
                self.hide()
        except ImportError as e:
            QMessageBox.critical(self, "Ralat",
                           f"Tidak dapat membuka modul:\n{e}\n\n"
                           "Pastikan fail Form_DeleteItem_PyQt5.py wujud.")
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Ralat: {e}")
    
    def open_signup_form(self):
        """Open Sign Up form"""
        try:
            from modules.Form_SignUp_PyQt5 import FormSignUp
            signup_dialog = FormSignUp(self)
            result = signup_dialog.exec_()
            # Show main window again when form closes
            self.show()
            self.raise_()
            self.activateWindow()
        except ImportError as e:
            QMessageBox.critical(self, "Ralat",
                               f"Tidak dapat membuka modul:\n{e}\n\n"
                               "Pastikan fail Form_SignUp_PyQt5.py wujud.")
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Ralat: {e}")
    
    def open_template_scanner(self):
        """Open Template Scanner dialog"""
        try:
            from helpers.template_completeness_dialog import TemplateScannerDialog
            scanner_dialog = TemplateScannerDialog(self)
            scanner_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Tidak dapat buka Template Scanner: {e}")
            import traceback
            traceback.print_exc()
    
    def exit_application(self):
        """Exit application with confirmation"""
        reply = QMessageBox.question(self, "Pengesahan",
                                    "Adakah anda pasti ingin keluar dari sistem?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set palette for better colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#F5F5F5'))
    palette.setColor(QPalette.WindowText, QColor('#1a1a1a'))
    app.setPalette(palette)
    
    window = MainMenu()
    window.show()
    
    sys.exit(app.exec_())
