"""
dynamic_form_generator.py - Generate forms dynamically from configuration
"""
import tkinter as tk
from tkinter import ttk

class DynamicFormGenerator:
    """Generate forms from configuration"""
    
    def generate_form(self, parent, config):
        """Generate form UI from configuration"""
        # Create form fields based on config
        for field_config in config.get('fields', []):
            self.create_field(parent, field_config)
        
        # Create checkboxes
        for checkbox_config in config.get('checkboxes', []):
            self.create_checkbox(parent, checkbox_config)
    
    def create_field(self, parent, field_config):
        """Create a field widget"""
        field_type = field_config.get('type', 'Entry')
        field_id = field_config.get('field_id', '')
        label = field_config.get('label', '')
        width = field_config.get('width', 30)
        
        # Create label
        label_widget = tk.Label(parent, text=label, font=('Arial', 10), bg='white')
        label_widget.pack(anchor='w', padx=10, pady=5)
        
        # Create field based on type
        if field_type == 'Entry':
            widget = tk.Entry(parent, width=width, font=('Arial', 10))
            if field_config.get('default_value'):
                widget.insert(0, field_config['default_value'])
        elif field_type == 'Text':
            widget = tk.Text(parent, width=width, height=4, font=('Arial', 10))
            if field_config.get('default_value'):
                widget.insert('1.0', field_config['default_value'])
        elif field_type == 'Combobox':
            widget = ttk.Combobox(parent, width=width, font=('Arial', 10))
            if field_config.get('options'):
                widget['values'] = field_config['options']
        
        widget.pack(fill=tk.X, padx=10, pady=5)
        
        return widget
    
    def create_checkbox(self, parent, checkbox_config):
        """Create a checkbox widget"""
        label = checkbox_config.get('label', '')
        default_checked = checkbox_config.get('default_checked', False)
        
        var = tk.BooleanVar(value=default_checked)
        checkbox = tk.Checkbutton(parent,
                                 text=label,
                                 variable=var,
                                 font=('Arial', 10),
                                 bg='white')
        checkbox.pack(anchor='w', padx=10, pady=5)
        
        return checkbox, var

