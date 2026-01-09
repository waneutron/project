"""
PDF Export Utilities
Multiple methods for converting Word documents to PDF
"""
import os
import platform
import subprocess
from tkinter import messagebox


def docx_to_pdf(docx_path, pdf_path):
    """
    Convert DOCX to PDF using available method
    Returns True if successful, False otherwise
    """
    
    # Method 1: Try docx2pdf (Windows only)
    if platform.system() == 'Windows':
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            return True
        except ImportError:
            pass
        except Exception as e:
            print(f"docx2pdf failed: {e}")
    
    # Method 2: Try LibreOffice (cross-platform)
    if try_libreoffice_convert(docx_path, pdf_path):
        return True
    
    # Method 3: Try Microsoft Word COM (Windows only)
    if platform.system() == 'Windows':
        if try_word_com_convert(docx_path, pdf_path):
            return True
    
    # All methods failed
    messagebox.showinfo(
        "PDF Conversion", 
        "Could not convert to PDF automatically.\n\n"
        "The document has been saved as .docx\n"
        "You can convert it manually using:\n"
        "- Microsoft Word (Save As > PDF)\n"
        "- LibreOffice (Export as PDF)\n"
        "- Online converters"
    )
    return False


def try_libreoffice_convert(docx_path, pdf_path):
    """Try converting using LibreOffice command line"""
    try:
        # Common LibreOffice executable paths
        libreoffice_paths = [
            'libreoffice',  # Linux/Mac with PATH
            'soffice',      # Alternative name
            r'C:\Program Files\LibreOffice\program\soffice.exe',  # Windows
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',  # Mac
        ]
        
        libreoffice_cmd = None
        for path in libreoffice_paths:
            if os.path.exists(path) or which_command(path):
                libreoffice_cmd = path
                break
        
        if not libreoffice_cmd:
            return False
        
        # Get output directory
        output_dir = os.path.dirname(pdf_path)
        
        # Convert command
        cmd = [
            libreoffice_cmd,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            docx_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        
        # LibreOffice saves with same name but .pdf extension
        expected_pdf = os.path.join(output_dir, 
                                    os.path.splitext(os.path.basename(docx_path))[0] + '.pdf')
        
        if os.path.exists(expected_pdf):
            # Rename to desired name if different
            if expected_pdf != pdf_path:
                os.rename(expected_pdf, pdf_path)
            return True
        
        return False
        
    except Exception as e:
        print(f"LibreOffice conversion failed: {e}")
        return False


def try_word_com_convert(docx_path, pdf_path):
    """Try converting using Microsoft Word COM (Windows only)"""
    try:
        import win32com.client
        
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        
        # Open document
        doc = word.Documents.Open(os.path.abspath(docx_path))
        
        # Export as PDF (wdFormatPDF = 17)
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        
        # Close
        doc.Close()
        word.Quit()
        
        return True
        
    except Exception as e:
        print(f"Word COM conversion failed: {e}")
        return False


def which_command(program):
    """Check if command exists in PATH (cross-platform)"""
    try:
        result = subprocess.run(['which', program], 
                              capture_output=True, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False


def install_docx2pdf():
    """Guide user to install docx2pdf"""
    msg = """
To enable PDF export, install docx2pdf:

Windows:
    pip install docx2pdf

This requires Microsoft Word to be installed.

Alternative: Install LibreOffice (free)
    Download from: https://www.libreoffice.org/
"""
    messagebox.showinfo("PDF Export Setup", msg)


# Optional: Async conversion for better UI responsiveness
def docx_to_pdf_async(docx_path, pdf_path, callback=None):
    """
    Convert DOCX to PDF in background thread
    callback: function to call when done, receives (success: bool, error: str)
    """
    import threading
    
    def convert_thread():
        try:
            success = docx_to_pdf(docx_path, pdf_path)
            if callback:
                callback(success, None)
        except Exception as e:
            if callback:
                callback(False, str(e))
    
    thread = threading.Thread(target=convert_thread)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    # Test conversion
    import sys
    if len(sys.argv) > 1:
        docx_file = sys.argv[1]
        pdf_file = docx_file.replace('.docx', '.pdf')
        
        print(f"Converting {docx_file} to {pdf_file}...")
        success = docx_to_pdf(docx_file, pdf_file)
        
        if success:
            print("✓ Conversion successful!")
        else:
            print("✗ Conversion failed")
    else:
        print("Usage: python pdf_utils.py <docx_file>")
