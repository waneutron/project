"""
placeholder_registry.py - Centralized Placeholder Registry
Standardizes placeholder names across all forms and makes it easy to manage
"""
from datetime import datetime

class PlaceholderRegistry:
    """Central registry for all placeholder names and their standard values"""
    
    # Standard placeholder names (all forms should use these)
    STANDARD_PLACEHOLDERS = {
        # Basic Information
        'RUJUKAN': 'RUJUKAN',  # Standard rujukan (Form2 style)
        'RUJUKAN_KAMI': 'RUJUKAN_KAMI',  # Rujukan kami (AMES style)
        'RUJUKAN_TUAN': 'RUJUKAN_TUAN',  # Rujukan syarikat/tuan
        'NAMA_SYARIKAT': 'NAMA_SYARIKAT',  # Nama syarikat
        'ALAMAT': 'ALAMAT',  # Alamat (3 lines combined)
        'TARIKH': 'TARIKH',  # Tarikh (DD/MM/YYYY)
        'TARIKH2': 'TARIKH2',  # Tarikh format Melayu (DD Month YYYY)
        'TARIKH_MALAY': 'TARIKH_MALAY',  # Tarikh format Melayu (alternative name)
        'TARIKH_ISLAM': 'TARIKH_ISLAM',  # Tarikh Islam
        'NAMA_PEGAWAI': 'NAMA_PEGAWAI',  # Nama pegawai
        
        # AMES Specific
        'NO_KELULUSAN': 'NO_KELULUSAN',  # Nombor kelulusan
        'KATEGORI': 'KATEGORI',  # Kategori (Pedagang/Pengilang)
        'TEMPOH_KELULUSAN': 'TEMPOH_KELULUSAN',  # Tempoh kelulusan
        
        # Pelupusan Specific
        'PROSES': 'PROSES',  # Proses (pemusnahan/penjualan/skrap)
        'JENIS_BARANG': 'JENIS_BARANG',  # Jenis barang
        'PENGECUALIAN': 'PENGECUALIAN',  # Pengecualian
        'AMOUNT': 'AMOUNT',  # Amaun
        'JENIS_TEMPLATE': 'JENIS_TEMPLATE',  # Jenis template (SST-ADM/AMES-03)
        'STATUS': 'STATUS',  # Status
        'TARIKH_MULA': 'TARIKH_MULA',  # Tarikh mula pemusnahan
        'TARIKH_TAMAT': 'TARIKH_TAMAT',  # Tarikh tamat pemusnahan
        'TEMPOH': 'TEMPOH',  # Tempoh pemusnahan
        'TAJUK_SURAT': 'TAJUK_SURAT',  # Tajuk surat (uppercase)
        'TAJUK_SURAT2': 'TAJUK_SURAT2',  # Tajuk surat (lowercase)
        'RUJUKAN_INFO': 'RUJUKAN_INFO',  # Rujukan info
        
        # Sign Up Specific
        'BUSINESS_NAME': 'BUSINESS_NAME',  # Nama perniagaan (Sign Up)
        'BUSINESS_ADDRESS': 'BUSINESS_ADDRESS',  # Alamat perniagaan (Sign Up)
        'SCHEDULE_TYPE': 'SCHEDULE_TYPE',  # Jenis jadual
        'REGISTRATION_NUMBER': 'REGISTRATION_NUMBER',  # Nombor pendaftaran
        'SALUTATION': 'SALUTATION',  # Salutation
        'SENARAI_SEMAK': 'SENARAI_SEMAK',  # Senarai semak
        'CHECKLIST': 'CHECKLIST',  # Checklist
        
        # Table placeholders
        'LAMPIRAN_A_TABLE': 'LAMPIRAN_A_TABLE',  # Table for AMES
        'LAMPIRAN_A': 'LAMPIRAN_A',  # Alternative table name
        'TARIKH_KUATKUASA': 'TARIKH_KUATKUASA',  # Tarikh kuatkuasa
    }
    
    # Alias mapping (for backward compatibility)
    ALIASES = {
        'RUJUKAN': ['RUJUKAN_KAMI'],  # Form2 uses RUJUKAN, Form3 uses RUJUKAN_KAMI
        'TARIKH2': ['TARIKH_MALAY'],  # Form2 uses TARIKH2, Form3 uses TARIKH_MALAY
        'NAMA_SYARIKAT': ['BUSINESS_NAME'],  # Sign Up uses BUSINESS_NAME
        'ALAMAT': ['BUSINESS_ADDRESS'],  # Sign Up uses BUSINESS_ADDRESS
    }
    
    @classmethod
    def normalize_placeholder(cls, placeholder_name):
        """Normalize placeholder name to standard format"""
        # Remove << >> if present
        name = placeholder_name.replace('<<', '').replace('>>', '').strip()
        
        # Check if it's a standard placeholder
        if name in cls.STANDARD_PLACEHOLDERS:
            return f"<<{name}>>"
        
        # Check aliases
        for standard, aliases in cls.ALIASES.items():
            if name in aliases or name == standard:
                return f"<<{standard}>>"
        
        # Return as-is (custom placeholder)
        return f"<<{name}>>"
    
    @classmethod
    def get_standard_name(cls, placeholder_name):
        """Get standard placeholder name (without << >>)"""
        name = placeholder_name.replace('<<', '').replace('>>', '').strip()
        
        # Check if it's a standard placeholder
        if name in cls.STANDARD_PLACEHOLDERS:
            return name
        
        # Check aliases
        for standard, aliases in cls.ALIASES.items():
            if name in aliases or name == standard:
                return standard
        
        # Return as-is (custom placeholder)
        return name
    
    @classmethod
    def get_all_standard_placeholders(cls):
        """Get list of all standard placeholder names"""
        return list(cls.STANDARD_PLACEHOLDERS.keys())
    
    @classmethod
    def get_placeholder_description(cls, placeholder_name):
        """Get description for placeholder"""
        name = cls.get_standard_name(placeholder_name)
        
        descriptions = {
            'RUJUKAN': 'Rujukan standard (format: KE.JB(90)650/05-02/XXXX)',
            'RUJUKAN_KAMI': 'Rujukan kami (format: KE.JB(90)650/14/AMES/XXX)',
            'RUJUKAN_TUAN': 'Rujukan syarikat/tuan',
            'NAMA_SYARIKAT': 'Nama syarikat (uppercase)',
            'ALAMAT': 'Alamat syarikat (3 baris digabungkan)',
            'TARIKH': 'Tarikh (format: DD/MM/YYYY)',
            'TARIKH2': 'Tarikh format Melayu (DD Month YYYY)',
            'TARIKH_MALAY': 'Tarikh format Melayu (sama dengan TARIKH2)',
            'TARIKH_ISLAM': 'Tarikh dalam kalendar Islam',
            'NAMA_PEGAWAI': 'Nama pegawai (uppercase)',
            'NO_KELULUSAN': 'Nombor kelulusan AMES',
            'KATEGORI': 'Kategori (Pedagang/Pengilang)',
            'TEMPOH_KELULUSAN': 'Tempoh kelulusan (format: DD Month YYYY hingga DD Month YYYY)',
            'PROSES': 'Proses (pemusnahan/penjualan/skrap)',
            'JENIS_BARANG': 'Jenis barang',
            'PENGECUALIAN': 'Pengecualian',
            'AMOUNT': 'Amaun dalam Ringgit Malaysia (RM)',
            'JENIS_TEMPLATE': 'Jenis template (SST-ADM/AMES-03)',
            'STATUS': 'Status (SST-ADM/AMES-03)',
            'TARIKH_MULA': 'Tarikh mula pemusnahan',
            'TARIKH_TAMAT': 'Tarikh tamat pemusnahan',
            'TEMPOH': 'Tempoh pemusnahan (dalam perkataan Melayu)',
            'TAJUK_SURAT': 'Tajuk surat (uppercase dan bold)',
            'TAJUK_SURAT2': 'Tajuk surat (lowercase untuk badan surat)',
            'RUJUKAN_INFO': 'Maklumat rujukan tambahan',
            'BUSINESS_NAME': 'Nama perniagaan (Sign Up)',
            'BUSINESS_ADDRESS': 'Alamat perniagaan (Sign Up)',
            'SCHEDULE_TYPE': 'Jenis jadual',
            'REGISTRATION_NUMBER': 'Nombor pendaftaran',
            'SALUTATION': 'Salutation',
            'SENARAI_SEMAK': 'Senarai semak',
            'CHECKLIST': 'Checklist',
        }
        
        return descriptions.get(name, f'Custom placeholder: {name}')


class PlaceholderBuilder:
    """Helper class to build placeholder replacements easily"""
    
    def __init__(self, form_instance):
        self.form = form_instance
        self.replacements = {}
    
    def add_standard(self, placeholder_name, value):
        """Add standard placeholder with normalized name"""
        normalized = PlaceholderRegistry.normalize_placeholder(placeholder_name)
        self.replacements[normalized] = value
        return self
    
    def add_custom(self, placeholder_name, value):
        """Add custom placeholder (as-is)"""
        if not placeholder_name.startswith('<<'):
            placeholder_name = f"<<{placeholder_name}>>"
        self.replacements[placeholder_name] = value
        return self
    
    def add_rujukan(self, rujukan_value, prefix="KE.JB(90)650/05-02/"):
        """Add rujukan with prefix"""
        full_rujukan = f"{prefix}{rujukan_value}" if rujukan_value else ""
        self.add_standard('RUJUKAN', full_rujukan)
        return self
    
    def add_rujukan_ames(self, rujukan_value):
        """Add AMES rujukan"""
        full_rujukan = f"KE.JB(90)650/14/AMES/{rujukan_value}" if rujukan_value else ""
        self.add_standard('RUJUKAN_KAMI', full_rujukan)
        return self
    
    def add_nama_syarikat(self, nama_value):
        """Add nama syarikat (uppercase)"""
        self.add_standard('NAMA_SYARIKAT', nama_value.upper() if nama_value else "")
        return self
    
    def add_alamat(self, alamat_lines):
        """Add alamat from list of lines"""
        if isinstance(alamat_lines, list):
            alamat_combined = "\n".join([line.strip() for line in alamat_lines if line.strip()])
        else:
            alamat_combined = str(alamat_lines) if alamat_lines else ""
        self.add_standard('ALAMAT', alamat_combined)
        return self
    
    def add_tarikh(self, tarikh_value):
        """Add tarikh (DD/MM/YYYY)"""
        self.add_standard('TARIKH', tarikh_value)
        return self
    
    def add_tarikh_malay(self, tarikh_malay_value):
        """Add tarikh format Melayu"""
        self.add_standard('TARIKH2', tarikh_malay_value)
        self.add_standard('TARIKH_MALAY', tarikh_malay_value)  # Alias
        return self
    
    def add_tarikh_islam(self, tarikh_islam_value):
        """Add tarikh Islam"""
        self.add_standard('TARIKH_ISLAM', tarikh_islam_value)
        return self
    
    def add_nama_pegawai(self, nama_pegawai_value):
        """Add nama pegawai (uppercase)"""
        self.add_standard('NAMA_PEGAWAI', nama_pegawai_value.upper() if nama_pegawai_value else "")
        return self
    
    def add_extra_placeholders(self, extra_placeholders_dict):
        """Add extra placeholders from dict"""
        for key, value in extra_placeholders_dict.items():
            self.add_custom(key, value)
        return self
    
    def build(self):
        """Build and return replacements dict"""
        return self.replacements.copy()
    
    def get(self):
        """Alias for build()"""
        return self.build()

