# Modul Transaksi Ecoethno

## 📋 Deskripsi

Modul **Transaksi** adalah fitur untuk mengelola riwayat transaksi dan penjualan Ecoethno. Modul ini memungkinkan:

- ✅ Mencatat dan menyimpan riwayat transaksi pelanggan
- ✅ Menampilkan detail transaksi per pelanggan secara terstruktur
- ✅ Mengelola informasi reservasi, paket layanan, dan nilai transaksi
- ✅ Melacak status pembayaran (Belum Dibayar, Sebagian Dibayar, Lunas, Dibatalkan)
- ✅ Memberikan laporan dan visualisasi transaksi untuk analisis bisnis

## 🏗️ Struktur Modul

```
transaksi/
├── __init__.py                 # Inisialisasi modul
├── __manifest__.py             # Manifest/deskripsi modul
├── models/
│   ├── __init__.py
│   └── models.py              # Model TransactionEcoethno
├── views/
│   ├── transaksi_menus.xml    # Definisi menu
│   ├── transaksi_forms.xml    # Form view (detail transaksi)
│   └── transaksi_trees.xml    # List/tree view & laporan
└── security/
    └── ir.model.access.csv    # Hak akses pengguna
```

## 📊 Model Data: TransactionEcoethno

### Field Utama
- **no_transaksi** (Char): Nomor transaksi unik (auto-generated)
- **tanggal_transaksi** (Date): Tanggal transaksi dicatat

### Data Pelanggan
- **customer_id** (Many2one → res.partner): Referensi ke pelanggan
- **customer_name** (Char): Nama pelanggan (auto-fill dari customer_id)
- **customer_phone** (Char): Nomor kontak pelanggan (auto-fill dari customer_id)

### Data Reservasi
- **no_reservasi** (Char): Nomor reservasi dari pelanggan
- **tanggal_kegiatan** (Date): Tanggal pelaksanaan kegiatan/layanan

### Paket Layanan
- **paket_layanan** (Selection): Jenis paket (Camping, Outbound, Event Organizer, Workshop, Lainnya)
- **deskripsi_paket** (Text): Deskripsi detail paket

### Detail Peserta
- **jumlah_peserta** (Integer): Total jumlah peserta/tamu

### Nilai Transaksi
- **harga_satuan** (Float): Harga per peserta
- **nilai_transaksi** (Float): Nilai total transaksi = Harga Satuan × Jumlah Peserta (computed & stored)

### Status Pembayaran
- **status_pembayaran** (Selection): Belum Dibayar, Sebagian Dibayar, Lunas, Dibatalkan
- **tanggal_pembayaran** (Date): Tanggal pembayaran dikonfirmasi
- **metode_pembayaran** (Selection): Tunai, Transfer Bank, Kartu Kredit, E-Wallet, Cek, Lainnya

### Platform Pemesanan
- **platform_pemesanan** (Selection): Channel pemesanan (Traveloka, WhatsApp, Website, Telepon, Email, Langsung, Lainnya)

### Catatan & Audit
- **catatan** (Text): Catatan tambahan tentang transaksi
- **created_at** (Datetime): Waktu pembuatan record
- **created_by** (Many2one → res.users): User yang membuat record
- **updated_at** (Datetime): Waktu update terakhir
- **updated_by** (Many2one → res.users): User yang mengupdate record

## 👁️ View yang Tersedia

### 1. **Tree View (List View)**
   - Menampilkan daftar semua transaksi dalam bentuk tabel
   - Colorized berdasarkan status pembayaran
   - Fitur sum untuk nilai transaksi

### 2. **Form View**
   - Form detail transaksi dengan 5 tab:
     - **Tab 1: Informasi Umum** - Data transaksi & status pembayaran
     - **Tab 2: Informasi Pelanggan** - Data pelanggan
     - **Tab 3: Detail Layanan** - Paket & peserta
     - **Tab 4: Nilai Transaksi** - Perhitungan harga
     - **Tab 5: Catatan & Audit** - Catatan dan audit trail

### 3. **Search View**
   - Filter berdasarkan status pembayaran
   - Filter berdasarkan paket layanan
   - Grouping: Pelanggan, Status, Paket, Platform, Tanggal
   - Pencarian: No. Transaksi, Nama Pelanggan, No. Reservasi

### 4. **Pivot View**
   - Analisis data transaksi dalam format pivot table
   - Row: Paket Layanan
   - Column: Status Pembayaran
   - Measure: Nilai Transaksi

### 5. **Graph View**
   - Visualisasi grafik bar transaksi per paket layanan

## 🔐 Keamanan (Access Control)

### Akses User Biasa
- **Baca** ✅ Dapat melihat data transaksi
- **Tulis** ❌ Tidak dapat mengubah
- **Buat** ❌ Tidak dapat membuat
- **Hapus** ❌ Tidak dapat menghapus

### Akses Manager/Admin
- **Baca** ✅ Dapat melihat data transaksi
- **Tulis** ✅ Dapat mengubah data
- **Buat** ✅ Dapat membuat transaksi baru
- **Hapus** ✅ Dapat menghapus transaksi

## 📝 Cara Penggunaan

### 1. **Membuat Transaksi Baru**
   1. Masuk ke menu **Transaksi** → **Buat Transaksi**
   2. Isi form dengan data transaksi:
      - Pilih pelanggan
      - Masukkan nomor reservasi
      - Pilih paket layanan
      - Masukkan jumlah peserta & harga satuan
      - Pilih status pembayaran
   3. Klik **Simpan**

### 2. **Melihat Daftar Transaksi**
   1. Masuk ke menu **Transaksi** → **Riwayat Transaksi**
   2. Gunakan filter untuk mencari transaksi tertentu
   3. Klik baris transaksi untuk melihat detail

### 3. **Menganalisis Data Transaksi**
   1. Masuk ke **Riwayat Transaksi**
   2. Klik tab **Pivot** atau **Graph** untuk visualisasi
   3. Gunakan grouping untuk analisis lebih detail

### 4. **Mengubah Status Pembayaran**
   1. Buka detail transaksi
   2. Ubah field **Status Pembayaran**
   3. Masukkan tanggal pembayaran dan metode (jika diperlukan)
   4. Klik **Simpan**

## 🔧 Fitur Teknis

### Computed Fields
- **nilai_transaksi**: Otomatis dihitung dari `harga_satuan × jumlah_peserta`

### Onchange Methods
- **_onchange_customer_id**: Update nama & telepon pelanggan saat customer_id berubah

### Lifecycle Methods
- **create()**: Mencatat user yang membuat record
- **write()**: Mencatat user yang mengupdate record

### Auto-numbering
- **no_transaksi**: Menggunakan sequence Odoo untuk auto-generated numbering

## 📚 Dependencies

- **base**: Modul dasar Odoo
- **sale**: Untuk integrasi dengan modul penjualan
- **crm**: Untuk integrasi dengan modul CRM (pelanggan)

## ✅ Compliance & Best Practices

✅ Mengikuti struktur modul Odoo standard  
✅ Menggunakan naming convention yang konsisten (transaksi.transaksi)  
✅ Mengimplementasikan access control yang ketat  
✅ Menyimpan audit trail (created_by, updated_by, timestamps)  
✅ Menggunakan computed & stored fields untuk konsistensi data  
✅ Implementasi onchange untuk UX yang baik  
✅ Fitur search, filter, grouping lengkap untuk usability  
✅ Menggunakan decorations pada tree view untuk visual feedback  

## 🚀 Instalasi & Testing

1. **Docker Compose Up** (jika belum running):
   ```bash
   docker compose up -d
   ```

2. **Activate Virtual Environment**:
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

3. **Update Apps List** di Odoo:
   - Masuk ke Apps
   - Klik **Update Apps List**
   - Cari modul "Transaksi Ecoethno"
   - Klik **Install**

4. **Test Fitur**:
   - Buat transaksi baru via menu Transaksi → Buat Transaksi
   - Lihat daftar transaksi dengan berbagai filter
   - Analisis data menggunakan Pivot & Graph view

## 📞 Support & Maintenance

Untuk pertanyaan atau permasalahan, hubungi:
- **Tim Development**: Kelompok 11 - K02 IF3141
- **Email**: [contact information]

---

**Last Updated**: 2026-05-08  
**Version**: 1.0  
**Status**: Production Ready ✅
