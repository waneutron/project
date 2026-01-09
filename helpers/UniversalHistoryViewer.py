"""
UniversalHistoryViewer.py - Universal History Viewer for All Forms
Central history window that displays records from all document types
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from helpers.unified_database import UnifiedDatabase
from PIL import Image, ImageTk
import os


class UniversalHistoryViewer:
    """Universal history viewer for all document types"""
    
    def __init__(self, parent):
        self.db = UnifiedDatabase()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Sejarah Semua Dokumen - Sistem Pengurusan Kastam")
        self.window.geometry("1400x800")
        self.window.configure(bg='#F5F5F5')
        
        # Colors
        self.colors = {
            'primary': '#003366',
            'bg_main': '#F5F5F5',
            'button_info': '#1976D2',
            'button_danger': '#C62828',
            'button_success': '#2E7D32',
            'button_warning': '#F57C00'
        }
        
        self.create_header()
        self.create_filter_section()
        self.create_stats_section()
        self.create_table_section()
        self.create_button_section()
        
        # Load initial data
        self.load_data()
        self.update_statistics()
    
    def create_header(self):
        """Create header"""
        header = tk.Frame(self.window, bg=self.colors['primary'], height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(header, bg=self.colors['primary'])
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        
        from helpers.resource_path import get_logo_path
        logo_path = get_logo_path()
        
        if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                
                # Convert to RGBA if not already
                if logo_image.mode != 'RGBA':
                    logo_image = logo_image.convert('RGBA')
                
                logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
                
                # Create a background image with the same color as the frame
                background_color = self.colors['primary']  # '#003366'
                bg_rgb = tuple(int(background_color[i:i+2], 16) for i in (1, 3, 5))
                
                # Create a new RGBA image with the background color
                background = Image.new('RGBA', logo_image.size, bg_rgb + (255,))
                
                # Composite the logo onto the background using alpha compositing
                if logo_image.mode == 'RGBA':
                    logo_image = Image.alpha_composite(background, logo_image)
                    # Convert back to RGB for PhotoImage (Tkinter doesn't support RGBA well)
                    logo_image = logo_image.convert('RGB')
                
                logo_photo = ImageTk.PhotoImage(logo_image)
                logo_label = tk.Label(logo_frame, image=logo_photo, bg=self.colors['primary'])
                logo_label.image = logo_photo
                logo_label.pack()
        
        # Title
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(title_frame, text="SEJARAH DOKUMEN",
                font=('Arial', 16, 'bold'), bg=self.colors['primary'], 
                fg='white').pack(pady=(20, 5))
        
        tk.Label(title_frame, text="Sistem Pengurusan Dokumen Automatik",
                font=('Arial', 10, 'italic'), bg=self.colors['primary'], 
                fg='#E0E0E0').pack()
        
        # Close button
        tk.Button(header, text="✕ TUTUP", font=('Arial', 10, 'bold'),
                 bg='#C62828', fg='white', relief=tk.FLAT, cursor='hand2',
                 width=12, height=2,
                 command=self.window.destroy).pack(side=tk.RIGHT, padx=20)
    
    def create_filter_section(self):
        """Create filter and search section"""
        filter_frame = tk.Frame(self.window, bg='white')
        filter_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Inner frame
        inner = tk.Frame(filter_frame, bg='white')
        inner.pack(fill=tk.X, padx=15, pady=15)
        
        # Search
        tk.Label(inner, text="Cari:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=0, column=0, padx=(0, 5), pady=5, sticky='e')
        
        self.search_entry = tk.Entry(inner, width=35, font=('Arial', 10))
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())
        
        tk.Button(inner, text="🔍 Cari", font=('Arial', 9, 'bold'),
                 bg=self.colors['button_info'], fg='white', relief=tk.FLAT,
                 cursor='hand2', width=10,
                 command=self.on_search).grid(row=0, column=2, padx=5, pady=5)
        
        # Form Type Filter
        tk.Label(inner, text="Jenis Borang:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=0, column=3, padx=(20, 5), pady=5, sticky='e')
        
        self.filter_combo = ttk.Combobox(inner, width=20, state='readonly', font=('Arial', 9))
        self.filter_combo['values'] = ['Semua', 'Pelupusan', 'Butiran 5D', 'AMES', 'Sign Up B']
        self.filter_combo.current(0)
        self.filter_combo.grid(row=0, column=4, padx=5, pady=5)
        self.filter_combo.bind('<<ComboboxSelected>>', lambda e: self.load_data())
        
        # Buttons
        tk.Button(inner, text="🔄 Refresh", font=('Arial', 9, 'bold'),
                 bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=10,
                 command=self.load_data).grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(inner, text="📊 Laporan", font=('Arial', 9, 'bold'),
                 bg=self.colors['button_warning'], fg='white', relief=tk.FLAT,
                 cursor='hand2', width=10,
                 command=self.show_report).grid(row=0, column=6, padx=5, pady=5)
    
    def create_stats_section(self):
        """Create statistics dashboard"""
        stats_frame = tk.Frame(self.window, bg='white')
        stats_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        inner = tk.Frame(stats_frame, bg='white')
        inner.pack(fill=tk.X, padx=15, pady=10)
        
        # Stats cards
        self.stat_cards = {}
        stats_data = [
            ('total', 'JUMLAH', '#1976D2'),
            ('approved', 'DILULUSKAN', '#2E7D32'),
            ('rejected', 'DITOLAK', '#C62828'),
            ('month', 'BULAN INI', '#F57C00'),
            ('week', '7 HARI', '#7B1FA2')
        ]
        
        for idx, (key, label, color) in enumerate(stats_data):
            card = tk.Frame(inner, bg=color, relief=tk.RAISED, bd=1)
            card.grid(row=0, column=idx, padx=8, pady=5, sticky='ew')
            
            tk.Label(card, text=label, font=('Arial', 9, 'bold'),
                    bg=color, fg='white').pack(pady=(8, 2))
            
            value_label = tk.Label(card, text="0", font=('Arial', 20, 'bold'),
                                  bg=color, fg='white')
            value_label.pack(pady=(0, 8))
            
            self.stat_cards[key] = value_label
        
        # Make columns expand equally
        for i in range(5):
            inner.grid_columnconfigure(i, weight=1)
    
    def create_table_section(self):
        """Create main data table"""
        table_frame = tk.Frame(self.window, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))
        
        # Table container
        container = tk.Frame(table_frame, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(container, orient='vertical')
        scroll_x = ttk.Scrollbar(container, orient='horizontal')
        
        # Treeview
        self.tree = ttk.Treeview(container,
                                columns=('ID', 'JENIS', 'KATEGORI', 'RUJUKAN', 
                                        'NAMA', 'TARIKH', 'STATUS', 'PEGAWAI', 'REKOD'),
                                show='headings',
                                yscrollcommand=scroll_y.set,
                                xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        columns_config = [
            ('ID', 50, 'center'),
            ('JENIS', 120, 'center'),
            ('KATEGORI', 100, 'center'),
            ('RUJUKAN', 200, 'w'),
            ('NAMA', 250, 'w'),
            ('TARIKH', 100, 'center'),
            ('STATUS', 120, 'center'),
            ('PEGAWAI', 200, 'w'),
            ('REKOD', 150, 'center')
        ]
        
        for col, width, anchor in columns_config:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        # Tag configurations for status colors
        self.tree.tag_configure('approved', background='#E8F5E9')
        self.tree.tag_configure('rejected', background='#FFEBEE')
        self.tree.tag_configure('pending', background='#FFF3E0')
    
    def create_button_section(self):
        """Create action buttons"""
        btn_frame = tk.Frame(self.window, bg='white')
        btn_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        inner = tk.Frame(btn_frame, bg='white')
        inner.pack(pady=10)
        
        buttons = [
            ("👁 Lihat Detail", self.colors['button_info'], self.view_details),
            ("📄 Buka Dokumen", self.colors['button_success'], self.open_document),
            ("🗑 Hapus Rekod", self.colors['button_danger'], self.delete_record),
            ("📊 Eksport CSV", '#2E7D32', self.export_csv),
            ("📈 Statistik", self.colors['button_warning'], self.show_statistics)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(inner, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', relief=tk.FLAT,
                           cursor='hand2', width=18, height=2,
                           command=command)
            btn.pack(side=tk.LEFT, padx=5)
    
    def load_data(self):
        """Load data based on filter"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filter
        filter_value = self.filter_combo.get()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        applications = self.db.get_all_applications(form_type=form_type, limit=200)
        
        for app in applications:
            # Determine tag based on status
            tag = ''
            status = app.get('status', '').upper()
            if 'DILULUSKAN' in status or 'LULUS' in status:
                tag = 'approved'
            elif 'TIDAK' in status or 'DITOLAK' in status:
                tag = 'rejected'
            
            self.tree.insert('', 'end', values=(
                app['id'],
                app['form_type'].upper(),
                app.get('category', '-'),
                app['rujukan_kami'] or '-',
                app['nama_syarikat'],
                app['tarikh'] or '-',
                app.get('status', '-'),
                app.get('nama_pegawai', '-'),
                app['created_at']
            ), tags=(tag,))
        
        self.update_statistics()
    
    def on_search(self):
        """Perform search"""
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            self.load_data()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filter_value = self.filter_combo.get()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        results = self.db.search_applications(search_text, form_type=form_type)
        
        for app in results:
            tag = ''
            status = app.get('status', '').upper()
            if 'DILULUSKAN' in status or 'LULUS' in status:
                tag = 'approved'
            elif 'TIDAK' in status or 'DITOLAK' in status:
                tag = 'rejected'
            
            self.tree.insert('', 'end', values=(
                app['id'],
                app['form_type'].upper(),
                app.get('category', '-'),
                app['rujukan_kami'] or '-',
                app['nama_syarikat'],
                app['tarikh'] or '-',
                app.get('status', '-'),
                app.get('nama_pegawai', '-'),
                app['created_at']
            ), tags=(tag,))
    
    def update_statistics(self):
        """Update statistics cards"""
        filter_value = self.filter_combo.get()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        stats = self.db.get_statistics(form_type=form_type)
        
        self.stat_cards['total'].config(text=str(stats.get('total_applications', 0)))
        
        by_status = stats.get('by_status', {})
        approved = sum(count for status, count in by_status.items() 
                      if 'DILULUSKAN' in status.upper() or 'LULUS' in status.upper())
        rejected = sum(count for status, count in by_status.items() 
                      if 'TIDAK' in status.upper() or 'DITOLAK' in status.upper())
        
        self.stat_cards['approved'].config(text=str(approved))
        self.stat_cards['rejected'].config(text=str(rejected))
        self.stat_cards['month'].config(text=str(stats.get('this_month', 0)))
        self.stat_cards['week'].config(text=str(stats.get('last_7_days', 0)))
    
    def view_details(self):
        """View application details"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Amaran", "Sila pilih rekod untuk dilihat")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        app_id = values[0]
        
        application = self.db.get_application_by_id(app_id)
        if not application:
            messagebox.showerror("Ralat", "Rekod tidak dijumpai")
            return
        
        DetailViewer(self.window, application)
    
    def open_document(self):
        """Open saved document"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Amaran", "Sila pilih rekod")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        app_id = values[0]
        
        application = self.db.get_application_by_id(app_id)
        if not application:
            return
        
        doc_path = application.get('document_path')
        if not doc_path or not os.path.exists(doc_path):
            messagebox.showwarning("Amaran", "Dokumen tidak dijumpai")
            return
        
        try:
            if os.name == 'nt':
                os.startfile(doc_path)
            else:
                import subprocess
                subprocess.call(['open', doc_path])
        except Exception as e:
            messagebox.showerror("Ralat", f"Tidak dapat buka dokumen: {e}")
    
    def delete_record(self):
        """Delete selected record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Amaran", "Sila pilih rekod untuk dihapus")
            return
        
        if not messagebox.askyesno("Pengesahan",
                                   "Adakah anda pasti ingin menghapus rekod ini?\n\n"
                                   "Tindakan ini tidak boleh dibatalkan."):
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        app_id = values[0]
        
        try:
            self.db.delete_application(app_id)
            self.tree.delete(item)
            self.update_statistics()
            messagebox.showinfo("Berjaya", "Rekod berjaya dihapus")
        except Exception as e:
            messagebox.showerror("Ralat", f"Gagal menghapus rekod: {str(e)}")
    
    def export_csv(self):
        """Export to CSV"""
        filter_value = self.filter_combo.get()
        form_type_map = {
            'Pelupusan': 'pelupusan',
            'Butiran 5D': 'butiran5d',
            'AMES': 'ames',
            'Sign Up B': 'signupb'
        }
        form_type = form_type_map.get(filter_value) if filter_value != 'Semua' else None
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"kastam_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                self.db.export_to_csv(form_type=form_type, filename=filename)
                messagebox.showinfo("Berjaya", f"Data berjaya dieksport ke:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ralat", f"Gagal eksport: {str(e)}")
    
    def show_statistics(self):
        """Show detailed statistics"""
        StatisticsWindow(self.window, self.db)
    
    def show_report(self):
        """Show monthly report"""
        ReportWindow(self.window, self.db)


class DetailViewer:
    """Detailed view of application"""
    
    def __init__(self, parent, application):
        self.app = application
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Detail - {application.get('rujukan_kami', 'N/A')}")
        self.window.geometry("900x700")
        self.window.configure(bg='white')
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 450
        y = (self.window.winfo_screenheight() // 2) - 350
        self.window.geometry(f'900x700+{x}+{y}')
        
        self.create_content()
    
    def create_content(self):
        """Create detail view content"""
        # Header
        header = tk.Frame(self.window, bg='#003366')
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"DETAIL PERMOHONAN - {self.app['form_type'].upper()}",
                font=('Arial', 13, 'bold'), bg='#003366', fg='white').pack(pady=15)
        
        # Scrollable content
        canvas = tk.Canvas(self.window, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=canvas.yview)
        
        content_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Content
        content = tk.Frame(content_frame, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Basic info
        tk.Label(content, text="MAKLUMAT ASAS", font=('Arial', 11, 'bold'),
                bg='white', fg='#003366').grid(row=0, column=0, columnspan=2, 
                                               sticky='w', pady=(0, 10))
        
        basic_info = [
            ("Rujukan:", self.app.get('rujukan_kami', '-')),
            ("Nama Syarikat:", self.app.get('nama_syarikat', '-')),
            ("Alamat:", self.app.get('alamat', '-')),
            ("Tarikh:", self.app.get('tarikh', '-')),
            ("Status:", self.app.get('status', '-')),
            ("Pegawai:", self.app.get('nama_pegawai', '-')),
            ("Tarikh Rekod:", self.app.get('created_at', '-'))
        ]
        
        row = 1
        for label, value in basic_info:
            tk.Label(content, text=label, font=('Arial', 9, 'bold'),
                    bg='white', anchor='e', width=20).grid(row=row, column=0,
                                                           sticky='e', padx=5, pady=5)
            tk.Label(content, text=value, font=('Arial', 9),
                    bg='white', anchor='w', wraplength=500).grid(row=row, column=1,
                                                                 sticky='w', padx=5, pady=5)
            row += 1
        
        # Close button
        tk.Button(content, text="Tutup", font=('Arial', 10, 'bold'),
                 bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15,
                 command=self.window.destroy).grid(row=row+5, column=0, 
                                                   columnspan=2, pady=20)


class StatisticsWindow:
    """Statistics dashboard window"""
    
    def __init__(self, parent, db):
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("Statistik Sistem")
        self.window.geometry("1000x600")
        self.window.configure(bg='#F5F5F5')
        
        self.create_content()
    
    def create_content(self):
        """Create statistics content"""
        # Header
        header = tk.Frame(self.window, bg='#003366')
        header.pack(fill=tk.X)
        
        tk.Label(header, text="STATISTIK SISTEM", font=('Arial', 14, 'bold'),
                bg='#003366', fg='white').pack(pady=15)
        
        # Content
        content = tk.Frame(self.window, bg='#F5F5F5')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats = self.db.get_statistics()
        
        # Display stats
        info_text = f"""
STATISTIK KESELURUHAN SISTEM

Jumlah Permohonan: {stats.get('total_applications', 0)}

Minggu Ini (7 hari): {stats.get('last_7_days', 0)}
Bulan Ini (30 hari): {stats.get('last_30_days', 0)}
Tahun Ini: {stats.get('this_year', 0)}

Status Permohonan:
"""
        
        for status, count in stats.get('by_status', {}).items():
            info_text += f"  - {status}: {count}\n"
        
        if 'by_form_type' in stats:
            info_text += "\n\nMengikut Jenis Borang:\n"
            for form_type, count in stats.get('by_form_type', {}).items():
                info_text += f"  - {form_type.upper()}: {count}\n"
        
        text_widget = tk.Text(content, font=('Arial', 11), bg='white',
                             relief=tk.FLAT, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        # Close button
        tk.Button(content, text="Tutup", font=('Arial', 10, 'bold'),
                 bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15,
                 command=self.window.destroy).pack(pady=10)


class ReportWindow:
    """Monthly report window"""
    
    def __init__(self, parent, db):
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("Laporan Bulanan")
        self.window.geometry("800x600")
        self.window.configure(bg='#F5F5F5')
        
        self.create_content()
    
    def create_content(self):
        """Create report content"""
        # Header
        header = tk.Frame(self.window, bg='#003366')
        header.pack(fill=tk.X)
        
        tk.Label(header, text="LAPORAN BULANAN", font=('Arial', 14, 'bold'),
                bg='#003366', fg='white').pack(pady=15)
        
        # Year selector
        selector_frame = tk.Frame(self.window, bg='white')
        selector_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(selector_frame, text="Tahun:", font=('Arial', 10, 'bold'),
                bg='white').pack(side=tk.LEFT, padx=5)
        
        current_year = datetime.now().year
        self.year_combo = ttk.Combobox(selector_frame, width=15, state='readonly')
        self.year_combo['values'] = [str(y) for y in range(2020, current_year + 2)]
        self.year_combo.set(str(current_year))
        self.year_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(selector_frame, text="Papar", font=('Arial', 9, 'bold'),
                 bg='#1976D2', fg='white', relief=tk.FLAT, cursor='hand2',
                 width=10, command=self.load_report).pack(side=tk.LEFT, padx=5)
        
        # Table
        table_frame = tk.Frame(self.window, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scroll = ttk.Scrollbar(table_frame, orient='vertical')
        
        self.report_tree = ttk.Treeview(table_frame,
                                       columns=('BULAN', 'JENIS', 'BILANGAN'),
                                       show='headings',
                                       yscrollcommand=scroll.set)
        
        scroll.config(command=self.report_tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_tree.pack(fill=tk.BOTH, expand=True)
        
        self.report_tree.heading('BULAN', text='BULAN')
        self.report_tree.heading('JENIS', text='JENIS BORANG')
        self.report_tree.heading('BILANGAN', text='BILANGAN')
        
        self.report_tree.column('BULAN', width=150, anchor='center')
        self.report_tree.column('JENIS', width=200, anchor='w')
        self.report_tree.column('BILANGAN', width=100, anchor='center')
        
        # Load initial report
        self.load_report()
        
        # Close button
        tk.Button(self.window, text="Tutup", font=('Arial', 10, 'bold'),
                 bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15,
                 command=self.window.destroy).pack(pady=10)
    
    def load_report(self):
        """Load monthly report"""
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        year = int(self.year_combo.get())
        report_data = self.db.get_monthly_report(year)
        
        month_names = {
            '01': 'Januari', '02': 'Februari', '03': 'Mac', '04': 'April',
            '05': 'Mei', '06': 'Jun', '07': 'Julai', '08': 'Ogos',
            '09': 'September', '10': 'Oktober', '11': 'November', '12': 'Disember'
        }
        
        for data in report_data:
            month_name = month_names.get(data['month'], data['month'])
            self.report_tree.insert('', 'end', values=(
                month_name,
                data['form_type'].upper(),
                data['count']
            ))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    UniversalHistoryViewer(root)
    root.mainloop()