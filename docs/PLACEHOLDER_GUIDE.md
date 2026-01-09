# Placeholder Naming Guide

## Standard Placeholder Names

Semua placeholder dalam sistem ini menggunakan nama standard untuk memastikan konsistensi dan kemudahan pengurusan.

### Basic Information Placeholders

| Placeholder | Description | Example Value |
|------------|-------------|---------------|
| `<<RUJUKAN>>` | Rujukan standard (Form2) | `KE.JB(90)650/05-02/1234` |
| `<<RUJUKAN_KAMI>>` | Rujukan kami (AMES) | `KE.JB(90)650/14/AMES/1234` |
| `<<RUJUKAN_TUAN>>` | Rujukan syarikat/tuan | `REF/2025/001` |
| `<<NAMA_SYARIKAT>>` | Nama syarikat (uppercase) | `ABC SDN BHD` |
| `<<ALAMAT>>` | Alamat (3 baris digabungkan) | `123 Jalan ABC\nTaman XYZ\n12345 Kuala Lumpur` |
| `<<TARIKH>>` | Tarikh (DD/MM/YYYY) | `17/12/2025` |
| `<<TARIKH2>>` | Tarikh format Melayu | `17 Disember 2025` |
| `<<TARIKH_MALAY>>` | Tarikh format Melayu (alias) | `17 Disember 2025` |
| `<<TARIKH_ISLAM>>` | Tarikh Islam | `17 Rabiulawal 1447H` |
| `<<NAMA_PEGAWAI>>` | Nama pegawai (uppercase) | `AHMAD BIN ABU` |

### AMES Specific Placeholders

| Placeholder | Description | Example Value |
|------------|-------------|---------------|
| `<<NO_KELULUSAN>>` | Nombor kelulusan AMES | `AMES-2025-001` |
| `<<KATEGORI>>` | Kategori (Pedagang/Pengilang) | `Pedagang` |
| `<<TEMPOH_KELULUSAN>>` | Tempoh kelulusan | `01 April 2025 hingga 31 Mac 2027` |

### Pelupusan Specific Placeholders

| Placeholder | Description | Example Value |
|------------|-------------|---------------|
| `<<PROSES>>` | Proses (pemusnahan/penjualan/skrap) | `pemusnahan` |
| `<<JENIS_BARANG>>` | Jenis barang | `Barang Terpakai` |
| `<<PENGECUALIAN>>` | Pengecualian | `Butiran 5D` |
| `<<AMOUNT>>` | Amaun dalam RM | `1234.56` |
| `<<JENIS_TEMPLATE>>` | Jenis template (SST-ADM/AMES-03) | `SST-ADM` |
| `<<STATUS>>` | Status (SST-ADM/AMES-03) | `SST-ADM` |
| `<<TARIKH_MULA>>` | Tarikh mula pemusnahan | `01 Januari 2025` |
| `<<TARIKH_TAMAT>>` | Tarikh tamat pemusnahan | `31 Januari 2025` |
| `<<TEMPOH>>` | Tempoh pemusnahan (perkataan) | `tiga puluh hari` |
| `<<TAJUK_SURAT>>` | Tajuk surat (uppercase, bold) | `PELUPUSAN SECARA PEMUSNAHAN...` |
| `<<TAJUK_SURAT2>>` | Tajuk surat (lowercase) | `pelupusan secara pemusnahan...` |
| `<<RUJUKAN_INFO>>` | Maklumat rujukan tambahan | `rujukan REF/2025/001 ` |

### Sign Up Specific Placeholders

| Placeholder | Description | Example Value |
|------------|-------------|---------------|
| `<<BUSINESS_NAME>>` | Nama perniagaan (alias untuk NAMA_SYARIKAT) | `ABC ENTERPRISE` |
| `<<BUSINESS_ADDRESS>>` | Alamat perniagaan (alias untuk ALAMAT) | `123 Jalan ABC...` |
| `<<SCHEDULE_TYPE>>` | Jenis jadual | `Jadual A` |
| `<<REGISTRATION_NUMBER>>` | Nombor pendaftaran | `REG-123456` |
| `<<SALUTATION>>` | Salutation | `Encik` |
| `<<SENARAI_SEMAK>>` | Senarai semak | `✓ Item 1\n✓ Item 2` |
| `<<CHECKLIST>>` | Checklist (alias untuk SENARAI_SEMAK) | `✓ Item 1\n✓ Item 2` |

### Table Placeholders

| Placeholder | Description | Usage |
|------------|-------------|-------|
| `<<LAMPIRAN_A_TABLE>>` | Table untuk AMES Lampiran A | Digunakan dalam Form3 |
| `<<LAMPIRAN_A>>` | Alternative table name | Digunakan dalam Form3 |
| `<<TARIKH_KUATKUASA>>` | Tarikh kuatkuasa untuk table items | Digunakan dalam Form3 tables |

## Placeholder Aliases

Sistem menyokong alias untuk backward compatibility:

- `<<RUJUKAN>>` = `<<RUJUKAN_KAMI>>` (Form2 vs Form3)
- `<<TARIKH2>>` = `<<TARIKH_MALAY>>` (Form2 vs Form3)
- `<<NAMA_SYARIKAT>>` = `<<BUSINESS_NAME>>` (Standard vs Sign Up)
- `<<ALAMAT>>` = `<<BUSINESS_ADDRESS>>` (Standard vs Sign Up)

## Using PlaceholderBuilder

Untuk memudahkan penggunaan, gunakan `PlaceholderBuilder`:

```python
from helpers.placeholder_registry import PlaceholderBuilder

builder = PlaceholderBuilder(form_instance)
builder.add_rujukan("1234", "KE.JB(90)650/05-02/")
builder.add_rujukan_ames("1234")
builder.add_nama_syarikat("ABC Sdn Bhd")
builder.add_alamat(["Line 1", "Line 2", "Line 3"])
builder.add_tarikh("17/12/2025")
builder.add_tarikh_malay("17 Disember 2025")
builder.add_tarikh_islam("17 Rabiulawal 1447H")
builder.add_nama_pegawai("Ahmad Bin Abu")
builder.add_standard('NO_KELULUSAN', 'AMES-2025-001')
builder.add_extra_placeholders(extra_placeholders_dict)

replacements = builder.build()
```

## Benefits

1. **Consistency**: Semua forms menggunakan nama placeholder yang sama
2. **Easy Management**: Centralized registry untuk semua placeholder
3. **Backward Compatibility**: Alias support untuk template lama
4. **Future Proof**: Mudah tambah placeholder baru tanpa ubah banyak code
5. **Type Safety**: Helper methods untuk common placeholders

## Adding New Placeholders

1. Tambah ke `PlaceholderRegistry.STANDARD_PLACEHOLDERS`
2. Tambah description ke `get_placeholder_description()`
3. Jika perlu alias, tambah ke `PlaceholderRegistry.ALIASES`
4. Semua forms akan automatik support placeholder baru!

