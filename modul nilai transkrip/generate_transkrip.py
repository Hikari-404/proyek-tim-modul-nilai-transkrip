from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_transkrip_pdf(data, output_path='transkrip.pdf'):
    """
    Generate transkrip PDF menggunakan ReportLab.

    Args:
        data (dict): Data mahasiswa dan nilai.
        output_path (str): Path untuk file PDF output.
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    # Logo (skip jika tidak ada)
    logo_path = data.get('logo_url')
    if logo_path:
        try:
            logo = Image(logo_path, width=1*inch, height=1*inch)
            elements.append(logo)
        except:
            pass  # Skip jika tidak ada logo

    title_style = ParagraphStyle(name='Title', fontSize=24, alignment=1, fontName='Helvetica-Bold')
    title = Paragraph("TRANSKRIP AKADEMIK", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Biodata
    biodata_data = [
        ['NIM:', data['nim'], 'Program Studi:', data['prodi']],
        ['Nama:', data['nama'], 'Angkatan:', data['angkatan']]
    ]
    biodata_table = Table(biodata_data, colWidths=[80, 150, 100, 150])
    biodata_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(biodata_table)
    elements.append(Spacer(1, 20))

    # Per semester
    for sem in data['semesters']:
        sem_title = Paragraph(sem['semester'], styles['Heading2'])
        elements.append(sem_title)
        elements.append(Spacer(1, 10))

        mk_data = [['Kode MK', 'Nama MK', 'SKS', 'Nilai', 'Mutu']]
        for mk in sem['mata_kuliah']:
            mk_data.append([mk['kode'], mk['nama'], str(mk['sks']), mk['nilai'], str(mk['mutu'])])

        mk_table = Table(mk_data, colWidths=[60, 200, 40, 50, 50])
        mk_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (1,1), (1,-1), 'LEFT'),  # Nama MK left align
        ]))
        elements.append(mk_table)
        elements.append(Spacer(1, 20))

    # Footer
    footer_data = [
        ['Total SKS:', str(data['total_sks']), 'IPK:', f"{data['ipk']:.2f}", 'Predikat:', data['predikat']]
    ]
    footer_table = Table(footer_data, colWidths=[80, 50, 50, 50, 80, 100])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(footer_table)
    elements.append(Spacer(1, 40))

    # TTD Dekan (skip jika tidak ada)
    ttd_path = data.get('ttd_dekan')
    if ttd_path:
        try:
            ttd = Image(ttd_path, width=2*inch, height=1*inch)
            elements.append(ttd)
        except:
            pass
    dekan_style = ParagraphStyle(name='Dekan', alignment=1)
    dekan = Paragraph("Dekan Fakultas<br/><br/><br/>Nama Dekan", dekan_style)
    elements.append(dekan)

    doc.build(elements)
    print(f"Transkrip PDF berhasil dibuat: {output_path}")

# Contoh data (ganti dengan data dinamis)
sample_data = {
    'nim': '12345678',
    'nama': 'John Doe',
    'prodi': 'Teknik Informatika',
    'angkatan': '2020',
    # 'logo_url': 'logo.png',  # Uncomment jika ada file logo
    'semesters': [
        {
            'semester': 'Semester 1',
            'mata_kuliah': [
                {'kode': 'TI101', 'nama': 'Pemrograman Dasar', 'sks': 3, 'nilai': 'A', 'mutu': 12.0},
                {'kode': 'TI102', 'nama': 'Matematika Diskrit', 'sks': 3, 'nilai': 'B', 'mutu': 9.0},
            ]
        },
        {
            'semester': 'Semester 2',
            'mata_kuliah': [
                {'kode': 'TI201', 'nama': 'Struktur Data', 'sks': 3, 'nilai': 'A', 'mutu': 12.0},
                {'kode': 'TI202', 'nama': 'Basis Data', 'sks': 3, 'nilai': 'C', 'mutu': 6.0},
            ]
        },
    ],
    'total_sks': 12,
    'ipk': 3.75,
    'predikat': 'Cum Laude',
    # 'ttd_dekan': 'ttd.png'  # Uncomment jika ada file ttd
}

if __name__ == '__main__':
    generate_transkrip_pdf(sample_data)