"""
ui_components.py - User-Friendly UI Components
Reusable components for better user experience
"""
import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
import os
from datetime import datetime


class Tooltip:
    """Create tooltip for any widget"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        
        # Bind events
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show tooltip"""
        if self.tooltip:
            return
        
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip,
                        text=self.text,
                        font=('Arial', 9),
                        bg='#FFFACD',
                        fg='#000000',
                        relief=tk.SOLID,
                        borderwidth=1,
                        padx=10,
                        pady=6,
                        justify=tk.LEFT)
        label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class FieldValidator:
    """Real-time field validation with visual feedback"""
    
    @staticmethod
    def validate_not_empty(entry_widget, status_label, field_name="Medan"):
        """Validate field is not empty"""
        value = entry_widget.get().strip() if hasattr(entry_widget, 'get') else entry_widget.get('1.0', tk.END).strip()
        
        if len(value) == 0:
            status_label.config(text="", fg='gray')
            return False
        elif len(value) < 3:
            status_label.config(text="⚠️ Terlalu pendek", fg='#F57C00')
            return False
        else:
            status_label.config(text="✓", fg='#2E7D32')
            return True
    
    @staticmethod
    def validate_rujukan(entry_widget, status_label):
        """Validate reference format KE.JB(90)650/14/XXX"""
        rujukan = entry_widget.get().strip()
        
        if not rujukan:
            status_label.config(text="", fg='gray')
            return False
        
        # Pattern: KE.JB(90)650/14/XXX where XXX is numbers
        pattern = r'^KE\.JB\(90\)650/14/\d+$'
        
        if re.match(pattern, rujukan):
            status_label.config(text="✓", fg='#2E7D32')
            return True
        else:
            status_label.config(text="❌ Format: KE.JB(90)650/14/001", fg='#C62828')
            return False
    
    @staticmethod
    def validate_email(entry_widget, status_label):
        """Validate email format"""
        email = entry_widget.get().strip()
        
        if not email:
            status_label.config(text="", fg='gray')
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            status_label.config(text="✓", fg='#2E7D32')
            return True
        else:
            status_label.config(text="❌ Format email tidak sah", fg='#C62828')
            return False
    
    @staticmethod
    def validate_phone(entry_widget, status_label):
        """Validate phone number"""
        phone = entry_widget.get().strip()
        
        if not phone:
            status_label.config(text="", fg='gray')
            return False
        
        # Remove spaces and dashes
        phone_clean = phone.replace(' ', '').replace('-', '')
        
        if len(phone_clean) >= 9 and phone_clean.isdigit():
            status_label.config(text="✓", fg='#2E7D32')
            return True
        else:
            status_label.config(text="❌ Nombor telefon tidak sah", fg='#C62828')
            return False


class HelpButton:
    """Context-sensitive help button"""
    
    @staticmethod
    def create(parent, command, colors=None):
        """Create help button"""
        if colors is None:
            colors = {'button_primary': '#2196F3'}
        
        btn = tk.Button(parent,
                       text="❓ Bantuan",
                       font=('Arial', 10, 'bold'),
                       bg='#2196F3',
                       fg='white',
                       relief=tk.FLAT,
                       cursor='hand2',
                       command=command,
                       padx=15,
                       pady=8)
        
        # Add hover effect
        def on_enter(e):
            btn.config(bg='#1976D2')
        
        def on_leave(e):
            btn.config(bg='#2196F3')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn


class ProgressIndicator:
    """Show progress through steps"""
    
    @staticmethod
    def create(parent, steps, current_step=0):
        """Create progress indicator
        
        Args:
            parent: Parent widget
            steps: List of step names
            current_step: Current step index (0-based)
        """
        progress_frame = tk.Frame(parent, bg='white', pady=15)
        progress_frame.pack(fill=tk.X, padx=20)
        
        for i, step_text in enumerate(steps):
            is_active = i == current_step
            is_completed = i < current_step
            
            if is_completed:
                color = '#2E7D32'
                font_weight = 'normal'
                icon = "✓ "
            elif is_active:
                color = '#003366'
                font_weight = 'bold'
                icon = "▶ "
            else:
                color = '#CCCCCC'
                font_weight = 'normal'
                icon = ""
            
            tk.Label(progress_frame,
                    text=f"{icon}{step_text}",
                    font=('Arial', 11, font_weight),
                    bg='white',
                    fg=color).pack(side=tk.LEFT, padx=20)
            
            if i < len(steps) - 1:
                tk.Label(progress_frame,
                        text="→",
                        font=('Arial', 14),
                        bg='white',
                        fg='#CCCCCC').pack(side=tk.LEFT, padx=5)
        
        return progress_frame


class NotificationBar:
    """Show temporary notification messages"""
    
    def __init__(self, parent):
        self.parent = parent
        self.notification = None
    
    def show(self, message, duration=3000, type='info'):
        """Show notification
        
        Args:
            message: Message to show
            duration: Duration in milliseconds
            type: 'info', 'success', 'warning', 'error'
        """
        # Remove existing notification
        if self.notification:
            self.notification.destroy()
        
        # Color based on type
        colors = {
            'info': {'bg': '#2196F3', 'fg': 'white'},
            'success': {'bg': '#2E7D32', 'fg': 'white'},
            'warning': {'bg': '#F57C00', 'fg': 'white'},
            'error': {'bg': '#C62828', 'fg': 'white'}
        }
        
        color = colors.get(type, colors['info'])
        
        self.notification = tk.Frame(self.parent, bg=color['bg'])
        self.notification.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        
        tk.Label(self.notification,
                text=message,
                font=('Arial', 10),
                bg=color['bg'],
                fg=color['fg'],
                padx=20,
                pady=10).pack()
        
        # Auto hide after duration
        if duration > 0:
            self.parent.after(duration, self.hide)
    
    def hide(self):
        """Hide notification"""
        if self.notification:
            self.notification.destroy()
            self.notification = None


class DraftManager:
    """Auto-save and load drafts"""
    
    def __init__(self, form_type):
        self.form_type = form_type
        self.draft_dir = 'drafts'
        self.draft_file = os.path.join(self.draft_dir, f'draft_{form_type}.json')
        
        # Create drafts directory if not exists
        os.makedirs(self.draft_dir, exist_ok=True)
    
    def save_draft(self, data):
        """Save draft data"""
        try:
            draft_data = {
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'form_type': self.form_type
            }
            
            with open(self.draft_file, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving draft: {e}")
            return False
    
    def load_draft(self):
        """Load draft if exists"""
        try:
            if os.path.exists(self.draft_file):
                with open(self.draft_file, 'r', encoding='utf-8') as f:
                    draft_data = json.load(f)
                return draft_data.get('data', {})
        except Exception as e:
            print(f"Error loading draft: {e}")
        
        return None
    
    def has_draft(self):
        """Check if draft exists"""
        return os.path.exists(self.draft_file)
    
    def delete_draft(self):
        """Delete draft file"""
        try:
            if os.path.exists(self.draft_file):
                os.remove(self.draft_file)
            return True
        except Exception as e:
            print(f"Error deleting draft: {e}")
            return False


class ConfirmationDialog:
    """Show confirmation dialog with preview"""
    
    @staticmethod
    def show(parent, title, summary_data, on_confirm, on_cancel=None):
        """Show confirmation dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            summary_data: Dictionary of data to show
            on_confirm: Callback when confirmed
            on_cancel: Callback when cancelled
        """
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("600x500")
        dialog.configure(bg='white')
        
        # Center window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 300
        y = (dialog.winfo_screenheight() // 2) - 250
        dialog.geometry(f'600x500+{x}+{y}')
        
        # Make modal
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#003366', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text=title,
                font=('Arial', 14, 'bold'),
                bg='#003366',
                fg='white').pack(pady=15)
        
        # Content
        content_frame = tk.Frame(dialog, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(content_frame,
                text="Sila semak maklumat sebelum menyimpan:",
                font=('Arial', 11),
                bg='white',
                fg='#666666').pack(anchor='w', pady=(0, 15))
        
        # Summary box
        summary_box = tk.Frame(content_frame, bg='#F5F5F5', relief=tk.SOLID, bd=1)
        summary_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollbar for summary
        canvas = tk.Canvas(summary_box, bg='#F5F5F5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(summary_box, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#F5F5F5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display summary data
        for key, value in summary_data.items():
            row_frame = tk.Frame(scrollable_frame, bg='#F5F5F5')
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(row_frame,
                    text=f"{key}:",
                    font=('Arial', 10, 'bold'),
                    bg='#F5F5F5',
                    fg='#003366',
                    anchor='w',
                    width=20).pack(side=tk.LEFT, padx=(0, 10))
            
            # Truncate long values
            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."
            
            tk.Label(row_frame,
                    text=display_value,
                    font=('Arial', 10),
                    bg='#F5F5F5',
                    fg='#333333',
                    anchor='w',
                    wraplength=300,
                    justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def confirm():
            dialog.destroy()
            if on_confirm:
                on_confirm()
        
        def cancel():
            dialog.destroy()
            if on_cancel:
                on_cancel()
        
        tk.Button(btn_frame,
                 text="✓ Ya, Simpan",
                 font=('Arial', 11, 'bold'),
                 bg='#2E7D32',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 command=confirm,
                 padx=25,
                 pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame,
                 text="✗ Batal",
                 font=('Arial', 11),
                 bg='#757575',
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 command=cancel,
                 padx=25,
                 pady=10).pack(side=tk.LEFT, padx=10)
        
        return dialog


class SuccessDialog:
    """Show success message with next steps"""
    
    @staticmethod
    def show(parent, pdf_path=None, docx_path=None, on_new_document=None, on_go_home=None):
        """Show success dialog
        
        Args:
            parent: Parent window
            pdf_path: Path to saved PDF
            docx_path: Path to saved DOCX
            on_new_document: Callback for creating new document
            on_go_home: Callback for going to home
        """
        success_window = tk.Toplevel(parent)
        success_window.title("✅ Berjaya!")
        success_window.geometry("600x550")
        success_window.configure(bg='white')
        
        # Center window
        success_window.update_idletasks()
        x = (success_window.winfo_screenwidth() // 2) - 300
        y = (success_window.winfo_screenheight() // 2) - 275
        success_window.geometry(f'600x550+{x}+{y}')
        
        # Make modal
        success_window.transient(parent)
        success_window.grab_set()
        
        # Success animation
        tk.Label(success_window,
                text="✅",
                font=('Arial', 80),
                bg='white',
                fg='#2E7D32').pack(pady=20)
        
        tk.Label(success_window,
                text="Dokumen Berjaya Disimpan!",
                font=('Arial', 16, 'bold'),
                bg='white',
                fg='#2E7D32').pack(pady=10)
        
        # File locations
        if pdf_path or docx_path:
            info_frame = tk.Frame(success_window, bg='#F5F5F5', relief=tk.SOLID, bd=1)
            info_frame.pack(fill=tk.X, padx=30, pady=15)
            
            tk.Label(info_frame,
                    text="📁 Lokasi Fail:",
                    font=('Arial', 11, 'bold'),
                    bg='#F5F5F5',
                    fg='#003366').pack(anchor='w', padx=15, pady=(10, 5))
            
            if pdf_path:
                pdf_frame = tk.Frame(info_frame, bg='white')
                pdf_frame.pack(fill=tk.X, padx=15, pady=5)
                
                tk.Label(pdf_frame,
                        text=f"PDF: {os.path.basename(pdf_path)}",
                        font=('Arial', 9),
                        bg='white',
                        fg='#333333').pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                tk.Button(pdf_frame,
                         text="📂 Buka",
                         font=('Arial', 8),
                         bg='#2196F3',
                         fg='white',
                         relief=tk.FLAT,
                         cursor='hand2',
                         command=lambda: os.startfile(pdf_path) if os.path.exists(pdf_path) else None).pack(side=tk.RIGHT)
            
            if docx_path:
                docx_frame = tk.Frame(info_frame, bg='white')
                docx_frame.pack(fill=tk.X, padx=15, pady=(5, 10))
                
                tk.Label(docx_frame,
                        text=f"DOCX: {os.path.basename(docx_path)}",
                        font=('Arial', 9),
                        bg='white',
                        fg='#333333').pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                tk.Button(docx_frame,
                         text="📂 Buka",
                         font=('Arial', 8),
                         bg='#2196F3',
                         fg='white',
                         relief=tk.FLAT,
                         cursor='hand2',
                         command=lambda: os.startfile(docx_path) if os.path.exists(docx_path) else None).pack(side=tk.RIGHT)
        
        # Next steps
        next_frame = tk.Frame(success_window, bg='white')
        next_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        tk.Label(next_frame,
                text="🎯 Apa yang boleh anda buat sekarang:",
                font=('Arial', 11, 'bold'),
                bg='white',
                fg='#003366').pack(anchor='w', pady=(0, 10))
        
        options_text = """✓ Buka fail PDF/DOCX untuk lihat dokumen
✓ Buat dokumen baru dengan data lain
✓ Lihat sejarah dokumen yang telah dibuat
✓ Kembali ke menu utama"""
        
        tk.Label(next_frame,
                text=options_text,
                font=('Arial', 10),
                bg='white',
                fg='#666666',
                justify=tk.LEFT).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(success_window, bg='white')
        btn_frame.pack(pady=15)
        
        if pdf_path and os.path.exists(pdf_path):
            tk.Button(btn_frame,
                     text="📂 Buka Fail",
                     font=('Arial', 10, 'bold'),
                     bg='#2196F3',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=lambda: [os.startfile(pdf_path), success_window.destroy()],
                     padx=15,
                     pady=8).pack(side=tk.LEFT, padx=5)
        
        if on_new_document:
            tk.Button(btn_frame,
                     text="📝 Dokumen Baru",
                     font=('Arial', 10, 'bold'),
                     bg='#2E7D32',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=lambda: [success_window.destroy(), on_new_document()],
                     padx=15,
                     pady=8).pack(side=tk.LEFT, padx=5)
        
        if on_go_home:
            tk.Button(btn_frame,
                     text="🏠 Menu Utama",
                     font=('Arial', 10, 'bold'),
                     bg='#757575',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=lambda: [success_window.destroy(), on_go_home()],
                     padx=15,
                     pady=8).pack(side=tk.LEFT, padx=5)
        
        # Close button at bottom
        tk.Button(success_window,
                 text="Tutup",
                 font=('Arial', 9),
                 bg='white',
                 fg='#666666',
                 relief=tk.FLAT,
                 cursor='hand2',
                 command=success_window.destroy).pack(pady=10)
        
        return success_window


class KeyboardShortcuts:
    """Setup keyboard shortcuts for forms"""
    
    @staticmethod
    def setup(root, callbacks):
        """Setup keyboard shortcuts
        
        Args:
            root: Root window
            callbacks: Dictionary of callbacks
                {
                    'save': function,
                    'preview': function,
                    'help': function,
                    'back': function
                }
        """
        if callbacks.get('save'):
            root.bind('<Control-s>', lambda e: callbacks['save']())
        
        if callbacks.get('preview'):
            root.bind('<Control-p>', lambda e: callbacks['preview']())
        
        if callbacks.get('help'):
            root.bind('<F1>', lambda e: callbacks['help']())
        
        if callbacks.get('back'):
            root.bind('<Escape>', lambda e: callbacks['back']())
    
    @staticmethod
    def show_hints(root):
        """Show keyboard shortcut hints in status bar"""
        hint_frame = tk.Frame(root, bg='#F5F5F5')
        hint_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        hints_text = "⌨️ Pintasan: Ctrl+S (Simpan) | Ctrl+P (Pratonton) | F1 (Bantuan) | Esc (Kembali)"
        
        tk.Label(hint_frame,
                text=hints_text,
                font=('Arial', 8),
                bg='#F5F5F5',
                fg='#666666',
                pady=4).pack()
        
        return hint_frame

