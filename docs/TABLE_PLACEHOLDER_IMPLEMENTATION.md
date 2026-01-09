# Form3 `<<table>>` Placeholder Implementation - Complete ✓

## Status: Working

All `<<table>>` placeholders are now properly handled in Form3 (AMES System).

### Template Status
✅ **ames_pedagang.docx** - Contains 1 `<<table>>` placeholder
✅ **ames_pengilang.docx** - Contains 1 `<<table>>` placeholder  
⚠️ **surat kelulusan butiran 5D (Lulus).docx** - No `<<table>>` placeholder (uses default behavior)

---

## Implementation Details

### New Methods in Form3

#### 1. `replace_table_placeholders(doc, kategori)`
**Purpose:** Main handler for `<<table>>` placeholder replacement

**Process:**
- Finds all `<<table>>` placeholders (case-insensitive)
- Processes in reverse order to preserve document indices
- Replaces based on category:
  - **Pedagang**: Single product table
  - **Pengilang**: Two tables (Bahan + Barang)
  - **Butiran 5D**: Vehicles table

#### 2. `_insert_table_after_element(parent, ref_element, title, table_data, headers)`
**Purpose:** Insert table into document XML at specific location

**Features:**
- Direct XML manipulation (more reliable than index-based insertion)
- Supports optional title paragraph
- Creates formatted table with:
  - Bold, centered headers
  - Proper table grid structure
  - Multiple data rows

#### 3. Data Extraction Methods
```python
get_pedagang_table_data()    # Returns pedagang table as list of lists
get_bahan_table_data()       # Returns bahan table as list of lists
get_barang_table_data()      # Returns barang table as list of lists
get_vehicles_table_data()    # Returns vehicles table as list of lists
```

---

## How It Works

### Step 1: User Creates Template
```
Nama: <<NAMA_SYARIKAT>>
Tarikh: <<TARIKH>>

Senarai Barang:

<<table>>

Pegawai: <<NAMA_PEGAWAI>>
```

### Step 2: User Fills Form3
- Enters company details
- Selects category (Pedagang/Pengilang/Butiran 5D)
- Adds rows to appropriate table

### Step 3: Generate Document
```python
generate_document():
    1. Load template
    2. Replace text placeholders (<<NAMA_SYARIKAT>>, etc.)
    3. Call replace_table_placeholders()
       - Find <<table>> placeholder
       - Remove placeholder paragraph
       - Insert actual data table (with formatting)
    4. Return populated document
```

### Step 4: Save as PDF
- Document is exported as PDF with table data

---

## Bug Fix

### Previous Error
```
ValueError: list.index(x): x not in list
```

**Cause:** Attempted to find paragraph index after removing it from document

**Solution:** 
- Changed to process placeholders in reverse order
- Use direct XML parent/element manipulation instead of index-based insertion
- Eliminated need to reference document.paragraphs after modification

---

## Placeholder Categories

### Pedagang (Merchant)
| Column | Source |
|--------|--------|
| BIL. | Row number |
| KOD TARIF | Code field |
| DESKRIPSI | Description field |
| TARIKH KUATKUASA | Effective date |

### Pengilang (Manufacturer)
**Table A: Bahan Mentah (Raw Materials)**
| BIL. | KOD TARIF | DESKRIPSI | NISBAH | TARIKH KUATKUASA |
|------|-----------|-----------|--------|-----------------|

**Table B: Barang Siap (Finished Goods)**
| BIL. | KOD TARIF | DESKRIPSI | TARIKH KUATKUASA |
|------|-----------|-----------|-----------------|

### Butiran 5D (Vehicles)
| NO CHASIS | NO ENJIN |
|-----------|----------|

---

## Testing

Run verification script:
```bash
python verify_table_placeholders.py
```

Expected output:
```
✓ Pedagang        | Found 1 <<table>> placeholder(s)
✓ Pengilang       | Found 1 <<table>> placeholder(s)
- Butiran 5D      | No <<table>> placeholders (will use default behavior)
```

---

## Files Modified

- ✅ `modules/Form3_Government_PySide2.py`
  - Modified `generate_document()` to call `replace_table_placeholders()`
  - Added `replace_table_placeholders()` method
  - Added `_insert_table_after_element()` helper
  - Added data extraction methods (get_*_table_data)

## Files Created

- ✅ `docs/FORM3_TABLE_PLACEHOLDER_GUIDE.md` - User guide
- ✅ `verify_table_placeholders.py` - Verification script
- ✅ `test_table_placeholder.py` - Test suite

---

## Key Features

✅ **Case-Insensitive** - Accepts `<<table>>`, `<<TABLE>>`, `<<Table>>`
✅ **Category-Aware** - Uses correct table structure per category
✅ **Error Handling** - Gracefully handles empty tables
✅ **XML-Direct** - Reliable insertion without index manipulation
✅ **Formatted Output** - Professional table formatting
✅ **Multiple Tables** - Pengilang automatically gets 2 tables from 1 placeholder

---

## Next Steps (Optional)

1. Add table styling (colors, borders)
2. Support multiple `<<table>>` placeholders (for advanced templates)
3. Add `<<subtable>>` for nested structures
4. Template preview before generation

---

## Conclusion

The `<<table>>` placeholder feature is fully functional and tested. Users can now:
- Add `<<table>>` to any Form3 template
- Generated documents will automatically replace it with populated data tables
- Supports all three categories (Pedagang, Pengilang, Butiran 5D)
