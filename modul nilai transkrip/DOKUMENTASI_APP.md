# Dokumentasi Aplikasi Manajemen Nilai & Transkrip Akademik

---

## 📋 Daftar Isi
1. [Pendahuluan](#pendahuluan)
2. [Teknologi yang Digunakan](#teknologi-yang-digunakan)
3. [Arsitektur Aplikasi](#arsitektur-aplikasi)
4. [Fitur-Fitur Utama](#fitur-fitur-utama)
5. [Struktur File & Folder](#struktur-file--folder)
6. [Panduan Instalasi](#panduan-instalasi)
7. [Panduan Penggunaan](#panduan-penggunaan)
8. [Penjelasan Modul Kode](#penjelasan-modul-kode)
9. [Database Schema](#database-schema)
10. [API Routes](#api-routes)

---

## Pendahuluan

Aplikasi ini adalah sistem manajemen akademik berbasis web yang dirancang untuk:
- **Mengelola data mahasiswa** (Nama, NIM, Program Studi)
- **Mencatat nilai mata kuliah** dengan tracking perubahan
- **Menghitung IPK** (Indeks Prestasi Kumulatif) secara otomatis
- **Menghasilkan transkrip akademik** dalam format PDF
- **Mencatat riwayat perubahan nilai** untuk audit trail

### Target Pengguna
- Akademik/Registrar Universitas
- Dosen Pembimbing
- Staff Administrasi

---

## Teknologi yang Digunakan

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| **Backend Framework** | Flask | Python 3.8+ |
| **Database** | SQLite/SQL | SQLAlchemy ORM |
| **Frontend** | HTML5, CSS3, Jinja2 | Bootstrap |
| **PDF Generation** | ReportLab / WeasyPrint | - |
| **Database ORM** | SQLAlchemy | - |

---

## Arsitektur Aplikasi

```
┌─────────────────────────────────────────┐
│           Web Browser (User)            │
└─────────────────┬───────────────────────┘
                  │ HTTP Request/Response
                  ▼
┌─────────────────────────────────────────┐
│          Flask Web Application          │
│  (app.py - Main Router & Controller)    │
└────────┬─────────────────────────────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
┌────────┐ ┌──────────┐ ┌────────┐ ┌─────────────┐
│database│ │ipk_      │ │generate│ │Template     │
│.py     │ │calculator│ │transkrip│ │(Jinja2)     │
│(ORM)   │ │.py       │ │.py     │ │             │
└────────┘ └──────────┘ └────────┘ └─────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│    SQLite Database (database.sql)       │
│  • Students • Grades • History          │
└─────────────────────────────────────────┘
```

---

## Fitur-Fitur Utama

### 1️⃣ Halaman Beranda
- **Endpoint**: `/`
- **Fungsi**: Menampilkan halaman sambutan dan navigasi
- **Template**: `home.html`

### 2️⃣ Kalkulator IPK (Indeks Prestasi Kumulatif)
- **Endpoint**: `/calculate_ipk`
- **Metode**: GET (form), POST (proses)
- **Input**: 
  - Kode Mata Kuliah (MK)
  - Jumlah SKS (Satuan Kredit Semester)
  - Nilai Huruf (A, B, C, D, E)
- **Proses**: Konversi nilai → perhitungan bobot → hasil IPK
- **Output**: Nilai IPK dan detail perhitungan

### 3️⃣ Generate Transkrip PDF
- **Endpoint**: `/generate_pdf`
- **Metode**: GET (form), POST (generate)
- **Input**:
  - Data Mahasiswa (NIM, Nama, Prodi, Angkatan)
  - Total SKS
  - IPK & Predikat
  - Daftar Mata Kuliah per semester
- **Output**: File PDF (transkrip akademik)
- **Format**: Sesuai template `transkrip_template.html`

### 4️⃣ Manajemen Data Mahasiswa
- **Endpoint**: `/students`
- **Fitur**:
  - Menampilkan daftar semua mahasiswa
  - Link ke detail nilai & riwayat
- **Database**: Tabel `Student`

### 5️⃣ Tambah Mahasiswa Baru
- **Endpoint**: `/add_student`
- **Metode**: GET (form), POST (simpan)
- **Input**:
  - ID/NIM Mahasiswa
  - Nama Mahasiswa
- **Redirect**: Kembali ke daftar mahasiswa

### 6️⃣ Manajemen Nilai Mata Kuliah
- **Endpoint**: `/grades/<student_id>`
- **Fungsi**: Menampilkan semua nilai untuk satu mahasiswa
- **Database**: Query tabel `Grade`

### 7️⃣ Tambah/Edit Nilai
- **Endpoint**: `/add_grade/<student_id>`
- **Metode**: GET (form), POST (simpan)
- **Input**:
  - Course ID (Kode MK)
  - Grade (Nilai Huruf)
  - Nama yang mengubah
  - Alasan perubahan
- **Tracking**: Mencatat siapa yang mengubah dan kapan

### 8️⃣ Riwayat Perubahan Nilai
- **Endpoint**: `/history/<student_id>`
- **Fungsi**: Audit trail semua perubahan nilai
- **Data Tercatat**:
  - Nilai lama vs nilai baru
  - Siapa yang mengubah
  - Kapan perubahan terjadi
  - Alasan perubahan

---

## Struktur File & Folder

```
modul nilai transkrip/
│
├── app.py                          ← MAIN APPLICATION (Flask Routes)
├── database.py                     ← Database Models & ORM Configuration
├── database_setup.sql              ← SQL Schema & Initial Data
├── ipk_calculator.py               ← Logika Perhitungan IPK
├── generate_transkrip.py           ← PDF Generation Engine
├── test_ipk.py                     ← Unit Tests untuk IPK
│
├── templates/                      ← Frontend Jinja2 Templates
│   ├── home.html                   (Halaman Utama)
│   ├── calculate_ipk.html          (Form & Result Kalkulator IPK)
│   ├── generate_pdf.html           (Form Generate Transkrip PDF)
│   ├── students.html               (Daftar Mahasiswa)
│   ├── add_student.html            (Form Tambah Mahasiswa)
│   ├── grades.html                 (Daftar Nilai per Mahasiswa)
│   ├── add_grade.html              (Form Tambah/Edit Nilai)
│   └── history.html                (Riwayat Perubahan Nilai)
│
├── static/                         ← Static Assets
│   └── style.css                   (Stylesheet Aplikasi)
│
├── transkrip_template.html         ← Template HTML untuk PDF
└── README.md                       ← File README

```

---

## Panduan Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Package Manager Python)
- Virtual Environment (recommended)

### Langkah-Langkah Instalasi

#### 1. Clone/Download Repository
```bash
cd "c:\Users\hakim\Documents\modul nilai transkrip"
```

#### 2. Buat Virtual Environment
```bash
python -m venv venv
```

#### 3. Aktivasi Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install flask sqlalchemy
# Optional: pip install weasyprint  (untuk PDF generation)
```

#### 5. Setup Database
```bash
# Jalankan SQL setup
python -c "import sqlite3; exec(open('database_setup.sql').read())"

# Atau via database.py
python database.py
```

#### 6. Jalankan Aplikasi
```bash
python app.py
```

#### 7. Akses Aplikasi
```
http://localhost:5000
```

---

## Panduan Penggunaan

### Workflow Pengguna Umum

#### Scenario 1: Menambah Mahasiswa Baru
```
1. Navigasi ke menu "Students"
2. Klik "Add New Student"
3. Isi NIM dan Nama
4. Submit
5. Mahasiswa akan muncul di daftar
```

#### Scenario 2: Memasukkan Nilai Mahasiswa
```
1. Di halaman Students, pilih mahasiswa
2. Klik "View Grades"
3. Klik "Add Grade"
4. Isi:
   - Kode MK (Contoh: IF101)
   - Nilai Huruf (A/B/C/D/E)
   - Nama pengubah (untuk audit)
   - Alasan (opsional)
5. Submit
```

#### Scenario 3: Menghitung IPK
```
1. Navigasi ke "Calculate IPK"
2. Masukkan hingga 10 mata kuliah:
   - Kode MK
   - SKS
   - Nilai Huruf
3. Sistem otomatis hitung IPK
4. Lihat hasil perhitungan dengan detail
```

#### Scenario 4: Generate Transkrip PDF
```
1. Navigasi ke "Generate PDF"
2. Isi data mahasiswa:
   - NIM, Nama, Prodi, Angkatan
3. Isi data akademik:
   - Total SKS
   - IPK, Predikat
4. Masukkan 5 mata kuliah terakhir
5. Klik "Generate PDF"
6. File transkrip.pdf akan diunduh
```

#### Scenario 5: Melihat Riwayat Perubahan
```
1. Di halaman Students, pilih mahasiswa
2. Klik "View History"
3. Lihat semua perubahan nilai dengan:
   - Waktu perubahan
   - Nilai lama → nilai baru
   - Siapa yang mengubah
   - Alasan perubahan
```

---

## Penjelasan Modul Kode

### 1. **app.py** - Main Application
Berisi router utama Flask dan controller logic:

| Function | Endpoint | Deskripsi |
|----------|----------|-----------|
| `home()` | `/` | Halaman utama aplikasi |
| `calculate_ipk_route()` | `/calculate_ipk` | Proses & tampilkan IPK |
| `generate_pdf_route()` | `/generate_pdf` | Generate PDF transkrip |
| `students()` | `/students` | Daftar semua mahasiswa |
| `add_student()` | `/add_student` | Tambah mahasiswa baru |
| `grades()` | `/grades/<sid>` | Lihat nilai mahasiswa |
| `add_grade()` | `/add_grade/<sid>` | Tambah/edit nilai |
| `history()` | `/history/<sid>` | Lihat riwayat perubahan |

**Alur Proses**:
```python
Request → Flask Route → Business Logic → Database Query → Response
         (app.py)     (ipk_calc, etc)  (database.py)     (Template)
```

### 2. **database.py** - ORM Models
Mendefinisikan struktur data menggunakan SQLAlchemy:

```python
Student
├── id: Primary Key (NIM)
├── name: String
└── relationship: grades (1-to-Many)

Grade
├── id: Primary Key
├── student_id: Foreign Key
├── course_id: String
├── grade: String
├── changed_by: String
├── change_reason: String
└── timestamp: DateTime

GradeHistory
├── id: Primary Key
├── grade_id: Foreign Key
├── old_grade: String
├── new_grade: String
├── changed_at: DateTime
└── changed_by: String
```

### 3. **ipk_calculator.py** - Logika IPK
Menghitung IPK dari daftar nilai:

**Formula IPK**:
```
IPK = Σ(Nilai Bobot × SKS) / Σ(SKS)

Konversi Nilai:
A = 4.0,  B = 3.0,  C = 2.0,  D = 1.0,  E = 0.0
```

### 4. **generate_transkrip.py** - PDF Generator
Mengkonversi data akademik ke PDF:
- Membaca `transkrip_template.html`
- Render dengan data mahasiswa
- Generate file PDF
- Return sebagai attachment

### 5. **test_ipk.py** - Unit Tests
Test cases untuk validasi perhitungan IPK:
```
✓ Test nilai A, B, C
✓ Test berbagai kombinasi SKS
✓ Test edge cases
```

---

## Database Schema

### Tabel: students
```sql
CREATE TABLE students (
    id VARCHAR(20) PRIMARY KEY,      -- NIM
    name VARCHAR(100) NOT NULL
);
```

### Tabel: grades
```sql
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    grade CHAR(1) NOT NULL,          -- A, B, C, D, E
    changed_by VARCHAR(100),          -- Nama yang mengubah
    change_reason TEXT,               -- Alasan perubahan
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

### Tabel: grade_history
```sql
CREATE TABLE grade_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade_id INTEGER NOT NULL,
    old_grade CHAR(1),
    new_grade CHAR(1),
    changed_by VARCHAR(100),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    FOREIGN KEY (grade_id) REFERENCES grades(id)
);
```

---

## API Routes

### Public Routes

#### 1. GET `/`
**Tujuan**: Menampilkan halaman utama
```
Status: 200
Response: home.html (HTML)
```

#### 2. GET/POST `/calculate_ipk`
**Tujuan**: Kalkulator IPK
```
Method GET:  Tampilkan form
Method POST: 
  Input Form:
    - kode_1...10 (Course Code)
    - sks_1...10 (Credit Hour)
    - nilai_1...10 (Grade Letter)
  
  Output: 
    {
      "ipk": 3.45,
      "nilai_list": [...]
    }
```

#### 3. GET/POST `/generate_pdf`
**Tujuan**: Generate transkrip PDF
```
Method GET:  Tampilkan form
Method POST:
  Input:
    - nim, nama, prodi, angkatan
    - total_sks, ipk, predikat
    - mk_kode_1...5, mk_nama, mk_sks, mk_nilai, mk_mutu
  
  Output: 
    File: transkrip.pdf (Binary)
    Content-Type: application/pdf
```

#### 4. GET `/students`
**Tujuan**: Daftar semua mahasiswa
```
Status: 200
Response: students.html
  Data: students = [Student...]
```

#### 5. GET/POST `/add_student`
**Tujuan**: Tambah mahasiswa baru
```
Method GET:  Tampilkan form input
Method POST:
  Input:
    - id (NIM)
    - name
  
  Response: Redirect ke /students
```

#### 6. GET `/grades/<student_id>`
**Tujuan**: Lihat nilai mahasiswa
```
Parameter: student_id (NIM)
Status: 200
Response: grades.html
  Data: 
    - student: Student object
    - grades: [Grade...]
```

#### 7. GET/POST `/add_grade/<student_id>`
**Tujuan**: Tambah/edit nilai
```
Parameter: student_id (NIM)

Method GET:  Tampilkan form
Method POST:
  Input:
    - course_id
    - grade (A-E)
    - changed_by (nama)
    - reason (alasan)
  
  Response: Redirect ke /grades/<student_id>
```

#### 8. GET `/history/<student_id>`
**Tujuan**: Riwayat perubahan nilai
```
Parameter: student_id (NIM)
Status: 200
Response: history.html
  Data: history = [
    {
      timestamp: "2024-01-15 10:30",
      old_grade: "B",
      new_grade: "A",
      changed_by: "Dr. Admin",
      reason: "Perbaikan nilai"
    },
    ...
  ]
```

---

## Deployment Checklist

- [ ] Test semua routes di local environment
- [ ] Jalankan unit tests (`test_ipk.py`)
- [ ] Setup database di production
- [ ] Disable debug mode (`app.run(debug=False)`)
- [ ] Setup production server (Gunicorn, uWSGI)
- [ ] Configure HTTPS/SSL
- [ ] Setup logging & monitoring
- [ ] Backup database secara berkala
- [ ] Document deployment process

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Database tidak ditemukan | Jalankan `database_setup.sql` |
| Template tidak ditemukan | Pastikan folder `templates/` ada di root |
| IPK tidak terhitung | Check input nilai huruf (A-E only) |
| PDF tidak bisa dihasilkan | Install `weasyprint` atau `reportlab` |
| Port 5000 sudah dipakai | Ubah port: `app.run(port=5001)` |

---

## Kontak & Support

Untuk pertanyaan atau bantuan, hubungi:
- **Email**: admin@universitas.ac.id
- **Phone**: (021) XXX-XXXX
- **Office Hours**: Senin-Jumat, 09:00-17:00

---

## Lisensi & Copyright

© 2024 Universitas. All rights reserved.

**Catatan**: Dokumentasi ini dibuat untuk keperluan presentasi internal dan referensi developer.

---

**Terakhir diupdate**: Januari 2026
**Versi**: 1.0
**Status**: Production Ready
