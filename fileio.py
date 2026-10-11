# fileio.py - semua operasi baca/tulis/tambah file
import os
from .models import Barang
from .validasi import DataTidakValidError

DATA_AWAL = (
    "B001;Beras 5kg;65000;10;Pangan\n"
    "B002;Minyak Goreng 2L;38000;3;Pangan\n"
    "B003;Sabun Mandi;4500;40;Kebersihan\n"
    "B004;Kopi Sachet;abc;25;Minuman\n"        # rusak: harga bukan angka
    "B005;;5000;8;Minuman\n"                     # rusak: nama kosong
    "B006;Teh Botol;5000;-4;Minuman\n"           # rusak: stok negatif
    "B007;Gula 1kg;16000;4;Pangan\n"
    "B008;Mie Instan;3500;120;Pangan\n"
)


def buat_file_data(path):
    """Mode 'x': membuat file pertama kali, tidak menimpa file yang sudah ada."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8") as file:
            file.write(DATA_AWAL)
        print(f"[INFO] File '{path}' berhasil dibuat")
        return True
    except FileExistsError:
        print(f"[INFO] File '{path}' sudah ada, tidak ditimpa")
        return False


def tambah_data(path, barang):
    """Mode 'a': menambah satu barang di akhir file tanpa menghapus data lama."""
    with open(path, "a", encoding="utf-8") as file:
        file.write(barang.ke_baris())


def baca_data(path):
    """Mode 'r': baca iteratif. Baris rusak dilewati, bukan menghentikan program.
    Mengembalikan (list_barang, list_baris_dilewati)."""
    hasil, dilewati = [], []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for no, baris in enumerate(file, start=1):   # iteratif
                if not baris.strip():
                    continue
                try:
                    hasil.append(Barang.dari_baris(baris))
                except DataTidakValidError as e:         # baris rusak -> lewati
                    dilewati.append((no, str(e)))
    except FileNotFoundError:
        print(f"[ERROR] File '{path}' belum ada. Pilih menu buat file data dulu.")
    return hasil, dilewati


def tulis_laporan(path, teks):
    """Mode 'w': menulis laporan (isi lama diganti dengan laporan terbaru)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(teks)


def tampilkan_file(path):
    """Tampilkan isi file ke layar."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"[ERROR] File '{path}' tidak ditemukan")
