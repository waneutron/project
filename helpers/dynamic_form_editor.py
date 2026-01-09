"""
dynamic_form_editor.py - Visual Form Builder for Non-Technical Users
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from helpers.form_config_manager import FormConfigManager
from helpers.dynamic_form_generator import DynamicFormGenerator

class DynamicFormEditor:
    """Visual editor for creating/editing forms dynamically"""
    
    def __init__(self, parent, form_name=None):
        try:
            # Validate parent window
            if parent is None:
                raise ValueError("Parent window cannot be None")
            
            try:
                # Check if parent window exists
                if not parent.winfo_exists():
                    raise ValueError("Parent window has been destroyed")
            except tk.TclError:
                raise ValueError("Parent window is invalid")
            
            self.parent = parent
            self.form_name = form_name or "NewForm"
            
            # Initialize config manager with error handling
            try:
                self.config_manager = FormConfigManager()
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to initialize config manager: {e}")
                raise
            
            # Load config with error handling
            try:
                self.config = self.config_manager.load_form_config(self.form_name)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error loading config, using default: {e}")
                self.config = self.config_manager.get_default_config(self.form_name)
            
            self.selected_item = None
            
            # Create window with error handling
            try:
                self.window = tk.Toplevel(parent)
                self.window.title(f"Form Editor - {self.form_name}")
                self.window.geometry("1400x800")
                self.window.configure(bg='#F5F5F5')
                
                # Center window
                try:
                    self.window.update_idletasks()
                    x = (self.window.winfo_screenwidth() // 2) - 700
                    y = (self.window.winfo_screenheight() // 2) - 400
                    self.window.geometry(f'1400x800+{x}+{y}')
                except Exception as e:
                    print(f"Error centering window: {e}")
                
                # Make window appear on top
                try:
                    self.window.attributes('-topmost', True)
                    self.window.after_idle(lambda: self.window.attributes('-topmost', False))
                    self.window.lift()
                    self.window.focus_force()
                except Exception as e:
                    print(f"Error setting window attributes: {e}")
                
                try:
                    self.window.transient(parent)
                except Exception as e:
                    print(f"Warning: Could not set transient: {e}")
                
                self.colors = {
                    'primary': '#003366',
                    'secondary': '#004080',
                    'bg_white': 'white',
                    'button_success': '#2E7D32',
                    'button_primary': '#003366',
                    'button_danger': '#C62828',
                    'border': '#CCCCCC'
                }
                
                # Create UI with error handling
                try:
                    print("Initializing: Creating UI...")
                    self.create_ui()
                    print("Initializing: UI created")
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"CRITICAL: Failed to create UI: {e}")
                    try:
                        messagebox.showerror("Error", f"Failed to create UI: {e}")
                    except:
                        pass
                    try:
                        self.window.destroy()
                    except:
                        pass
                    raise
                
                # Load config to UI with error handling
                try:
                    print("Initializing: Loading config to UI...")
                    self.load_config_to_ui()
                    print("Initializing: Config loaded")
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Warning: Error loading config to UI: {e}")
                    # Don't raise, just show warning
                    try:
                        messagebox.showwarning("Warning", f"Some form data could not be loaded: {e}")
                    except:
                        pass
                
                # Ensure window is visible and updated
                try:
                    print("Initializing: Making window visible...")
                    self.window.deiconify()
                    self.window.update()
                    self.window.update_idletasks()
                    print("Initializing: Window should now be visible")
                    
                    # Set grab after window is visible (optional, can cause issues)
                    try:
                        self.window.grab_set()
                        print("Initializing: Grab set")
                    except Exception as e:
                        print(f"Warning: Could not set grab (non-critical): {e}")
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"ERROR making window visible: {e}")
            except Exception as window_error:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to create window: {window_error}")
                raise
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to initialize Form Editor: {e}")
            raise
    
    def create_ui(self):
        """Create the form editor interface"""
        try:
            print(f"Creating UI for form: {self.form_name}")
            # Header
            header = tk.Frame(self.window, bg=self.colors['primary'], height=70)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            tk.Label(header,
                    text=f"📝 Form Editor: {self.form_name}",
                    font=('Arial', 16, 'bold'),
                    bg=self.colors['primary'],
                    fg='white').pack(pady=20)
            
            # Main container
            main_frame = tk.Frame(self.window, bg='#F5F5F5')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Left panel - Form structure
            left_panel = tk.Frame(main_frame, bg='white')
            left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            border_left = tk.Frame(left_panel, bg=self.colors['border'], bd=1)
            border_left.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
            
            content_left = tk.Frame(border_left, bg='white', padx=15, pady=15)
            content_left.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(content_left,
                    text="Form Structure",
                    font=('Arial', 12, 'bold'),
                    bg='white',
                    fg=self.colors['primary']).pack(anchor='w', pady=(0, 10))
            
            # Buttons for adding elements
            btn_frame = tk.Frame(content_left, bg='white')
            btn_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Button(btn_frame,
                     text="➕ Add Field",
                     font=('Arial', 10, 'bold'),
                     bg=self.colors['button_success'],
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=self.add_field).pack(side=tk.LEFT, padx=5)
            
            tk.Button(btn_frame,
                     text="☑ Add Checkbox",
                     font=('Arial', 10, 'bold'),
                     bg=self.colors['button_primary'],
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=self.add_checkbox).pack(side=tk.LEFT, padx=5)
            
            tk.Button(btn_frame,
                     text="📋 Add Section",
                     font=('Arial', 10, 'bold'),
                     bg='#1976D2',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=self.add_section).pack(side=tk.LEFT, padx=5)
            
            # Import existing fields button
            tk.Button(btn_frame,
                     text="📥 Import Existing Fields",
                     font=('Arial', 10, 'bold'),
                     bg='#FF9800',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     command=self.import_existing_fields).pack(side=tk.LEFT, padx=5)
            
            # Fields list with scroll
            print("create_ui: Creating fields tree...")
            list_frame = tk.Frame(content_left, bg='white')
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.fields_tree = ttk.Treeview(list_frame,
                                            columns=('Type', 'Label', 'ID', 'Placeholder'),
                                            show='tree headings',
                                            yscrollcommand=scrollbar.set,
                                            height=20)
            print("create_ui: Treeview created")
            self.fields_tree.heading('#0', text='Element')
            self.fields_tree.heading('Type', text='Type')
            self.fields_tree.heading('Label', text='Label')
            self.fields_tree.heading('ID', text='Field ID')
            self.fields_tree.heading('Placeholder', text='Placeholder')
            
            self.fields_tree.column('#0', width=150)
            self.fields_tree.column('Type', width=100)
            self.fields_tree.column('Label', width=200)
            self.fields_tree.column('ID', width=150)
            self.fields_tree.column('Placeholder', width=200)
            
            self.fields_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.fields_tree.yview)
            print("create_ui: Treeview configured")
            
            # Bind events
            print("create_ui: Binding events...")
            self.fields_tree.bind('<Double-Button-1>', self.edit_selected)
            self.fields_tree.bind('<<TreeviewSelect>>', self.on_select)
            print("create_ui: Events bound")
            
            # Right panel - Properties editor
            right_panel = tk.Frame(main_frame, bg='white')
            right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            border_right = tk.Frame(right_panel, bg=self.colors['border'], bd=1)
            border_right.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
            
            content_right = tk.Frame(border_right, bg='white', padx=15, pady=15)
            content_right.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(content_right,
                    text="Properties Editor",
                    font=('Arial', 12, 'bold'),
                    bg='white',
                    fg=self.colors['primary']).pack(anchor='w', pady=(0, 15))
            
            # Properties form (will be populated dynamically)
            self.properties_frame = tk.Frame(content_right, bg='white')
            self.properties_frame.pack(fill=tk.BOTH, expand=True)
            
            # Placeholder mapping section
            mapping_frame = tk.LabelFrame(content_right,
                                          text="Placeholder Mapping",
                                          font=('Arial', 10, 'bold'),
                                          bg='white',
                                          fg=self.colors['primary'],
                                          padx=10,
                                          pady=10)
            mapping_frame.pack(fill=tk.X, pady=(10, 0))
            
            tk.Label(mapping_frame,
                    text="Map this field to template placeholder:",
                    font=('Arial', 9),
                    bg='white').pack(anchor='w')
            
            self.placeholder_entry = tk.Entry(mapping_frame, width=40, font=('Arial', 10))
            self.placeholder_entry.pack(fill=tk.X, pady=5)
            
            tk.Label(mapping_frame,
                    text="Example: <<NAMA_SYARIKAT>>",
                    font=('Arial', 8),
                    bg='white',
                    fg='#666666').pack(anchor='w')
            
            # Bottom buttons
            btn_bottom = tk.Frame(self.window, bg='#F5F5F5', pady=15)
            btn_bottom.pack(fill=tk.X)
            
            tk.Button(btn_bottom,
                     text="💾 Save Form",
                     font=('Arial', 11, 'bold'),
                     bg=self.colors['button_success'],
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     width=20,
                     command=self.save_form).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_bottom,
                     text="🗑️ Delete Selected",
                     font=('Arial', 10),
                     bg=self.colors['button_danger'],
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     width=18,
                     command=self.delete_selected).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_bottom,
                     text="🔄 Preview Form",
                     font=('Arial', 10),
                     bg='#1976D2',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     width=18,
                     command=self.preview_form).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_bottom,
                     text="Tutup",
                     font=('Arial', 10),
                     bg='#666666',
                     fg='white',
                     relief=tk.FLAT,
                     cursor='hand2',
                     width=15,
                     command=self.window.destroy).pack(side=tk.LEFT, padx=10)
            print("create_ui: All UI elements created successfully")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"CRITICAL ERROR in create_ui: {e}")
            try:
                messagebox.showerror("Error", f"Failed to create UI: {e}\n\nCheck console for details.")
            except:
                print("Could not show error messagebox")
            raise
    
    def add_field(self):
        """Add a new field"""
        dialog = FieldPropertiesDialog(self.window, field_type='Entry')
        if dialog.result:
            field_config = dialog.result
            
            # Check for duplicate field_id
            existing_ids = [f.get('field_id', '') for f in self.config.get('fields', [])]
            existing_ids += [c.get('field_id', '') for c in self.config.get('checkboxes', [])]
            
            if field_config.get('field_id') in existing_ids:
                messagebox.showerror("Error", 
                                   f"Field ID '{field_config.get('field_id')}' already exists!\n\n"
                                   "Please use a unique Field ID.")
                return
            
            # Check for duplicate label
            existing_labels = [f.get('label', '') for f in self.config.get('fields', [])]
            existing_labels += [c.get('label', '') for c in self.config.get('checkboxes', [])]
            
            if field_config.get('label') in existing_labels:
                if not messagebox.askyesno("Warning", 
                                          f"Label '{field_config.get('label')}' already exists.\n\n"
                                          "Do you want to add it anyway?"):
                    return
            
            self.config['fields'].append(field_config)
            self.refresh_tree()
            
            # Select the newly added field
            self.window.after(100, lambda: self.select_item_by_text(f"Field: {field_config['label']}"))
    
    def add_checkbox(self):
        """Add a new checkbox"""
        dialog = CheckboxPropertiesDialog(self.window)
        if dialog.result:
            checkbox_config = dialog.result
            
            # Check for duplicate field_id
            existing_ids = [f.get('field_id', '') for f in self.config.get('fields', [])]
            existing_ids += [c.get('field_id', '') for c in self.config.get('checkboxes', [])]
            
            if checkbox_config.get('field_id') in existing_ids:
                messagebox.showerror("Error", 
                                   f"Field ID '{checkbox_config.get('field_id')}' already exists!\n\n"
                                   "Please use a unique Field ID.")
                return
            
            self.config['checkboxes'].append(checkbox_config)
            self.refresh_tree()
            
            # Select the newly added checkbox
            self.window.after(100, lambda: self.select_item_by_text(f"Checkbox: {checkbox_config['label']}"))
    
    def add_section(self):
        """Add a new section"""
        section_name = simpledialog.askstring("Add Section", "Enter section name:")
        if section_name:
            self.config['sections'].append({
                'name': section_name,
                'title': section_name,
                'fields': []
            })
            self.refresh_tree()
    
    def edit_selected(self, event=None):
        """Edit selected element"""
        selection = self.fields_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        item_text = self.fields_tree.item(item, 'text')
        item_values = self.fields_tree.item(item, 'values')
        
        # Find in config and edit
        if item_text.startswith('Field:'):
            field_label = item_text.replace('Field: ', '')
            for idx, field in enumerate(self.config['fields']):
                if field['label'] == field_label:
                    dialog = FieldPropertiesDialog(self.window, field_config=field)
                    if dialog.result:
                        self.config['fields'][idx] = dialog.result
                        self.refresh_tree()
                    break
        elif item_text.startswith('Checkbox:'):
            checkbox_label = item_text.replace('Checkbox: ', '')
            for idx, checkbox in enumerate(self.config['checkboxes']):
                if checkbox['label'] == checkbox_label:
                    dialog = CheckboxPropertiesDialog(self.window, checkbox_config=checkbox)
                    if dialog.result:
                        self.config['checkboxes'][idx] = dialog.result
                        self.refresh_tree()
                    break
    
    def on_select(self, event=None):
        """Handle selection change"""
        selection = self.fields_tree.selection()
        if not selection:
            self.clear_properties()
            return
        
        item = selection[0]
        item_text = self.fields_tree.item(item, 'text')
        
        # Clear and populate properties
        self.clear_properties()
        
        if item_text.startswith('Field:'):
            field_label = item_text.replace('Field: ', '')
            for field in self.config['fields']:
                if field['label'] == field_label:
                    self.show_field_properties(field)
                    break
        elif item_text.startswith('Checkbox:'):
            checkbox_label = item_text.replace('Checkbox: ', '')
            for checkbox in self.config['checkboxes']:
                if checkbox['label'] == checkbox_label:
                    self.show_checkbox_properties(checkbox)
                    break
    
    def clear_properties(self):
        """Clear properties frame"""
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
        # Also clear grid configuration
        for i in range(20):  # Clear up to 20 rows
            self.properties_frame.grid_rowconfigure(i, weight=0)
        self.placeholder_entry.delete(0, tk.END)
    
    def show_field_properties(self, field):
        """Show field properties in properties frame"""
        row = 0
        
        # Type
        tk.Label(self.properties_frame, text="Type:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(self.properties_frame, text=field.get('type', 'Entry'), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        # Label
        tk.Label(self.properties_frame, text="Label:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(self.properties_frame, text=field.get('label', ''), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        # Field ID
        tk.Label(self.properties_frame, text="Field ID:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(self.properties_frame, text=field.get('field_id', ''), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        # Default Value
        if field.get('default_value'):
            tk.Label(self.properties_frame, text="Default Value:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
            tk.Label(self.properties_frame, text=field.get('default_value', ''), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
            row += 1
        
        # Placeholder mapping - Always set, clear first
        placeholder = self.config.get('placeholder_mappings', {}).get(field.get('field_id', ''), '')
        self.placeholder_entry.delete(0, tk.END)  # Clear first
        if placeholder:
            self.placeholder_entry.insert(0, placeholder)
    
    def show_checkbox_properties(self, checkbox):
        """Show checkbox properties"""
        row = 0
        
        tk.Label(self.properties_frame, text="Label:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(self.properties_frame, text=checkbox.get('label', ''), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        tk.Label(self.properties_frame, text="Field ID:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        tk.Label(self.properties_frame, text=checkbox.get('field_id', ''), font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        row += 1
        
        tk.Label(self.properties_frame, text="Default:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        default_text = "Checked" if checkbox.get('default_checked', False) else "Unchecked"
        tk.Label(self.properties_frame, text=default_text, font=('Arial', 10), bg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        
        # Placeholder mapping - Always set, clear first
        placeholder = self.config.get('placeholder_mappings', {}).get(checkbox.get('field_id', ''), '')
        self.placeholder_entry.delete(0, tk.END)  # Clear first
        if placeholder:
            self.placeholder_entry.insert(0, placeholder)
    
    def delete_selected(self):
        """Delete selected element"""
        selection = self.fields_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an element to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Delete selected element?"):
            return
        
        item = selection[0]
        item_text = self.fields_tree.item(item, 'text')
        
        if item_text.startswith('Field:'):
            field_label = item_text.replace('Field: ', '')
            self.config['fields'] = [f for f in self.config['fields'] if f['label'] != field_label]
        elif item_text.startswith('Checkbox:'):
            checkbox_label = item_text.replace('Checkbox: ', '')
            self.config['checkboxes'] = [c for c in self.config['checkboxes'] if c['label'] != checkbox_label]
        elif item_text.startswith('Section:'):
            section_name = item_text.replace('Section: ', '')
            self.config['sections'] = [s for s in self.config['sections'] if s['name'] != section_name]
        
        self.refresh_tree()
        self.clear_properties()
    
    def refresh_tree(self):
        """Refresh the fields tree"""
        try:
            print("refresh_tree: Starting...")
            if not hasattr(self, 'fields_tree') or not self.fields_tree:
                print("ERROR: fields_tree not available")
                return
            
            if not hasattr(self, 'config') or not self.config:
                print("ERROR: config not available")
                return
            
            print(f"refresh_tree: Config has {len(self.config.get('sections', []))} sections, {len(self.config.get('fields', []))} fields, {len(self.config.get('checkboxes', []))} checkboxes")
            
            # Save current selection
            try:
                print("refresh_tree: Getting current selection...")
                current_selection = self.fields_tree.selection()
                selected_text = None
                if current_selection:
                    selected_text = self.fields_tree.item(current_selection[0], 'text')
                print(f"refresh_tree: Current selection: {selected_text}")
            except Exception as e:
                print(f"ERROR getting selection: {e}")
                import traceback
                traceback.print_exc()
                selected_text = None
            
            # Clear tree
            try:
                print("refresh_tree: Clearing tree...")
                for item in self.fields_tree.get_children():
                    self.fields_tree.delete(item)
                print("refresh_tree: Tree cleared")
            except Exception as e:
                print(f"ERROR clearing tree: {e}")
                import traceback
                traceback.print_exc()
            
            # Add sections
            try:
                print("refresh_tree: Adding sections...")
                for section in self.config.get('sections', []):
                    try:
                        if not isinstance(section, dict) or 'name' not in section:
                            continue
                        item_id = self.fields_tree.insert('', 'end',
                                           text=f"Section: {section['name']}",
                                           values=('Section', section.get('title', ''), '', ''))
                        if selected_text and selected_text == f"Section: {section['name']}":
                            self.fields_tree.selection_set(item_id)
                    except Exception as e:
                        print(f"ERROR adding section: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
                print("refresh_tree: Sections added")
            except Exception as e:
                print(f"ERROR processing sections: {e}")
                import traceback
                traceback.print_exc()
            
            # Add fields
            try:
                print("refresh_tree: Adding fields...")
                for field in self.config.get('fields', []):
                    try:
                        if not isinstance(field, dict) or 'label' not in field:
                            continue
                        placeholder = self.config.get('placeholder_mappings', {}).get(field.get('field_id', ''), '')
                        item_id = self.fields_tree.insert('', 'end',
                                           text=f"Field: {field['label']}",
                                           values=(field.get('type', 'Entry'),
                                                  field['label'],
                                                  field.get('field_id', ''),
                                                  placeholder))
                        if selected_text and selected_text == f"Field: {field['label']}":
                            self.fields_tree.selection_set(item_id)
                    except Exception as e:
                        print(f"ERROR adding field: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
                print("refresh_tree: Fields added")
            except Exception as e:
                print(f"ERROR processing fields: {e}")
                import traceback
                traceback.print_exc()
            
            # Add checkboxes
            try:
                print("refresh_tree: Adding checkboxes...")
                for checkbox in self.config.get('checkboxes', []):
                    try:
                        if not isinstance(checkbox, dict) or 'label' not in checkbox:
                            continue
                        placeholder = self.config.get('placeholder_mappings', {}).get(checkbox.get('field_id', ''), '')
                        item_id = self.fields_tree.insert('', 'end',
                                          text=f"Checkbox: {checkbox['label']}",
                                          values=('Checkbox',
                                                 checkbox['label'],
                                                 checkbox.get('field_id', ''),
                                                 placeholder))
                        if selected_text and selected_text == f"Checkbox: {checkbox['label']}":
                            self.fields_tree.selection_set(item_id)
                    except Exception as e:
                        print(f"ERROR adding checkbox: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
                print("refresh_tree: Checkboxes added")
            except Exception as e:
                print(f"ERROR processing checkboxes: {e}")
                import traceback
                traceback.print_exc()
            
            # Restore selection and trigger on_select if there was a selection
            try:
                print("refresh_tree: Restoring selection...")
                if current_selection and selected_text:
                    # Trigger selection event to update properties panel after a short delay
                    def update_properties():
                        try:
                            print("update_properties: Starting...")
                            # Find and select the item again
                            for item in self.fields_tree.get_children():
                                if self.fields_tree.item(item, 'text') == selected_text:
                                    self.fields_tree.selection_set(item)
                                    self.fields_tree.see(item)
                                    if hasattr(self, 'on_select'):
                                        self.on_select()
                                    break
                            print("update_properties: Completed")
                        except Exception as e:
                            print(f"ERROR in update_properties: {e}")
                            import traceback
                            traceback.print_exc()
                    self.window.after(50, update_properties)
                print("refresh_tree: Selection restoration scheduled")
            except Exception as e:
                print(f"ERROR restoring selection: {e}")
                import traceback
                traceback.print_exc()
            print("refresh_tree: Completed successfully")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"CRITICAL ERROR in refresh_tree: {e}")
    
    def select_item_by_text(self, text):
        """Select item in tree by text"""
        for item in self.fields_tree.get_children():
            if self.fields_tree.item(item, 'text') == text:
                self.fields_tree.selection_set(item)
                self.fields_tree.see(item)
                self.on_select()
                break
    
    def import_existing_fields(self):
        """Import predefined fields for this form"""
        try:
            predefined = self.config_manager.get_predefined_fields(self.form_name)
            if not predefined:
                messagebox.showinfo("Info", f"No predefined fields found for {self.form_name}.\n\nYou can add fields manually using the 'Add Field' button.")
                return
            
            # Ask for confirmation if there are existing fields
            if self.config.get('fields') or self.config.get('checkboxes'):
                result = messagebox.askyesno(
                    "Import Fields",
                    f"This will add {len(predefined.get('fields', []))} fields and {len(predefined.get('checkboxes', []))} checkboxes.\n\n"
                    "Existing fields will be preserved.\n\n"
                    "Do you want to continue?"
                )
                if not result:
                    return
            
            # Merge predefined fields with existing config
            existing_field_ids = {f.get('field_id') for f in self.config.get('fields', [])}
            existing_checkbox_ids = {c.get('field_id') for c in self.config.get('checkboxes', [])}
            
            # Add fields that don't already exist
            for field in predefined.get('fields', []):
                if field.get('field_id') not in existing_field_ids:
                    self.config.setdefault('fields', []).append(field)
            
            # Add checkboxes that don't already exist
            for checkbox in predefined.get('checkboxes', []):
                if checkbox.get('field_id') not in existing_checkbox_ids:
                    self.config.setdefault('checkboxes', []).append(checkbox)
            
            # Merge placeholder mappings
            if predefined.get('placeholder_mappings'):
                self.config.setdefault('placeholder_mappings', {}).update(predefined.get('placeholder_mappings', {}))
            
            # Refresh tree to show imported fields
            self.refresh_tree()
            messagebox.showinfo("Success", f"Imported {len(predefined.get('fields', []))} fields and {len(predefined.get('checkboxes', []))} checkboxes.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to import fields: {e}")
    
    def load_config_to_ui(self):
        """Load configuration into UI"""
        try:
            print(f"Loading config to UI for form: {self.form_name}")
            if not hasattr(self, 'fields_tree'):
                print("Warning: fields_tree not found, skipping refresh")
                return
            print("Calling refresh_tree()...")
            self.refresh_tree()
            print("refresh_tree() completed successfully")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"ERROR in load_config_to_ui: {e}")
            # Don't raise, just log the error
            try:
                messagebox.showwarning("Warning", f"Some form data could not be loaded: {e}")
            except:
                pass
    
    def save_form(self):
        """Save form configuration"""
        # Save placeholder mapping if selected
        selection = self.fields_tree.selection()
        if selection:
            item = selection[0]
            item_text = self.fields_tree.item(item, 'text')
            placeholder = self.placeholder_entry.get().strip()
            
            if 'placeholder_mappings' not in self.config:
                self.config['placeholder_mappings'] = {}
            
            if item_text.startswith('Field:'):
                field_label = item_text.replace('Field: ', '')
                for field in self.config['fields']:
                    if field['label'] == field_label:
                        if placeholder:
                            self.config['placeholder_mappings'][field.get('field_id', '')] = placeholder
                        elif field.get('field_id', '') in self.config['placeholder_mappings']:
                            # Remove if empty
                            del self.config['placeholder_mappings'][field.get('field_id', '')]
                        break
            elif item_text.startswith('Checkbox:'):
                checkbox_label = item_text.replace('Checkbox: ', '')
                for checkbox in self.config['checkboxes']:
                    if checkbox['label'] == checkbox_label:
                        if placeholder:
                            self.config['placeholder_mappings'][checkbox.get('field_id', '')] = placeholder
                        elif checkbox.get('field_id', '') in self.config['placeholder_mappings']:
                            # Remove if empty
                            del self.config['placeholder_mappings'][checkbox.get('field_id', '')]
                        break
        
        # Validate for duplicates
        field_ids = [f.get('field_id', '') for f in self.config.get('fields', []) if f.get('field_id')]
        checkbox_ids = [c.get('field_id', '') for c in self.config.get('checkboxes', []) if c.get('field_id')]
        
        duplicates = []
        seen = set()
        for field_id in field_ids + checkbox_ids:
            if field_id in seen:
                duplicates.append(field_id)
            seen.add(field_id)
        
        if duplicates:
            messagebox.showwarning("Warning", 
                                 f"Duplicate Field IDs found: {', '.join(duplicates)}\n\n"
                                 "Please ensure each field has a unique ID.")
            return
        
        self.config['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.config_manager.save_form_config(self.form_name, self.config):
            messagebox.showinfo("Success", f"Form '{self.form_name}' saved successfully!")
            self.refresh_tree()
    
    def preview_form(self):
        """Preview the form"""
        # Create a preview window with the form
        preview_window = tk.Toplevel(self.window)
        preview_window.title(f"Preview - {self.form_name}")
        preview_window.geometry("800x600")
        preview_window.configure(bg='white')
        # Make window appear on top
        preview_window.attributes('-topmost', True)
        preview_window.after_idle(lambda: preview_window.attributes('-topmost', False))
        preview_window.lift()
        preview_window.focus_force()
        
        # Scrollable frame
        canvas = tk.Canvas(preview_window, bg='white')
        scrollbar = ttk.Scrollbar(preview_window, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Generate form from config
        form_generator = DynamicFormGenerator()
        form_generator.generate_form(scrollable_frame, self.config)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class FieldPropertiesDialog:
    """Dialog for editing field properties"""
    
    def __init__(self, parent, field_type='Entry', field_config=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Field Properties")
        self.dialog.geometry("500x650")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 250
        y = (self.dialog.winfo_screenheight() // 2) - 325
        self.dialog.geometry(f'500x650+{x}+{y}')
        # Make window appear on top
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.create_ui(field_type, field_config)
        self.dialog.wait_window()
    
    def create_ui(self, field_type, field_config):
        """Create properties form"""
        # Form fields
        form_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        
        # Field Type
        tk.Label(form_frame, text="Field Type:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        type_combo = ttk.Combobox(form_frame, values=['Entry', 'Text', 'Combobox', 'Date'], state='readonly', width=30)
        type_combo.set(field_type)
        type_combo.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # Label
        tk.Label(form_frame, text="Label:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        label_entry = tk.Entry(form_frame, width=33, font=('Arial', 10))
        if field_config:
            label_entry.insert(0, field_config.get('label', ''))
        label_entry.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # Field ID
        tk.Label(form_frame, text="Field ID:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        id_entry = tk.Entry(form_frame, width=33, font=('Arial', 10))
        if field_config:
            id_entry.insert(0, field_config.get('field_id', ''))
        else:
            id_entry.insert(0, 'entry_')
        id_entry.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # Placeholder
        tk.Label(form_frame, text="Placeholder Text:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        placeholder_entry = tk.Entry(form_frame, width=33, font=('Arial', 10))
        if field_config:
            placeholder_entry.insert(0, field_config.get('placeholder', ''))
        placeholder_entry.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # Default Value
        tk.Label(form_frame, text="Default Value:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        default_entry = tk.Entry(form_frame, width=33, font=('Arial', 10))
        if field_config:
            default_entry.insert(0, field_config.get('default_value', ''))
        default_entry.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # Required
        required_var = tk.BooleanVar()
        if field_config:
            required_var.set(field_config.get('required', False))
        tk.Checkbutton(form_frame, text="Required Field", variable=required_var, bg='white').grid(row=row, column=0, columnspan=2, sticky='w', pady=5)
        row += 1
        
        # Width
        tk.Label(form_frame, text="Width:", font=('Arial', 10, 'bold'), bg='white').grid(row=row, column=0, sticky='w', pady=5)
        width_entry = tk.Entry(form_frame, width=33, font=('Arial', 10))
        if field_config:
            width_entry.insert(0, str(field_config.get('width', 30)))
        else:
            width_entry.insert(0, '30')
        width_entry.grid(row=row, column=1, sticky='ew', pady=5, padx=10)
        row += 1
        
        # For Combobox - Options
        options_frame = tk.LabelFrame(form_frame, text="Options (for Combobox - one per line)", bg='white', padx=10, pady=10)
        options_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=10, padx=10)
        
        options_text = tk.Text(options_frame, width=40, height=5, font=('Arial', 9))
        if field_config and field_config.get('options'):
            options_text.insert('1.0', '\n'.join(field_config['options']))
        options_text.pack(fill=tk.BOTH, expand=True)
        row += 1
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white', pady=15)
        btn_frame.pack(fill=tk.X)
        
        def save():
            if not label_entry.get().strip():
                messagebox.showwarning("Warning", "Label is required")
                return
            
            self.result = {
                'type': type_combo.get(),
                'label': label_entry.get().strip(),
                'field_id': id_entry.get().strip() or f"entry_{label_entry.get().strip().lower().replace(' ', '_')}",
                'placeholder': placeholder_entry.get().strip(),
                'default_value': default_entry.get().strip(),
                'required': required_var.get(),
                'width': int(width_entry.get()) if width_entry.get().isdigit() else 30
            }
            
            if type_combo.get() == 'Combobox':
                options = options_text.get('1.0', tk.END).strip().split('\n')
                self.result['options'] = [opt.strip() for opt in options if opt.strip()]
            
            self.dialog.destroy()
        
        tk.Button(btn_frame, text="Save", bg='#2E7D32', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15, command=save).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15, command=self.dialog.destroy).pack(side=tk.LEFT)


class CheckboxPropertiesDialog:
    """Dialog for editing checkbox properties"""
    
    def __init__(self, parent, checkbox_config=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Checkbox Properties")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 200
        y = (self.dialog.winfo_screenheight() // 2) - 150
        self.dialog.geometry(f'400x300+{x}+{y}')
        # Make window appear on top
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.create_ui(checkbox_config)
        self.dialog.wait_window()
    
    def create_ui(self, checkbox_config):
        form_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label
        tk.Label(form_frame, text="Checkbox Label:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=5)
        label_entry = tk.Entry(form_frame, width=40, font=('Arial', 10))
        if checkbox_config:
            label_entry.insert(0, checkbox_config.get('label', ''))
        label_entry.pack(fill=tk.X, pady=5)
        
        # Field ID
        tk.Label(form_frame, text="Field ID:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w', pady=5)
        id_entry = tk.Entry(form_frame, width=40, font=('Arial', 10))
        if checkbox_config:
            id_entry.insert(0, checkbox_config.get('field_id', ''))
        else:
            id_entry.insert(0, 'var_')
        id_entry.pack(fill=tk.X, pady=5)
        
        # Default checked
        default_var = tk.BooleanVar()
        if checkbox_config:
            default_var.set(checkbox_config.get('default_checked', False))
        tk.Checkbutton(form_frame, text="Checked by default", variable=default_var, bg='white').pack(anchor='w', pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg='white', pady=15)
        btn_frame.pack(fill=tk.X)
        
        def save():
            if not label_entry.get().strip():
                messagebox.showwarning("Warning", "Label is required")
                return
            
            self.result = {
                'label': label_entry.get().strip(),
                'field_id': id_entry.get().strip() or f"var_{label_entry.get().strip().lower().replace(' ', '_')}",
                'default_checked': default_var.get()
            }
            self.dialog.destroy()
        
        tk.Button(btn_frame, text="Save", bg='#2E7D32', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15, command=save).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", bg='#666666', fg='white', relief=tk.FLAT,
                 cursor='hand2', width=15, command=self.dialog.destroy).pack(side=tk.LEFT)

