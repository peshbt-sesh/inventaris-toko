# validasi.py - pengecekan input dan data


class DataTidakValidError(Exception):
    """Exception buatan sendiri untuk data barang yang tidak valid."""


def validasi_field_kosong(nilai, nama_field):
    """Raise error jika field kosong."""
    if str(nilai).strip() == "":
        raise DataTidakValidError(f"Field '{nama_field}' tidak boleh kosong")


def validasi_tidak_negatif(nilai, nama_field):
    """Raise error jika angka bernilai negatif."""
    if nilai < 0:
        raise DataTidakValidError(f"'{nama_field}' tidak boleh negatif ({nilai})")


def ke_integer(teks, nama_field):
    """Konversi teks ke int; ValueError diubah menjadi pesan yang jelas."""
    try:
        return int(teks)
    except ValueError:
        raise DataTidakValidError(f"'{nama_field}' bukan angka: '{teks}'")


# Pengujian lokal: hanya jalan bila file ini dieksekusi langsung
if __name__ == "__main__":
    assert ke_integer("10", "stok") == 10
    try:
        ke_integer("abc", "stok")
    except DataTidakValidError as e:
        print("OK, error tertangkap:", e)
    print("Pengujian lokal validasi.py selesai")
