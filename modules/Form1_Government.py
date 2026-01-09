"""
Form1_Government.py - Government-Styled Category Selection Form (PySide2)
Professional government interface design
"""
import sys
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
                                QGridLayout, QFrame, QLabel, QPushButton, 
                                QComboBox, QMessageBox, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PIL import Image
from helpers.resource_path import get_logo_path
import json
import os

class Form1(QDialog):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Sistem Pengurusan Dokumen Kastam - Pemilihan Kategori")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Add borders to text boxes (QTextEdit) only
        self.setStyleSheet("""
            QLineEdit, QComboBox {
                border: none;
            }
            QTextEdit {
                border: 1px solid #CCCCCC;
            }
        """)
        
        # Government color scheme
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
            'button_hover': '#004d99'
        }
        
        # Category options data
        self.category_options = {
            "Pelupusan": ["pemusnahan", "penjualan", "skrap", "tidak_lulus"],
            "Lain-lain": ["batal_sijil", "butiran_5d_lulus", "butiran_5d_tidak_lulus"]
        }
        
        # Create main layout first
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create interface
        self.create_header(main_layout)
        self.create_main_content(main_layout)
        
        # Center window
        self.center_window()
        
        # Initialize suboptions (after all widgets are created)
        # Use QTimer to ensure widgets are fully initialized
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, lambda: (
            self.on_category_changed(),
            self.load_last_selection()
        ))
    
    def create_header(self, parent_layout):
        """Create official government header"""
        # Top banner - Government blue
        header_frame = QFrame()
        header_frame.setFixedHeight(120)
        header_frame.setStyleSheet(f"background-color: {self.colors['primary']};")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Logo section (left)
        logo_widget = QWidget()
        logo_widget.setStyleSheet(f"background-color: {self.colors['primary']};")
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(20, 10, 20, 10)
        
        try:
            logo_image = Image.open(get_logo_path())
            
            if logo_image.mode != 'RGBA':
                logo_image = logo_image.convert('RGBA')
            
            logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
            
            background_color = self.colors['primary']
            bg_rgb = tuple(int(background_color[i:i+2], 16) for i in (1, 3, 5))
            background = Image.new('RGBA', logo_image.size, bg_rgb + (255,))
            
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
        except Exception:
            pass
        
        header_layout.addWidget(logo_widget)
        
        # Title section (center)
        title_widget = QWidget()
        title_widget.setStyleSheet(f"background-color: {self.colors['primary']};")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setContentsMargins(20, 20, 20, 20)
        
        # Main title
        title_main = QLabel("JABATAN KASTAM DIRAJA MALAYSIA")
        title_main.setStyleSheet(f"background-color: {self.colors['primary']}; color: white; font-size: 20px; font-weight: bold;")
        title_main.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_main)
        
        # Subtitle
        title_sub = QLabel("Sistem Pengurusan Dokumen Rasmi")
        title_sub.setStyleSheet(f"background-color: {self.colors['primary']}; color: #E0E0E0; font-size: 13px;")
        title_sub.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_sub)
        
        # Department info
        dept_info = QLabel("Bahagian Penguatkuasaan")
        dept_info.setStyleSheet(f"background-color: {self.colors['primary']}; color: #B0B0B0; font-size: 11px; font-style: italic;")
        dept_info.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(dept_info)
        
        header_layout.addWidget(title_widget, stretch=1)
        
        # Back button (right side)
        if self.parent_window:
            btn_back = QPushButton("← KEMBALI")
            btn_back.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.colors['secondary']};
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 5px;
                    min-width: 150px;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['button_hover']};
                }}
            """)
            btn_back.clicked.connect(self.on_back_click)
            header_layout.addWidget(btn_back)
        
        # Add header to parent layout
        parent_layout.addWidget(header_frame)
        
        # Separator line
        separator = QFrame()
        separator.setFixedHeight(3)
        separator.setStyleSheet(f"background-color: {self.colors['accent']};")
        parent_layout.addWidget(separator)
    
    def create_main_content(self, parent_layout):
        """Create main form content"""
        
        # Main container with grey background
        main_container = QWidget()
        main_container.setStyleSheet(f"background-color: {self.colors['bg_main']};")
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(80, 40, 80, 20)
        container_layout.setSpacing(20)
        
        # Content card (white panel)
        content_card = QFrame()
        content_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 5px;
            }
        """)
        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        
        # Form title
        form_title = QLabel("Sila Pilih Kategori Surat")
        form_title.setStyleSheet(f"color: {self.colors['primary']}; font-size: 18px; font-weight: bold;")
        form_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(form_title)
        card_layout.addSpacing(30)
        
        # Form section
        form_section = QWidget()
        form_layout = QVBoxLayout(form_section)
        form_layout.setSpacing(15)
        
        # Category selection
        category_widget = QWidget()
        category_layout = QGridLayout(category_widget)
        category_layout.setSpacing(10)
        
        category_label = QLabel("Kategori Surat:")
        category_label.setStyleSheet(f"color: {self.colors['text_dark']}; font-size: 13px; font-weight: bold;")
        category_layout.addWidget(category_label, 0, 0)
        
        self.combo_category = QComboBox()
        self.combo_category.setEditable(False)  # Make it non-editable (dropdown only)
        self.combo_category.addItems(list(self.category_options.keys()))
        self.combo_category.setCurrentIndex(0)  # Set default selection
        self.combo_category.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                border-radius: 3px;
                min-width: 200px;
            }
            QComboBox:hover {
                border: 1px solid #003366;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #003366;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: none;
                selection-background-color: #E3F2FD;
            }
        """)
        self.combo_category.currentTextChanged.connect(self.on_category_changed)
        category_layout.addWidget(self.combo_category, 0, 1)
        
        form_layout.addWidget(category_widget)
        
        # SubOption selection
        sub_widget = QWidget()
        sub_layout = QGridLayout(sub_widget)
        sub_layout.setSpacing(10)
        
        sub_label = QLabel("Sub-Kategori:")
        sub_label.setStyleSheet(f"color: {self.colors['text_dark']}; font-size: 13px; font-weight: bold;")
        sub_layout.addWidget(sub_label, 0, 0)
        
        self.combo_sub = QComboBox()
        self.combo_sub.setEditable(False)  # Make it non-editable (dropdown only)
        self.combo_sub.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                border-radius: 3px;
                min-width: 200px;
            }
            QComboBox:hover {
                border: 1px solid #003366;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #003366;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: none;
                selection-background-color: #E3F2FD;
            }
        """)
        sub_layout.addWidget(self.combo_sub, 0, 1)
        
        form_layout.addWidget(sub_widget)
        card_layout.addLayout(form_layout)
        card_layout.addSpacing(40)
        
        # Button section
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.btn_next = QPushButton("TERUSKAN")
        self.btn_next.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['button_primary']};
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 5px;
                min-width: 200px;
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['button_hover']};
            }}
        """)
        self.btn_next.clicked.connect(self.on_next_click)
        button_layout.addWidget(self.btn_next)
        
        card_layout.addWidget(button_widget)
        container_layout.addWidget(content_card, stretch=1)
        
        # Footer info
        footer_text = QLabel("© 2025 Jabatan Kastam Diraja Malaysia. Semua hak terpelihara.")
        footer_text.setStyleSheet("color: #666666; font-size: 10px;")
        footer_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(footer_text)
        
        parent_layout.addWidget(main_container, stretch=1)
    
    def center_window(self):
        """Center window on screen"""
        frame_geometry = self.frameGeometry()
        try:
            from PyQt5.QtWidgets import QDesktopWidget
            desktop = QDesktopWidget()
            screen_geometry = desktop.availableGeometry(desktop.primaryScreen())
        except:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        self.raise_()
        self.activateWindow()
    
    def load_last_selection(self):
        """Load last selected category and sub-option"""
        try:
            # Check if widgets are still valid
            if not hasattr(self, 'combo_category') or self.combo_category is None:
                return
            if not hasattr(self, 'combo_sub') or self.combo_sub is None:
                return
            
            config_file = "form1_last_selection.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    category = data.get('category', '')
                    sub_option = data.get('sub_option', '')
                    
                    if category in self.category_options:
                        index = self.combo_category.findText(category)
                        if index >= 0:
                            self.combo_category.setCurrentIndex(index)
                            self.on_category_changed()
                            if sub_option and hasattr(self, 'combo_sub'):
                                try:
                                    sub_index = self.combo_sub.findText(sub_option)
                                    if sub_index >= 0:
                                        self.combo_sub.setCurrentIndex(sub_index)
                                except RuntimeError:
                                    pass
        except RuntimeError:
            # Widget was deleted
            pass
        except Exception:
            pass
    
    def save_last_selection(self):
        """Save current selection"""
        try:
            data = {
                'category': self.combo_category.currentText(),
                'sub_option': self.combo_sub.currentText()
            }
            with open("form1_last_selection.json", 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass
    
    def on_back_click(self):
        """Go back to main menu"""
        # Just close this dialog, don't close parent
        self.reject()  # Use reject instead of accept to just close dialog
    
    def on_category_changed(self):
        """Update suboptions when category changes"""
        # Check if combo_sub exists and is valid
        if not hasattr(self, 'combo_sub') or self.combo_sub is None:
            return
        
        try:
            self.combo_sub.clear()
            selected_category = self.combo_category.currentText()
            
            if selected_category in self.category_options:
                self.combo_sub.addItems(self.category_options[selected_category])
                if self.combo_sub.count() > 0:
                    self.combo_sub.setCurrentIndex(0)
        except RuntimeError:
            # Widget was deleted, ignore
            pass
        except Exception as e:
            print(f"Warning: on_category_changed error: {e}")
    
    def on_next_click(self):
        """Open Form2 with selected options"""
        # Check if widgets are still valid
        try:
            if not hasattr(self, 'combo_category') or self.combo_category is None:
                return
            if not hasattr(self, 'combo_sub') or self.combo_sub is None:
                return
            
            category = self.combo_category.currentText()
            sub_opt = self.combo_sub.currentText()
        except RuntimeError:
            # Widget was deleted
            return
        
        if not category or not sub_opt:
            QMessageBox.warning(self, "Amaran",
                              "Sila pilih kategori dan sub-kategori terlebih dahulu.")
            return
        
        # Save selection
        self.save_last_selection()
        
        # Determine template file
        template_file = None
        if category == "Pelupusan":
            if sub_opt == "pemusnahan":
                template_file = "pelupusan_pemusnahan.docx"
            elif sub_opt == "penjualan":
                template_file = "pelupusan_penjualan.docx"
            elif sub_opt == "skrap":
                template_file = "pelupusan_skrap.docx"
            elif sub_opt == "tidak_lulus":
                template_file = "pelupusan_tidak_lulus.docx"
        elif category == "Lain-lain":
            if sub_opt == "batal_sijil":
                template_file = "batal_sijil.doc"
            elif sub_opt == "butiran_5d_lulus":
                template_file = "surat kelulusan butiran 5D (Lulus).docx"
            elif sub_opt == "butiran_5d_tidak_lulus":
                template_file = "surat kelulusan butiran 5D (tidak lulus).docx"
        
        if not template_file:
            QMessageBox.critical(self, "Ralat", f"Templat tidak dijumpai untuk: {category} - {sub_opt}")
            return
        
        # Determine requirements
        requires_amount = (category == "Pelupusan" and sub_opt == "penjualan")
        requires_pengecualian = (category == "Pelupusan")
        
        # Import and open Form2
        try:
            from modules.form2_Government_PyQt5 import Form2
            form2_dialog = Form2(self, category, sub_opt, template_file,
                                requires_amount, requires_pengecualian)
            form2_dialog.exec_()
            self.show()  # Show Form1 again after Form2 closes
        except ImportError as e:
            QMessageBox.critical(self, "Ralat", f"Tidak dapat membuka form2: {e}")


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Form1()
    window.show()
    sys.exit(app.exec_())
