"""
seed_questions.py — Bank soal Matematika Kelas 1 SD
Referensi:
- Buku Matematika untuk SD/MI Kelas I (HaiBunda)
- Bimbel Brilian Soal Kelas 1 SD Kurikulum Merdeka
- Buku Jago Matika SD/MI Kelas 1 (Hurriyah Badriyah)
- ATP Matematika Fase A Kemendikbud
Prinsip: soal cerita pendek, benda konkret, bahasa sangat sederhana
"""

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from database import init_db, insert_question, count_questions, get_conn

init_db()

QUESTIONS = [

    # ── KC-B01: Mengenal bilangan 1–10 ───────────────────────────────────────
    ("KC-B01","Angka 5 dibaca ...","tiga","empat","lima","enam","c",1),
    ("KC-B01","Angka 8 dibaca ...","enam","tujuh","delapan","sembilan","c",1),
    ("KC-B01","Angka 3 dibaca ...","satu","dua","tiga","empat","c",1),
    ("KC-B01","Bilangan TUJUH ditulis ...","5","6","7","8","c",1),
    ("KC-B01","Bilangan SEMBILAN ditulis ...","7","8","9","10","c",1),
    ("KC-B01","Angka 2 dibaca ...","satu","dua","tiga","empat","b",1),
    ("KC-B01","Bilangan EMPAT ditulis ...","2","3","4","5","c",1),

    # ── KC-B02: Membilang 1–10 ────────────────────────────────────────────────
    ("KC-B02","Hitung! 🍎🍎🍎","2","3","4","5","b",1),
    ("KC-B02","Hitung! 🐥🐥🐥🐥🐥","3","4","5","6","c",1),
    ("KC-B02","Hitung! ⭐⭐⭐⭐⭐⭐⭐","5","6","7","8","c",1),
    ("KC-B02","Hitung! 🎈🎈","1","2","3","4","b",1),
    ("KC-B02","Hitung! 🐠🐠🐠🐠🐠🐠🐠🐠","6","7","8","9","c",1),
    ("KC-B02","Hitung! 🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸","8","9","10","11","c",1),

    # ── KC-B03: Mengenal bilangan 11–20 ──────────────────────────────────────
    ("KC-B03","Angka 11 dibaca ...","sepuluh","sebelas","dua belas","tiga belas","b",1),
    ("KC-B03","Angka 14 dibaca ...","tiga belas","empat belas","lima belas","enam belas","b",1),
    ("KC-B03","Angka 17 dibaca ...","enam belas","tujuh belas","delapan belas","sembilan belas","b",1),
    ("KC-B03","Angka 20 dibaca ...","delapan belas","sembilan belas","dua puluh","dua belas","c",1),
    ("KC-B03","DUA BELAS ditulis ...","10","11","12","13","c",1),
    ("KC-B03","SEMBILAN BELAS ditulis ...","17","18","19","20","c",1),

    # ── KC-B04: Membilang 11–20 ───────────────────────────────────────────────
    ("KC-B04","Hitung! 🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊","10","11","12","13","c",2),
    ("KC-B04","Di keranjang ada 10 telur. Ibu menaruh 5 telur lagi. Ada berapa telur sekarang?","13","14","15","16","c",2),
    ("KC-B04","Hitung! ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️","12","13","14","15","c",2),
    ("KC-B04","Budi punya 10 kelereng. Ayah memberi 7 kelereng lagi. Ada berapa kelereng sekarang?","15","16","17","18","c",2),
    ("KC-B04","Hitung! 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟","16","17","18","19","c",2),

    # ── KC-B05: Membandingkan dua bilangan ───────────────────────────────────
    ("KC-B05","Siti punya 7 permen. Ani punya 5 permen. Siapa yang punya lebih banyak?","Ani","Siti","sama banyak","tidak tahu","b",1),
    ("KC-B05","Mana yang lebih besar, 9 atau 6?","6","9","sama besar","tidak tahu","b",1),
    ("KC-B05","Mana yang lebih kecil, 4 atau 8?","8","4","sama kecil","tidak tahu","b",1),
    ("KC-B05","Di kelas ada 12 anak laki-laki dan 15 anak perempuan. Mana yang lebih banyak?","anak laki-laki","sama banyak","anak perempuan","tidak tahu","c",2),
    ("KC-B05","3 ... 3. Isi titik-titik dengan tanda yang tepat!","lebih dari (>)","kurang dari (<)","sama dengan (=)","tidak bisa dibanding","c",1),
    ("KC-B05","Mana yang lebih kecil, 11 atau 15?","15","sama kecil","11","tidak tahu","c",2),

    # ── KC-B06: Urutan bilangan ───────────────────────────────────────────────
    ("KC-B06","Angka setelah 7 adalah ...","6","8","9","10","b",1),
    ("KC-B06","Angka sebelum 10 adalah ...","8","9","11","12","b",1),
    ("KC-B06","Urutkan dari kecil ke besar: 5, 2, 8, 1","1 2 5 8","8 5 2 1","5 2 8 1","2 5 1 8","a",1),
    ("KC-B06","Angka yang ada di antara 6 dan 8 adalah ...","5","7","9","10","b",1),
    ("KC-B06","Angka setelah 15 adalah ...","13","14","16","17","c",2),
    ("KC-B06","Urutkan dari besar ke kecil: 4, 9, 2, 7","2 4 7 9","9 7 4 2","4 9 2 7","7 4 9 2","b",1),

    # ── KC-B07: Nilai tempat satuan ───────────────────────────────────────────
    # Referensi: Bimbel Brilian "1 puluhan dan X satuan"
    ("KC-B07","Pada angka 13, angka 3 ada di tempat ...","puluhan","satuan","ratusan","ribuan","b",2),
    ("KC-B07","Pada angka 18, angka 8 ada di tempat ...","puluhan","ratusan","satuan","ribuan","c",2),
    ("KC-B07","Pada angka 20, angka 0 ada di tempat ...","satuan","puluhan","ratusan","ribuan","a",2),
    ("KC-B07","Angka 16 terdiri dari 1 puluhan dan ... satuan","4","5","6","7","c",2),
    ("KC-B07","Angka 19 terdiri dari 1 puluhan dan ... satuan","7","8","9","10","c",2),
    ("KC-B07","Angka berapa yang ada di tempat satuan pada bilangan 15?","1","5","15","0","b",2),

    # ── KC-B08: Nilai tempat puluhan ──────────────────────────────────────────
    ("KC-B08","Pada angka 17, angka 1 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2),
    ("KC-B08","Pada angka 20, angka 2 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2),
    ("KC-B08","1 puluhan dan 3 satuan = ...","31","13","3","10","b",2),
    ("KC-B08","1 puluhan dan 7 satuan = ...","71","17","7","10","b",2),
    ("KC-B08","1 puluhan dan 9 satuan = ...","91","19","9","10","b",2),
    ("KC-B08","Angka berapa yang ada di tempat puluhan pada bilangan 16?","6","16","0","1","d",2),

    # ── KC-O01: Konsep penjumlahan ────────────────────────────────────────────
    # Referensi: Soal cerita HaiBunda & Kumparan
    ("KC-O01","Dito punya 2 kue. Ibu memberi 1 kue lagi. Sekarang Dito punya berapa kue?","2","3","4","1","b",1),
    ("KC-O01","Ada 3 anak laki-laki dan 2 anak perempuan. Ada berapa anak semuanya?","3","4","5","6","c",1),
    ("KC-O01","Tanda '+' artinya ...","kurang","tambah","bagi","sama dengan","b",1),
    ("KC-O01","Rani punya 4 pensil. Budi memberi 2 pensil. Rani sekarang punya berapa pensil?","4","5","6","7","c",1),
    ("KC-O01","Penjumlahan artinya ...","mengambil","menghitung mundur","menggabungkan","memotong","c",1),
    ("KC-O01","0 + 5 = ...","0","4","5","6","c",1),

    # ── KC-O02: Penjumlahan hasil sampai 10 ──────────────────────────────────
    # Referensi: Buku Jago Matika SD/MI
    ("KC-O02","3 + 4 = ...","5","6","7","8","c",1),
    ("KC-O02","5 + 2 = ...","5","6","7","8","c",1),
    ("KC-O02","4 + 4 = ...","6","7","8","9","c",1),
    ("KC-O02","Ada 4 🍎 merah dan 3 🍎 hijau. Ada berapa apel semuanya?","5","6","7","8","c",1),
    ("KC-O02","1 + 9 = ...","8","9","10","11","c",1),
    ("KC-O02","6 + 3 = ...","7","8","9","10","c",1),
    ("KC-O02","Ibu membeli 5 jeruk dan 4 mangga. Ada berapa buah semuanya?","7","8","9","10","c",1),

    # ── KC-O03: Penjumlahan hasil sampai 20 ──────────────────────────────────
    # Referensi: Soal bimbelbrilian.com
    ("KC-O03","9 + 5 = ...","12","13","14","15","c",2),
    ("KC-O03","8 + 7 = ...","13","14","15","16","c",2),
    ("KC-O03","Ada 9 siswa kelas A dan 8 siswa kelas B. Ada berapa siswa semuanya?","15","16","17","18","c",2),
    ("KC-O03","10 + 6 = ...","14","15","16","17","c",2),
    ("KC-O03","7 + 8 = ...","13","14","15","16","c",2),
    ("KC-O03","Ibu membeli 9 butir telur pagi dan 9 butir telur sore. Ada berapa telur?","16","17","18","19","c",2),
    ("KC-O03","6 + 9 = ...","13","14","15","16","c",2),

    # ── KC-O04: Konsep pengurangan ────────────────────────────────────────────
    ("KC-O04","Ada 5 kue di piring. Dimakan 2. Sisa berapa kue?","2","3","4","5","b",1),
    ("KC-O04","Rani punya 6 balon. 1 balon meletus. Sisa berapa balon?","4","5","6","7","b",1),
    ("KC-O04","Tanda '-' artinya ...","tambah","kurang","kali","bagi","b",1),
    ("KC-O04","Pengurangan artinya ...","menggabungkan","menambah","mengambil sebagian","melipatkan","c",1),
    ("KC-O04","8 - 0 = ...","0","7","8","80","c",1),
    ("KC-O04","5 - 5 = ...","0","1","5","10","a",1),

    # ── KC-O05: Pengurangan dari bilangan sampai 10 ───────────────────────────
    # Referensi: Bimbelbrilian soal penjumlahan pengurangan kelas 1
    ("KC-O05","7 - 3 = ...","3","4","5","6","b",1),
    ("KC-O05","10 - 6 = ...","3","4","5","6","b",1),
    ("KC-O05","Ada 10 kupu-kupu di bunga. 3 kupu-kupu terbang. Sisa berapa?","5","6","7","8","c",1),
    ("KC-O05","9 - 4 = ...","4","5","6","7","b",1),
    ("KC-O05","Ada 8 anak bermain. 3 anak pulang. Sisa berapa anak?","4","5","6","7","b",1),
    ("KC-O05","6 - 2 = ...","3","4","5","6","b",1),
    ("KC-O05","10 - 3 = ...","5","6","7","8","c",1),

    # ── KC-O06: Pengurangan dari bilangan sampai 20 ───────────────────────────
    # Referensi: Buku Jago Matika & tirto.id
    ("KC-O06","15 - 7 = ...","6","7","8","9","c",2),
    ("KC-O06","18 - 9 = ...","7","8","9","10","c",2),
    ("KC-O06","Lani menyiapkan 15 balon. 7 balon pecah. Sisa berapa?","6","7","8","9","c",2),
    ("KC-O06","17 - 8 = ...","7","8","9","10","c",2),
    ("KC-O06","Citra punya 14 kelereng. 6 kelereng hilang. Sisa berapa?","6","7","8","9","c",2),
    ("KC-O06","20 - 6 = ...","12","13","14","15","c",2),
    ("KC-O06","16 - 7 = ...","7","8","9","10","c",2),

    # ── KC-O07: Hubungan penjumlahan dan pengurangan ──────────────────────────
    # Referensi: ATP Matematika Fase A
    ("KC-O07","4 + 5 = 9. Berarti 9 - 5 = ...","3","4","5","6","b",3),
    ("KC-O07","6 + 7 = 13. Berarti 13 - 7 = ...","5","6","7","8","b",3),
    ("KC-O07","Ada 8 apel. Diambil beberapa. Sisa 3. Berapa yang diambil?","3","4","5","6","c",3),
    ("KC-O07","3 + ... = 10. Angka yang hilang adalah ...","5","6","7","8","c",3),
    ("KC-O07","8 + 9 = 17. Berarti 17 - 9 = ...","6","7","8","9","c",3),
    ("KC-O07","12 - ... = 5. Angka yang hilang adalah ...","5","6","7","8","c",3),

    # ── KC-G01: Mengenal bangun datar ─────────────────────────────────────────
    # Referensi: Bimbel Brilian Bab 8 Bangun Datar & Kumparan
    ("KC-G01","Roda sepeda bentuknya ...","segitiga","persegi","lingkaran","persegi panjang","c",1),
    ("KC-G01","Buku tulis bentuknya ...","lingkaran","segitiga","persegi panjang","bintang","c",1),
    ("KC-G01","Potongan pizza biasanya berbentuk ...","persegi","lingkaran","segitiga","persegi panjang","c",1),
    ("KC-G01","Uang koin bentuknya ...","segitiga","persegi","lingkaran","persegi panjang","c",1),
    ("KC-G01","Saputangan bentuknya ...","lingkaran","segitiga","persegi","persegi panjang","c",1),
    ("KC-G01","Papan tulis di kelas bentuknya ...","lingkaran","segitiga","persegi","persegi panjang","d",1),

    # ── KC-G02: Sifat bangun datar ────────────────────────────────────────────
    # Referensi: Soal Bimbel Brilian Bab 8
    ("KC-G02","Segitiga punya berapa sisi?","2","3","4","5","b",2),
    ("KC-G02","Persegi punya berapa sudut?","2","3","4","5","c",2),
    ("KC-G02","Lingkaran punya berapa sudut?","1","2","4","tidak ada sudut","d",2),
    ("KC-G02","Persegi panjang punya berapa sisi?","2","3","4","6","c",2),
    ("KC-G02","Bangun datar yang tidak punya sudut adalah ...","persegi","segitiga","lingkaran","persegi panjang","c",2),
    ("KC-G02","Segitiga punya berapa sudut?","2","3","4","5","b",2),

    # ── KC-G03: Mengelompokkan bangun datar ──────────────────────────────────
    # Referensi: Kumparan & Bimbel Brilian
    ("KC-G03","Uang koin, roda, dan jam dinding semuanya berbentuk ...","segitiga","persegi","lingkaran","persegi panjang","c",2),
    ("KC-G03","Buku, papan tulis, dan pintu semuanya berbentuk ...","lingkaran","segitiga","persegi panjang","bintang","c",2),
    ("KC-G03","Mana yang bentuknya berbeda dari yang lain?","roda sepeda","uang logam","piring","buku tulis","d",2),
    ("KC-G03","Segitiga dan persegi sama-sama punya ...","tidak punya sudut","punya sudut","berbentuk bulat","tidak punya sisi","b",2),
    ("KC-G03","Mana yang berbentuk lingkaran?","penggaris","buku","piring","pintu","c",2),

    # ── KC-P01: Perbandingan panjang ──────────────────────────────────────────
    # Referensi: ATP Fase A - membandingkan panjang secara langsung
    ("KC-P01","Pensil atau penghapus, yang lebih panjang adalah ...","penghapus","sama panjang","pensil","tidak tahu","c",1),
    ("KC-P01","Lawan kata PANJANG adalah ...","besar","tebal","pendek","tinggi","c",1),
    ("KC-P01","Ular atau cacing, yang lebih panjang adalah ...","cacing","sama panjang","ular","tidak tahu","c",1),
    ("KC-P01","Tali A lebih pendek dari tali B. Berarti tali B lebih ... dari tali A","pendek","sama panjang","panjang","tidak tahu","c",1),
    ("KC-P01","Meja atau pensil, yang lebih panjang adalah ...","pensil","sama panjang","meja","tidak tahu","c",1),
    ("KC-P01","Jalan raya atau gang kecil, yang lebih panjang adalah ...","gang kecil","sama panjang","jalan raya","tidak tahu","c",1),

    # ── KC-P02: Perbandingan berat ────────────────────────────────────────────
    # Referensi: ATP Fase A - membandingkan berat secara langsung
    ("KC-P02","Bola sepak atau bola pingpong, yang lebih berat adalah ...","bola pingpong","sama berat","bola sepak","tidak tahu","c",1),
    ("KC-P02","Lawan kata BERAT adalah ...","kecil","tipis","ringan","pendek","c",1),
    ("KC-P02","Gajah atau kelinci, yang lebih berat adalah ...","kelinci","sama berat","gajah","tidak tahu","c",1),
    ("KC-P02","Semangka atau anggur, yang lebih berat adalah ...","anggur","semangka","sama berat","tidak tahu","b",1),
    ("KC-P02","Tas berisi buku atau tas kosong, yang lebih berat adalah ...","tas kosong","sama berat","tas berisi buku","tidak tahu","c",1),
    ("KC-P02","Buku tebal atau pensil, yang lebih berat adalah ...","pensil","buku tebal","sama berat","tidak tahu","b",1),

    # ── KC-P03: Urutan kejadian dan waktu ────────────────────────────────────
    # Referensi: Tirto.id soal semester 2 Kurikulum Merdeka
    ("KC-P03","Kegiatan yang dilakukan di PAGI hari adalah ...","tidur malam","makan malam","sarapan dan berangkat sekolah","nonton TV malam","c",1),
    ("KC-P03","Yang dilakukan PERTAMA setiap pagi adalah ...","makan siang","berangkat sekolah","bangun tidur","bermain sore","c",1),
    ("KC-P03","Kegiatan yang dilakukan di MALAM hari adalah ...","sarapan","berangkat sekolah","bermain siang","tidur","d",1),
    ("KC-P03","Urutan kegiatan pagi yang benar adalah ...","mandi lalu tidur lalu sarapan","bangun lalu mandi lalu sarapan lalu sekolah","sekolah lalu bangun lalu mandi","makan malam lalu sekolah","b",1),
    ("KC-P03","Hari ini Selasa. Besok adalah hari ...","Senin","Selasa","Rabu","Kamis","c",1),
    ("KC-P03","Hari ini Jumat. Kemarin adalah hari ...","Kamis","Jumat","Sabtu","Rabu","a",1),

    # ── KC-A01: Mengenal pola berulang ────────────────────────────────────────
    # Referensi: ATP Fase A - pola bukan bilangan (gambar, warna, suara)
    ("KC-A01","🔴🔵🔴🔵🔴🔵 — bagian yang diulang adalah ...","🔴🔴","🔵🔵","🔴🔵","🔵🔴","c",1),
    ("KC-A01","⭐🌙⭐🌙⭐🌙 — ini adalah pola ...","AAAA","ABAB","AABB","ABBA","b",1),
    ("KC-A01","🐱🐶🐱🐶🐱🐶 — satu bagian yang diulang ada berapa gambar?","1","2","3","4","b",1),
    ("KC-A01","Mana yang merupakan pola berulang?","1 2 3 4 5 6","🔴🔵🔴🔵🔴🔵","A B C D E F","berbeda semua","b",1),
    ("KC-A01","🟡🟢🟣🟡🟢🟣 — ada berapa warna dalam satu bagian pola?","1","2","3","4","c",1),
    ("KC-A01","Ketukan: duk-tak-duk-tak-duk-tak. Bagian yang diulang adalah ...","duk saja","tak saja","duk-tak","duk-duk","c",1),

    # ── KC-A02: Melanjutkan pola ──────────────────────────────────────────────
    # Referensi: ATP Fase A - meniru dan melanjutkan pola
    ("KC-A02","🔴🔵🔴🔵🔴 ___ → selanjutnya?","🔴","🔵","🟡","🟢","b",1),
    ("KC-A02","⭐🌙⭐🌙⭐ ___ → selanjutnya?","⭐","🌙","☀️","🌟","b",1),
    ("KC-A02","🟡🟢🟣🟡🟢 ___ → selanjutnya?","🟡","🟢","🟣","🔵","c",1),
    ("KC-A02","1 2 1 2 1 ___ → selanjutnya?","1","2","3","4","b",1),
    ("KC-A02","🐱🐱🐶🐱🐱🐶🐱🐱 ___ → selanjutnya?","🐱","🐶","🐰","🐷","b",1),
    ("KC-A02","besar-kecil-besar-kecil-besar ___ → selanjutnya?","besar","kecil","sedang","sangat besar","b",1),
]


def seed():
    if count_questions() > 0:
        print(f"Soal sudah ada ({count_questions()} soal). Gunakan --force untuk reset.")
        return

    for q in QUESTIONS:
        insert_question(*q)

    total = count_questions()
    print(f"Selesai: {total} soal ditambahkan.\n")
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT kc_id, COUNT(*) as n FROM questions GROUP BY kc_id ORDER BY kc_id"
        ).fetchall()
    for row in rows:
        print(f"  {row['kc_id']}: {row['n']} soal")


if __name__ == "__main__":
    import sys as _sys
    if "--force" in _sys.argv:
        with get_conn() as conn:
            conn.execute("DELETE FROM questions")
        print("Bank soal dikosongkan.\n")
    seed()
