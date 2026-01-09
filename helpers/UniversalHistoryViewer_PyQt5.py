"""
UniversalHistoryViewer_PyQt5.py - Universal History Viewer (PyQt5)
Optimized OOP structure with lazy loading
"""
import sys
import os
from datetime import datetime

# Core PyQt5 imports
from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                QFrame, QLabel, QPushButton, QLineEdit, QComboBox,
                                QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
                                QMessageBox, QFileDialog, QDesktopWidget, QAbstractItemView,
                                QTextEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QColor, QPixmap

# Lazy imports
_pil_image = None

def _lazy_import_pil():
    """Lazy import PIL"""
    global _pil_image
    if _pil_image is None:
        from PIL import Image
        _pil_image = Image
    return _pil_image

# Database
from helpers.unified_database import UnifiedDatabase
from helpers.resource_path import get_logo_path


# ============================================
# HELPER DIALOG CLASSES
# ============================================

class DetailViewerDialog(QDialog):
    """Detailed view of application"""
    __slots__ = ('app', 'db')
    
    def __init__(self, parent, application):
        super().__init__(parent)
        self.app = application
        self.setWindowTitle(f"Detail - {application.get('rujukan_kami', 'N/A')}")
        self.setGeometry(100, 100, 900, 700)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #003366;")
        header.setFixedHeight(60)
        header_layout = QVBoxLayout(header)
        title = QLabel(f"DETAIL PERMOHONAN - {self.app['form_type'].upper()}")
        title.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        layout.addWidget(header)
        
        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(30, 20, 30, 20)
        
        # Basic info
        info_label = QLabel("MAKLUMAT ASAS")
        info_label.setStyleSheet("color: #003366; font-size: 11px; font-weight: bold;")
        scroll_layout.addWidget(info_label)
        
        basic_info = [
            ("Rujukan:", self.app.get('rujukan_kami', '-')),
            ("Nama Syarikat:", self.app.get('nama_syarikat', '-')),
            ("Alamat:", self.app.get('alamat', '-')),
            ("Tarikh:", self.app.get('tarikh', '-')),
            ("Status:", self.app.get('status', '-')),
            ("Pegawai:", self.app.get('nama_pegawai', '-')),
            ("Tarikh Rekod:", self.app.get('created_at', '-'))
        ]
        
        info_grid = QGridLayout()
        row = 0
        for label, value in basic_info:
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold;")
            info_grid.addWidget(label_widget, row, 0)
            
            value_widget = QLabel(str(value))
            value_widget.setWordWrap(True)
            info_grid.addWidget(value_widget, row, 1)
            row += 1
        
        scroll_layout.addLayout(info_grid)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Close button
        btn_close = QPushButton("Tutup")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 5px;
            }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.center_dialog()
    
    def center_dialog(self):
        """Center dialog on screen"""
        self.setGeometry(
            (QDesktopWidget().screenGeometry().width() - self.width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.height()) // 2,
            self.width(), self.height()
        )


class StatisticsDialog(QDialog):
    """Statistics dashboard dialog"""
    __slots__ = ('db',)
    
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Statistik Sistem")
        self.setGeometry(100, 100, 1000, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #003366;")
        header.setFixedHeight(60)
        header_layout = QVBoxLayout(header)
        title = QLabel("STATISTIK SISTEM")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        layout.addWidget(header)
        
        # Content
        stats = self.db.get_statistics()
        
        info_text = f"""STATISTIK KESELURUHAN SISTEM

Jumlah Permohonan: {stats.get('total_applications', 0)}

Minggu Ini (7 hari): {stats.get('last_7_days', 0)}
Bulan Ini (30 hari): {stats.get('last_30_days', 0)}
Tahun Ini: {stats.get('this_year', 0)}

Status Permohonan:
"""
        
        for status, count in stats.get('by_status', {}).items():
            info_text += f"  - {status}: {count}\n"
        
        if 'by_form_type' in stats:
            info_text += "\n\nMengikut Jenis Borang:\n"
            for form_type, count in stats.get('by_form_type', {}).items():
                info_text += f"  - {form_type.upper()}: {count}\n"
        
        text_widget = QTextEdit()
        text_widget.setPlainText(info_text)
        text_widget.setReadOnly(True)
        text_widget.setStyleSheet("font-size: 11px; padding: 10px;")
        layout.addWidget(text_widget)
        
        # Close button
        btn_close = QPushButton("Tutup")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 5px;
            }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.center_dialog()
    
    def center_dialog(self):
        """Center dialog on screen"""
        self.setGeometry(
            (QDesktopWidget().screenGeometry().width() - self.width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.height()) // 2,
            self.width(), self.height()
        )


# ============================================
# MAIN HISTORY VIEWER CLASS
# ============================================

class UniversalHistoryViewer(QDialog):
    """Universal history viewer for all document types"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = UnifiedDatabase()
        
        self.setWindowTitle("Sejarah Semua Dokumen - Sistem Pengurusan Kastam")
        self.setGeometry(100, 100, 1400, 800)
        
        # Colors
        self.colors = {
            'primary': '#003366',
            'bg_main': '#F5F5F5',
            'button_info': '#1976D2',
            'button_danger': '#C62828',
            'button_success': '#2E7D32',
            'button_warning': '#F57C00'
        }
        
        # Create UI
        self.create_ui()
        self.center_window()
        
        # Load initial data
        QTimer.singleShot(100, lambda: (
            self.load_data(),
            self.update_statistics()
        ))
    
    def create_ui(self):
        """Create the main UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self.create_header(main_layout)
        
        # Filter section
        self.create_filter_section(main_layout)
        
        # Stats section
        self.create_stats_section(main_layout)
        
        # Table section
        self.create_table_section(main_layout)
        
        # Button section
        self.create_button_section(main_layout)
    
    def create_header(self, parent_layout):
        """Create header"""
        header = QFrame()
        header.setFixedHeight(90)
        header.setStyleSheet(f"background-color: {self.colors['primary']};")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo
        try:
            Image = _lazy_import_pil()
            logo_image = Image.open(get_logo_path())
            if logo_image.mode != 'RGBA':
                logo_image = logo_image.convert('RGBA')
            logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
            
            bg_rgb = tuple(int(self.colors['primary'][i:i+2], 16) for i in (1, 3, 5))
            background = Image.new('RGBA', logo_image.size, bg_rgb + (255,))
            if logo_image.mode == 'RGBA':
                logo_image = Image.alpha_composite(background, logo_image)
                logo_image = logo_image.convert('RGB')
            
            from io import BytesIO
            buf = BytesIO()
            logo_image.save(buf, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            
            logo_label = QLabel()
            logo_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setStyleSheet(f"background-color: {self.colors['primary']};")
            header_layout.addWidget(logo_label)
        except:
            pass
        
        # Title
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("SEJARAH DOKUMEN")
        title.setStyleSheet(f"background-color: {self.colors['primary']}; color: white; font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Sistem Pengurusan Dokumen Automatik")
        subtitle.setStyleSheet(f"background-color: {self.colors['primary']}; color: #E0E0E0; font-size: 10px; font-style: italic;")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        header_layout.addWidget(title_widget, stretch=1)
        
        # Close button
        btn_close = QPushButton("✕ TUTUP")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #C62828;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        btn_close.clicked.connect(self.reject)
        header_layout.addWidget(btn_close)
        
        parent_layout.addWidget(header)
    
    def create_filter_section(self, parent_layout):
        """Create filter and search section"""
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: white;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        
        # Search
        filter_layout.addWidget(QLabel("Cari:"))
        self.search_entry = QLineEdit()
        self.search_entry.setMinimumWidth(300)
        self.search_entry.textChanged.connect(self.on_search)
        filter_layout.addWidget(self.search_entry)
        
        btn_search = QPushButton("🔍 Cari")
        btn_search.setStyleSheet(f"background-color: {self.colors['button_info']}; color: white; padding: 5px 10px;")
        btn_search.clicked.connect(self.on_search)
        filter_layout.addWidget(btn_search)
        
        # Form Type Filter
        filter_layout.addWidget(QLabel("Jenis Borang:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Semua', 'Pelupusan', 'Butiran 5D', 'AMES', 'Sign Up B'])
        self.filter_combo.currentTextChanged.connect(self.load_data)
        filter_layout.addWidget(self.filter_combo)
        
        # Buttons
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setStyleSheet("background-color: #666666; color: white; padding: 5px 10px;")
        btn_refresh.clicked.connect(self.load_data)
        filter_layout.addWidget(btn_refresh)
        
        btn_report = QPushButton("📊 Laporan")
        btn_report.setStyleSheet(f"background-color: {self.colors['button_warning']}; color: white; padding: 5px 10px;")
        btn_report.clicked.connect(self.show_report)
        filter_layout.addWidget(btn_report)
        
        parent_layout.addWidget(filter_frame)
    
    def create_stats_section(self, parent_layout):
        """Create statistics dashboard"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: white;")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        self.stat_cards = {}
        stats_data = [
            ('total', 'JUMLAH', '#1976D2'),
            ('approved', 'DILULUSKAN', '#2E7D32'),
            ('rejected', 'DITOLAK', '#C62828'),
            ('month', 'BULAN INI', '#F57C00'),
            ('week', '7 HARI', '#7B1FA2')
        ]
        
        for key, label, color in stats_data:
            card = QFrame()
            card.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            card.setFixedHeight(80)
            card_layout = QVBoxLayout(card)
            card_layout.setAlignment(Qt.AlignCenter)
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"background-color: {color}; color: white; font-size: 9px; font-weight: bold;")
            label_widget.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(label_widget)
            
            value_label = QLabel("0")
            value_label.setStyleSheet(f"background-color: {color}; color: white; font-size: 20px; font-weight: bold;")
            value_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(value_label)
            
            self.stat_cards[key] = value_label
            stats_layout.addWidget(card)
        
        parent_layout.addWidget(stats_frame)
    
    def create_table_section(self, parent_layout):
        """Create main data table"""
        table_frame = QFrame()
        table_frame.setStyleSheet("background-color: white;")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'JENIS', 'KATEGORI', 'RUJUKAN', 
                                             'NAMA', 'TARIKH', 'STATUS', 'PEGAWAI', 'REKOD'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(False)
        # Ensure all rows have white background (no stripes)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: white;
            }
            QTableWidget::item {
                background-color: white;
            }
        """)
        
        # Set column widths
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 250)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 120)
        self.table.setColumnWidth(7, 200)
        self.table.setColumnWidth(8, 150)
        
        table_layout.addWidget(self.table)
        parent_layout.addWidget(table_frame, stretch=1)
    
    def create_button_section(self, parent_layout):
        """Create action buttons"""
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background-color: white;")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(20, 10, 20, 20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        buttons = [
            ("👁 Lihat Detail", self.colors['button_info'], self.view_details),
            ("📄 Buka Dokumen", self.colors['button_success'], self.open_document),
            ("🗑 Hapus Rekod", self.colors['button_danger'], self.delete_record),
            ("📊 Eksport CSV", '#2E7D32', self.export_csv),
            ("📈 Statistik", self.colors['button_warning'], self.show_statistics)
        ]
        
        for text, color, command in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 5px;
                }}
            """)
            btn.clicked.connect(command)
            btn_layout.addWidget(btn)
        
        parent_layout.addWidget(btn_frame)
    
    def load_data(self):
        """Load data based on filter"""
        self.table.setRowCount(0)
        
        filter_value = self.filter_combo.currentText()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        applications = self.db.get_all_applications(form_type=form_type, limit=200)
        
        self.table.setRowCount(len(applications))
        for row, app in enumerate(applications):
            self.table.setItem(row, 0, QTableWidgetItem(str(app['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(app['form_type'].upper()))
            self.table.setItem(row, 2, QTableWidgetItem(app.get('category', '-')))
            self.table.setItem(row, 3, QTableWidgetItem(app['rujukan_kami'] or '-'))
            self.table.setItem(row, 4, QTableWidgetItem(app['nama_syarikat']))
            self.table.setItem(row, 5, QTableWidgetItem(app['tarikh'] or '-'))
            self.table.setItem(row, 6, QTableWidgetItem(app.get('status', '-')))
            self.table.setItem(row, 7, QTableWidgetItem(app.get('nama_pegawai', '-')))
            self.table.setItem(row, 8, QTableWidgetItem(app['created_at']))
            
            # Color coding based on status
            status = app.get('status', '').upper()
            color = QColor(255, 255, 255)  # Default white
            if 'DILULUSKAN' in status or 'LULUS' in status:
                color = QColor(232, 245, 233)  # Light green
            elif 'TIDAK' in status or 'DITOLAK' in status:
                color = QColor(255, 235, 238)  # Light red
            
            for col in range(9):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)
        
        self.update_statistics()
    
    def on_search(self):
        """Perform search"""
        search_text = self.search_entry.text().strip()
        
        if not search_text:
            self.load_data()
            return
        
        self.table.setRowCount(0)
        
        filter_value = self.filter_combo.currentText()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        results = self.db.search_applications(search_text, form_type=form_type)
        
        self.table.setRowCount(len(results))
        for row, app in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(app['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(app['form_type'].upper()))
            self.table.setItem(row, 2, QTableWidgetItem(app.get('category', '-')))
            self.table.setItem(row, 3, QTableWidgetItem(app['rujukan_kami'] or '-'))
            self.table.setItem(row, 4, QTableWidgetItem(app['nama_syarikat']))
            self.table.setItem(row, 5, QTableWidgetItem(app['tarikh'] or '-'))
            self.table.setItem(row, 6, QTableWidgetItem(app.get('status', '-')))
            self.table.setItem(row, 7, QTableWidgetItem(app.get('nama_pegawai', '-')))
            self.table.setItem(row, 8, QTableWidgetItem(app['created_at']))
            
            # Color coding
            status = app.get('status', '').upper()
            color = QColor(255, 255, 255)
            if 'DILULUSKAN' in status or 'LULUS' in status:
                color = QColor(232, 245, 233)
            elif 'TIDAK' in status or 'DITOLAK' in status:
                color = QColor(255, 235, 238)
            
            for col in range(9):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)
    
    def update_statistics(self):
        """Update statistics cards"""
        filter_value = self.filter_combo.currentText()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        stats = self.db.get_statistics(form_type=form_type)
        
        self.stat_cards['total'].setText(str(stats.get('total_applications', 0)))
        
        by_status = stats.get('by_status', {})
        approved = sum(count for status, count in by_status.items() 
                      if 'DILULUSKAN' in status.upper() or 'LULUS' in status.upper())
        rejected = sum(count for status, count in by_status.items() 
                      if 'TIDAK' in status.upper() or 'DITOLAK' in status.upper())
        
        self.stat_cards['approved'].setText(str(approved))
        self.stat_cards['rejected'].setText(str(rejected))
        self.stat_cards['month'].setText(str(stats.get('this_month', 0)))
        self.stat_cards['week'].setText(str(stats.get('last_7_days', 0)))
    
    def view_details(self):
        """View application details"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Amaran", "Sila pilih rekod untuk dilihat")
            return
        
        app_id = int(self.table.item(selected, 0).text())
        application = self.db.get_application_by_id(app_id)
        if not application:
            QMessageBox.critical(self, "Ralat", "Rekod tidak dijumpai")
            return
        
        dialog = DetailViewerDialog(self, application)
        dialog.exec_()
    
    def open_document(self):
        """Open saved document"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Amaran", "Sila pilih rekod")
            return
        
        app_id = int(self.table.item(selected, 0).text())
        application = self.db.get_application_by_id(app_id)
        if not application:
            return
        
        doc_path = application.get('document_path')
        if not doc_path or not os.path.exists(doc_path):
            QMessageBox.warning(self, "Amaran", "Dokumen tidak dijumpai")
            return
        
        try:
            if os.name == 'nt':
                os.startfile(doc_path)
            else:
                import subprocess
                subprocess.call(['open', doc_path])
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Tidak dapat buka dokumen: {e}")
    
    def delete_record(self):
        """Delete selected record"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Amaran", "Sila pilih rekod untuk dihapus")
            return
        
        reply = QMessageBox.question(self, "Pengesahan",
            "Adakah anda pasti ingin menghapus rekod ini?\n\n"
            "Tindakan ini tidak boleh dibatalkan.",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply != QMessageBox.Yes:
            return
        
        app_id = int(self.table.item(selected, 0).text())
        try:
            self.db.delete_application(app_id)
            self.table.removeRow(selected)
            self.update_statistics()
            QMessageBox.information(self, "Berjaya", "Rekod berjaya dihapus")
        except Exception as e:
            QMessageBox.critical(self, "Ralat", f"Gagal menghapus rekod: {str(e)}")
    
    def export_csv(self):
        """Export to CSV"""
        filter_value = self.filter_combo.currentText()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Eksport CSV",
            f"kastam_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV files (*.csv);;All files (*.*)")
        
        if filename:
            try:
                self.db.export_to_csv(form_type=form_type, filename=filename)
                QMessageBox.information(self, "Berjaya", f"Data berjaya dieksport ke:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Ralat", f"Gagal eksport: {str(e)}")
    
    def show_statistics(self):
        """Show detailed statistics"""
        dialog = StatisticsDialog(self, self.db)
        dialog.exec_()
    
    def show_report(self):
        """Show monthly report"""
        QMessageBox.information(self, "Info", "Laporan bulanan akan ditambah kemudian")
    
    def center_window(self):
        """Center window on screen"""
        self.setGeometry(
            (QDesktopWidget().screenGeometry().width() - self.width()) // 2,
            (QDesktopWidget().screenGeometry().height() - self.height()) // 2,
            self.width(), self.height()
        )

