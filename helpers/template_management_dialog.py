"""
template_management_dialog.py - COMPREHENSIVE Template Management GUI
Combines template selection, scanning, and placeholder mapping in one interface
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QProgressBar, QGroupBox, QWidget, QMessageBox,
    QTextEdit, QScrollArea, QFrame, QComboBox, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QTabWidget, QSplitter
)
from PyQt5.QtCore import Qt
from helpers.template_field_validator import TemplateFieldValidator
from helpers.template_selector_dialog import TemplateSelector
import os


class TemplateManagementDialog(QDialog):
    """
    COMPREHENSIVE Dialog that combines:
    - Template Selection (with compatibility checking)
    - Template Scanning
    - Placeholder Mapping
    All in one integrated workflow
    """

    def __init__(self, parent, module_name=None):
        super().__init__(parent)
        self.parent_window = parent
        self.module_name = module_name or 'Form2'

        # Initialize components
        from helpers.placeholder_mapper import PlaceholderMapper
        self.mapper = PlaceholderMapper()
        self.validator = TemplateFieldValidator()

        self.setWindowTitle("Template Management Center")
        self.setGeometry(100, 50, 1400, 900)
        self.setMinimumSize(1200, 700)

        self.selected_template = None
        self.template_path = None
        self.placeholders = []

        self.setup_ui()

    def setup_ui(self):
        """Create comprehensive UI with tabs"""
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

        title = QLabel("🎯 Template Management Center")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title)

        subtitle = QLabel("Integrated template selection, scanning, and mapping workflow")
        subtitle.setStyleSheet("color: #E0E0E0; font-size: 12px;")
        header_layout.addWidget(subtitle)

        layout.addWidget(header_frame)

        # Main content with splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - Template Selection & Info
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Main workflow tabs
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([400, 1000])
        layout.addWidget(splitter)

        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_help = QPushButton("❓ Help")
        btn_help.clicked.connect(self.show_help)
        btn_layout.addWidget(btn_help)

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

    def create_left_panel(self):
        """Create left panel with template selection and info"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Module selection
        module_group = QGroupBox("Module Selection")
        module_layout = QVBoxLayout()

        module_layout.addWidget(QLabel("Select Module:"))
        self.module_combo = QComboBox()
        modules = ['Form2', 'Form3', 'FormDeleteItem', 'FormSignUp']
        self.module_combo.addItems(modules)
        self.module_combo.setCurrentText(self.module_name)
        self.module_combo.currentTextChanged.connect(self.on_module_changed)
        module_layout.addWidget(self.module_combo)

        module_group.setLayout(module_layout)
        layout.addWidget(module_group)

        # Template selection
        template_group = QGroupBox("Template Selection")
        template_layout = QVBoxLayout()

        btn_select_template = QPushButton("🎯 Select Compatible Template")
        btn_select_template.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_select_template.clicked.connect(self.select_template)
        template_layout.addWidget(btn_select_template)

        self.selected_template_label = QLabel("No template selected")
        self.selected_template_label.setStyleSheet(
            "padding: 10px; border: 1px solid #CCCCCC; border-radius: 3px; "
            "background-color: #F5F5F5; font-weight: bold;"
        )
        self.selected_template_label.setWordWrap(True)
        template_layout.addWidget(self.selected_template_label)

        template_group.setLayout(template_layout)
        layout.addWidget(template_group)

        # Template info
        info_group = QGroupBox("Template Information")
        info_layout = QVBoxLayout()

        self.template_info = QTextEdit()
        self.template_info.setReadOnly(True)
        self.template_info.setMaximumHeight(200)
        self.template_info.setPlaceholderText("Template details will appear here...")
        info_layout.addWidget(self.template_info)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()

        btn_scan = QPushButton("🔍 Scan Template")
        btn_scan.clicked.connect(self.scan_template)
        btn_scan.setEnabled(False)
        self.btn_scan = btn_scan
        actions_layout.addWidget(btn_scan)

        btn_configure = QPushButton("⚙️ Configure Mapping")
        btn_configure.clicked.connect(self.configure_mapping)
        btn_configure.setEnabled(False)
        self.btn_configure = btn_configure
        actions_layout.addWidget(btn_configure)

        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        layout.addStretch()
        return panel

    def create_right_panel(self):
        """Create right panel with workflow tabs"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Tab widget
        self.tabs = QTabWidget()

        # Tab 1: Template Scanner
        self.scanner_tab = self.create_scanner_tab()
        self.tabs.addTab(self.scanner_tab, "🔍 Scanner")

        # Tab 2: Placeholder Mapper
        self.mapper_tab = self.create_mapper_tab()
        self.tabs.addTab(self.mapper_tab, "⚙️ Mapper")

        # Tab 3: Compatibility Report
        self.compatibility_tab = self.create_compatibility_tab()
        self.tabs.addTab(self.compatibility_tab, "📊 Compatibility")

        layout.addWidget(self.tabs)
        return panel

    def create_scanner_tab(self):
        """Create scanner tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Instructions
        instructions = QLabel(
            "📄 <b>Template Scanner</b><br><br>"
            "This tab shows the results of scanning your selected template for placeholders.<br>"
            "Select a template from the left panel and click 'Scan Template' to begin."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666666; padding: 10px; font-size: 13px;")
        layout.addWidget(instructions)

        # Results area
        results_group = QGroupBox("Scan Results")
        results_layout = QVBoxLayout()

        self.scan_results = QTextEdit()
        self.scan_results.setReadOnly(True)
        self.scan_results.setPlaceholderText("Scan results will appear here...")
        self.scan_results.setStyleSheet("background-color: #F5F5F5; font-family: Consolas, monospace;")
        results_layout.addWidget(self.scan_results)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        return tab

    def create_mapper_tab(self):
        """Create mapper tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Instructions
        instructions = QLabel(
            "⚙️ <b>Placeholder Mapper</b><br><br>"
            "Configure how placeholders in your template map to form fields.<br>"
            "This mapping is saved and remembered for future use."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666666; padding: 10px; font-size: 13px;")
        layout.addWidget(instructions)

        # Mapping table
        self.mapping_table = QTableWidget()
        self.mapping_table.setColumnCount(3)
        self.mapping_table.setHorizontalHeaderLabels(['Placeholder', 'Map To Field', 'Custom Value'])
        self.mapping_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.mapping_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.mapping_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.mapping_table.setAlternatingRowColors(True)
        layout.addWidget(self.mapping_table)

        # Stats
        self.mapping_stats = QLabel()
        self.mapping_stats.setStyleSheet("color: #666; font-size: 12px; font-style: italic; padding: 5px;")
        layout.addWidget(self.mapping_stats)

        # Buttons
        mapper_btn_layout = QHBoxLayout()
        mapper_btn_layout.addStretch()

        btn_save_mapping = QPushButton("💾 Save Mapping")
        btn_save_mapping.clicked.connect(self.save_mapping)
        btn_save_mapping.setEnabled(False)
        self.btn_save_mapping = btn_save_mapping
        mapper_btn_layout.addWidget(btn_save_mapping)

        layout.addLayout(mapper_btn_layout)

        return tab

    def create_compatibility_tab(self):
        """Create compatibility report tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Instructions
        instructions = QLabel(
            "📊 <b>Compatibility Report</b><br><br>"
            "This report shows how well your selected template works with different modules.<br>"
            "Higher match scores indicate better compatibility."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666666; padding: 10px; font-size: 13px;")
        layout.addWidget(instructions)

        # Compatibility table
        self.compatibility_table = QTableWidget()
        self.compatibility_table.setColumnCount(6)
        self.compatibility_table.setHorizontalHeaderLabels([
            'Module', 'Match Score', 'Required Found', 'Status', 'Recommendation', 'Details'
        ])
        self.compatibility_table.setColumnWidth(0, 120)
        self.compatibility_table.setColumnWidth(1, 100)
        self.compatibility_table.setColumnWidth(2, 120)
        self.compatibility_table.setColumnWidth(3, 80)
        self.compatibility_table.setColumnWidth(4, 200)
        self.compatibility_table.setColumnWidth(5, 250)
        layout.addWidget(self.compatibility_table)

        return tab

    def on_module_changed(self, module_name):
        """Handle module selection change"""
        self.module_name = module_name
        # Reset template selection when module changes
        self.selected_template = None
        self.template_path = None
        self.selected_template_label.setText("No template selected")
        self.template_info.clear()
        self.btn_scan.setEnabled(False)
        self.btn_configure.setEnabled(False)

    def select_template(self):
        """Open template selector dialog"""
        dialog = TemplateSelector(self, self.module_name)
        if dialog.exec_() == QDialog.Accepted:
            self.selected_template = dialog.get_selected_template()
            if self.selected_template:
                self.selected_template_label.setText(f"Selected: {self.selected_template}")

                # Try to get template path
                try:
                    from helpers.resource_path import get_template_path
                    self.template_path = get_template_path(self.selected_template)
                    if os.path.exists(self.template_path):
                        self.btn_scan.setEnabled(True)
                        self.update_template_info()
                        self.update_compatibility_report()
                    else:
                        QMessageBox.warning(self, "Template Not Found",
                            f"Template file not found: {self.selected_template}")
                except ImportError:
                    QMessageBox.warning(self, "Error", "Template storage system not available")

    def update_template_info(self):
        """Update template information display"""
        if not self.selected_template or not self.template_path:
            return

        # Get basic file info
        try:
            file_size = os.path.getsize(self.template_path)
            file_size_kb = file_size / 1024

            info = f"<b>Template:</b> {self.selected_template}<br>"
            info += f"<b>Path:</b> {self.template_path}<br>"
            info += f"<b>Size:</b> {file_size_kb:.1f} KB<br><br>"

            # Check configuration status
            if self.mapper.is_template_configured(self.selected_template):
                info += "✅ <b>Status:</b> Configured<br>"
                mapping = self.mapper.get_template_mapping(self.selected_template)
                info += f"📋 <b>Mapped placeholders:</b> {len(mapping)}<br>"
            else:
                info += "⚠️ <b>Status:</b> Not configured<br>"

            self.template_info.setHtml(info)

        except Exception as e:
            self.template_info.setText(f"Error getting template info: {str(e)}")

    def update_compatibility_report(self):
        """Update compatibility report for current template"""
        if not self.selected_template:
            return

        self.compatibility_table.setRowCount(0)

        modules = ['Form2', 'Form3', 'FormDeleteItem', 'FormSignUp']

        for module in modules:
            row = self.compatibility_table.rowCount()
            self.compatibility_table.insertRow(row)

            # Module name
            self.compatibility_table.setItem(row, 0, QTableWidgetItem(module))

            # Get compatibility
            try:
                match_result = self.validator.match_template_to_module(self.selected_template, module)

                score = match_result['match_score']
                score_item = QTableWidgetItem(f"{score:.1f}%")

                # Color based on score
                if score >= 90:
                    score_item.setBackground(Qt.green)
                elif score >= 70:
                    score_item.setBackground(Qt.yellow)
                else:
                    score_item.setBackground(Qt.red)

                self.compatibility_table.setItem(row, 1, score_item)

                # Required found
                required_found = match_result.get('required_found', 0)
                required_total = match_result.get('required_total', 0)
                self.compatibility_table.setItem(row, 2, QTableWidgetItem(f"{required_found}/{required_total}"))

                # Status
                if score >= 80:
                    status = "✓ Good"
                    status_color = Qt.green
                elif score >= 50:
                    status = "~ Fair"
                    status_color = Qt.yellow
                else:
                    status = "✗ Poor"
                    status_color = Qt.red

                status_item = QTableWidgetItem(status)
                status_item.setBackground(status_color)
                self.compatibility_table.setItem(row, 3, status_item)

                # Recommendation
                recommendation = match_result.get('recommendation', 'N/A')
                self.compatibility_table.setItem(row, 4, QTableWidgetItem(recommendation))

                # Details
                details = f"Score: {score:.1f}%, Required: {required_found}/{required_total}"
                self.compatibility_table.setItem(row, 5, QTableWidgetItem(details))

            except Exception as e:
                error_item = QTableWidgetItem(f"Error: {str(e)}")
                self.compatibility_table.setItem(row, 1, error_item)

    def scan_template(self):
        """Scan selected template for placeholders"""
        if not self.template_path or not os.path.exists(self.template_path):
            QMessageBox.warning(self, "No Template", "Please select a template first")
            return

        try:
            # Scan for placeholders
            self.placeholders = self.mapper.scan_template_placeholders(self.template_path)

            # Display results
            self.scan_results.clear()

            html = f"<h3 style='color: #003366;'>Template: {self.selected_template}</h3>"
            html += f"<p style='color: #666;'>Found <b>{len(self.placeholders)}</b> placeholders</p>"

            if self.placeholders:
                html += "<hr>"
                html += "<table style='width: 100%; border-collapse: collapse;'>"
                html += "<tr style='background-color: #E3F2FD;'><th style='padding: 8px; text-align: left;'>#</th><th style='padding: 8px; text-align: left;'>Placeholder</th><th style='padding: 8px; text-align: left;'>Status</th></tr>"

                # Check mapping status for each
                existing_mapping = self.mapper.get_template_mapping(self.selected_template) or {}

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
                self.tabs.setCurrentIndex(1)  # Switch to mapper tab
                self.populate_mapping_table()

            else:
                html += "<p style='color: #4CAF50; font-weight: bold;'>✅ No placeholders found in template.</p>"
                html += "<p>This template can be used as-is without configuration.</p>"
                self.btn_configure.setEnabled(False)

            self.scan_results.setHtml(html)

        except Exception as e:
            QMessageBox.critical(self, "Scan Error", f"Failed to scan template:\n{str(e)}")

    def populate_mapping_table(self):
        """Populate the mapping table with placeholders"""
        if not self.placeholders:
            return

        self.mapping_table.setRowCount(len(self.placeholders))

        field_options = self.mapper.get_field_options()
        existing_mapping = self.mapper.get_template_mapping(self.selected_template) or {}

        for row, placeholder in enumerate(self.placeholders):
            # Placeholder name (read-only, styled)
            item = QTableWidgetItem(placeholder)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setForeground(Qt.blue)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.mapping_table.setItem(row, 0, item)

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

            # Pre-select if already mapped
            if placeholder in existing_mapping:
                mapped_field = existing_mapping[placeholder]
                if mapped_field.startswith('CUSTOM:'):
                    combo.setCurrentText('✏️ Custom Value')
                else:
                    # Find the display name for the mapped field
                    for field_id, display_name in field_options.items():
                        if field_id == mapped_field:
                            combo.setCurrentText(display_name)
                            break

            self.mapping_table.setCellWidget(row, 1, combo)

            # Custom value input
            custom_value = ""
            if placeholder in existing_mapping:
                mapped_field = existing_mapping[placeholder]
                if mapped_field.startswith('CUSTOM:'):
                    custom_value = mapped_field.replace('CUSTOM:', '')

            custom_input = QLineEdit(custom_value)
            custom_input.setEnabled(combo.currentData() == 'CUSTOM')
            custom_input.setPlaceholderText("Enter custom value here...")
            self.mapping_table.setCellWidget(row, 2, custom_input)

            # Connect signals
            def on_combo_change(text, p=placeholder, ci=custom_input, c=combo):
                field_id = c.currentData()
                ci.setEnabled(field_id == 'CUSTOM')
                if field_id != 'CUSTOM':
                    ci.clear()
                self.update_mapping_stats()

            combo.currentTextChanged.connect(on_combo_change)

            def on_custom_change(text, p=placeholder):
                self.update_mapping_stats()

            custom_input.textChanged.connect(on_custom_change)

        self.update_mapping_stats()
        self.btn_save_mapping.setEnabled(True)

    def update_mapping_stats(self):
        """Update mapping statistics"""
        if not self.placeholders:
            return

        mapped_count = 0
        for row in range(self.mapping_table.rowCount()):
            combo = self.mapping_table.cellWidget(row, 1)
            custom_input = self.mapping_table.cellWidget(row, 2)

            if combo and combo.currentData():
                field_id = combo.currentData()
                if field_id == 'CUSTOM':
                    if custom_input and custom_input.text().strip():
                        mapped_count += 1
                else:
                    mapped_count += 1

        total_count = len(self.placeholders)
        unmapped_count = total_count - mapped_count

        if mapped_count == total_count:
            self.mapping_stats.setText(f"✅ All {total_count} placeholders mapped!")
            self.mapping_stats.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold;")
        else:
            self.mapping_stats.setText(
                f"Mapped: {mapped_count}/{total_count} | "
                f"Remaining: {unmapped_count}"
            )
            self.mapping_stats.setStyleSheet("color: #FF9800; font-size: 12px; font-style: italic;")

    def save_mapping(self):
        """Save the mapping configuration"""
        if not self.selected_template:
            QMessageBox.warning(self, "No Template", "No template selected")
            return

        # Collect mapping
        temp_mapping = {}
        for row in range(self.mapping_table.rowCount()):
            placeholder_item = self.mapping_table.item(row, 0)
            combo = self.mapping_table.cellWidget(row, 1)
            custom_input = self.mapping_table.cellWidget(row, 2)

            if placeholder_item and combo:
                placeholder = placeholder_item.text()
                field_id = combo.currentData()

                if field_id:
                    if field_id == 'CUSTOM':
                        if custom_input and custom_input.text().strip():
                            temp_mapping[placeholder] = f"CUSTOM:{custom_input.text().strip()}"
                    else:
                        temp_mapping[placeholder] = field_id

        # Save mapping
        self.mapper.set_template_mapping(self.selected_template, temp_mapping)

        QMessageBox.information(self, "Success",
            f"✅ Mapping saved!\n\n"
            f"Template: {self.selected_template}\n"
            f"Mapped: {len(temp_mapping)}/{len(self.placeholders)} placeholders\n\n"
            f"This template is now ready to use.\n"
            f"You won't need to configure it again.")

        # Refresh scan results
        self.scan_template()
        self.update_template_info()

    def configure_mapping(self):
        """Open detailed mapping configuration dialog"""
        if not self.placeholders:
            QMessageBox.warning(self, "No Placeholders", "Please scan template first")
            return

        # Import and use the detailed mapping dialog
        from helpers.template_completeness_dialog import PlaceholderMappingDialog

        dialog = PlaceholderMappingDialog(
            self, self.selected_template, self.template_path, self.mapper
        )

        if dialog.exec_():
            # Refresh everything
            self.scan_template()
            self.populate_mapping_table()
            self.update_template_info()

    def show_help(self):
        """Show help dialog"""
        help_text = """
        <h2>Template Management Center - Help</h2>

        <h3>Overview</h3>
        <p>This dialog provides a comprehensive interface for managing templates, including selection, scanning, and placeholder mapping.</p>

        <h3>Workflow</h3>
        <ol>
        <li><b>Select Module:</b> Choose the form module you want to work with</li>
        <li><b>Select Template:</b> Choose a compatible template from the list</li>
        <li><b>Scan Template:</b> Analyze the template for placeholders</li>
        <li><b>Configure Mapping:</b> Map placeholders to form fields</li>
        </ol>

        <h3>Tabs</h3>
        <ul>
        <li><b>Scanner:</b> Shows scan results and placeholder status</li>
        <li><b>Mapper:</b> Configure placeholder-to-field mappings</li>
        <li><b>Compatibility:</b> View how well the template works with different modules</li>
        </ul>

        <h3>Tips</h3>
        <ul>
        <li>Templates are configured once and remembered forever</li>
        <li>Use the compatibility report to choose the best template for your needs</li>
        <li>Custom values can be entered for placeholders that don't map to form fields</li>
        </ul>
        """

        QMessageBox.information(self, "Help - Template Management Center", help_text)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = TemplateManagementDialog(None, 'Form2')
    dialog.exec_()
    sys.exit(0)
