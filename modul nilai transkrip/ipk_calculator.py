from collections import defaultdict

def calculate_ipk(nilai_list):
    """
    Menghitung IPK berdasarkan aturan:
    IPK = Σ(SKS × Nilai Angka) / Σ(SKS)
    Hanya hitung MK yang sudah lulus (nilai ≥ D, yaitu nilai angka ≥ 1.0)
    Jika MK diulang, ambil nilai tertinggi
    Jika belum ada nilai, return 0.0
    """
    if not nilai_list:
        return 0.0

    # Mapping nilai huruf ke angka
    nilai_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'E': 0.0}

    # Group by kode_mk, ambil max nilai untuk yang lulus
    max_nilai = defaultdict(float)
    sks_per_kode = {}

    for item in nilai_list:
        kode = item['kode_mk']
        huruf = item['nilai_huruf']
        angka = nilai_map.get(huruf, 0.0)
        sks = item['sks']

        if kode not in sks_per_kode:
            sks_per_kode[kode] = sks

        if angka >= 1.0:  # lulus
            max_nilai[kode] = max(max_nilai[kode], angka)

    # Hitung total
    total_sks_nilai = 0.0
    total_sks = 0.0

    for kode, nilai in max_nilai.items():
        sks = sks_per_kode[kode]
        total_sks_nilai += sks * nilai
        total_sks += sks

    if total_sks == 0:
        return 0.0

    return total_sks_nilai / total_sks