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

## Instalasi

1. Clone atau download repository ini.
2. Install dependencies:
   ```bash
   pip install reportlab sqlalchemy flask
   ```
   Untuk fitur tambahan:
   ```bash
   pip install jinja2 weasyprint  # WeasyPrint mungkin perlu setup GTK di Windows
   ```

## Cara Mengoperasikan

### 1. Perhitungan IPK

#### Menjalankan Fungsi
Edit `ipk_calculator.py` atau buat script baru untuk memanggil fungsi:

```python
from ipk_calculator import calculate_ipk

# Contoh data nilai
nilai_list = [
    {'kode_mk': 'TI101', 'sks': 3, 'nilai_huruf': 'A'},
    {'kode_mk': 'TI102', 'sks': 2, 'nilai_huruf': 'B'},
    # Tambah data lainnya
]

ipk = calculate_ipk(nilai_list)
print(f"IPK: {ipk}")
```

#### Menjalankan Unit Test
```bash
python -m unittest test_ipk.py
```
Akan menjalankan 4 test case dan menampilkan hasil.

### 2. Generate PDF Transkrip

#### Menjalankan Script
Edit data di `generate_transkrip.py` (lihat sample_data) atau pass data dinamis:

```python
from generate_transkrip import generate_transkrip_pdf

data = {
    'nim': '12345678',
    'nama': 'John Doe',
    'prodi': 'Teknik Informatika',
    'angkatan': '2020',
    # 'logo_url': 'path/to/logo.png',  # Opsional
    'semesters': [
        {
            'semester': 'Semester 1',
            'mata_kuliah': [
                {'kode': 'TI101', 'nama': 'Pemrograman Dasar', 'sks': 3, 'nilai': 'A', 'mutu': 12.0},
                # Tambah MK lainnya
            ]
        }
    ],
    'total_sks': 3,
    'ipk': 4.0,
    'predikat': 'Cum Laude',
    # 'ttd_dekan': 'path/to/ttd.png'  # Opsional
}

generate_transkrip_pdf(data, 'output.pdf')
```

Jalankan:
```bash
python generate_transkrip.py
```
Akan menghasilkan `transkrip.pdf` (atau custom path).

### 4. Web Application

Jalankan web app dengan Flask:
```bash
python app.py
```
Akses di browser: http://localhost:5000

Fitur web:
- **Home**: Menu utama.
- **Hitung IPK**: Form input nilai MK, hitung IPK.
- **Generate PDF**: Form input data mahasiswa, download PDF transkrip.
- **Kelola Mahasiswa**: List mahasiswa, tambah mahasiswa.
- **Nilai**: Lihat nilai per mahasiswa, tambah nilai (dengan audit).
- **Riwayat**: Lihat history perubahan nilai per mahasiswa.

## Contoh Output

### IPK Calculation
```
IPK: 3.75
```

### PDF Transkrip
File PDF dengan layout tabel, biodata, dll.

### Database Audit
```
('John Doe', 'TI101', 'B', 'A', 'lecturer', datetime.datetime(...), 'Improved performance')
```

### Web App
- Interface web di http://localhost:5000 untuk semua fitur di atas.

## Catatan

- Untuk production, ganti SQLite ke PostgreSQL/MySQL di `database.py`.
- Gambar logo/ttd opsional; skip jika tidak ada file.
- Pastikan data input valid untuk menghindari error.
- Unit test memverifikasi logika IPK.

## Lisensi

Proyek ini untuk tujuan edukasi. Gunakan sesuai kebutuhan.

Jika ada pertanyaan atau bug, silakan laporkan!