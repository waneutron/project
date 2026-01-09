"""
template_field_mapper.py - Template-Field Mapping System
Maps custom fields dengan template placeholders untuk Form2
"""
import json
import os
from helpers.template_field_validator import TemplateFieldMapper as PlaceholderScanner

class TemplateFieldMapper:
    """Manage mapping antara extra fields dengan template placeholders"""
    
    def __init__(self):
        self.mapping_dir = "template_field_mappings"
        os.makedirs(self.mapping_dir, exist_ok=True)
        self.scanner = PlaceholderScanner()  # Use the scanner from validator
    
    def get_mapping_path(self, form_name, template_name):
        """Get mapping file path"""
        safe_template = template_name.replace('.docx', '').replace('.doc', '')
        return os.path.join(self.mapping_dir, f"{form_name}_{safe_template}_mapping.json")
    
    def scan_template_placeholders(self, template_file):
        """Scan template untuk detect semua placeholders"""
        return self.scanner.scan_template_placeholders(template_file)
    
    def create_mapping(self, form_name, template_name, custom_fields):
        """Create mapping antara custom fields dengan template"""
        # Scan template untuk placeholders
        placeholders = self.scan_template_placeholders(template_name)
        
        # Auto-map fields dengan placeholders (by name matching)
        mapping = {
            'form_name': form_name,
            'template_name': template_name,
            'placeholders_found': placeholders,
            'field_mappings': {},
            'unmapped_placeholders': [],
            'unmapped_fields': []
        }
        
        # Try to auto-match
        for field in custom_fields:
            field_id = field.get('field_id', '')
            field_label = field.get('label', '')
            
            # Try to find matching placeholder
            matched = False
            for placeholder in placeholders:
                # Case-insensitive matching
                if (field_id.upper() in placeholder.upper() or 
                    field_label.upper() in placeholder.upper() or
                    placeholder.upper() in field_id.upper()):
                    mapping['field_mappings'][field_id] = {
                        'placeholder': f"<<{placeholder}>>",
                        'field_label': field_label,
                        'field_type': field.get('type', 'text'),
                        'auto_matched': True
                    }
                    matched = True
                    break
            
            if not matched:
                mapping['unmapped_fields'].append(field)
        
        # Find unmapped placeholders
        mapped_placeholders = {m['placeholder'] for m in mapping['field_mappings'].values()}
        for placeholder in placeholders:
            if f"<<{placeholder}>>" not in mapped_placeholders:
                mapping['unmapped_placeholders'].append(f"<<{placeholder}>>")
        
        return mapping
    
    def save_mapping(self, form_name, template_name, mapping):
        """Save mapping to JSON"""
        mapping_path = self.get_mapping_path(form_name, template_name)
        try:
            mapping['form_name'] = form_name
            mapping['template_name'] = template_name
            with open(mapping_path, 'w', encoding='utf-8') as f:
                json.dump(mapping, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving mapping: {e}")
            return False
    
    def load_mapping(self, form_name, template_name):
        """Load mapping from JSON"""
        mapping_path = self.get_mapping_path(form_name, template_name)
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading mapping: {e}")
        return None
    
    def get_all_templates_for_form(self, form_name):
        """Get semua templates yang ada mapping untuk form ini"""
        templates = []
        if not os.path.exists(self.mapping_dir):
            return templates
        
        for filename in os.listdir(self.mapping_dir):
            if filename.startswith(f"{form_name}_") and filename.endswith("_mapping.json"):
                # Extract template name
                template_part = filename.replace(f"{form_name}_", "").replace("_mapping.json", "")
                templates.append(template_part)
        
        return templates

