# Sistem Manajemen Pasien Rumah Sakit

Sistem Manajemen Pasien Rumah Sakit adalah aplikasi berbasis **Command Line Interface (CLI)** yang dikembangkan menggunakan bahasa pemrograman **Python**. Aplikasi ini dirancang untuk membantu proses pencatatan, pengelolaan, dan pemantauan data pasien secara sederhana, cepat, dan efisien tanpa memerlukan koneksi database eksternal, karena seluruh data disimpan secara *in-memory* menggunakan struktur `list of dictionary`.

Sistem ini cocok digunakan sebagai simulasi, media pembelajaran, maupun prototipe awal sebelum dikembangkan ke sistem yang lebih kompleks.

---

## Fitur

### 1. Login
- Autentikasi menggunakan password sebelum masuk ke menu utama.
- Password disembunyikan menggunakan karakter `*` saat pengetikan.
- Maksimal **3 kali percobaan login**, jika gagal maka program akan berhenti.

### 2. CRUD Data Pasien
- Lihat seluruh data pasien
- Tambah data pasien baru
- Edit data pasien
- Hapus data pasien
- Cari data pasien
- Lihat detail pasien

### 3. Validasi Data
- Nomor rekam medis (No. RM) dibuat otomatis oleh sistem
- Validasi format nama
- Validasi format tanggal lahir
- Validasi format nomor telepon
- Validasi golongan darah (A, B, AB, O)
- Perhitungan umur pasien secara otomatis berdasarkan tanggal lahir

### 4. Statistik
- Total keseluruhan pasien
- Jumlah pasien berjenis kelamin laki-laki
- Jumlah pasien berjenis kelamin perempuan
- Rekap jenis penyakit pasien
- Rekap golongan darah pasien

---

## Struktur Program
sistem-manajemen-pasien/
│
├── cli.py # File utama untuk menjalankan program
├── modules/
│ ├── auth.py # Modul autentikasi/login
│ ├── pasien.py # Modul CRUD data pasien
│ ├── validasi.py # Modul validasi input data
│ └── statistik.py # Modul pengolahan statistik
│
├── README.md # Dokumentasi project
└── requirements.txt # Daftar library yang dibutuhkan

> Struktur di atas bersifat contoh dan dapat disesuaikan dengan implementasi aktual project.

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| Python | Bahasa pemrograman utama |
| tabulate | Menampilkan data pasien dalam bentuk tabel |
| datetime | Mengelola tanggal lahir, umur, dan tanggal daftar |
| os | Mengelola tampilan terminal (clear screen, dll) |
| sys | Mengatur keluar program dan operasi sistem |
| msvcrt | Menangkap input password secara tersembunyi (khusus Windows) |

---

## Instalasi

Sebelum menjalankan program, pastikan Python sudah terpasang di perangkat Anda. Kemudian install library yang dibutuhkan dengan perintah berikut:

```bash
pip install tabulate
```

> Library `datetime`, `os`, `sys`, dan `msvcrt` merupakan library bawaan Python (built-in), sehingga tidak perlu instalasi tambahan. Library `msvcrt` hanya tersedia pada sistem operasi **Windows**.

---

## ▶Cara Menjalankan

Jalankan program melalui terminal dengan perintah berikut:

```bash
python cli.py
```

Setelah program berjalan, Anda akan diminta memasukkan password untuk masuk ke sistem sebelum dapat mengakses menu utama.

---

## Struktur Data Pasien

Setiap data pasien disimpan dalam bentuk `dictionary` dengan struktur berikut:

| Field | Tipe Data | Keterangan |
|-------|-----------|------------|
| `no_rm` | String/Integer | Nomor Rekam Medis, dibuat otomatis oleh sistem |
| `nama` | String | Nama lengkap pasien |
| `tanggal_lahir` | String (DD-MM-YYYY) | Tanggal lahir pasien |
| `umur` | Integer | Dihitung otomatis berdasarkan tanggal lahir |
| `jenis_kelamin` | String | Laki-laki / Perempuan |
| `alamat` | String | Alamat tempat tinggal pasien |
| `no_telepon` | String | Nomor telepon aktif pasien |
| `golongan_darah` | String | A, B, AB, atau O |
| `penyakit` | String | Diagnosis atau jenis penyakit pasien |
| `keluhan` | String | Keluhan yang disampaikan pasien |
| `tanggal_daftar` | String (DD-MM-YYYY) | Tanggal pasien terdaftar dalam sistem |

---

## Validasi Data

Sistem menerapkan validasi input untuk menjaga konsistensi dan keakuratan data, di antaranya:

- **Nama**: hanya menerima huruf dan spasi, tidak boleh kosong.
- **Tanggal Lahir**: harus sesuai format tanggal yang valid dan tidak melebihi tanggal saat ini.
- **Nomor Telepon**: hanya menerima angka dengan panjang digit sesuai standar nomor telepon.
- **Golongan Darah**: hanya menerima nilai `A`, `B`, `AB`, atau `O`.
- **Umur**: dihitung secara otomatis oleh sistem berdasarkan tanggal lahir dan tanggal saat ini, sehingga tidak diinput manual oleh pengguna.

---

## Menu Program

Berikut adalah gambaran alur menu utama program:
=== SISTEM MANAJEMEN PASIEN RUMAH SAKIT ===

Lihat Seluruh Pasien
Tambah Pasien
Edit Pasien
Hapus Pasien
Cari Pasien
Detail Pasien
Statistik Pasien
Keluar

Pengguna cukup memilih menu dengan memasukkan angka sesuai pilihan yang tersedia.

---

## Screenshot
<img width="476" height="261" alt="image" src="https://github.com/user-attachments/assets/5bf7ad4e-97dd-4ed9-bd04-ff5f0f3e2d6b" />
Tampilan sistem login untuk masuk menu 



