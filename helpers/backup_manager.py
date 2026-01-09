"""
backup_manager.py - Automatic Backup System
Backs up templates, database, and drafts daily
"""
import os
import shutil
import zipfile
from datetime import datetime, timedelta
import json
import threading
import time

class BackupManager:
    """Manages automatic backups of critical files"""
    
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        self.critical_files = [
            'TemplateEditor.py',
            'kastam_documents.db',
            'template_storage.py',
            'user_preferences.json'
        ]
        self.critical_dirs = [
            'Templates'
        ]
        
        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_type='full'):
        """Create a backup with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{backup_type}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup files
            backed_up_files = []
            for filename in self.critical_files:
                if os.path.exists(filename):
                    dest = os.path.join(backup_path, filename)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(filename, dest)
                    backed_up_files.append(filename)
            
            # Backup directories
            for dirname in self.critical_dirs:
                if os.path.exists(dirname):
                    dest = os.path.join(backup_path, dirname)
                    shutil.copytree(dirname, dest, dirs_exist_ok=True)
                    backed_up_files.append(dirname)
            
            # Create backup manifest
            manifest = {
                'timestamp': timestamp,
                'type': backup_type,
                'files': backed_up_files,
                'python_version': self._get_python_version(),
                'app_version': '2.0.0'
            }
            
            with open(os.path.join(backup_path, 'manifest.json'), 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Create ZIP archive
            zip_path = f"{backup_path}.zip"
            self._create_zip(backup_path, zip_path)
            
            # Remove uncompressed backup
            shutil.rmtree(backup_path)
            
            # Clean old backups (keep last 30 days)
            self._clean_old_backups(days=30)
            
            return zip_path
            
        except Exception as e:
            print(f"Backup failed: {e}")
            return None
    
    def _create_zip(self, source_dir, zip_path):
        """Create ZIP archive of backup"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    def _clean_old_backups(self, days=30):
        """Remove backups older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.backup_dir):
            if filename.startswith('backup_') and filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff:
                    try:
                        os.remove(filepath)
                        print(f"Removed old backup: {filename}")
                    except Exception as e:
                        print(f"Failed to remove {filename}: {e}")
    
    def restore_backup(self, backup_zip_path):
        """Restore from a backup ZIP file"""
        try:
            # Create restore directory
            restore_dir = 'restore_temp'
            os.makedirs(restore_dir, exist_ok=True)
            
            # Extract ZIP
            with zipfile.ZipFile(backup_zip_path, 'r') as zipf:
                zipf.extractall(restore_dir)
            
            # Read manifest
            with open(os.path.join(restore_dir, 'manifest.json'), 'r') as f:
                manifest = json.load(f)
            
            # Restore files
            for filename in manifest['files']:
                source = os.path.join(restore_dir, filename)
                if os.path.exists(source):
                    if os.path.isfile(source):
                        # Backup current file first
                        if os.path.exists(filename):
                            shutil.copy2(filename, f"{filename}.pre-restore")
                        shutil.copy2(source, filename)
                    elif os.path.isdir(source):
                        if os.path.exists(filename):
                            shutil.rmtree(filename)
                        shutil.copytree(source, filename)
                    print(f"Restored: {filename}")
            
            # Cleanup
            shutil.rmtree(restore_dir)
            return True
            
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for filename in sorted(os.listdir(self.backup_dir), reverse=True):
            if filename.startswith('backup_') and filename.endswith('.zip'):
                filepath = os.path.join(self.backup_dir, filename)
                size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'size_mb': round(size, 2),
                    'date': mtime.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return backups
    
    def _get_python_version(self):
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def schedule_daily_backup(self):
        """Schedule daily backup at midnight"""
        def backup_thread():
            while True:
                now = datetime.now()
                # Calculate seconds until midnight
                tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                seconds_until_midnight = (tomorrow - now).total_seconds()
                
                print(f"Next backup in {seconds_until_midnight/3600:.1f} hours")
                time.sleep(seconds_until_midnight)
                
                # Create backup
                backup_path = self.create_backup('daily')
                if backup_path:
                    print(f"Daily backup created: {backup_path}")
        
        # Start backup thread
        thread = threading.Thread(target=backup_thread, daemon=True)
        thread.start()
        print("Daily backup scheduler started")


# GUI for backup management
class BackupManagerGUI:
    """GUI interface for backup management"""
    
    def __init__(self, parent=None):
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        self.backup_manager = BackupManager()
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Backup Manager")
        self.window.geometry("800x600")
        self.window.configure(bg='#F5F5F5')
        
        self.create_ui()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        # Header
        header = tk.Frame(self.window, bg='#003366', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="💾 Backup Manager",
                font=('Arial', 16, 'bold'),
                bg='#003366', fg='white').pack(pady=15)
        
        tk.Label(header, text="Manage your system backups",
                font=('Arial', 10),
                bg='#003366', fg='#E0E0E0').pack()
        
        # Buttons
        btn_frame = tk.Frame(self.window, bg='#F5F5F5')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="📥 Create Backup Now",
                 font=('Arial', 10, 'bold'),
                 bg='#2E7D32', fg='white',
                 padx=20, pady=10,
                 cursor='hand2',
                 command=self.create_backup_now).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="📤 Restore from Backup",
                 font=('Arial', 10, 'bold'),
                 bg='#1976D2', fg='white',
                 padx=20, pady=10,
                 cursor='hand2',
                 command=self.restore_backup).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🔄 Refresh List",
                 font=('Arial', 10, 'bold'),
                 bg='#666666', fg='white',
                 padx=20, pady=10,
                 cursor='hand2',
                 command=self.refresh_list).pack(side=tk.LEFT, padx=10)
        
        # List of backups
        list_frame = tk.Frame(self.window, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        tk.Label(list_frame, text="📋 Available Backups",
                font=('Arial', 12, 'bold'),
                bg='white', fg='#003366').pack(pady=10)
        
        # Treeview
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Date', 'Size (MB)', 'Type')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings', height=12)
        
        self.tree.heading('#0', text='Filename')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Size (MB)', text='Size (MB)')
        self.tree.heading('Type', text='Type')
        
        self.tree.column('#0', width=300)
        self.tree.column('Date', width=180)
        self.tree.column('Size (MB)', width=100)
        self.tree.column('Type', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label = tk.Label(self.window, text="Ready",
                                     font=('Arial', 9),
                                     bg='#E0E0E0', fg='#333333',
                                     anchor='w', padx=10)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Load backups
        self.refresh_list()
    
    def create_backup_now(self):
        import tkinter.messagebox as messagebox
        
        result = messagebox.askyesno("Confirm Backup",
                                     "Create a backup now?\n\nThis will save all critical files.")
        if result:
            self.status_label.config(text="Creating backup...")
            self.window.update()
            
            backup_path = self.backup_manager.create_backup('manual')
            if backup_path:
                messagebox.showinfo("Success",
                                   f"✅ Backup created successfully!\n\n{os.path.basename(backup_path)}")
                self.status_label.config(text=f"Backup created: {os.path.basename(backup_path)}")
                self.refresh_list()
            else:
                messagebox.showerror("Error", "❌ Backup failed!")
                self.status_label.config(text="Backup failed")
    
    def restore_backup(self):
        import tkinter.messagebox as messagebox
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a backup to restore")
            return
        
        item = self.tree.item(selection[0])
        backup_filename = item['text']
        backup_path = os.path.join('backups', backup_filename)
        
        result = messagebox.askyesnocancel(
            "Confirm Restore",
            f"⚠️ Restore from backup:\n{backup_filename}\n\n"
            "This will overwrite current files!\n\n"
            "Create a backup of current state first?"
        )
        
        if result is None:  # Cancel
            return
        elif result:  # Yes, backup first
            self.status_label.config(text="Creating pre-restore backup...")
            self.window.update()
            self.backup_manager.create_backup('pre-restore')
        
        # Restore
        self.status_label.config(text="Restoring backup...")
        self.window.update()
        
        if self.backup_manager.restore_backup(backup_path):
            messagebox.showinfo("Success", 
                              "✅ Backup restored successfully!\n\n"
                              "Please restart the application.")
            self.status_label.config(text="Restore completed - please restart app")
        else:
            messagebox.showerror("Error", "❌ Restore failed!")
            self.status_label.config(text="Restore failed")
    
    def refresh_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load backups
        backups = self.backup_manager.list_backups()
        for backup in backups:
            # Extract type from filename
            backup_type = 'Manual'
            if 'daily' in backup['filename']:
                backup_type = 'Daily'
            elif 'pre-restore' in backup['filename']:
                backup_type = 'Pre-Restore'
            
            self.tree.insert('', 'end',
                           text=backup['filename'],
                           values=(backup['date'], backup['size_mb'], backup_type))
        
        self.status_label.config(text=f"Found {len(backups)} backup(s)")


if __name__ == '__main__':
    # Test backup system
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    
    BackupManagerGUI()
    root.mainloop()

