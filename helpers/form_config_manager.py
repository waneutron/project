"""
form_config_manager.py - Dynamic Form Configuration System
Allows non-technical users to edit forms, fields, mappings, and checkboxes
"""
import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class FormConfigManager:
    """Manage form configurations dynamically"""
    
    def __init__(self):
        self.config_dir = "form_configs"
        os.makedirs(self.config_dir, exist_ok=True)
    
    def get_config_path(self, form_name):
        """Get config file path for form"""
        return os.path.join(self.config_dir, f"{form_name}_config.json")
    
    def load_form_config(self, form_name):
        """Load form configuration"""
        config_path = self.get_config_path(form_name)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # If config exists but has no fields, merge with predefined fields
                    if not config.get('fields') and not config.get('checkboxes'):
                        print(f"Config file exists but is empty, merging with predefined fields for {form_name}")
                        predefined = self.get_predefined_fields(form_name)
                        if predefined:
                            config['fields'] = predefined.get('fields', [])
                            config['checkboxes'] = predefined.get('checkboxes', [])
                            config['sections'] = predefined.get('sections', [])
                            if not config.get('placeholder_mappings'):
                                config['placeholder_mappings'] = predefined.get('placeholder_mappings', {})
                    print(f"Loaded config for {form_name}: {len(config.get('fields', []))} fields, {len(config.get('checkboxes', []))} checkboxes")
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.get_default_config(form_name)
        else:
            print(f"No config file found for {form_name}, using default with predefined fields")
        return self.get_default_config(form_name)
    
    def save_form_config(self, form_name, config):
        """Save form configuration"""
        config_path = self.get_config_path(form_name)
        try:
            config['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
            return False
    
    def get_default_config(self, form_name):
        """Get default configuration structure with predefined fields for known forms"""
        config = {
            "form_name": form_name,
            "version": "1.0",
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sections": [],
            "fields": [],
            "checkboxes": [],
            "placeholder_mappings": {},
            "field_validations": {},
            "conditional_fields": {}
        }
        
        # Add predefined fields for known forms
        predefined_fields = self.get_predefined_fields(form_name)
        if predefined_fields:
            config['fields'] = predefined_fields.get('fields', [])
            config['checkboxes'] = predefined_fields.get('checkboxes', [])
            config['sections'] = predefined_fields.get('sections', [])
            config['placeholder_mappings'] = predefined_fields.get('placeholder_mappings', {})
        
        return config
    
    def get_predefined_fields(self, form_name):
        """Get predefined fields for known forms"""
        predefined = {
            'Form2': {
                'fields': [
                    {'field_id': 'entry_nama', 'label': 'Nama Syarikat', 'type': 'Entry', 'width': 38, 'placeholder': ''},
                    {'field_id': 'entry_alamat1', 'label': 'Alamat Baris 1', 'type': 'Entry', 'width': 40, 'placeholder': ''},
                    {'field_id': 'entry_alamat2', 'label': 'Alamat Baris 2', 'type': 'Entry', 'width': 40, 'placeholder': ''},
                    {'field_id': 'entry_tarikh', 'label': 'Tarikh', 'type': 'Date', 'width': 38, 'placeholder': ''},
                    {'field_id': 'entry_rujukan', 'label': 'No. Rujukan', 'type': 'Entry', 'width': 25, 'placeholder': ''},
                    {'field_id': 'combo_process', 'label': 'Jenis Proses', 'type': 'Combobox', 'width': 35, 'placeholder': '', 'options': []},
                ],
                'checkboxes': [],
                'sections': [],
                'placeholder_mappings': {}
            },
            'Form3': {
                'fields': [
                    {'field_id': 'entry_nama', 'label': 'Nama', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                    {'field_id': 'entry_no_rujukan', 'label': 'No. Rujukan', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                    {'field_id': 'entry_tarikh', 'label': 'Tarikh', 'type': 'Date', 'width': 30, 'placeholder': ''},
                ],
                'checkboxes': [],
                'sections': [],
                'placeholder_mappings': {}
            },
            'FormSignUp': {
                'fields': [
                    {'field_id': 'entry_nama', 'label': 'Nama', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                    {'field_id': 'entry_ic', 'label': 'No. IC', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                    {'field_id': 'entry_alamat', 'label': 'Alamat', 'type': 'Text', 'width': 30, 'placeholder': ''},
                ],
                'checkboxes': [],
                'sections': [],
                'placeholder_mappings': {}
            },
            'FormDeleteItem': {
                'fields': [
                    {'field_id': 'entry_kategori', 'label': 'Kategori', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                    {'field_id': 'entry_no_rujukan', 'label': 'No. Rujukan', 'type': 'Entry', 'width': 30, 'placeholder': ''},
                ],
                'checkboxes': [],
                'sections': [],
                'placeholder_mappings': {}
            }
        }
        
        return predefined.get(form_name, None)
    
    def get_all_forms(self):
        """Get list of all configured forms"""
        forms = []
        if os.path.exists(self.config_dir):
            for filename in os.listdir(self.config_dir):
                if filename.endswith("_config.json"):
                    form_name = filename.replace("_config.json", "")
                    forms.append(form_name)
        return forms

