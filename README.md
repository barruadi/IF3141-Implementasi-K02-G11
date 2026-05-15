# Sistem Informasi Manajemen Terintegrasi Ecoethno
> Disusun oleh: K02 - G11
- Muhammad Ghifary Komara Putra (13523066)
- Anella Utari Gunadi (13523078)
- Aramazaya (13523082)
- Muhammad Izzat Jundy (13523092)
- Barru Adi Utomo (13523101)
- Athian Nugraha Muarajuang (13523106)

## Deskripsi Sistem
Sistem Informasi Manajemen Terintegrasi Ecoethno adalah sebuah sistem berbasis Enterprise Resource Planning (ERP) yang dikembangkan menggunakan platform Odoo. Sistem ini berfokus pada dua ruang lingkup utama: digitalisasi pencatatan inventaris (logistik dapur dan perlengkapan outbound) secara real-time dan sentralisasi data pelanggan melalui modul Customer Relationship Management (CRM).


Sistem ini dirancang untuk menggantikan proses pencatatan manual yang rentan kesalahan (seperti selisih barang di lapangan) dan mengonsolidasikan data yang sebelumnya terfragmentasi di berbagai media seperti WhatsApp dan Google Drive. Dengan sistem ini, seluruh aliran informasi dari pelanggan, operasional lapangan, hingga manajemen tingkat atas dapat saling terhubung dalam satu basis data terpusat.


## Panduan Penggunaan Umum
Untuk menjalankan sistem informasi ini, ikuti langkah berikut:
1. clone dan buka repository, kemudian jalankan script import db (pastikan dump yang digunakan adalah ```odoo_backup_backup_ecoethno.dump```)
2. Jalankan perintah ```docker compose up -d```
3. Buka aplikasi pada browser dengan mengakses ```http://localhost:8069```
4. Login dengan kredensial berikut:
- username: admin_eco
- password: admin123
5. Unduh semua modul yang telah dikembangkan
6. Sistem informasi siap untuk digunakan

## Panduan Penggunaan Masing-Masing Fitur
Tangkapan layar sebagai ilustrasi dapat diakses melalui tautan berikut: ```https://canva.link/2rz10wvo7idilz6```

### A. Login
1. Buka halaman login sistem informasi Ecoethno.
2. Masukkan username pada kolom login yang tersedia (no 1 di gambar).
3. Masukkan password pada kolom password (no 2 di gambar).
4. Tekan tombol “Log In” untuk masuk ke dalam sistem (no 3 di gambar).
5. Sistem akan melakukan validasi data pengguna.
6. Jika username dan password sesuai, pengguna akan diarahkan ke halaman utama sistem.
7. Jika data login tidak valid, sistem akan menampilkan pesan kesalahan dan pengguna diminta untuk mencoba kembali.

### B. Dashboard
1. Sistem akan menampilkan ringkasan utama berupa Pendapatan, Transaksi, dan Inventaris.
2. Pilih periode laporan dengan menekan tombol “Hari ini”, “Minggu ini”, “Bulan ini”, atau “Tahun ini”.
3. Untuk melihat periode khusus, isi tanggal awal dan tanggal akhir pada kolom tanggal.
4. Tekan tombol “terapkan” untuk menerapkan rentang tanggal awal hingga tanggal akhir
5. Tekan tombol reset bila ingin mengembalikan tampilan ke periode tahun berjalan.
6. Grafik “Tren Reservasi” untuk melihat perubahan jumlah kunjungan pada periode yang dipilih.
7. Diagram “Kunjungan” untuk melihat persebaran reservasi berdasarkan platform pemesanan.
8. Tabel “Reservasi Terbaru” untuk meninjau data reservasi paling baru. Tekan tombol “Detail” pada baris tertentu apabila ingin membuka formulir reservasi tersebut.
9. Tabel “Inventaris” untuk memantau stok barang. Tekan tombol “Detail” pada baris tertentu apabila ingin membuka formulir item inventaris tersebut

### C. Manajemen Inventaris

### D. Manajemen Pengguna
1. Klik menu “User Management” pada navigation bar sistem. 
2. Sistem akan menampilkan daftar pengguna yang telah terdaftar.
3. Untuk menambahkan pengguna baru, tekan tombol “New”.
4. Isi data pengguna seperti nama, username/login, password, jabatan, divisi, dan role pengguna.
5. Pilih hak akses pengguna sesuai kebutuhan, seperti Admin, Manager, atau Staff.
6. Tekan tombol “Save” untuk menyimpan data pengguna baru.
7. Untuk mengubah data pengguna, pilih salah satu pengguna pada daftar kemudian lakukan perubahan data yang diperlukan.
8. Untuk menghapus pengguna, admin dapat memilih data pengguna kemudian menekan tombol delete.
9. Sistem akan secara otomatis membatasi akses pengguna berdasarkan role yang dimiliki.

### E. Manajemen Reservasi
1. Klik tombol “Reservasi” pada menu yang tersedia di bagian atas
2. Menekan tanggal reservasi yang diinginkan pada kalender
3. Mengisi nama reservasi kemudian menekan tombol “Create” jika ingin menambahkan reservasi, “Edit” jika ingin memperbarui data reservasi, atau “Delete” jika ingin menghapus data reservasi
4. Jika memilih “Create” atau “Edit, ” pengguna kemudian mengisi data detail reservasi sesuai pada form
5. Menekan tombol “Save manually” untuk menyimpan perubahan ke dalam basis data

### F. Manajemen Ulasan
Langkah-langkah untuk melihat history transaksi dalam sistem adalah sebagai berikut:
1. Menekan tombol “Daftar Feedback” pada menu yang tersedia di bagian atas. Ulasan dalam bentuk daftar ulasan akan langsung terlihat.
2. Menekan salah satu ikon di pojok kanan atas untuk melihat statistik dari histori transaksi. Terdapat beberapa opsi penggambaran grafik yang dapat dicoba


Langkah-langkah untuk menambah sebuah ulasan dalam sistem adalah sebagai berikut:
1. Menekan tombol “Tambah Feedback” pada menu yang tersedia di bagian atas
2. Memilih reservasi dan memastikan semua data benar
3. Menekan tombol Rating yang diberikan pelanggan
4. Mengisi catatan ulasan
5. Menekan ikon awan dengan panah ke atas untuk mengunggah transaksi yang baru dibuat

### G. Histori Transaksi
Menekan tombol “Riwayat Transaksi” pada menu yang tersedia di bagian atas. Histori transaksi dalam bentuk daftar transaksi akan langsung terlihat
Menekan salah satu ikon di pojok kanan atas untuk melihat statistik dari histori transaksi. Terdapat beberapa opsi penggambaran grafik yang dapat dicoba


## Kredensial
Akun berikut terdapat pada ```odoo_backup_backup_ecoethno.dump```


```
user: admin_eco
pass: admin123

user: manager_eco
pass: manager123

user: staff_eco
pass: staff123
```

## Kesimpulan dan Saran
Repositori ini berisi sistem informasi yang telah dikembangkan sebagai prototipe alternatif solusi dari masalah yang ditemukan dalam proses Ecoethno. Sistem informasi mencakup fitur login, dashboard, manajemen pengguna, manajemen inventaris, manajemen reservasi, manajemen feedback, serta histori transaksi. Beberapa saran pengembangan dari sistem informasi ini adalah untuk terus melakukan pengembangan terhadap prototipe menjadi suatu produk yang siap digunakan serta mengembangkan prototipe untuk mengatasi masalah-masalah bisnis lain yang ditemukan dalam perusahaan.
