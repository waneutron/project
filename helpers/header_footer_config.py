"""
header_footer_config.py - Configurable Header/Footer System
Allows non-coding users to edit document headers and footers via JSON config
"""
import json
import os
from datetime import datetime


class HeaderFooterConfig:
    """Manage header and footer configuration"""
    
    def __init__(self):
        self.config_file = "header_footer_config.json"
        self.default_config = {
            "header": {
                "enabled": True,
                "force_replace": False,  # Set to True to replace existing template headers
                "logo_placeholder": "",  # Leave empty to hide, or put text/placeholder
                "department_name": "JABATAN KASTAM DIRAJA MALAYSIA JOHOR",
                "address_lines": [
                    "Bahagian Cukai Dalam Negeri (CDN),",
                    "Unit Kawalan Kemudahan,",
                    "Tingkat 9, Menara Kastam Johor,",
                    "Karung Berkunci 780,",
                    "80990 Johor Bahru,",
                    "Johor Darul Ta'zim."
                ],
                "contact": {
                    "phone_label": "Telefon :",
                    "phone_value": "07 2076000 samb. 1916",
                    "email_label": "Laman Web :",
                    "email_value": "ukk.jb@customs.gov.my"
                },
                "show_border": True
            },
            "footer": {
                "enabled": True,
                "force_replace": False,  # Set to True to replace existing template footers
                "show_border": True,
                "yellow_bar": True,
                "blue_bar": True,
                "motto_text": "CEKAP • TANGKAS • INTEGRITI",
                "motto_font_size": 10,
                "motto_bold": True
            },
            "last_modified": None
        }
    
    def load_config(self):
        """Load configuration from file, create default if not exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default to ensure all keys exist
                    merged = self.default_config.copy()
                    merged.update(config)
                    # Deep merge for nested dicts
                    if 'header' in config:
                        merged['header'] = {**self.default_config['header'], **config['header']}
                        if 'contact' in config['header']:
                            merged['header']['contact'] = {**self.default_config['header']['contact'], **config['header']['contact']}
                    if 'footer' in config:
                        merged['footer'] = {**self.default_config['footer'], **config['footer']}
                    return merged
            except Exception as e:
                print(f"Error loading header/footer config: {e}")
                return self.default_config
        else:
            # Create default config file
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config):
        """Save configuration to file"""
        try:
            config['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving header/footer config: {e}")
            return False
    
    def get_header_config(self):
        """Get header configuration"""
        config = self.load_config()
        return config.get('header', {})
    
    def get_footer_config(self):
        """Get footer configuration"""
        config = self.load_config()
        return config.get('footer', {})

