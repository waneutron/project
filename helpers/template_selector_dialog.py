"""
template_selector_dialog.py - PyQt5 Dialog for selecting templates based on module compatibility
Allows users to scan templates and choose compatible ones for their forms
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, 
                             QProgressBar, QTabWidget, QWidget)
from helpers.template_validator import TemplateValidator


class TemplateSelector(QDialog):
    """Dialog to select templates based on module requirements"""
    
    def __init__(self, parent=None, module_name=None):
        super().__init__(parent)
        self.setWindowTitle("Template Selector - By Module Compatibility")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1000, 600)
        
        self.validator = TemplateValidator()
        self.selected_template = None
        self.module_name = module_name or 'Form2'
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        
        # Top section - Module selector
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Select Module:"))
        
        self.module_combo = QComboBox()
        modules = list(self.validator.module_field_mappings.keys())
        self.module_combo.addItems(modules)
        
        # Set current module
        if self.module_name in modules:
            self.module_combo.setCurrentText(self.module_name)
        
        self.module_combo.currentTextChanged.connect(self.on_module_changed)
        top_layout.addWidget(self.module_combo)
        
        # Scan button
        btn_scan = QPushButton("🔍 Scan Templates")
        btn_scan.clicked.connect(self.scan_templates)
        top_layout.addWidget(btn_scan)
        
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Tab widget for compatible and incompatible templates
        self.tabs = QTabWidget()
        
        # Compatible templates tab
        self.table_compatible = QTableWidget()
        self.table_compatible.setColumnCount(5)
        self.table_compatible.setHorizontalHeaderLabels([
            'Template Name', 'Match Score %', 'Required Fields', 'Status', 'Recommendation'
        ])
        self.table_compatible.setColumnWidth(0, 250)
        self.table_compatible.setColumnWidth(1, 120)
        self.table_compatible.setColumnWidth(2, 130)
        self.table_compatible.setColumnWidth(3, 100)
        self.table_compatible.setColumnWidth(4, 300)
        self.table_compatible.itemDoubleClicked.connect(self.on_select_compatible)
        
        self.tabs.addTab(self.table_compatible, "✓ Compatible Templates")
        
        # Incompatible templates tab
        self.table_incompatible = QTableWidget()
        self.table_incompatible.setColumnCount(4)
        self.table_incompatible.setHorizontalHeaderLabels([
            'Template Name', 'Match Score %', 'Required Fields', 'Issue'
        ])
        self.table_incompatible.setColumnWidth(0, 250)
        self.table_incompatible.setColumnWidth(1, 120)
        self.table_incompatible.setColumnWidth(2, 130)
        self.table_incompatible.setColumnWidth(3, 400)
        
        self.tabs.addTab(self.table_incompatible, "✗ Incompatible Templates")
        
        # All templates report tab
        self.table_all_compatibility = QTableWidget()
        self.table_all_compatibility.setColumnCount(6)
        self.table_all_compatibility.setHorizontalHeaderLabels([
            'Template', 'Form2 Score', 'Form3 Score', 'DeleteItem Score', 'SignUp Score', 'Best For'
        ])
        self.table_all_compatibility.setColumnWidth(0, 200)
        for i in range(1, 5):
            self.table_all_compatibility.setColumnWidth(i, 110)
        self.table_all_compatibility.setColumnWidth(5, 150)
        
        self.tabs.addTab(self.table_all_compatibility, "📊 All Templates Report")
        
        main_layout.addWidget(self.tabs)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        btn_details = QPushButton("📋 View Details")
        btn_details.clicked.connect(self.show_template_details)
        button_layout.addWidget(btn_details)
        
        button_layout.addStretch()
        
        btn_select = QPushButton("✓ Select Template")
        btn_select.clicked.connect(self.select_template)
        button_layout.addWidget(btn_select)
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancel)
        
        main_layout.addLayout(button_layout)
    
    def on_module_changed(self, module_name):
        """Handle module selection change"""
        self.module_name = module_name
    
    def scan_templates(self):
        """Scan templates and populate tables"""
        self.progress.setVisible(True)
        self.progress.setValue(25)
        
        try:
            # Get compatible templates
            result = self.validator.select_templates_for_module(
                self.module_name, 
                template_dir='Templates', 
                min_score=50
            )
            
            self.progress.setValue(50)
            
            # Clear tables
            self.table_compatible.setRowCount(0)
            self.table_incompatible.setRowCount(0)
            
            # Populate compatible templates
            for i, template in enumerate(result['compatible_templates']):
                self.table_compatible.insertRow(i)
                
                self.table_compatible.setItem(i, 0, QTableWidgetItem(template['template_name']))
                
                score_item = QTableWidgetItem(f"{template['match_score']:.1f}%")
                score_item.setForeground(self.get_score_color(template['match_score']))
                self.table_compatible.setItem(i, 1, score_item)
                
                required_item = QTableWidgetItem(
                    f"{template['required_found']}/{template['required_total']}"
                )
                self.table_compatible.setItem(i, 2, required_item)
                
                status = "✓ Perfect" if template['match_score'] == 100 else "✓ Compatible"
                self.table_compatible.setItem(i, 3, QTableWidgetItem(status))
                
                self.table_compatible.setItem(i, 4, QTableWidgetItem(template['recommendation']))
            
            self.progress.setValue(75)
            
            # Populate incompatible templates
            for i, template in enumerate(result['incompatible_templates']):
                self.table_incompatible.insertRow(i)
                
                self.table_incompatible.setItem(i, 0, QTableWidgetItem(template['template_name']))
                
                score = template.get('match_score', 0)
                score_item = QTableWidgetItem(f"{score:.1f}%")
                score_item.setForeground(self.get_score_color(score))
                self.table_incompatible.setItem(i, 1, score_item)
                
                required_found = template.get('required_found', 0)
                required_total = template.get('required_total', 0)
                required_item = QTableWidgetItem(f"{required_found}/{required_total}")
                self.table_incompatible.setItem(i, 2, required_item)
                
                issue = template.get('recommendation', 'Unknown issue')
                self.table_incompatible.setItem(i, 3, QTableWidgetItem(issue))
            
            # Populate all templates report
            self.populate_all_compatibility_report()
            
            self.progress.setValue(100)
            self.progress.setVisible(False)
            
            # Show message
            compatible_count = len(result['compatible_templates'])
            total_count = compatible_count + len(result['incompatible_templates'])
            
            QMessageBox.information(
                self, 
                "Scan Complete", 
                f"Found {total_count} templates\n"
                f"{compatible_count} compatible with {self.module_name}\n"
                f"{total_count - compatible_count} need adjustment"
            )
            
        except Exception as e:
            self.progress.setVisible(False)
            QMessageBox.critical(self, "Error", f"Failed to scan templates:\n{str(e)}")
    
    def populate_all_compatibility_report(self):
        """Populate table showing all templates' compatibility with all modules"""
        templates = self.validator.scan_all_templates('Templates')
        
        self.table_all_compatibility.setRowCount(0)
        
        for template_name in templates.keys():
            row = self.table_all_compatibility.rowCount()
            self.table_all_compatibility.insertRow(row)
            
            self.table_all_compatibility.setItem(row, 0, QTableWidgetItem(template_name))
            
            # Get scores for each module
            best_score = 0
            best_module = ""
            
            col = 1
            for module_name in ['Form2', 'Form3', 'FormDeleteItem', 'FormSignUp']:
                match_result = self.validator.match_template_to_module(template_name, module_name)
                score = match_result['match_score']
                
                if score > best_score:
                    best_score = score
                    best_module = module_name
                
                score_item = QTableWidgetItem(f"{score:.1f}%")
                score_item.setForeground(self.get_score_color(score))
                self.table_all_compatibility.setItem(row, col, score_item)
                col += 1
            
            # Best for column
            best_text = f"{best_module} ({best_score:.1f}%)" if best_module else "N/A"
            self.table_all_compatibility.setItem(row, 5, QTableWidgetItem(best_text))
    
    def get_score_color(self, score):
        """Get color based on match score"""
        from PyQt5.QtGui import QColor
        if score >= 90:
            return QColor(34, 139, 34)  # Dark green
        elif score >= 70:
            return QColor(255, 165, 0)  # Orange
        else:
            return QColor(205, 92, 92)  # Indian red
    
    def show_template_details(self):
        """Show detailed report of selected template"""
        # Get selected template from compatible table
        selected_rows = self.table_compatible.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a template first")
            return
        
        row = selected_rows[0].row()
        template_name = self.table_compatible.item(row, 0).text()
        
        # Get detailed report
        report = self.validator.get_template_field_report(template_name, 'Templates')
        
        # Create message
        message = f"Template: {report['template']}\n\n"
        message += f"Placeholders ({len(report['placeholders'])}):\n"
        for ph in report['placeholders']:
            message += f"  • {ph}\n"
        
        message += f"\nModule Compatibility:\n"
        for module, compat in report['modules_compatibility'].items():
            status = "✓" if compat['compatible'] else "✗"
            message += f"  {status} {module}: {compat['score']:.1f}% ({compat['required_found']} required)\n"
        
        QMessageBox.information(self, "Template Details", message)
    
    def on_select_compatible(self, item):
        """Handle double-click on compatible template"""
        row = item.row()
        template_name = self.table_compatible.item(row, 0).text()
        self.selected_template = template_name
        self.accept()
    
    def select_template(self):
        """Select template from compatible list"""
        selected_rows = self.table_compatible.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a compatible template")
            return
        
        row = selected_rows[0].row()
        template_name = self.table_compatible.item(row, 0).text()
        self.selected_template = template_name
        self.accept()
    
    def get_selected_template(self):
        """Return selected template name"""
        return self.selected_template


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    dialog = TemplateSelector(module_name='Form2')
    if dialog.exec_() == QDialog.Accepted:
        print(f"Selected template: {dialog.get_selected_template()}")
    sys.exit(0)
