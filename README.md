# DOWNLOADER-UX v1.0.0

## Deskripsi
DOWNLOADER-UX adalah alat universal untuk mengunduh dan menganalisis konten dari URL web. Script ini memungkinkan pengguna untuk memindai halaman web, mengunduh gambar, script, file, dan mengekstrak link dengan mudah. Dibuat oleh [@GenzPX](https://github.com/GenzPX), alat ini dirancang untuk pengguna yang ingin mengelola unduhan dari situs web secara efisien melalui antarmuka command-line yang sederhana.

Script ini menggunakan BeautifulSoup untuk parsing HTML, requests untuk permintaan HTTP, dan tqdm untuk tampilan progress bar. Ini juga mencakup mekanisme retry untuk menangani error jaringan, logging error, dan animasi loading untuk pengalaman pengguna yang lebih baik.

## Fitur
- **Analisis URL**: Memindai halaman web untuk menghitung dan mengidentifikasi elemen seperti gambar, script, file, dan link.
- **Unduhan Khusus**:
  - Unduh gambar (images) dari halaman web.
  - Unduh script (seperti file JavaScript).
  - Unduh file (dengan ekstensi seperti .pdf, .zip, .mp3, dll.).
  - Ekstrak dan simpan link ke file teks.
- **Pengelolaan Unduhan**:
  - Menggunakan progress bar untuk memantau proses unduhan.
  - Otomatis membuat direktori 'download' untuk menyimpan file.
  - Opsional: Membuat arsip ZIP untuk unduhan massal dan mengunggah ke Catbox.moe untuk mendapatkan link unduhan.
- **Menu Interaktif**: Antarmuka menu utama untuk memilih opsi (unduh, analisis, kredit, atau keluar).
- **Penanganan Error**: Retry otomatis untuk permintaan HTTP yang gagal, logging error ke file, dan penanganan dependensi yang hilang.
- **Visualisasi**: Menampilkan banner ASCII dan animasi loading untuk tampilan yang menarik.

## Persyaratan
- **Python**: Versi 3.6 atau lebih baru (script menggunakan `#!/usr/bin/env python3`).
- **Dependensi Eksternal**:
  - `requests`: Untuk permintaan HTTP.
  - `beautifulsoup4`: Untuk parsing HTML.
  - `tqdm`: Untuk progress bar.
  - `zipfile`: Sudah termasuk dalam Python standar.
  
  Script ini secara otomatis memeriksa dan menginstal dependensi yang hilang menggunakan pip saat dijalankan.

## Instalasi
1. **Clone atau Download Script**: Unduh file script (misalnya, `downloader_ux.py`) dari repositori Anda atau salin kode ke file baru.
2. **Instal Dependensi**:
   Script akan secara otomatis mendeteksi dan menginstal dependensi yang hilang. Namun, untuk memastikan, jalankan perintah berikut di terminal:
   ```
   pip install requests beautifulsoup4 tqdm
   ```
3. **Jalankan Script**:
   Pastikan script memiliki hak eksekusi (jika di Linux/macOS):
   ```
   chmod +x downloader_ux.py
   ```
   Kemudian, jalankan:
   ```
   python3 downloader_ux.py
   ```
   Atau langsung:
   ```
   ./downloader_ux.py
   ```

## Penggunaan
Script ini berjalan melalui menu interaktif. Berikut adalah panduan langkah demi langkah:

1. **Menu Utama**:
   Saat script dijalankan, Anda akan melihat banner dan menu utama:
   ```
   [ 1 ] Download
   [ 2 ] Analyst
   [ 3 ] Credits
   [ 4 ] Exit
   ```
   - Pilih opsi dengan memasukkan nomor (1-4) dan tekan Enter.

2. **Opsi Download (Pilihan 1)**:
   - Masukkan URL yang valid (misalnya, https://example.com).
   - Script akan menganalisis URL dan menampilkan ringkasan (jumlah gambar, script, file, dan link).
   - Pilih apa yang ingin diunduh:
     - **1**: Unduh gambar.
     - **2**: Unduh script.
     - **3**: Unduh file.
     - **4**: Ekstrak link (disimpan ke file teks).
   - Contoh:
     ```
     Masukkan URL: https://example.com
     [ + ] URL: https://example.com
     [ 1 ] Image : 10
     [ 2 ] Script : 5
     [ 3 ] File : 3
     [ 4 ] Link  : 20
     What do you want to download? Enter choice (1-4): 1
     ```
     Ini akan mengunduh gambar ke direktori `download/images/`.

3. **Opsi Analyst (Pilihan 2)**:
   - Masukkan URL untuk menganalisis konten tanpa mengunduh.
   - Script akan menampilkan jumlah gambar, script, file, dan link yang ditemukan.

4. **Opsi Credits (Pilihan 3)**:
   - Menampilkan informasi kredit, seperti pembuat dan ucapan terima kasih.

5. **Keluar (Pilihan 4)**:
   - Keluar dari script.

**Catatan Penting**:
- Pastikan URL yang dimasukkan valid dan dapat diakses. Script menggunakan header User-Agent untuk meniru browser.
- File unduhan disimpan di direktori `download/`. Pastikan Anda memiliki ruang penyimpanan yang cukup.
- Jika unduhan massal, script akan membuat arsip ZIP dan mencoba mengunggah ke Catbox.moe untuk mendapatkan link unduhan.

## Kontribusi
Jika Anda ingin berkontribusi, fork repositori ini dan buat pull request. Saran perbaikan:
- Tambahkan dukungan untuk lebih banyak jenis file.
- Tingkatkan keamanan dengan memverifikasi SSL (saat ini, `verify=False` digunakan).
- Tambahkan opsi konfigurasi melalui file JSON.

Hubungi pembuat (@GenzPX) melalui profil GitHub jika ada pertanyaan.

## Kredit
- **Pembuat**: @GenzPX
- **Terima Kasih Kepada**: Semua pengguna yang telah mencoba dan memberikan umpan balik.

## Lisensi
Script ini belum menentukan lisensi resmi. Disarankan untuk menambahkan lisensi seperti MIT atau GPL di bagian atas script untuk melindungi dan membagikan kode. Contoh:
```
# MIT License
# Copyright (c) [Tahun] [Nama Anda]
# Permission is hereby granted, free of charge, to any person obtaining a copy...
```
