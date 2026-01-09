"""
template_storage.py - Shared Template Storage System
Provides access to embedded templates for all forms
"""
import os
import base64
import io
from docx import Document
from helpers.resource_path import get_template_path, get_templates_dir

# Import the EmbeddedTemplateStorage from TemplateEditor
try:
    from modules.TemplateEditor import EmbeddedTemplateStorage
except ImportError:
    # Fallback if TemplateEditor not available
    class EmbeddedTemplateStorage:
        def __init__(self):
            self.templates = {}
        
        def get_template(self, filename):
            return None
        
        def has_template(self, filename):
            return False


# Global template storage instance
_template_storage = None


def get_template_storage():
    """Get global template storage instance"""
    global _template_storage
    if _template_storage is None:
        _template_storage = EmbeddedTemplateStorage()
    return _template_storage


def get_template_document(template_filename):
    """
    Get template as Document object from embedded storage
    Falls back to file system if not found in embedded storage
    
    Args:
        template_filename: Name of template file (e.g., 'pelupusan_pemusnahan.docx')
    
    Returns:
        Document object or None if not found
    """
    storage = get_template_storage()
    
    # Try embedded storage first (only if it has actual content)
    if storage.has_template(template_filename):
        doc = storage.get_template(template_filename)
        if doc is not None:
            return doc
    
    # Fallback to file system (for backward compatibility)
    # This handles cases where:
    # 1. Template not in embedded storage
    # 2. Template in embedded storage but content is None (not imported yet)
    template_path = get_template_path(template_filename)
    if os.path.exists(template_path):
        # Check if file is .doc (old format) - python-docx doesn't support it
        if template_filename.lower().endswith('.doc') and not template_filename.lower().endswith('.docx'):
            print(f"Warning: Template {template_filename} is in old .doc format. python-docx only supports .docx files.")
            print(f"Please convert {template_filename} to .docx format.")
            return None
        
        try:
            doc = Document(template_path)
            # Auto-import to embedded storage for future use
            try:
                storage.add_template_from_file(template_path, template_filename, is_new=False)
            except:
                pass  # Don't fail if auto-import fails
            return doc
        except Exception as e:
            # Check if it's a .doc file causing the error
            if template_filename.lower().endswith('.doc') and not template_filename.lower().endswith('.docx'):
                print(f"Error loading template {template_filename}: Old .doc format not supported. Please convert to .docx")
            else:
                print(f"Error loading template {template_filename} from file system: {e}")
            return None
    
    # Template not found in embedded storage and not in file system
    return None


def template_exists(template_filename):
    """Check if template exists in embedded storage or file system"""
    storage = get_template_storage()
    
    if storage.has_template(template_filename):
        return True
    
    # Fallback to file system
    template_path = get_template_path(template_filename)
    return os.path.exists(template_path)

