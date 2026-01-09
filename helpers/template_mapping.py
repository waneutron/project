"""
template_mapping.py - Template Name Mapping
Maps template categories from template_categories_table.md to actual template file names
"""
# Template mapping based on template_categories_table.md
TEMPLATE_MAPPING = {
    # APPROVAL templates
    'ames_pedagang': {
        'category': 'APPROVAL',
        'file': 'ames_pedagang.docx',
        'description': 'AMES Trader Approval',
        'form': 'Form3_Government'
    },
    'ames_pengilang': {
        'category': 'APPROVAL',
        'file': 'ames_pengilang.docx',
        'description': 'AMES Manufacturer Approval',
        'form': 'Form3_Government'
    },
    'butiran_5d_lulus': {
        'category': 'APPROVAL',
        'file': 'surat kelulusan butiran 5D (Lulus).docx',
        'description': 'Item 5D Approval',
        'form': 'Form1_Government'
    },
    'pelupusan_jual_skrap': {
        'category': 'APPROVAL',
        'file': 'pelupusan_penjualan.docx',  # Maps to penjualan or skrap
        'description': 'Disposal Approval (Sale/Scrap)',
        'form': 'Form1_Government'
    },
    
    # REJECTION templates
    'pelupusan_tidak_lulus': {
        'category': 'REJECTION',
        'file': 'pelupusan_tidak_lulus.docx',
        'description': 'Disposal Rejection',
        'form': 'Form1_Government'
    },
    'butiran_5d_tidak_lulus': {
        'category': 'REJECTION',
        'file': 'surat kelulusan butiran 5D (tidak lulus).docx',
        'description': 'Item 5D Rejection',
        'form': 'Form1_Government'
    },
    
    # DISPOSAL templates
    'pelupusan_pemusnahan': {
        'category': 'DISPOSAL',
        'file': 'pelupusan_pemusnahan.docx',
        'description': 'Disposal by Destruction',
        'form': 'Form1_Government'
    },
    'pelupusan_penjualan': {
        'category': 'DISPOSAL',
        'file': 'pelupusan_penjualan.docx',
        'description': 'Disposal by Sale',
        'form': 'Form1_Government'
    },
    'pelupusan_skrap': {
        'category': 'DISPOSAL',
        'file': 'pelupusan_skrap.docx',
        'description': 'Disposal by Scrap',
        'form': 'Form1_Government'
    },
    
    # REGISTRATION templates
    'sign_up_b': {
        'category': 'REGISTRATION',
        'file': 'signUpB.docx',
        'description': 'Sign Up Schedule B',
        'form': 'Form1_Government'
    },
    
    # Delete Item templates
    'delete_item_ames': {
        'category': 'Delete Item',
        'file': 'delete_item_ames.docx',
        'description': 'Delete Item AMES',
        'form': 'Form_DeleteItem'
    },
    'delete_item': {
        'category': 'Delete Item',
        'file': 'delete_item.doc',
        'description': 'Delete Item (Old Format)',
        'form': 'Form_DeleteItem'
    },
    
    # Other templates
    'batal_sijil': {
        'category': 'Lain-lain',
        'file': 'batal_sijil.doc',
        'description': 'Certificate Cancellation',
        'form': 'Form1_Government'
    }
}

# Category to template mapping for Form1
FORM1_CATEGORY_MAPPING = {
    'Pelupusan': {
        'pemusnahan': 'pelupusan_pemusnahan.docx',
        'penjualan': 'pelupusan_penjualan.docx',
        'skrap': 'pelupusan_skrap.docx',
        'tidak_lulus': 'pelupusan_tidak_lulus.docx'
    },
    'Lain-lain': {
        'signUpB': 'signUpB.docx',
        'batal_sijil': 'batal_sijil.doc',
        'delete_item(makluman),': 'delete_item.doc'
    }
}

# Get template file by category and sub-option
def get_template_file(category, sub_option):
    """Get template file name based on category and sub-option"""
    if category in FORM1_CATEGORY_MAPPING:
        if sub_option in FORM1_CATEGORY_MAPPING[category]:
            return FORM1_CATEGORY_MAPPING[category][sub_option]
    return None

# Get template category from file name
def get_template_category(template_file):
    """Get template category from file name"""
    for key, value in TEMPLATE_MAPPING.items():
        if value['file'] == template_file:
            return value['category']
    return 'Lain-lain'

# Get all templates by category
def get_templates_by_category(category):
    """Get all templates in a specific category"""
    templates = []
    for key, value in TEMPLATE_MAPPING.items():
        if value['category'] == category:
            templates.append({
                'id': key,
                'file': value['file'],
                'description': value['description'],
                'form': value['form']
            })
    return templates

