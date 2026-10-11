# processing.py - perhitungan dan analisis data


def hitung_rata_rata(*angka):
    """*args: jumlah angka fleksibel. assert memastikan minimal ada satu angka."""
    assert len(angka) > 0, "Minimal satu angka diperlukan"
    return sum(angka) / len(angka)


def stok_menipis(daftar, batas=5):
    """filter + lambda: barang dengan stok <= batas."""
    return list(filter(lambda b: b.stok <= batas, daftar))


def urutkan_barang(daftar, berdasarkan="harga", terbalik=False):
    """sorted + lambda sebagai key; atribut yang diurutkan bisa dipilih."""
    return sorted(daftar, key=lambda b: getattr(b, berdasarkan), reverse=terbalik)


def total_per_kategori(daftar):
    """Jumlah nilai persediaan per kategori (dictionary)."""
    hasil = {}
    for b in daftar:
        hasil[b.kategori] = hasil.get(b.kategori, 0) + b.total_nilai()
    return hasil


def buat_laporan(daftar, dilewati, batas_stok=5):
    """Susun teks laporan lengkap."""
    baris = ["LAPORAN INVENTARIS TOKO", "=" * 40]
    baris.append(f"Jumlah barang valid : {len(daftar)}")
    baris.append(f"Baris data dilewati : {len(dilewati)}")
    for no, alasan in dilewati:
        baris.append(f"  - baris {no}: {alasan}")
    if daftar:
        rata = hitung_rata_rata(*[b.harga for b in daftar])
        baris.append(f"Rata-rata harga     : Rp{rata:,.0f}")
        baris.append(f"Total nilai stok    : Rp{sum(b.total_nilai() for b in daftar):,}")
        termahal = urutkan_barang(daftar, berdasarkan="harga", terbalik=True)[0]
        baris.append(f"Barang termahal     : {termahal.nama} (Rp{termahal.harga:,})")
        baris.append("Nilai per kategori  :")
        for kat, nilai in total_per_kategori(daftar).items():
            baris.append(f"  - {kat}: Rp{nilai:,}")
        baris.append(f"Stok menipis (<= {batas_stok}):")
        for b in stok_menipis(daftar, batas=batas_stok):
            baris.append(f"  - {b.nama} (sisa {b.stok})")
    return "\n".join(baris) + "\n"
