import unittest
from ipk_calculator import calculate_ipk

class TestIPK(unittest.TestCase):

    def test_mahasiswa_sempurna(self):
        """Test mahasiswa dengan nilai sempurna (semua A)"""
        nilai = [
            {'kode_mk': 'MK1', 'sks': 3, 'nilai_huruf': 'A'},
            {'kode_mk': 'MK2', 'sks': 2, 'nilai_huruf': 'A'},
        ]
        self.assertEqual(calculate_ipk(nilai), 4.0)

    def test_mk_diulang(self):
        """Test mahasiswa dengan MK diulang, ambil nilai tertinggi"""
        nilai = [
            {'kode_mk': 'MK1', 'sks': 3, 'nilai_huruf': 'B'},
            {'kode_mk': 'MK1', 'sks': 3, 'nilai_huruf': 'A'},  # ulang, ambil A
            {'kode_mk': 'MK2', 'sks': 2, 'nilai_huruf': 'C'},
        ]
        # Perhitungan: (3*4.0 + 2*2.0) / (3+2) = 16/5 = 3.2
        self.assertEqual(calculate_ipk(nilai), 3.2)

    def test_semester_awal_belum_ada_nilai(self):
        """Test mahasiswa semester awal belum ada nilai"""
        self.assertEqual(calculate_ipk([]), 0.0)

    def test_tidak_lulus(self):
        """Test dengan MK yang tidak lulus (E), tidak dihitung"""
        nilai = [
            {'kode_mk': 'MK1', 'sks': 3, 'nilai_huruf': 'E'},
            {'kode_mk': 'MK2', 'sks': 2, 'nilai_huruf': 'A'},
        ]
        # Hanya MK2 yang dihitung: 2*4.0 / 2 = 4.0
        self.assertEqual(calculate_ipk(nilai), 4.0)

if __name__ == '__main__':
    unittest.main()