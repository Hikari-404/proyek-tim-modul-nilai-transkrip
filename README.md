# proyek-tim-modul-nilai-transkrip

pada proyek ini tim kami berisikan
Shafwan Hakim 
Matin waliyyu kartar
Abby gustian
Dosma silitonga
Bayu 
Rifqi suryana

# Sistem Transkrip Akademik

Sistem ini dirancang untuk mengelola transkrip akademik mahasiswa, termasuk perhitungan IPK, generate PDF transkrip, dan audit perubahan nilai. Dibangun menggunakan Python dengan berbagai library untuk memudahkan pengelolaan data akademik.

## Fitur Utama

### 1. Perhitungan IPK
- Fungsi `calculate_ipk` untuk menghitung Indeks Prestasi Kumulatif (IPK) berdasarkan aturan:
  - IPK = Σ(SKS × Nilai Angka) / Σ(SKS)
  - Hanya hitung MK yang lulus (nilai ≥ D)
  - Jika MK diulang, ambil nilai tertinggi
  - Edge case: mahasiswa semester 1 belum ada nilai → return 0.0
- Unit test untuk berbagai skenario (nilai sempurna, MK diulang, belum ada nilai)

### 2. Generate PDF Transkrip
- Script untuk generate PDF transkrip akademik menggunakan ReportLab.
- Layout profesional mirip ijazah resmi:
  - Header: Logo universitas (opsional) + judul 'TRANSKRIP AKADEMIK'
  - Biodata: NIM, Nama, Program Studi, Angkatan
  - Tabel per semester: Kode MK | Nama MK | SKS | Nilai | Mutu
  - Footer: Total SKS, IPK, Predikat, TTD Dekan (opsional)
- Data dinamis dari dictionary Python.

### 3. Database Audit untuk Perubahan Nilai
- Tabel `grade_history` untuk track perubahan nilai.
- Kolom: id, grade_id, old_value, new_value, changed_by, changed_at, reason
- Trigger audit: setiap UPDATE pada tabel grades, insert row ke grade_history.
- View untuk lihat riwayat perubahan per mahasiswa.
- Implementasi menggunakan SQLAlchemy (SQLite untuk demo) atau SQL script (PostgreSQL).

## Struktur File

```
nilai transkrip/
├── ipk_calculator.py          # Fungsi calculate_ipk
├── test_ipk.py                # Unit test untuk IPK
├── generate_transkrip.py      # Script generate PDF transkrip
├── transkrip_template.html    # Template HTML (opsional, untuk WeasyPrint)
├── database_setup.sql         # SQL script untuk setup database (PostgreSQL)
├── database.py                # Implementasi database dengan SQLAlchemy
├── app.py                     # Flask web application
├── templates/                 # Folder untuk HTML templates
│   ├── home.html
│   ├── calculate_ipk.html
│   ├── generate_pdf.html
│   ├── students.html
│   ├── add_student.html
│   ├── grades.html
│   ├── add_grade.html
│   └── history.html
├── transkrip.pdf              # Output PDF (dihasilkan saat run generate_transkrip.py)
├── transkrip.db               # Database SQLite (dihasilkan saat run database.py)
└── README.md                  # Dokumentasi ini
```

## Prerequisites

- Python 3.8+
- Library Python:
  - reportlab (untuk generate PDF)
  - sqlalchemy (untuk ORM database)
  - flask (untuk web application)
  - jinja2 (opsional, untuk template HTML)
  - weasyprint (opsional, alternatif untuk PDF, tapi bermasalah di Windows)
