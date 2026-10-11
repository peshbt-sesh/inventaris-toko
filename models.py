# models.py - dua class: Barang dan Inventaris
from .validasi import (DataTidakValidError, validasi_field_kosong,
                       validasi_tidak_negatif, ke_integer)


class Barang:
    def __init__(self, kode, nama, harga, stok, **atribut):
        """**atribut: atribut tambahan yang bervariasi (mis. kategori, supplier)."""
        validasi_field_kosong(kode, "kode")
        validasi_field_kosong(nama, "nama")
        validasi_tidak_negatif(harga, "harga")
        validasi_tidak_negatif(stok, "stok")
        self.kode, self.nama, self.harga, self.stok = kode, nama, harga, stok
        self.atribut = atribut
        self.kategori = atribut.get("kategori", "Umum")

    def total_nilai(self):
        """Nilai persediaan = harga x stok."""
        return self.harga * self.stok

    def ke_baris(self):
        """Ubah objek menjadi satu baris teks untuk disimpan ke file."""
        return f"{self.kode};{self.nama};{self.harga};{self.stok};{self.kategori}\n"

    @classmethod
    def dari_baris(cls, baris):
        """Buat Barang dari baris 'kode;nama;harga;stok;kategori'."""
        bagian = baris.strip().split(";")
        if len(bagian) != 5:
            raise DataTidakValidError(f"Jumlah kolom salah ({len(bagian)}), harusnya 5")
        kode, nama, harga, stok, kategori = bagian
        return cls(kode, nama, ke_integer(harga, "harga"),
                   ke_integer(stok, "stok"), kategori=kategori)


class Inventaris:
    def __init__(self):
        self.daftar = []

    def tambah(self, barang):
        """Tambah barang; kode tidak boleh kembar."""
        if self.cari(barang.kode):
            raise DataTidakValidError(f"Kode {barang.kode} sudah ada")
        self.daftar.append(barang)

    def cari(self, kode):
        """Cari barang berdasarkan kode, None jika tidak ada."""
        for b in self.daftar:
            if b.kode == kode:
                return b
        return None

    def hapus(self, kode):
        barang = self.cari(kode)
        if barang is None:
            raise DataTidakValidError(f"Kode {kode} tidak ditemukan")
        self.daftar.remove(barang)

    def total_nilai(self):
        return sum(b.total_nilai() for b in self.daftar)
