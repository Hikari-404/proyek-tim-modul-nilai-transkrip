"""
================================================================================
    SISTEM MANAJEMEN NILAI & TRANSKRIP AKADEMIK
    File: app.py
    Deskripsi: Flask Application - Main Router & Controller
    Fungsi: Handle semua HTTP request dan route ke halaman yang sesuai
================================================================================
"""

# ============================================================================
# IMPORT LIBRARY & MODULE
# ============================================================================
from flask import Flask, render_template, request, send_file, redirect, url_for
from ipk_calculator import calculate_ipk              # Modul perhitungan IPK
from generate_transkrip import generate_transkrip_pdf # Modul generate PDF
from database import Session, Student, Grade, get_student_grade_history  # Database ORM
import os                                              # Operating system utilities
import tempfile                                        # Temporary file handling

# ============================================================================
# INISIALISASI FLASK APPLICATION
# ============================================================================
# Membuat instance aplikasi Flask dengan __name__ (nama module sebagai root)
app = Flask(__name__)

# ============================================================================
# ROUTE 1: HOME PAGE (Halaman Utama / Beranda)
# ============================================================================
@app.route('/')
def home():
    """
    Menampilkan halaman utama aplikasi
    
    HTTP Method: GET
    URL: http://localhost:5000/
    
    Alur:
    1. User akses "/" (root URL)
    2. Flask route handler tertrigger
    3. Load dan render template 'home.html'
    4. Kirim HTML ke browser user
    
    Return: Halaman HTML berisi navigasi menu utama
    """
    return render_template('home.html')


# ============================================================================
# ROUTE 2: IPK CALCULATOR (Kalkulator Indeks Prestasi Kumulatif)
# ============================================================================
@app.route('/calculate_ipk', methods=['GET', 'POST'])
def calculate_ipk_route():
    """
    Menampilkan form kalkulator IPK dan memproses perhitungan
    
    HTTP Method: GET (tampilkan form), POST (proses perhitungan)
    URL: http://localhost:5000/calculate_ipk
    
    Alur Saat GET Request:
    1. User navigasi ke /calculate_ipk
    2. Tampilkan form kosong untuk input nilai
    3. User dapat input hingga 10 mata kuliah
    
    Alur Saat POST Request:
    1. User submit form dengan data nilai
    2. Loop melalui 10 field input (kode_1 sampai kode_10)
    3. Validasi: hanya process jika semua field (kode, sks, nilai) terisi
    4. Kumpulkan data valid ke dalam list 'nilai_list'
    5. Panggil function calculate_ipk() untuk hitung IPK
    6. Tampilkan hasil IPK dan detail perhitungan
    
    Form Input (POST):
    - kode_1...10: Kode mata kuliah (contoh: IF101)
    - sks_1...10: Jumlah SKS (1-4)
    - nilai_1...10: Nilai huruf (A/B/C/D/E)
    
    Return: 
    - GET: HTML form kosong
    - POST: HTML hasil perhitungan IPK dengan tabel detail
    """
    if request.method == 'POST':
        # ===== STEP 1: PERSIAPAN VARIABEL UNTUK MENAMPUNG DATA =====
        nilai_list = []  # List untuk menyimpan data nilai yang valid
        
        # ===== STEP 2: LOOP MELALUI SEMUA INPUT FIELD (MAKSIMAL 10 MK) =====
        for i in range(1, 11):  # Mulai dari 1 sampai 10 (inclusive)
            # Ambil data dari form dengan key: kode_1, kode_2, ... kode_10
            kode = request.form.get(f'kode_{i}')
            sks = request.form.get(f'sks_{i}')
            nilai = request.form.get(f'nilai_{i}')
            
            # ===== STEP 3: VALIDASI DATA - HANYA PROSES JIKA SEMUA FIELD TERISI =====
            if kode and sks and nilai:  # Cek ketiga field tidak kosong
                # Tambahkan ke list dalam format dictionary
                nilai_list.append({
                    'kode_mk': kode,           # Kode mata kuliah (string)
                    'sks': int(sks),           # Konversi SKS ke integer
                    'nilai_huruf': nilai       # Nilai huruf (string: A-E)
                })
        
        # ===== STEP 4: PANGGIL FUNCTION CALCULATOR UNTUK HITUNG IPK =====
        # Function ini ada di file ipk_calculator.py
        # Input: list of dict dengan struktur {kode_mk, sks, nilai_huruf}
        # Output: float IPK (contoh: 3.45)
        ipk = calculate_ipk(nilai_list)
        
        # ===== STEP 5: RENDER TEMPLATE DENGAN HASIL PERHITUNGAN =====
        # Pass ipk dan nilai_list ke template untuk ditampilkan
        return render_template('calculate_ipk.html', ipk=ipk, nilai_list=nilai_list)
    
    # ===== JIKA REQUEST METHOD ADALAH GET =====
    # Tampilkan form kosong tanpa data perhitungan
    return render_template('calculate_ipk.html')


# ============================================================================
# ROUTE 3: GENERATE TRANSKRIP PDF (Membuat File PDF Transkrip Akademik)
# ============================================================================
@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf_route():
    """
    Menampilkan form input data akademik dan generate PDF transkrip
    
    HTTP Method: GET (tampilkan form), POST (generate PDF)
    URL: http://localhost:5000/generate_pdf
    
    Alur Saat GET Request:
    1. User navigasi ke /generate_pdf
    2. Tampilkan form untuk input data mahasiswa dan nilai
    
    Alur Saat POST Request:
    1. Terima data dari form HTML
    2. Buat dictionary 'data' untuk menyimpan semua informasi akademik
    3. Parse data mahasiswa (NIM, Nama, Prodi, Angkatan)
    4. Loop dan kumpulkan data mata kuliah (maksimal 5 per semester)
    5. Buat temporary file PDF
    6. Panggil generator PDF dengan data yang sudah dikumpulkan
    7. Kirim file PDF ke user untuk didownload
    
    Form Input (POST):
    - nim, nama, prodi, angkatan: Data mahasiswa
    - total_sks, ipk, predikat: Data akademik
    - mk_kode_1...5, mk_nama_1...5, mk_sks_1...5, mk_nilai_1...5, mk_mutu_1...5
    
    Return:
    - GET: HTML form input
    - POST: File PDF (binary) siap didownload
    """
    if request.method == 'POST':
        # ===== STEP 1: PERSIAPAN DICTIONARY UNTUK MENYIMPAN SEMUA DATA =====
        data = {
            'nim': request.form['nim'],                        # NIM/ID Mahasiswa
            'nama': request.form['nama'],                      # Nama mahasiswa
            'prodi': request.form['prodi'],                    # Program studi
            'angkatan': request.form['angkatan'],              # Tahun angkatan
            'semesters': [],                                   # List untuk semester (akan diisi nanti)
            'total_sks': int(request.form['total_sks']),       # Total SKS (konversi ke int)
            'ipk': float(request.form['ipk']),                 # IPK (konversi ke float)
            'predikat': request.form['predikat']               # Predikat (Cum Laude, Sangat Memuaskan, dll)
        }
        
        # ===== STEP 2: PERSIAPAN LIST UNTUK MENYIMPAN DATA MATA KULIAH =====
        mk_list = []  # List untuk mata kuliah dalam satu semester
        
        # ===== STEP 3: LOOP & KUMPULKAN DATA MATA KULIAH (MAX 5 PER SEMESTER) =====
        for i in range(1, 6):  # Loop dari 1 sampai 5
            # Ambil data dari form
            kode = request.form.get(f'mk_kode_{i}')
            nama = request.form.get(f'mk_nama_{i}')
            sks = request.form.get(f'mk_sks_{i}')
            nilai = request.form.get(f'mk_nilai_{i}')
            mutu = request.form.get(f'mk_mutu_{i}')
            
            # ===== STEP 4: VALIDASI - HANYA PROSES JIKA KODE TERISI =====
            if kode:
                # Tambahkan mata kuliah ke list
                mk_list.append({
                    'kode': kode,              # Kode mata kuliah (string)
                    'nama': nama,              # Nama mata kuliah (string)
                    'sks': int(sks),           # SKS (konversi ke int)
                    'nilai': nilai,            # Nilai huruf (string)
                    'mutu': float(mutu)        # Mutu/bobot nilai (konversi ke float)
                })
        
        # ===== STEP 5: TAMBAHKAN DATA SEMESTER KE DALAM DATA UTAMA =====
        # Struktur: data['semesters'] adalah list yang berisi dict semester
        # Setiap semester berisi: semester name dan mata_kuliah list
        data['semesters'].append({
            'semester': 'Semester 1',          # Nama semester (bisa disesuaikan)
            'mata_kuliah': mk_list             # List mata kuliah yang sudah dikumpulkan
        })
        
        # ===== STEP 6: BUAT TEMPORARY FILE UNTUK MENYIMPAN PDF =====
        # tempfile.NamedTemporaryFile: Buat file sementara di system folder temp
        # delete=False: Jangan hapus file setelah ditutup (kita yang hapus nanti)
        # suffix='.pdf': Beri ekstensi .pdf pada file temporary
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            # ===== STEP 7: GENERATE PDF DENGAN MODUL EXTERNAL =====
            # Function generate_transkrip_pdf ada di file generate_transkrip.py
            # Input: data (dictionary) dan nama file temporary
            # Output: File PDF yang sudah dibuat di path tmp.name
            generate_transkrip_pdf(data, tmp.name)
            
            # ===== STEP 8: KIRIM FILE PDF KE USER UNTUK DIDOWNLOAD =====
            # send_file: Fungsi Flask untuk mengirim file ke user
            # as_attachment=True: Browser akan download bukan display
            # download_name: Nama file yang akan muncul saat user download
            return send_file(tmp.name, as_attachment=True, download_name='transkrip.pdf')
    
    # ===== JIKA REQUEST METHOD ADALAH GET =====
    # Tampilkan form input data (kosong)
    return render_template('generate_pdf.html')


# ============================================================================
# ROUTE 4: TAMPILKAN DAFTAR SEMUA MAHASISWA (Student List)
# ============================================================================
@app.route('/students')
def students():
    """
    Menampilkan daftar semua mahasiswa yang ada di database
    
    HTTP Method: GET (only)
    URL: http://localhost:5000/students
    
    Alur:
    1. User klik menu "Students" atau akses /students
    2. Buka database session (koneksi ke database)
    3. Query semua record dari tabel 'Student'
    4. Tutup session database
    5. Kirim list mahasiswa ke template untuk ditampilkan
    
    Database Query:
    - Query semua data Student tanpa filter
    - ORDER BY: tidak ada (default dari database)
    
    Return: HTML halaman daftar mahasiswa dengan table
    """
    # ===== STEP 1: BUKA KONEKSI DATABASE =====
    # Session() dari SQLAlchemy untuk komunikasi dengan database
    session = Session()
    
    # ===== STEP 2: QUERY SEMUA DATA MAHASISWA DARI TABEL 'STUDENT' =====
    # query(Student).all(): Ambil semua record dari tabel Student
    # Return: List of Student objects
    students = session.query(Student).all()
    
    # ===== STEP 3: TUTUP KONEKSI DATABASE =====
    # Penting untuk menutup session agar tidak memory leak
    session.close()
    
    # ===== STEP 4: RENDER TEMPLATE DENGAN DATA MAHASISWA =====
    # Pass students list ke template untuk ditampilkan dalam table
    return render_template('students.html', students=students)


# ============================================================================
# ROUTE 5: TAMBAH MAHASISWA BARU (Add New Student)
# ============================================================================
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """
    Menampilkan form untuk menambah mahasiswa baru ke database
    
    HTTP Method: GET (tampilkan form), POST (simpan ke database)
    URL: http://localhost:5000/add_student
    
    Alur Saat GET Request:
    1. User klik tombol "Add New Student"
    2. Tampilkan form kosong untuk input NIM dan Nama
    
    Alur Saat POST Request:
    1. User submit form dengan data mahasiswa
    2. Buka koneksi database session
    3. Ambil data dari form (id dan name)
    4. Buat object Student baru dengan data tersebut
    5. Tambahkan object ke session (session.add)
    6. Commit perubahan ke database (session.commit)
    7. Tutup session
    8. Redirect ke halaman students (daftar mahasiswa)
    
    Form Input (POST):
    - id: NIM mahasiswa (Primary Key, unik)
    - name: Nama lengkap mahasiswa
    
    Return:
    - GET: HTML form input
    - POST: Redirect ke /students (setelah berhasil simpan)
    """
    if request.method == 'POST':
        # ===== STEP 1: BUKA KONEKSI DATABASE =====
        session = Session()
        
        # ===== STEP 2: AMBIL DATA DARI FORM =====
        # request.form['id']: NIM mahasiswa dari input form
        # request.form['name']: Nama mahasiswa dari input form
        
        # ===== STEP 3: BUAT OBJECT STUDENT BARU =====
        # Student() adalah class dari database.py (SQLAlchemy Model)
        student = Student(id=request.form['id'], name=request.form['name'])
        
        # ===== STEP 4: TAMBAHKAN OBJECT KE SESSION =====
        # session.add(): Tandai object untuk disimpan
        # (belum disimpan ke database, masih di memory)
        session.add(student)
        
        # ===== STEP 5: COMMIT PERUBAHAN KE DATABASE =====
        # session.commit(): Simpan semua perubahan ke database secara permanen
        session.commit()
        
        # ===== STEP 6: TUTUP KONEKSI DATABASE =====
        session.close()
        
        # ===== STEP 7: REDIRECT KE HALAMAN DAFTAR MAHASISWA =====
        # url_for('students'): Generate URL untuk function students()
        # Ini akan merefresh halaman dan menampilkan mahasiswa yang baru ditambah
        return redirect(url_for('students'))
    
    # ===== JIKA REQUEST METHOD ADALAH GET =====
    # Tampilkan form kosong untuk input data baru
    return render_template('add_student.html')


# ============================================================================
# ROUTE 6: TAMPILKAN DAFTAR NILAI MAHASISWA (Student Grades)
# ============================================================================
@app.route('/grades/<student_id>')
def grades(student_id):
    """
    Menampilkan semua nilai mata kuliah untuk satu mahasiswa spesifik
    
    HTTP Method: GET (only)
    URL: http://localhost:5000/grades/<NIM_MAHASISWA>
    Contoh: http://localhost:5000/grades/21001001
    
    Alur:
    1. User klik nama mahasiswa di halaman /students
    2. URL parameter <student_id> berisi NIM mahasiswa
    3. Buka koneksi database
    4. Query data mahasiswa dari tabel Student (filter by ID/NIM)
    5. Query semua nilai dari tabel Grade (filter by student_id)
    6. Tutup koneksi database
    7. Tampilkan data mahasiswa dan tabel nilai-nilainya
    
    URL Parameter:
    - student_id: NIM mahasiswa (Primary Key)
    
    Database Query:
    - SELECT * FROM student WHERE id = <student_id> LIMIT 1
    - SELECT * FROM grade WHERE student_id = <student_id>
    
    Return: HTML halaman nilai dengan tabel mata kuliah
    """
    # ===== STEP 1: BUKA KONEKSI DATABASE =====
    session = Session()
    
    # ===== STEP 2: QUERY DATA MAHASISWA BERDASARKAN NIM =====
    # filter(Student.id == student_id): Cari mahasiswa dengan ID = student_id
    # .first(): Ambil hanya 1 record (karena ID adalah primary key, pasti unik)
    # Return: 1 object Student atau None jika tidak ditemukan
    student = session.query(Student).filter(Student.id == student_id).first()
    
    # ===== STEP 3: QUERY SEMUA NILAI UNTUK MAHASISWA TERSEBUT =====
    # filter(Grade.student_id == student_id): Cari semua nilai dengan student_id
    # .all(): Ambil semua record yang match
    # Return: List of Grade objects
    grades = session.query(Grade).filter(Grade.student_id == student_id).all()
    
    # ===== STEP 4: TUTUP KONEKSI DATABASE =====
    session.close()
    
    # ===== STEP 5: RENDER TEMPLATE DENGAN DATA MAHASISWA & NILAI =====
    # Pass 2 variabel ke template:
    # - student: object mahasiswa (untuk menampilkan nama, NIM, dll)
    # - grades: list nilai (untuk menampilkan tabel nilai)
    return render_template('grades.html', student=student, grades=grades)


# ============================================================================
# ROUTE 7: TAMBAH/EDIT NILAI MAHASISWA (Add New Grade)
# ============================================================================
@app.route('/add_grade/<student_id>', methods=['GET', 'POST'])
def add_grade(student_id):
    """
    Menampilkan form untuk menambah atau edit nilai mata kuliah mahasiswa
    
    HTTP Method: GET (tampilkan form), POST (simpan ke database)
    URL: http://localhost:5000/add_grade/<NIM_MAHASISWA>
    Contoh: http://localhost:5000/add_grade/21001001
    
    Alur Saat GET Request:
    1. User klik tombol "Add Grade" di halaman nilai mahasiswa
    2. Tampilkan form kosong untuk input nilai
    
    Alur Saat POST Request:
    1. User submit form dengan data nilai
    2. Buka koneksi database
    3. Buat object Grade baru dengan data dari form
    4. Simpan data ke tabel Grade dengan informasi audit:
       - Siapa yang mengubah nilai (changed_by)
       - Alasan perubahan (change_reason)
    5. Commit ke database
    6. Tutup session
    7. Redirect ke halaman nilai mahasiswa untuk melihat perubahan
    
    URL Parameter:
    - student_id: NIM mahasiswa
    
    Form Input (POST):
    - course_id: Kode mata kuliah (contoh: IF101)
    - grade: Nilai huruf (A/B/C/D/E)
    - changed_by: Nama user yang input/mengubah nilai
    - reason: Alasan mengapa nilai diubah
    
    Database Tracking (Audit Trail):
    - Setiap perubahan nilai dicatat: siapa dan alasannya
    - Untuk keamanan dan akuntabilitas data
    
    Return:
    - GET: HTML form input
    - POST: Redirect ke /grades/<student_id> (lihat nilai yang baru disimpan)
    """
    if request.method == 'POST':
        # ===== STEP 1: BUKA KONEKSI DATABASE =====
        session = Session()
        
        # ===== STEP 2: BUAT OBJECT GRADE BARU =====
        # Grade() adalah class dari database.py (SQLAlchemy Model)
        # Kumpulkan data dari form HTML:
        grade = Grade(
            student_id=student_id,                          # NIM dari URL parameter
            course_id=request.form['course_id'],            # Kode mata kuliah
            grade=request.form['grade'],                    # Nilai huruf (A-E)
            changed_by=request.form['changed_by'],          # Nama yang input (untuk audit)
            change_reason=request.form['reason']            # Alasan perubahan (untuk audit)
        )
        
        # ===== STEP 3: TAMBAHKAN OBJECT KE SESSION =====
        # Tandai object untuk disimpan ke database
        session.add(grade)
        
        # ===== STEP 4: COMMIT PERUBAHAN KE DATABASE =====
        # Simpan record Grade baru + informasi audit trail
        session.commit()
        
        # ===== STEP 5: TUTUP KONEKSI DATABASE =====
        session.close()
        
        # ===== STEP 6: REDIRECT KE HALAMAN NILAI MAHASISWA =====
        # Menampilkan daftar nilai terbaru termasuk yang baru ditambah
        return redirect(url_for('grades', student_id=student_id))
    
    # ===== JIKA REQUEST METHOD ADALAH GET =====
    # Tampilkan form kosong untuk input nilai baru
    # Pass student_id ke template agar tahu mahasiswa mana yang ditambah nilainya
    return render_template('add_grade.html', student_id=student_id)


# ============================================================================
# ROUTE 8: TAMPILKAN RIWAYAT PERUBAHAN NILAI (Audit Trail / History)
# ============================================================================
@app.route('/history/<student_id>')
def history(student_id):
    """
    Menampilkan riwayat perubahan semua nilai untuk satu mahasiswa
    Fitur Audit Trail - tracking siapa mengubah apa dan kapan
    
    HTTP Method: GET (only)
    URL: http://localhost:5000/history/<NIM_MAHASISWA>
    Contoh: http://localhost:5000/history/21001001
    
    Alur:
    1. User klik menu "View History" untuk mahasiswa tertentu
    2. URL parameter <student_id> berisi NIM mahasiswa
    3. Panggil function get_student_grade_history() dari database.py
    4. Function ini query tabel grade_history dan return data history
    5. Tampilkan riwayat dalam tabel dengan kolom:
       - Timestamp (kapan perubahan)
       - Nilai lama → Nilai baru
       - Siapa yang mengubah (audit trail)
       - Alasan perubahan
    
    URL Parameter:
    - student_id: NIM mahasiswa
    
    Fungsi Audit Trail:
    - Mencatat setiap perubahan nilai
    - Siapa yang mengubah
    - Kapan diubah
    - Alasan perubahan
    - Nilai lama vs nilai baru
    
    Tujuan: Transparansi & Akuntabilitas data akademik
    
    Return: HTML halaman history dengan tabel perubahan nilai
    """
    # ===== STEP 1: QUERY RIWAYAT PERUBAHAN DARI DATABASE =====
    # get_student_grade_history() adalah function di database.py
    # Parameter: student_id (NIM mahasiswa)
    # Return: List of history records dengan detail perubahan nilai
    # Contoh data:
    # [
    #   {
    #     'timestamp': '2024-01-15 10:30:00',
    #     'old_grade': 'B',
    #     'new_grade': 'A',
    #     'changed_by': 'Dr. Ari Sudarso',
    #     'reason': 'Perbaikan nilai dari review ulang',
    #     'course_id': 'IF101'
    #   },
    #   {...},
    #   ...
    # ]
    history = get_student_grade_history(student_id)
    
    # ===== STEP 2: RENDER TEMPLATE DENGAN DATA HISTORY =====
    # Pass 2 variabel ke template:
    # - history: list data perubahan nilai (untuk tabel history)
    # - student_id: NIM (untuk menampilkan judul atau navigasi)
    return render_template('history.html', history=history, student_id=student_id)


# ============================================================================
# ENTRY POINT - JALANKAN APLIKASI
# ============================================================================
if __name__ == '__main__':
    """
    Entry point aplikasi Flask
    
    __name__: Variabel special Python yang berisi nama module saat ini
    - Jika file dijalankan langsung: __name__ == '__main__'
    - Jika file di-import oleh file lain: __name__ == nama module file
    
    Fungsi: Memastikan app.run() hanya jalan ketika file dijalankan langsung
    (bukan saat file di-import untuk testing atau keperluan lain)
    
    Cara Jalankan:
    $ python app.py
    
    Output:
    * Running on http://127.0.0.1:5000
    * Debug mode: ON
    """
    # ===== JALANKAN FLASK APPLICATION =====
    # app.run(): Start Flask development server
    # debug=True: 
    #   - Auto-reload saat ada perubahan kode
    #   - Detailed error messages
    #   - Interactive debugger untuk error handling
    # 
    # CATATAN: debug=True untuk development saja, 
    #          ganti debug=False saat production
    app.run(debug=True)