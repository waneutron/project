"""
template_completeness_dialog.py - ENHANCED with Placeholder Mapping
User-friendly GUI for one-time template configuration
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QProgressBar, QGroupBox, QWidget, QMessageBox,
    QTextEdit, QScrollArea, QFrame, QComboBox, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog
)
from PyQt5.QtCore import Qt
from helpers.template_field_validator import TemplateFieldValidator
import os


class PlaceholderMappingDialog(QDialog):
    """
    ONE-TIME Configuration Dialog for Template Placeholders
    User maps placeholders to form fields ONCE, system remembers forever
    """
    
    def __init__(self, parent, template_file, template_path, mapper):
        super().__init__(parent)
        self.parent_window = parent
        self.template_file = template_file
        self.template_path = template_path
        self.mapper = mapper
        
        # Scan template for placeholders
        self.placeholders = self.mapper.scan_template_placeholders(template_path)
        self.temp_mapping = {}
        
        self.setWindowTitle(f"Configure Template Mapping - {template_file}")
        self.setGeometry(150, 100, 1100, 750)
        self.setModal(True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #003366;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("⚙️ One-Time Template Configuration")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        subtitle = QLabel(f"Template: {self.template_file}")
        subtitle.setStyleSheet("color: #E0E0E0; font-size: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Instructions
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border-left: 4px solid #FF9800;
                border-radius: 3px;
                padding: 10px;
            }
        """)
        instructions_layout = QVBoxLayout(instructions_frame)
        
        instructions = QLabel(
            "📌 <b>Configure this mapping ONCE</b> - The system will remember it forever.<br>"
            "🎯 <b>Task:</b> Map each placeholder to a form field or custom value.<br>"
            "💡 <b>Tip:</b> Use <i>COMPUTED</i> fields for auto-calculated values (like full address)."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #333; font-size: 13px;")
        instructions_layout.addWidget(instructions)
        layout.addWidget(instructions_frame)
        
        # Stats
        if not self.placeholders:
            no_placeholders = QLabel("✅ No placeholders found - Template ready to use as-is")
            no_placeholders.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold; padding: 10px;")
            layout.addWidget(no_placeholders)
            
            # Just close button
            btn_ok = QPushButton("OK")
            btn_ok.clicked.connect(self.save_empty_and_close)
            layout.addWidget(btn_ok)
            return
        
        stats = QLabel(f"Found {len(self.placeholders)} placeholders to configure")
        stats.setStyleSheet("color: #FF9800; font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(stats)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Placeholder', 'Map To Field', 'Custom Value'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setRowCount(len(self.placeholders))
        self.table.setAlternatingRowColors(True)
        
        field_options = self.mapper.get_field_options()
        
        for row, placeholder in enumerate(self.placeholders):
            # Placeholder name (read-only, styled)
            item = QTableWidgetItem(placeholder)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setForeground(Qt.blue)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.table.setItem(row, 0, item)
            
            # Field selector combo
            combo = QComboBox()
            combo.addItem("-- Select Field --", "")
            
            for field_id, display_name in field_options.items():
                # Add icon/prefix for special types
                if field_id.startswith('COMPUTED:'):
                    icon = "🔧 "
                elif field_id == 'CUSTOM':
                    icon = "✏️ "
                else:
                    icon = "📝 "
                combo.addItem(icon + display_name, field_id)
            
            # Auto-suggest based on placeholder name
            placeholder_clean = placeholder.replace('<<', '').replace('>>', '').upper()
            best_match = None
            best_score = 0
            
            for field_id, display_name in field_options.items():
                if placeholder_clean in display_name.upper():
                    # Calculate similarity score
                    if placeholder_clean == field_id.upper():
                        best_match = display_name
                        best_score = 100
                        break
                    elif field_id.upper() in placeholder_clean:
                        if len(field_id) > best_score:
                            best_match = display_name
                            best_score = len(field_id)
            
            if best_match:
                combo.setCurrentText(best_match)
            
            self.table.setCellWidget(row, 1, combo)
            
            # Custom value input (only enabled if CUSTOM selected)
            custom_input = QLineEdit()
            custom_input.setEnabled(False)
            custom_input.setPlaceholderText("Enter custom value here...")
            self.table.setCellWidget(row, 2, custom_input)
            
            # Connect combo change
            def on_combo_change(text, p=placeholder, ci=custom_input, c=combo):
                field_id = c.currentData()
                if field_id == 'CUSTOM':
                    ci.setEnabled(True)
                    ci.setFocus()
                    ci.setStyleSheet("background-color: #FFFACD;")
                else:
                    ci.setEnabled(False)
                    ci.clear()
                    ci.setStyleSheet("")
                
                # Update temp mapping
                if field_id:
                    if field_id == 'CUSTOM':
                        # Will be updated when custom_input changes
                        pass
                    else:
                        self.temp_mapping[p] = field_id
                else:
                    self.temp_mapping.pop(p, None)
                
                self.update_stats_label()
            
            combo.currentTextChanged.connect(on_combo_change)
            
            # Connect custom input
            def on_custom_change(text, p=placeholder):
                if text.strip():
                    self.temp_mapping[p] = f"CUSTOM:{text.strip()}"
                else:
                    self.temp_mapping.pop(p, None)
                self.update_stats_label()
            
            custom_input.textChanged.connect(on_custom_change)
        
        layout.addWidget(self.table)
        
        # Stats label for mapping progress
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #666; font-size: 12px; font-style: italic;")
        layout.addWidget(self.stats_label)
        self.update_stats_label()
        
        # Warning
        warning = QLabel("⚠️ Unmapped placeholders will remain as <<PLACEHOLDER>> in the document")
        warning.setStyleSheet("color: #F44336; font-size: 12px; font-style: italic;")
        layout.addWidget(warning)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("❌ Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        
        btn_save = QPushButton("💾 Save Configuration")
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_save.clicked.connect(self.save_mapping)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
    
    def update_stats_label(self):
        """Update mapping statistics"""
        mapped_count = len(self.temp_mapping)
        total_count = len(self.placeholders)
        unmapped_count = total_count - mapped_count
        
        if mapped_count == total_count:
            self.stats_label.setText(f"✅ All {total_count} placeholders mapped!")
            self.stats_label.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold;")
        else:
            self.stats_label.setText(
                f"Mapped: {mapped_count}/{total_count} | "
                f"Remaining: {unmapped_count}"
            )
            self.stats_label.setStyleSheet("color: #FF9800; font-size: 12px; font-style: italic;")
    
    def save_mapping(self):
        """Save the mapping configuration"""
        mapped_count = len(self.temp_mapping)
        unmapped_count = len(self.placeholders) - mapped_count
        
        if unmapped_count > 0:
            reply = QMessageBox.question(self, "Confirm",
                f"You have mapped {mapped_count}/{len(self.placeholders)} placeholders.\n"
                f"{unmapped_count} placeholder(s) will remain unmapped.\n\n"
                f"Save this configuration?",
                QMessageBox.Yes | QMessageBox.No)
            
            if reply != QMessageBox.Yes:
                return
        
        # Save mapping
        self.mapper.set_template_mapping(self.template_file, self.temp_mapping)
        
        QMessageBox.information(self, "Success",
            f"✅ Configuration saved!\n\n"
            f"Mapped: {mapped_count}/{len(self.placeholders)}\n"
            f"Template: {self.template_file}\n\n"
            f"This template is now ready to use.\n"
            f"You won't need to configure it again.")
        
        self.accept()
    
    def save_empty_and_close(self):
        """Save empty mapping for templates without placeholders"""
        self.mapper.set_template_mapping(self.template_file, {})
        self.accept()


class TemplateScannerDialog(QDialog):
    """
    ENHANCED Dialog to scan templates and configure mappings
    All-in-one interface for template management
    """
    
    def __init__(self, parent, mapper=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # Use provided mapper or create new one
        if mapper is None:
            from helpers.placeholder_mapper import PlaceholderMapper
            self.mapper = PlaceholderMapper()
        else:
            self.mapper = mapper
        
        self.setWindowTitle("Template Scanner & Mapper")
        self.setGeometry(200, 200, 900, 700)
        self.setup_ui()
    
    def setup_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #003366;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        header = QLabel("📄 Template Scanner & Placeholder Mapper")
        header.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(header)
        
        subtitle = QLabel("Scan templates and configure placeholder mappings")
        subtitle.setStyleSheet("color: #E0E0E0; font-size: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Instructions
        instructions = QLabel(
            "Select a template file to scan for placeholders (<<PLACEHOLDER>>).\n"
            "Configure the mapping once, and the system will remember it forever."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666666; padding: 10px; font-size: 13px;")
        layout.addWidget(instructions)
        
        # File selection
        file_frame = QGroupBox("Template Selection")
        file_layout = QVBoxLayout()

        # Template selection combo
        template_row = QHBoxLayout()
        template_row.addWidget(QLabel("Select Template:"))

        self.template_combo = QComboBox()
        self.template_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                background-color: white;
            }
        """)
        self.load_available_templates()
        self.template_combo.currentTextChanged.connect(self.on_template_selected)
        template_row.addWidget(self.template_combo, 1)

        btn_load_selected = QPushButton("📋 Load Selected")
        btn_load_selected.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_load_selected.clicked.connect(self.load_selected_template)
        template_row.addWidget(btn_load_selected)

        file_layout.addLayout(template_row)

        # OR separator
        or_label = QLabel("— OR —")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("color: #666666; margin: 10px 0px;")
        file_layout.addWidget(or_label)

        # File browsing
        file_row = QHBoxLayout()
        file_row.addWidget(QLabel("Browse File:"))

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet(
            "padding: 8px; border: 1px solid #CCCCCC; border-radius: 3px; "
            "background-color: white;"
        )
        file_row.addWidget(self.file_label, 1)

        btn_browse = QPushButton("📁 Browse...")
        btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_browse.clicked.connect(self.browse_template)
        file_row.addWidget(btn_browse)

        file_layout.addLayout(file_row)
        
        # Configuration status
        self.config_status = QLabel()
        self.config_status.setStyleSheet("font-size: 12px; padding: 5px;")
        file_layout.addWidget(self.config_status)
        
        file_frame.setLayout(file_layout)
        layout.addWidget(file_frame)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.btn_scan = QPushButton("🔍 Scan Template")
        self.btn_scan.setEnabled(False)
        self.btn_scan.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)
        self.btn_scan.clicked.connect(self.scan_template)
        action_layout.addWidget(self.btn_scan)
        
        self.btn_configure = QPushButton("⚙️ Configure Mapping")
        self.btn_configure.setEnabled(False)
        self.btn_configure.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)
        self.btn_configure.clicked.connect(self.configure_mapping)
        action_layout.addWidget(self.btn_configure)
        
        layout.addLayout(action_layout)
        
        # Results area
        results_group = QGroupBox("Scan Results")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Select a template and click 'Scan Template' to see results...")
        self.results_text.setStyleSheet("background-color: #F5F5F5; font-family: Consolas, monospace;")
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        
        layout.addLayout(btn_layout)
        
        self.template_file = None
        self.template_path = None
        self.placeholders = []

    def load_available_templates(self):
        """Load available templates from template storage"""
        templates = []

        # Try to get from template storage first
        try:
            from helpers.template_storage import get_template_storage
            storage = get_template_storage()
            if hasattr(storage, 'templates'):
                for template_name in storage.templates.keys():
                    display_name = template_name.replace('.docx', '').replace('.doc', '').replace('_', ' ').title()
                    templates.append((template_name, display_name))
        except ImportError:
            pass

        # Fallback to common templates
        if not templates:
            templates = [
                ("pelupusan_pemusnahan.docx", "Pelupusan - Pemusnahan"),
                ("pelupusan_penjualan.docx", "Pelupusan - Penjualan"),
                ("pelupusan_skrap.docx", "Pelupusan - Skrap"),
                ("pelupusan_tidak_lulus.docx", "Pelupusan - Tidak Lulus"),
                ("batal_sijil.doc", "Batal Sijil"),
                ("surat kelulusan butiran 5D (Lulus).docx", "Butiran 5D - Lulus"),
                ("surat kelulusan butiran 5D (tidak lulus).docx", "Butiran 5D - Tidak Lulus"),
            ]

        # Add to combo
        self.template_combo.clear()
        self.template_combo.addItem("-- Select Template --", "")
        for template_file, display_name in templates:
            self.template_combo.addItem(display_name, template_file)

    def on_template_selected(self, text):
        """Handle template selection from combo"""
        if text and text != "-- Select Template --":
            # Clear file selection when template is selected
            self.file_label.setText("Template selected from list")
            self.template_file = self.template_combo.currentData()
            self.template_path = None  # Will be resolved when loaded
            self.btn_scan.setEnabled(True)
            self.results_text.clear()

            # Check if already configured
            if self.mapper.is_template_configured(self.template_file):
                self.config_status.setText("✅ This template is already configured")
                self.config_status.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold;")
            else:
                self.config_status.setText("⚠️ This template needs configuration")
                self.config_status.setStyleSheet("color: #FF9800; font-size: 12px; font-weight: bold;")
        else:
            self.template_file = None
            self.template_path = None
            self.btn_scan.setEnabled(False)
            self.config_status.setText("")

    def load_selected_template(self):
        """Load the selected template from combo"""
        if not self.template_file:
            QMessageBox.warning(self, "No Selection", "Please select a template first")
            return

        # Try to get template path
        try:
            from helpers.resource_path import get_template_path
            self.template_path = get_template_path(self.template_file)
            if not os.path.exists(self.template_path):
                QMessageBox.warning(self, "Template Not Found",
                    f"Template file not found: {self.template_file}\n\n"
                    f"Expected path: {self.template_path}")
                return
        except ImportError:
            QMessageBox.warning(self, "Error", "Template storage system not available")
            return

        self.file_label.setText(f"Loaded: {self.template_file}")
        self.btn_scan.setEnabled(True)
        self.results_text.clear()

        QMessageBox.information(self, "Template Loaded",
            f"Template '{self.template_file}' has been loaded successfully.\n\n"
            f"You can now scan it for placeholders.")

    def browse_template(self):
        """Browse for template file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template File",
            "",
            "Word Documents (*.docx *.doc);;All Files (*.*)"
        )
        
        if file_path:
            self.template_path = file_path
            self.template_file = os.path.basename(file_path)
            self.file_label.setText(self.template_file)
            self.btn_scan.setEnabled(True)
            self.results_text.clear()
            
            # Check if already configured
            if self.mapper.is_template_configured(self.template_file):
                self.config_status.setText("✅ This template is already configured")
                self.config_status.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold;")
            else:
                self.config_status.setText("⚠️ This template needs configuration")
                self.config_status.setStyleSheet("color: #FF9800; font-size: 12px; font-weight: bold;")
    
    def scan_template(self):
        """Scan template for placeholders"""
        if not self.template_file or not self.template_path:
            QMessageBox.warning(self, "Warning", "Please select a template file first")
            return
        
        # Scan for placeholders
        self.placeholders = self.mapper.scan_template_placeholders(self.template_path)
        
        # Display results
        self.results_text.clear()
        
        html = f"<h3 style='color: #003366;'>Template: {self.template_file}</h3>"
        html += f"<p style='color: #666;'>Found <b>{len(self.placeholders)}</b> placeholders</p>"
        
        if self.placeholders:
            html += "<hr>"
            html += "<table style='width: 100%; border-collapse: collapse;'>"
            html += "<tr style='background-color: #E3F2FD;'><th style='padding: 8px; text-align: left;'>#</th><th style='padding: 8px; text-align: left;'>Placeholder</th><th style='padding: 8px; text-align: left;'>Status</th></tr>"
            
            # Check mapping status for each
            existing_mapping = self.mapper.get_template_mapping(self.template_file) or {}
            
            for i, placeholder in enumerate(self.placeholders, 1):
                if placeholder in existing_mapping:
                    status = f"<span style='color: #4CAF50;'>✓ Mapped to: {existing_mapping[placeholder]}</span>"
                    row_color = "#E8F5E9"
                else:
                    status = "<span style='color: #F44336;'>✗ Not mapped</span>"
                    row_color = "#FFEBEE"
                
                html += f"<tr style='background-color: {row_color};'>"
                html += f"<td style='padding: 8px;'>{i}</td>"
                html += f"<td style='padding: 8px; color: #1976D2; font-weight: bold;'>{placeholder}</td>"
                html += f"<td style='padding: 8px;'>{status}</td>"
                html += "</tr>"
            
            html += "</table>"
            
            self.btn_configure.setEnabled(True)
        else:
            html += "<p style='color: #4CAF50; font-weight: bold;'>✅ No placeholders found in template.</p>"
            html += "<p>This template can be used as-is without configuration.</p>"
            self.btn_configure.setEnabled(False)
        
        # Show configuration summary
        if self.mapper.is_template_configured(self.template_file):
            mapping = self.mapper.get_template_mapping(self.template_file)
            mapped_count = len(mapping)
            html += f"<hr><p style='color: #4CAF50; font-weight: bold;'>✅ Template Configuration: {mapped_count}/{len(self.placeholders)} placeholders mapped</p>"
        else:
            html += "<hr><p style='color: #FF9800; font-weight: bold;'>⚠️ This template is not configured yet. Click 'Configure Mapping' to set it up.</p>"
        
        self.results_text.setHtml(html)
    
    def configure_mapping(self):
        """Open configuration dialog"""
        if not self.placeholders:
            QMessageBox.warning(self, "Warning", "Please scan template first")
            return
        
        # Open mapping dialog
        dialog = PlaceholderMappingDialog(
            self, self.template_file, self.template_path, self.mapper
        )
        
        if dialog.exec_():
            # Refresh scan to show updated status
            self.scan_template()
            
            QMessageBox.information(self, "Configuration Complete",
                f"Template '{self.template_file}' has been configured.\n\n"
                f"The system will now use this mapping automatically\n"
                f"every time you generate documents with this template.")


# Keep original TemplateCompletenessDialog for backward compatibility
class TemplateCompletenessDialog(QDialog):
    """Dialog untuk check template-field completeness"""
    
    def __init__(self, parent, form_name, template_file, custom_fields=None, existing_mapping=None):
        super().__init__(parent)
        self.parent_window = parent
        self.form_name = form_name
        self.template_file = template_file
        self.custom_fields = custom_fields or []
        self.existing_mapping = existing_mapping
        
        self.validator = TemplateFieldValidator()
        
        self.setWindowTitle(f"Template Completeness Check - {template_file}")
        self.setGeometry(200, 200, 800, 700)
        self.setup_ui()
        self.run_check()
    
    def setup_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #003366;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel(f"📄 Template Completeness Check")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        template_label = QLabel(f"Template: {self.template_file}")
        template_label.setStyleSheet("color: white; font-size: 12px;")
        header_layout.addWidget(template_label)
        
        layout.addWidget(header_frame)
        
        # Status section
        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFormat("%p% Complete")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Statistics
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 12px; color: #666666;")
        layout.addWidget(self.stats_label)
        
        # Scroll area untuk content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(15)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)
        
        layout.addLayout(btn_layout)
    
    def run_check(self):
        """Run completeness check"""
        result = self.validator.validate_template_completeness(
            self.form_name,
            self.template_file,
            self.custom_fields,
            self.existing_mapping
        )
        
        self.display_results(result)
    
    def display_results(self, result):
        """Display check results"""
        # Update status
        if result['is_complete']:
            self.status_label.setText(f"✅ {result['message']}")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold; padding: 10px;")
        else:
            self.status_label.setText(f"⚠️ {result['message']}")
            self.status_label.setStyleSheet("color: #FF9800; font-size: 14px; font-weight: bold; padding: 10px;")
        
        # Update progress
        self.progress_bar.setValue(int(result['completeness_percent']))
        
        # Update statistics
        self.stats_label.setText(
            f"Mapped: {result['mapped_count']}/{result['total_placeholders']} placeholders "
            f"({result['completeness_percent']:.1f}%)"
        )
        
        # Clear previous content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Show all placeholders
        all_section = QGroupBox("📋 All Placeholders in Template")
        all_layout = QVBoxLayout()
        
        all_list = QListWidget()
        all_list.setMaximumHeight(150)
        for placeholder in result['all_placeholders']:
            item = QListWidgetItem(f"<<{placeholder}>>")
            if placeholder in result['mapped_placeholders']:
                item.setForeground(Qt.green)
            else:
                item.setForeground(Qt.red)
            all_list.addItem(item)
        all_layout.addWidget(all_list)
        all_section.setLayout(all_layout)
        self.content_layout.addWidget(all_section)
        
        # Add stretch
        self.content_layout.addStretch()