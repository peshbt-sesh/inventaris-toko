# testing.py - pengujian dengan unittest (jalankan: python main.py test)
import os
import tempfile
import unittest
from .models import Barang, Inventaris
from .validasi import DataTidakValidError, ke_integer
from . import processing, fileio


class TestValidasi(unittest.TestCase):
    def test_ke_integer_valid(self):
        self.assertEqual(ke_integer("12", "stok"), 12)

    def test_ke_integer_tidak_valid(self):
        with self.assertRaises(DataTidakValidError):
            ke_integer("abc", "stok")

    def test_barang_stok_negatif(self):
        with self.assertRaises(DataTidakValidError):
            Barang("B1", "Gula", 1000, -1)

    def test_barang_nama_kosong(self):
        with self.assertRaises(DataTidakValidError):
            Barang("B1", "", 1000, 1)


class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.daftar = [Barang("B1", "A", 1000, 10, kategori="X"),
                       Barang("B2", "B", 5000, 2, kategori="Y"),
                       Barang("B3", "C", 3000, 7, kategori="X")]

    def test_rata_rata(self):
        self.assertAlmostEqual(processing.hitung_rata_rata(1000, 5000, 3000), 3000)

    def test_rata_rata_kosong_assert(self):
        with self.assertRaises(AssertionError):
            processing.hitung_rata_rata()

    def test_stok_menipis(self):
        hasil = processing.stok_menipis(self.daftar, batas=5)
        self.assertEqual([b.kode for b in hasil], ["B2"])

    def test_urutkan(self):
        hasil = processing.urutkan_barang(self.daftar, berdasarkan="harga", terbalik=True)
        self.assertEqual(hasil[0].kode, "B2")

    def test_total_per_kategori(self):
        self.assertEqual(processing.total_per_kategori(self.daftar), {"X": 31000, "Y": 10000})


class TestInventaris(unittest.TestCase):
    def test_kode_kembar(self):
        inv = Inventaris()
        inv.tambah(Barang("B1", "A", 1000, 1))
        with self.assertRaises(DataTidakValidError):
            inv.tambah(Barang("B1", "B", 2000, 2))


class TestFileIO(unittest.TestCase):
    def test_baca_lewati_baris_rusak(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "d.txt")
            with open(path, "w") as f:
                f.write("B1;A;1000;5;X\nB2;B;abc;5;X\n")
            data, dilewati = fileio.baca_data(path)
            self.assertEqual((len(data), len(dilewati)), (1, 1))

    def test_file_tidak_ada(self):
        data, dilewati = fileio.baca_data("tidak_ada.txt")
        self.assertEqual(data, [])

    def test_mode_x_tidak_menimpa(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "d.txt")
            self.assertTrue(fileio.buat_file_data(path))
            self.assertFalse(fileio.buat_file_data(path))


def jalankan():
    unittest.main(module="inventaris.testing", argv=["testing", "-v"], exit=False)
