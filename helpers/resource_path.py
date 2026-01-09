"""
resource_path.py - Resource Path Helper for PyInstaller
Handles resource paths for both development and bundled applications
"""
import os
import sys


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller.
    
    When running as a PyInstaller bundle, resources are in sys._MEIPASS.
    When running as a script, resources are in the current directory.
    
    Args:
        relative_path: Path relative to the resource directory (e.g., 'Templates/pelupusan.docx' or 'logo.png')
    
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running as a script, use current directory
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    return os.path.join(base_path, relative_path)


def get_template_path(template_filename):
    """
    Get full path to a template file.
    
    Args:
        template_filename: Name of template file (e.g., 'pelupusan_pemusnahan.docx')
    
    Returns:
        Full path to the template file
    """
    return resource_path(os.path.join("Templates", template_filename))


def get_logo_path():
    """
    Get full path to logo.png.
    
    Returns:
        Full path to logo.png
    """
    return resource_path("logo.png")


def get_templates_dir():
    """
    Get full path to Templates directory.
    
    Returns:
        Full path to Templates directory
    """
    return resource_path("Templates")

