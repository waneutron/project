# Sistem Integrasi - Gambaran Keseluruhan
## Document Management System for JKDM

---

## 🏗️ ARKITEKTUR SISTEM

### 1. **ENTRY POINT: Main Menu** (`main_Government.py`)
   - **Fungsi**: Menu utama sistem
   - **Ciri-ciri**:
     - 4 modul utama dalam grid layout
     - Logo boleh diklik untuk akses Template Editor (tersembunyi)
     - Butang "Sejarah" untuk melihat semua rekod
     - Window size: 1600x1000 (standardized)
   
   **Modul yang disediakan:**
   1. 📋 Pengurusan Pelupusan & Lain-lain → `Form1_Government.py`
   2. 🗑 Pemadaman Item AMES → `Form_DeleteItem.py`
   3. 📊 Jadual Data AMES → `Form3_Government.py`
   4. 📝 Pendaftaran Sign Up → `Form_SignUp.py`

---

## 📋 ALIRAN DATA DAN INTEGRASI

### 2. **FORM NAVIGATION FLOW**

```
Main Menu (main_Government.py)
    │
    ├─→ Form1 (Form1_Government.py)
    │      │
    │      └─→ Form2 (form2_Government.py) → [Pelupusan forms]
    │
    ├─→ Form3 (Form3_Government.py) → [AMES forms]
    │
    ├─→ Form_SignUp (Form_SignUp.py) → [Sign Up B registration]
    │
    ├─→ Form_DeleteItem (Form_DeleteItem.py) → [Delete AMES items]
    │
    └─→ TemplateEditor (TemplateEditor.py) → [Hidden access via logo click]
```

### 3. **DATABASE INTEGRATION** (`unified_database.py`)

**Centralized Database System:**
- **Database File**: `kastam_documents.db`
- **Main Table**: `applications` (stores all document records)
- **Detail Tables**:
  - `pelupusan_details` - Pelupusan specific data
  - `butiran5d_details` - Butiran 5D specific data
  - `butiran5d_vehicles` - Vehicle data for Butiran 5D
  - `ames_details` - AMES specific data
  - `ames_items` - AMES items/products
  - `signupb_details` - Sign Up B specific data (email, talian)

**Integration Points:**
- Semua forms menggunakan `UnifiedDatabase` class
- Method `save_application()` digunakan untuk menyimpan data
- Auto-increment ID untuk setiap rekod
- Timestamp tracking (created_at, updated_at)

**Example Usage:**
```python
from unified_database import UnifiedDatabase
db = UnifiedDatabase()

# Save application
app_id = db.save_application(
    form_type='pelupusan',
    application_data={...},
    details={...}
)
```

---

### 4. **TEMPLATE SYSTEM INTEGRATION**

**Two-Layer Template System:**

#### Layer 1: Embedded Template Storage (`TemplateEditor.py`)
- Templates disimpan sebagai base64-encoded strings dalam memory
- Metadata tracking (version, category, dates, is_new)
- Auto-loading dari folder `Templates` pada startup
- Categories: APPROVAL, REJECTION, DISPOSAL, REGISTRATION, Delete Item, Lain-lain

#### Layer 2: Template Storage Access (`template_storage.py`)
- Shared access layer untuk semua forms
- Function `get_template_document()` - main access point
- Fallback mechanism:
  1. Try embedded storage (if has content)
  2. Fallback to `Templates/` folder
  3. Auto-import to embedded storage for future use

**Template Loading Flow:**
```
Form needs template
    ↓
get_template_document(template_name)
    ↓
Check embedded storage (has content?)
    ├─ YES → Return Document
    └─ NO → Check Templates/ folder
            ├─ EXISTS → Load + Auto-import → Return Document
            └─ NOT EXISTS → Return None
```

**All Forms Use:**
```python
from template_storage import get_template_document
doc = get_template_document("pelupusan_pemusnahan.docx")
```

---

### 5. **DOCUMENT GENERATION FLOW**

**Standard Process for All Forms:**

1. **User Input** → Form fields filled
2. **Validation** → Required fields checked
3. **Template Loading** → `get_template_document()`
4. **Placeholder Replacement** → `replace_in_document()` from `docx_helper.py`
5. **Document Save** → Save as .docx
6. **PDF Conversion** → Convert to PDF (if docx2pdf available)
7. **Database Save** → `db.save_application()`
8. **Success Message** → Show file paths

**Placeholder Format:**
- Standard: `<<PLACEHOLDER_NAME>>`
- Examples: `<<NAMA_SYARIKAT>>`, `<<TARIKH>>`, `<<ALAMAT>>`

---

### 6. **WINDOW MANAGEMENT SYSTEM**

**Standardized Window Properties:**
- **Size**: 1600x1000 (all windows)
- **Centering**: Auto-center on screen
- **Parent-Child Relationship**:
  - Main Menu → Parent for all forms
  - Forms → Destroy previous, open new
  - Back buttons → Deiconify parent window

**Navigation Pattern:**
```python
# Opening new form
self.root.withdraw()  # Hide current
new_window = tk.Toplevel()
NewForm(new_window, parent_window=self.parent_window)
self.root.destroy()  # Close current

# Going back
if self.parent_window and self.parent_window.winfo_exists():
    self.parent_window.deiconify()
self.root.destroy()
```

---

### 7. **FORM-SPECIFIC INTEGRATIONS**

#### **Form1_Government.py** (Category Selection)
- **Purpose**: Select category and sub-option
- **Integration**:
  - Maps category/sub-option to template file
  - Passes template info to Form2
  - Remembers last selection (JSON persistence)
  - Opens Form2 with parent_window = main menu

#### **form2_Government.py** (Pelupusan Forms)
- **Purpose**: Data entry for Pelupusan documents
- **Integration**:
  - Uses `UnifiedDatabase` to save
  - Uses `template_storage` for templates
  - Generates Word + PDF documents
  - Saves to `pelupusan_details` table

#### **Form3_Government.py** (AMES Forms)
- **Purpose**: Data entry for AMES approval letters
- **Integration**:
  - Uses `UnifiedDatabase` to save
  - Saves to `ames_details` and `ames_items` tables
  - Dynamic table for items/products
  - Generates Word + PDF with table

#### **Form_SignUp.py** (Sign Up B Registration)
- **Purpose**: Sign Up B registration form
- **Integration**:
  - Uses `UnifiedDatabase` to save
  - Saves to `signupb_details` table
  - **NEW**: Checklist system with checkboxes
  - Generates Word + PDF documents

#### **Form_DeleteItem.py** (Delete AMES Items)
- **Purpose**: Delete items from AMES lists
- **Integration**:
  - Uses `UnifiedDatabase` to save
  - Color coding (Green = Added, Red = Deleted)
  - Generates Word + PDF documents

---

### 8. **HISTORY VIEWER** (`UniversalHistoryViewer.py`)

**Features:**
- View all records from all forms
- Filter by form type, date range
- Search functionality
- Open/view generated documents
- Delete records

**Integration:**
- Reads from `applications` table
- Joins with detail tables based on `form_type`
- Displays comprehensive record information

---

### 9. **TEMPLATE EDITOR** (`TemplateEditor.py`)

**Access Method:**
- **Hidden**: Click logo in main menu
- **No visible button** (removed settings button)

**Features:**
- View all templates with status (✓/○)
- Category filtering
- Import/Export templates
- Open in Word for editing
- Copy/Delete templates
- Version tracking
- Auto-loading from Templates folder

**Integration:**
- All forms use templates from this system
- Templates stored in memory (base64)
- Fallback to file system if not in memory

---

## 🔄 DATA FLOW DIAGRAM

```
┌─────────────────┐
│   Main Menu     │
│ (main_Government)│
└────────┬────────┘
         │
         ├─→ Form1 → Form2 → [Generate Doc] → [Save to DB]
         │
         ├─→ Form3 → [Generate Doc] → [Save to DB]
         │
         ├─→ Form_SignUp → [Generate Doc] → [Save to DB]
         │
         ├─→ Form_DeleteItem → [Generate Doc] → [Save to DB]
         │
         └─→ TemplateEditor (hidden)
                │
                └─→ [Manage Templates] → [Used by all forms]
```

---

## 📦 KEY COMPONENTS

### **Core Files:**
1. `main_Government.py` - Entry point
2. `unified_database.py` - Database layer
3. `template_storage.py` - Template access layer
4. `TemplateEditor.py` - Template management
5. `docx_helper.py` - Document manipulation
6. `pdf_utils.py` - PDF conversion utilities

### **Form Files:**
1. `Form1_Government.py` - Category selection
2. `form2_Government.py` - Pelupusan forms
3. `Form3_Government.py` - AMES forms
4. `Form_SignUp.py` - Sign Up B registration
5. `Form_DeleteItem.py` - Delete AMES items

### **Utility Files:**
1. `UniversalHistoryViewer.py` - History viewer
2. `template_mapping.py` - Template mapping logic
3. `template_categories_table.md` - Template categorization

---

## 🔐 SECURITY & ACCESS CONTROL

**Template Editor Access:**
- Hidden from normal users
- Accessible only by clicking logo
- No password required (removed)
- No settings button visible

---

## 📊 DATABASE SCHEMA

**Main Table: `applications`**
- Stores all document records
- Common fields: form_type, rujukan_kami, rujukan_tuan, nama_syarikat, etc.
- Links to detail tables via form_type

**Detail Tables:**
- `pelupusan_details` - proses, jenis_barang, pengecualian, amount, etc.
- `ames_details` - no_kelulusan, kategori, tempoh_kelulusan
- `ames_items` - item details (kod, butiran, unit, etc.)
- `signupb_details` - email, talian
- `butiran5d_details` - scheme-specific data

---

## 🎯 KEY INTEGRATION POINTS

1. **Template System**:
   - All forms → `template_storage.get_template_document()`
   - TemplateEditor → Manages templates
   - Auto-loading from Templates folder

2. **Database System**:
   - All forms → `UnifiedDatabase.save_application()`
   - UniversalHistoryViewer → Reads from database
   - Centralized schema management

3. **Window Management**:
   - Standardized sizes (1600x1000)
   - Parent-child relationships
   - Proper cleanup on close

4. **Document Generation**:
   - Standardized placeholder replacement
   - Word + PDF generation
   - File path tracking in database

---

## 🚀 STARTUP SEQUENCE

1. **Main Menu Opens** (`main_Government.py`)
2. **Template Storage Initializes**:
   - `EmbeddedTemplateStorage` loads default structure
   - Auto-scans `Templates/` folder
   - Loads templates into memory (base64)
3. **Database Initializes**:
   - `UnifiedDatabase` creates tables if not exist
   - Checks schema integrity
4. **User Selects Module**:
   - Opens corresponding form
   - Form loads template when needed
   - Form saves to database on submit

---

## ✅ CURRENT STATUS

**Fully Integrated:**
- ✅ All forms connected to database
- ✅ Template system working (embedded + file system)
- ✅ Window management standardized
- ✅ Document generation working
- ✅ PDF conversion available
- ✅ History viewer functional
- ✅ Template Editor accessible (hidden)
- ✅ Sign Up form with checklist
- ✅ Error handling for .doc files

**System is production-ready!**

