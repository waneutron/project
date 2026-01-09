# Form3 `<<table>>` Placeholder Guide

## Overview

Form3 (AMES System) now supports `<<table>>` placeholder replacement in Word templates. When you add a `<<table>>` placeholder in your template document, it will be automatically replaced with the corresponding data table based on the selected category.

## How It Works

### 1. **Template Placeholder**
Add `<<table>>` anywhere in your Word template where you want the table to be inserted:
```
Sila rujuk jadual di bawah:

<<table>>

Terima kasih
```

### 2. **Category-Based Replacement**
When the document is generated, the placeholder is replaced based on the selected category:

#### **Pedagang** (Merchant)
- Replaced with: Barang-barang yang diluluskan table
- Columns: BIL, KOD TARIF, DESKRIPSI, TARIKH KUATKUASA
- Source: `table_pedagang` from Form3 UI

#### **Pengilang** (Manufacturer)
- Replaced with: TWO tables
  1. A. Bahan Mentah, Komponen, Bahan Bungkusan (5 columns)
  2. B. Barang Siap yang Dikilangkan (4 columns)
- Source: `table_bahan` and `table_barang` from Form3 UI

#### **Butiran 5D** (Vehicles)
- Replaced with: Senarai Kenderaan table
- Columns: NO CHASIS, NO ENJIN
- Source: `table_vehicles` from Form3 UI

### 3. **Example Template Setup**

**Before (Template):**
```
AMES - PERMOHONAN SKIM PENGEKSPORT UTAMA

Nama Syarikat: <<NAMA_SYARIKAT>>
Alamat: <<ALAMAT>>
Tarikh: <<TARIKH>>

Senarai barang-barang yang diluluskan:

<<table>>

Nama Pegawai: <<NAMA_PEGAWAI>>
```

**After (Generated Document):**
```
AMES - PERMOHONAN SKIM PENGEKSPORT UTAMA

Nama Syarikat: ABC Sdn Bhd
Alamat: No 1, Jalan Merdeka, KL
Tarikh: 01/01/2024

Senarai barang-barang yang diluluskan:

[TABLE DATA INSERTED HERE WITH ACTUAL ROWS]

Nama Pegawai: HABBAH SYAKIRAH
```

## Key Features

✅ **Multiple Placeholders**: Each template can have ONE `<<table>>` placeholder  
✅ **Category-Aware**: Automatically uses correct table structure for selected category  
✅ **Empty Tables Handled**: If no rows in table, empty table with headers is inserted  
✅ **Automatic Formatting**: Tables use Arial 10pt font with bold headers  
✅ **Centered Headers**: Column headers are center-aligned  

## Implementation Details

### Methods Used

1. **`replace_table_placeholders(doc, kategori)`**
   - Main handler that finds and replaces `<<table>>` placeholders
   - Supports case-insensitive matching (<<table>>, <<TABLE>>, <<Table>>)
   - Calls data extraction methods based on category

2. **Data Extraction Methods**
   - `get_pedagang_table_data()` - Returns pedagang table rows
   - `get_bahan_table_data()` - Returns bahan table rows
   - `get_barang_table_data()` - Returns barang table rows
   - `get_vehicles_table_data()` - Returns vehicles table rows

3. **`_insert_table_at_index(doc, index, title, table_data, headers)`**
   - Helper method to insert table at specific document position
   - Handles title paragraph insertion for Pengilang (2 tables)
   - Applies formatting: Arial 10pt, bold headers, centered alignment

### Integration Flow

```
generate_document()
    ↓
[1] Build replacement dict with PlaceholderBuilder
[2] Replace text placeholders via replace_in_document()
[3] Call replace_table_placeholders(doc, kategori)
    ↓
    ├─ Pedagang: Insert 1 table
    ├─ Pengilang: Insert 2 tables (Bahan + Barang)
    └─ Butiran 5D: Insert vehicles table
```

## Usage Scenario

### Step 1: Create Template
1. Open your Word template file (e.g., `ames_pedagang.docx`)
2. Position cursor where you want the table
3. Type: `<<table>>`

### Step 2: Use Form3
1. Fill in all form fields (Rujukan, Nama Syarikat, etc.)
2. Select category (Pedagang/Pengilang/Butiran 5D)
3. Add rows to the corresponding table in the UI
4. Click "SIMPAN DOKUMEN"

### Step 3: Result
- Document is generated with `<<table>>` replaced by actual data
- All other placeholders are also replaced
- PDF is created with fully populated document

## Troubleshooting

### Table Not Appearing
- Check that `<<table>>` is exactly spelled (case-insensitive OK)
- Ensure the form's data table has at least one row
- Verify template path is correct in `get_template_path()`

### Table in Wrong Location
- `<<table>>` replaces the entire paragraph it's in
- Ensure `<<table>>` is on its own paragraph (not mixed with other text)

### Multiple Tables Issue
- Only **one** `<<table>>` placeholder per template is supported
- For Pengilang, the single `<<table>>` is replaced with both tables automatically

## Related Files

- `modules/Form3_Government_PySide2.py` - Main implementation
- `helpers/placeholder_registry.py` - Placeholder registry
- `helpers/docx_helper.py` - Text replacement utilities
- `Templates/ames_pedagang.docx` - Template example
- `Templates/ames_pengilang.docx` - Template example
- `Templates/surat kelulusan butiran 5D (Lulus).docx` - Template example
