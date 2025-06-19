import random

# Kelompok dan waktu kosongnya
kelompok_mahasiswa = {
    "Kelompok1": [("Senin", "08:00"), ("Rabu", "10:00")],
    "Kelompok2": [("Selasa", "09:00"), ("Jumat", "13:00")],
    "Kelompok3": [("Kamis", "08:00"), ("Senin", "10:00")],
    "Kelompok4": [("Rabu", "13:00"), ("Kamis", "09:00")],
    "Kelompok5": [("Senin", "09:00"), ("Jumat", "08:00")],
    "Kelompok6": [("Selasa", "13:00"), ("Kamis", "14:00")],
    "Kelompok7": [("Rabu", "10:00"), ("Jumat", "10:00")],
    "Kelompok8": [("Senin", "14:00"), ("Selasa", "10:00")],
    "Kelompok9": [("Kamis", "13:00"), ("Jumat", "09:00")],
    "Kelompok10": [("Selasa", "10:00"), ("Kamis", "08:00")]
}

# Jadwal asisten: 13 slot total (11 cocok, 2 dummy)
jadwal_asisten = [
    ("Senin", "08:00"), ("Senin", "10:00"), ("Senin", "14:00"),
    ("Selasa", "09:00"), ("Selasa", "10:00"), ("Selasa", "13:00"),
    ("Rabu", "10:00"), ("Rabu", "13:00"),
    ("Kamis", "08:00"), ("Kamis", "13:00"),
    ("Jumat", "08:00"),  # semua di atas bisa digunakan
    ("Jumat", "14:00"),  # dummy
    ("Rabu", "08:00")    # dummy
]

# Buat jadwal acak tanpa bentrok
def buat_jadwal():
    jadwal = {}
    dipakai = set()
    for kelompok, waktu_kosong in kelompok_mahasiswa.items():
        pilihan = list(set(waktu_kosong) & set(jadwal_asisten) - dipakai)
        if pilihan:
            waktu = random.choice(pilihan)
            jadwal[kelompok] = waktu
            dipakai.add(waktu)
        else:
            return None
    return jadwal

# Hitung fitness
def hitung_fitness(jadwal):
    return sum(1 for k in jadwal if jadwal[k] is not None) if jadwal else 0

# Genetic Algorithm
def genetic_algorithm(generasi=200):
    populasi = []
    while len(populasi) < 10:
        jadwal = buat_jadwal()
        if jadwal:
            populasi.append(jadwal)

    for _ in range(generasi):
        populasi.sort(key=hitung_fitness, reverse=True)
        if hitung_fitness(populasi[0]) == len(kelompok_mahasiswa):
            break

        induk1, induk2 = populasi[0], populasi[1]
        anak = {}
        dipakai = set()

        for k in induk1:
            prefer = induk1[k] if random.random() < 0.5 else induk2[k]
            pilihan_valid = (set(kelompok_mahasiswa[k]) & set(jadwal_asisten)) - dipakai
            if prefer in pilihan_valid:
                anak[k] = prefer
                dipakai.add(prefer)
            else:
                alternatif = list(pilihan_valid)
                if alternatif:
                    anak[k] = random.choice(alternatif)
                    dipakai.add(anak[k])
                else:
                    anak[k] = None

        if hitung_fitness(anak) == len(kelompok_mahasiswa):
            return anak
        populasi[-1] = anak
    return populasi[0]

# Cek slot asisten yang tidak dipakai
def cek_jadwal_asisten_tidak_terpakai(jadwal, kelompok_mahasiswa, jadwal_asisten):
    waktu_terpakai = set(jadwal.values())
    tidak_terpakai = set(jadwal_asisten) - waktu_terpakai
    hasil_cek = []
    for waktu in tidak_terpakai:
        cocok_dengan = [k for k in kelompok_mahasiswa if waktu in kelompok_mahasiswa[k]]
        if cocok_dengan:
            alasan = "Tidak terpakai karena waktu lain sudah dipilih oleh kelompok yang cocok"
        else:
            alasan = "Tidak terpakai karena tidak ada kelompok yang tersedia di waktu ini"
        hasil_cek.append((waktu, alasan))
    return hasil_cek

# Jalankan program
hasil = genetic_algorithm()
print("📅 Jadwal Praktikum Terbaik:")
for kelompok, waktu in hasil.items():
    print(f"{kelompok}: Hari {waktu[0]}, Jam {waktu[1]}")

# Tampilkan slot asisten yang tidak digunakan
sisa = cek_jadwal_asisten_tidak_terpakai(hasil, kelompok_mahasiswa, jadwal_asisten)
print("\n⛔ Waktu Asisten yang Tidak Terpakai dan Alasannya:")
for (hari, jam), alasan in sisa:
    print(f"- Hari {hari}, Jam {jam} → {alasan}")
