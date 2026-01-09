# Template Categorization Summary

## Overview
This document summarizes how templates are categorized and used across all forms, based on `template_categories_table.md`.

## Template Categories

### ✅ APPROVAL Templates
Templates for approval letters (Surat Kelulusan):
- **ames_pedagang.docx** - Used by `Form3_Government.py` (AMES Trader)
- **ames_pengilang.docx** - Used by `Form3_Government.py` (AMES Manufacturer)
- **surat kelulusan butiran 5D (Lulus).docx** - Used by `Form1_Government.py` (Butiran 5D)
- **pelupusan_penjualan.docx** - Used by `Form1_Government.py` (Disposal by Sale - Approval)
- **pelupusan_skrap.docx** - Used by `Form1_Government.py` (Disposal by Scrap - Approval)

### ❌ REJECTION Templates
Templates for rejection letters (Surat Tidak Lulus):
- **pelupusan_tidak_lulus.docx** - Used by `Form1_Government.py` (Disposal Rejection)
- **surat kelulusan butiran 5D (tidak lulus).docx** - Used by `Form1_Government.py` (Butiran 5D Rejection)

### 🗑️ DISPOSAL Templates
Templates for disposal letters (Surat Pelupusan):
- **pelupusan_pemusnahan.docx** - Used by `Form1_Government.py` (Disposal by Destruction)
- **pelupusan_penjualan.docx** - Used by `Form1_Government.py` (Disposal by Sale)
- **pelupusan_skrap.docx** - Used by `Form1_Government.py` (Disposal by Scrap)

### 📋 REGISTRATION Templates
Templates for registration letters (Surat Pendaftaran):
- **signUpB.docx** - Used by `Form1_Government.py` (Sign Up Schedule B)

### 🗂️ Delete Item Templates
Templates for item deletion:
- **delete_item_ames.docx** - Used by `Form_DeleteItem.py` (Delete Item AMES - New Format)
- **delete_item.doc** - Used by `Form_DeleteItem.py` (Delete Item - Old Format)

### 📄 Other Templates
Miscellaneous templates:
- **batal_sijil.doc** - Used by `Form1_Government.py` (Certificate Cancellation)

## Form-to-Template Mapping

### Form1_Government.py
**Category: Pelupusan**
- `pemusnahan` → `pelupusan_pemusnahan.docx` (DISPOSAL)
- `penjualan` → `pelupusan_penjualan.docx` (DISPOSAL/APPROVAL)
- `skrap` → `pelupusan_skrap.docx` (DISPOSAL/APPROVAL)
- `tidak_lulus` → `pelupusan_tidak_lulus.docx` (REJECTION)

**Category: Lain-lain**
- `signUpB` → `signUpB.docx` (REGISTRATION)
- `batal_sijil` → `batal_sijil.doc` (Other)
- `butiran_5d_lulus` → `surat kelulusan butiran 5D (Lulus).docx` (APPROVAL)
- `butiran_5d_tidak_lulus` → `surat kelulusan butiran 5D (tidak lulus).docx` (REJECTION)

### Form3_Government.py
**AMES Templates** (APPROVAL):
- `ames_pedagang.docx` - For Trader category
- `ames_pengilang.docx` - For Manufacturer category

### Form_DeleteItem.py
**Delete Item Templates**:
- `delete_item_ames.docx` - Primary template (New Format)
- `delete_item.doc` - Fallback template (Old Format)

## Template Storage

All templates are managed through:
- **TemplateEditor.py** - Embedded template storage with base64 encoding
- **template_storage.py** - Centralized template access for all forms
- **template_mapping.py** - Template name mapping and categorization helper

## Notes

1. **Dual Category Templates**: Some templates like `pelupusan_penjualan.docx` and `pelupusan_skrap.docx` can be both APPROVAL and DISPOSAL depending on context.

2. **Template Access**: All forms use `template_storage.get_template_document()` which:
   - First checks embedded storage (TemplateEditor)
   - Falls back to file system (`Templates/` directory)
   - Returns `None` if template not found

3. **Category Filtering**: TemplateEditor allows filtering by:
   - APPROVAL
   - REJECTION
   - DISPOSAL
   - REGISTRATION
   - Delete Item
   - Lain-lain
   - 🆕 Baru Sahaja (New templates only)

4. **Template Naming**: Template file names match actual files in the `Templates/` directory, ensuring compatibility with both embedded and file-based storage.

## Updates Made

1. ✅ Updated `Form1_Government.py` to include `skrap` option and Butiran 5D templates
2. ✅ Updated `TemplateEditor.py` categorization to match `template_categories_table.md`
3. ✅ Created `template_mapping.py` for centralized template name mapping
4. ✅ Verified all forms use correct template names
5. ✅ Updated help documentation in TemplateEditor with new categorization

