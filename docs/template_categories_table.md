# Template Categories - Quick Lookup Table

## Template Categorization Matrix

| Category | Template ID | Template Name | File Name | Key Fields |
|----------|-------------|---------------|-----------|------------|
| **APPROVAL** | `ames_pedagang` | AMES Trader Approval | SURAT KELULUSAN AMES PEDAGANG.docx | no_siri, butiran, recipient_type |
| **APPROVAL** | `ames_pengilang` | AMES Manufacturer Approval | SURAT KELULUSAN AMES PENGILANG.docx | no_siri, butiran, recipient_type |
| **APPROVAL** | `butiran_5d_lulus` | Item 5D Approval | surat kelulusan butiran 5D (Lulus).docx | no_siri, butiran, scheme_type |
| **APPROVAL** | `pelupusan_jual_skrap` | Disposal Approval | 2 SURAT KELULUSAN PELUPUSAN - JUAL - SKRAP.docx | no_siri, butiran, disposal_method |
| **REJECTION** | `pelupusan_tidak_lulus` | Disposal Rejection | 2 SURAT TIDAK LULUS PELUPUSAN - JUAL - SKRAP.docx | alasan_penolakan, butiran |
| **REJECTION** | `butiran_5d_tidak_lulus` | Item 5D Rejection | surat kelulusan butiran 5D (tidak lulus).docx | alasan_penolakan, butiran |
| **REJECTION** | `pelupusan_tidak_diluluskan` | General Disposal Rejection | TEMPLATE SURAT UKK - PELUPUSAN TIDAK DILULUSKAN.docx | alasan_penolakan, butiran |
| **DISPOSAL** | `pelupusan_jualan` | Disposal by Sale | TEMPLATE SURAT UKK - PELUPUSAN SECARA JUALAN.docx | disposal_method, item_category, regulatory_reference |
| **DISPOSAL** | `pelupusan_pemusnahan` | Disposal by Destruction | TEMPLATE SURAT UKK - PELUPUSAN SECARA PEMUSNAHAN.docx | disposal_method, item_category, regulatory_reference |
| **DISPOSAL** | `pelupusan_scrap` | Disposal by Scrap | TEMPLATE SURAT UKK - PELUPUSAN SECARA SCRAP.docx | disposal_method, item_category, regulatory_reference |
| **REGISTRATION** | `sign_up_b` | Sign Up Schedule B | TEMPLATE SURAT UKK - SIGN UP B.docx | business_name, business_address, schedule_type |

---

## Field Requirements by Category

### ✅ All Categories (100%)
```
rujukan_tuan    [Text]     Required
rujukan_kami    [Text]     Required
tarikh          [Date]     Required (dual calendar)
```

### 📝 Approval Letters
```
+ nama_pemohon      [Text]     Required
+ alamat_pemohon    [Textarea] Required
+ salutation        [Select]   Optional (default: Tuan)
+ no_siri           [Text]     Required
+ butiran           [Textarea] Required
+ kelulusan_status  [Select]   Required (default: Lulus)
+ scheme_type       [Select]   Conditional (AMES/Butiran 5D)
+ recipient_type    [Select]   Conditional (Pedagang/Pengilang)
+ conditions        [Textarea] Optional
```

### ❌ Rejection Letters
```
+ nama_pemohon          [Text]     Required
+ alamat_pemohon        [Textarea] Required
+ salutation            [Select]   Optional (default: Tuan)
+ alasan_penolakan      [Textarea] Required
+ butiran               [Textarea] Required
+ rujukan_surat_pemohon [Text]     Optional
```

### 🗑️ Disposal Letters
```
+ nama_pemohon          [Text]     Required
+ alamat_pemohon        [Textarea] Required
+ salutation            [Select]   Optional (default: Tuan)
+ disposal_method       [Select]   Required (jualan/pemusnahan/scrap)
+ item_category         [Multi]    Required (multiple selection)
+ regulatory_reference  [Multi]    Required (multiple selection)
+ butiran_barang        [Textarea] Required
+ quantity              [Text]     Optional
+ value                 [Number]   Optional
```

### 📋 Registration Letters
```
+ business_name      [Text]     Required
+ business_address   [Textarea] Required
+ schedule_type      [Select]   Required (default: Jadual B)
+ registration_number [Text]    Optional
+ salutation         [Select]   Optional
```

---

## Placeholder Mapping

| Template Placeholder | Form Field ID | Type | Required |
|---------------------|---------------|------|----------|
| `< Nama pemohon >` | `nama_pemohon` | Text | ✅ |
| `< Alamat pemohon >` | `alamat_pemohon` | Textarea | ✅ |
| `MERGEFIELD Business_name` | `business_name` | Text | ✅ |
| `MERGEFIELD ALAMAT` | `business_address` | Textarea | ✅ |
| `Ruj. Tuan` | `rujukan_tuan` | Text | ✅ |
| `Ruj. Kami` | `rujukan_kami` | Text | ✅ |
| `Tarikh` | `tarikh` | Date | ✅ |

---

## Category Selection Logic

```javascript
// Pseudo-code for category selection
if (category === "approval") {
  showFields([
    "nama_pemohon", "alamat_pemohon", "salutation",
    "no_siri", "butiran", "kelulusan_status"
  ]);
  
  if (template === "ames_pedagang" || template === "ames_pengilang") {
    showField("recipient_type"); // Pedagang or Pengilang
    showField("scheme_type"); // AMES
  }
  
  if (template === "butiran_5d_lulus") {
    showField("scheme_type"); // Butiran 5D
  }
}

if (category === "rejection") {
  showFields([
    "nama_pemohon", "alamat_pemohon", "salutation",
    "alasan_penolakan", "butiran"
  ]);
}

if (category === "disposal") {
  showFields([
    "nama_pemohon", "alamat_pemohon", "salutation",
    "disposal_method", "item_category", "regulatory_reference",
    "butiran_barang"
  ]);
  
  // Show method-specific options
  if (disposal_method === "jualan") {
    // Additional fields for sale
  }
}

if (category === "registration") {
  showFields([
    "business_name", "business_address", "schedule_type"
  ]);
}
```

---

## Quick Field Checklist

### For Approval Letters:
- [ ] rujukan_tuan
- [ ] rujukan_kami
- [ ] tarikh
- [ ] nama_pemohon
- [ ] alamat_pemohon
- [ ] salutation
- [ ] no_siri
- [ ] butiran
- [ ] kelulusan_status
- [ ] scheme_type (if AMES/5D)
- [ ] recipient_type (if AMES)

### For Rejection Letters:
- [ ] rujukan_tuan
- [ ] rujukan_kami
- [ ] tarikh
- [ ] nama_pemohon
- [ ] alamat_pemohon
- [ ] salutation
- [ ] alasan_penolakan
- [ ] butiran

### For Disposal Letters:
- [ ] rujukan_tuan
- [ ] rujukan_kami
- [ ] tarikh
- [ ] nama_pemohon
- [ ] alamat_pemohon
- [ ] salutation
- [ ] disposal_method
- [ ] item_category (at least one)
- [ ] regulatory_reference (at least one)
- [ ] butiran_barang

### For Registration Letters:
- [ ] rujukan_tuan
- [ ] rujukan_kami
- [ ] tarikh
- [ ] business_name
- [ ] business_address
- [ ] schedule_type

