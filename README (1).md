# SPK AHP — Sistem Pendukung Keputusan Perbaikan Fasilitas Kampus

> Sistem Pendukung Keputusan berbasis metode **Analytic Hierarchy Process (AHP)** untuk menentukan prioritas perbaikan fasilitas kampus secara sistematis dan terukur.

---

## Deskripsi

SPK AHP adalah aplikasi web yang dibangun menggunakan **Flask (Python)** dan **MySQL** yang membantu pengambilan keputusan dalam menentukan fasilitas kampus mana yang perlu diprioritaskan untuk diperbaiki. Sistem ini menggunakan metode AHP dengan 4 kriteria tetap yang telah dikonfigurasi, serta mendukung hingga 20 alternatif fasilitas yang dapat dibandingkan.

---

## Fitur Utama

- **Input Alternatif** — Menentukan jumlah dan nama fasilitas kampus yang akan dinilai (2–20 alternatif)
- **Tabel Perbandingan Berpasangan** — Input nilai perbandingan antar alternatif menggunakan Skala Saaty untuk setiap kriteria
- **Kalkulasi AHP Otomatis** — Sistem menghitung bobot, skor akhir, dan *Consistency Ratio* (CR) secara otomatis
- **Hasil & Ranking** — Menampilkan peringkat prioritas perbaikan fasilitas secara lengkap
- **Dashboard Visualisasi** — Grafik batang, grafik horizontal, dan *donut chart* untuk mempermudah interpretasi hasil
- **History Analisis** — Riwayat semua sesi analisis yang pernah dilakukan tersimpan otomatis
- **Tabel Prediksi** — Dokumentasi permanen hasil keputusan ke dalam database
- **Export Data** — Unduh hasil analisis dalam format CSV dan JSON
- **Cetak / Print** — Hasil analisis dapat langsung dicetak

---

## Kriteria Penilaian

Sistem menggunakan 4 kriteria tetap yang telah dikonfigurasi:

| No | Kriteria | Deskripsi |
|----|----------|-----------|
| 1 | **Tingkat Kerusakan** | Seberapa parah kerusakan fasilitas |
| 2 | **Dampak terhadap Akademik** | Pengaruh terhadap kegiatan belajar mengajar |
| 3 | **Frekuensi Penggunaan** | Seberapa sering fasilitas digunakan |
| 4 | **Biaya Perbaikan** | Estimasi biaya yang dibutuhkan untuk perbaikan |

---

## Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python, Flask |
| Database | MySQL (via Laragon) |
| Frontend | HTML, CSS, JavaScript |
| Koneksi DB | mysql-connector-python |

---

## Instalasi & Cara Menjalankan

### Prasyarat
Pastikan perangkat Anda telah menginstal:
- [Python 3.x](https://www.python.org/)
- [Laragon](https://laragon.org/) (untuk layanan MySQL)
- pip (Python package manager)

### Langkah Instalasi

**1. Clone repository ini**
```bash
git clone https://github.com/username/spk_fixed.git
cd spk_fixed
```

**2. Install dependensi Python**
```bash
pip install -r requirements.txt
```

**3. Aktifkan Laragon**

Buka aplikasi Laragon dan klik **Start All** untuk mengaktifkan layanan MySQL.


**4. Jalankan aplikasi**
```bash
python App.py
atau langsung running App.py pada visual studio code
```

**5. Buka di browser**

Akses sistem melalui URL berikut:
```
http://127.0.0.1:5000
```

---

## Alur Penggunaan Sistem

```
Beranda → Jumlah Alternatif → Nama Alternatif → Tabel Perbandingan → Hasil Analisis
```

1. **Beranda** — Halaman utama yang menampilkan informasi kriteria dan tombol memulai analisis
2. **Jumlah Alternatif** — Tentukan jumlah fasilitas yang akan dibandingkan (2–20)
3. **Nama Alternatif** — Isi nama masing-masing fasilitas kampus
4. **Tabel Perbandingan** — Input nilai perbandingan berpasangan antar alternatif menggunakan Skala Saaty
5. **Hasil Analisis** — Lihat peringkat prioritas perbaikan, bobot kriteria, dan nilai konsistensi

---

## Skala Saaty

| Nilai | Keterangan |
|-------|------------|
| 1 | Sama pentingnya |
| 3 | Sedikit lebih penting |
| 5 | Lebih penting |
| 7 | Sangat lebih penting |
| 9 | Mutlak lebih penting |
| 1/3, 1/5, 1/7, 1/9 | Kebalikan dari nilai di atas |

> Nilai *Consistency Ratio* (CR) harus **≤ 0,1** agar hasil analisis dinyatakan konsisten.

---

## Struktur Direktori

```
spk_fixed/
├── App.py                      # File utama Flask (entry point aplikasi)
├── requirements.txt            # Daftar dependensi Python
├── temp_dashboard_test.py      # File pengujian dashboard
├── static/
│   └── base.css                # File stylesheet utama
└── template/
    ├── base.css                # Stylesheet tambahan
    ├── base_sidebar.html       # Komponen sidebar navigasi
    ├── index.html              # Halaman Beranda
    ├── alternatif.html         # Halaman pilihan alternatif
    ├── alternatif_input.html   # Halaman input jumlah & nama alternatif
    ├── alternatif_matrix.html  # Halaman tabel perbandingan berpasangan
    ├── kriteria.html           # Halaman informasi kriteria
    ├── matrix.html             # Halaman matriks AHP
    ├── hasil.html              # Halaman hasil analisis
    ├── dashboard.html          # Halaman dashboard visualisasi
    ├── history.html            # Halaman history analisis
    └── prediksi.html           # Halaman tabel prediksi
```

---

## Author

Dibuat sebagai implementasi Sistem Pendukung Keputusan perbaikan fasilitas kampus menggunakan metode AHP.

---

## Lisensi

Proyek ini dibuat untuk keperluan akademis.
