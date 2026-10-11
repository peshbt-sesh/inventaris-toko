# main.py - file utama: mengimpor package dan menjalankan program
import sys
from inventaris import fileio, processing, testing
from inventaris.models import Barang
from inventaris.validasi import DataTidakValidError

FILE_DATA = "data/barang.txt"
FILE_LAPORAN = "output/laporan_inventaris.txt"


def tambah_barang_baru():
    """Input dari user -> validasi -> simpan (mode 'a')."""
    try:
        kode = input("Kode   : ")
        nama = input("Nama   : ")
        harga = int(input("Harga  : "))     
        stok = int(input("Stok   : "))
        kategori = input("Kategori: ") or "Umum"
        barang = Barang(kode, nama, harga, stok, kategori=kategori)
        fileio.tambah_data(FILE_DATA, barang)
        print("Barang berhasil ditambahkan")
    except ValueError:
        print("[ERROR] Harga dan stok harus berupa angka")
    except DataTidakValidError as e:
        print("[ERROR]", e)


def buat_laporan():
    daftar, dilewati = fileio.baca_data(FILE_DATA)
    if not daftar and not dilewati:
        return
    teks = processing.buat_laporan(daftar, dilewati, batas_stok=5)
    fileio.tulis_laporan(FILE_LAPORAN, teks)    
    fileio.tampilkan_file(FILE_LAPORAN)


def menu():
    while True:
        print("\n=== INVENTARIS TOKO ===")
        print("1. Buat file data awal   2. Tambah barang")
        print("3. Lihat data            4. Buat laporan")
        print("5. Jalankan pengujian    0. Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            fileio.buat_file_data(FILE_DATA)
        elif pilih == "2":
            tambah_barang_baru()
        elif pilih == "3":
            daftar, dilewati = fileio.baca_data(FILE_DATA)
            for b in processing.urutkan_barang(daftar, berdasarkan="nama"):
                print(f"{b.kode} | {b.nama:<18} | Rp{b.harga:>7,} | stok {b.stok:>3} | {b.kategori}")
            print(f"({len(dilewati)} baris rusak dilewati)")
        elif pilih == "4":
            buat_laporan()
        elif pilih == "5":
            testing.jalankan()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak dikenal")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        testing.jalankan()
    else:
        menu()
