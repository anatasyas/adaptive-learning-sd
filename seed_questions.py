"""
seed_questions.py — Bank soal interaktif Matematika Kelas 1 SD
Tipe soal:
  pilgan       — 4 pilihan (a/b/c/d)
  isian        — ketik angka jawaban
  hitung       — klik emoji satu per satu untuk menghitung
  visual_pilgan— lihat visual emoji, pilih angka dari 4 opsi

Format per tipe:
  pilgan:       (kc, soal, a, b, c, d, 'a'/'b'/'c'/'d', diff, 'pilgan')
  isian:        (kc, soal, '','','','', angka_benar, diff, 'isian')
  hitung:       (kc, soal, emoji, jumlah, '','', jumlah_str, diff, 'hitung')
  visual_pilgan:(kc, soal, emoji, jumlah, opsi_salah1, opsi_salah2, jumlah_str, diff, 'visual_pilgan')
"""

import os, sys, random
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from database import init_db, insert_question, count_questions, get_conn

init_db()

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # KC-B01: Mengenal bilangan 1–10
    # ══════════════════════════════════════════════════════════════════
    ("KC-B01","Angka ini dibaca apa? → 5","tiga","empat","lima","enam","c",1,"pilgan"),
    ("KC-B01","Angka ini dibaca apa? → 8","enam","tujuh","delapan","sembilan","c",1,"pilgan"),
    ("KC-B01","Angka ini dibaca apa? → 3","satu","dua","tiga","empat","c",1,"pilgan"),
    ("KC-B01","Bilangan TUJUH ditulis ...","5","6","7","8","c",1,"pilgan"),
    ("KC-B01","Bilangan SEMBILAN ditulis ...","7","8","9","10","c",1,"pilgan"),
    ("KC-B01","Ketik angkanya! Angka EMPAT ditulis ...","","","","","4",1,"isian"),
    ("KC-B01","Ketik angkanya! Angka ENAM ditulis ...","","","","","6",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B02: Membilang 1–10
    # ══════════════════════════════════════════════════════════════════
    # hitung: klik satu per satu
    ("KC-B02","Klik setiap 🍎 untuk menghitung! Ada berapa apel?","🍎","4","","","4",1,"hitung"),
    ("KC-B02","Klik setiap 🌸 untuk menghitung! Ada berapa bunga?","🌸","6","","","6",1,"hitung"),
    ("KC-B02","Klik setiap ⭐ untuk menghitung! Ada berapa bintang?","⭐","7","","","7",1,"hitung"),
    ("KC-B02","Klik setiap 🐥 untuk menghitung! Ada berapa anak ayam?","🐥","3","","","3",1,"hitung"),
    # visual_pilgan: lihat emoji, pilih angka
    ("KC-B02","Ada berapa 🦋 kupu-kupu?","🦋","5","3","8","5",1,"visual_pilgan"),
    ("KC-B02","Ada berapa 🎈 balon?","🎈","8","6","10","8",1,"visual_pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B03: Mengenal bilangan 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B03","Angka 14 dibaca ...","tiga belas","empat belas","lima belas","enam belas","b",1,"pilgan"),
    ("KC-B03","Angka 17 dibaca ...","enam belas","tujuh belas","delapan belas","sembilan belas","b",1,"pilgan"),
    ("KC-B03","Angka 20 dibaca ...","delapan belas","sembilan belas","dua puluh","dua belas","c",1,"pilgan"),
    ("KC-B03","Ketik angkanya! DUA BELAS ditulis ...","","","","","12",1,"isian"),
    ("KC-B03","Ketik angkanya! SEMBILAN BELAS ditulis ...","","","","","19",1,"isian"),
    ("KC-B03","Angka 11 dibaca ...","sepuluh","sebelas","dua belas","tiga belas","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B04: Membilang 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B04","Klik setiap 🌟 untuk menghitung! Ada berapa bintang?","🌟","12","","","12",2,"hitung"),
    ("KC-B04","Klik setiap 🍊 untuk menghitung! Ada berapa jeruk?","🍊","15","","","15",2,"hitung"),
    ("KC-B04","Ada berapa ❤️ hati?","❤️","13","11","16","13",2,"visual_pilgan"),
    ("KC-B04","Di keranjang ada 10 telur 🥚. Ibu menaruh 5 lagi. Ada berapa telur?","13","14","15","16","c",2,"pilgan"),
    ("KC-B04","Ketik jawabannya! 10 + 7 = ?","","","","","17",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B05: Membandingkan dua bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B05","Siti punya 7 permen 🍬. Ani punya 5 permen. Siapa yang lebih banyak?","Ani","Siti","sama banyak","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Mana yang lebih besar? 9 atau 6?","6","9","sama besar","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Mana yang lebih kecil? 4 atau 8?","8","4","sama kecil","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Di kelas ada 12 anak laki-laki dan 15 anak perempuan. Mana yang lebih banyak?","anak laki-laki","sama banyak","anak perempuan","tidak tahu","c",2,"pilgan"),
    ("KC-B05","Mana yang lebih kecil, 11 atau 15?","15","sama kecil","11","tidak tahu","c",2,"pilgan"),
    ("KC-B05","Mana yang lebih besar? 7 atau 3?","3","7","sama besar","tidak tahu","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B06: Urutan bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B06","Angka setelah 7 adalah ...","6","8","9","10","b",1,"pilgan"),
    ("KC-B06","Angka sebelum 10 adalah ...","8","9","11","12","b",1,"pilgan"),
    ("KC-B06","Ketik jawabannya! Angka yang ada di antara 5 dan 7 adalah ...","","","","","6",1,"isian"),
    ("KC-B06","Ketik jawabannya! Angka setelah 15 adalah ...","","","","","16",1,"isian"),
    ("KC-B06","Urutkan dari kecil ke besar: 5, 2, 8, 1 🔢","1 2 5 8","8 5 2 1","5 2 8 1","2 5 1 8","a",1,"pilgan"),
    ("KC-B06","Angka yang ada di antara 12 dan 14 adalah ...","11","13","15","16","b",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B07: Nilai tempat satuan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B07","Pada angka 13, angka 3 ada di tempat ...","puluhan","satuan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B07","Pada angka 18, angka 8 ada di tempat ...","puluhan","ratusan","satuan","ribuan","c",2,"pilgan"),
    ("KC-B07","Angka 16 terdiri dari 1 puluhan dan ... satuan","4","5","6","7","c",2,"pilgan"),
    ("KC-B07","Ketik jawabannya! Pada angka 15, berapa angka satuannya?","","","","","5",2,"isian"),
    ("KC-B07","Ketik jawabannya! Pada angka 19, berapa angka satuannya?","","","","","9",2,"isian"),
    ("KC-B07","Pada angka 20, angka 0 ada di tempat ...","satuan","puluhan","ratusan","ribuan","a",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B08: Nilai tempat puluhan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B08","Pada angka 17, angka 1 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B08","Pada angka 20, angka 2 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B08","1 puluhan dan 5 satuan = angka ...","51","15","5","10","b",2,"pilgan"),
    ("KC-B08","Ketik jawabannya! 1 puluhan dan 3 satuan = ?","","","","","13",2,"isian"),
    ("KC-B08","Ketik jawabannya! 1 puluhan dan 7 satuan = ?","","","","","17",2,"isian"),
    ("KC-B08","1 puluhan dan 9 satuan = angka ...","91","19","9","10","b",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O01: Konsep penjumlahan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O01","Dito 🧒 punya 2 kue 🎂. Ibu memberi 1 kue lagi. Sekarang Dito punya berapa kue?","2","3","4","1","b",1,"pilgan"),
    ("KC-O01","Ada 3 anak laki-laki 🧒 dan 2 anak perempuan 👧. Ada berapa anak semuanya?","3","4","5","6","c",1,"pilgan"),
    ("KC-O01","Tanda ➕ artinya ...","kurang","tambah","bagi","sama dengan","b",1,"pilgan"),
    ("KC-O01","Ketik jawabannya! 0 + 6 = ?","","","","","6",1,"isian"),
    # visual
    ("KC-O01","Klik apel satu per satu! 🍎🍎 + 🍎 = berapa?","🍎","3","","","3",1,"hitung"),
    ("KC-O01","Penjumlahan artinya kita ...","mengambil","menghitung mundur","menggabungkan","memotong","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O02: Penjumlahan hasil sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O02","Ada berapa 🐟 ikan semuanya?","🐟","7","5","9","7",1,"visual_pilgan"),
    ("KC-O02","Ketik jawabannya! 3 + 4 = ?","","","","","7",1,"isian"),
    ("KC-O02","Ketik jawabannya! 5 + 5 = ?","","","","","10",1,"isian"),
    ("KC-O02","4 + 4 = ...","6","7","8","9","c",1,"pilgan"),
    ("KC-O02","Ketik jawabannya! 2 + 7 = ?","","","","","9",1,"isian"),
    ("KC-O02","6 + 3 = ...","7","8","9","10","c",1,"pilgan"),
    ("KC-O02","Ada 4 🍎 merah dan 3 🍊 jeruk. Ada berapa buah?","5","6","7","8","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O03: Penjumlahan hasil sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O03","Ketik jawabannya! 9 + 5 = ?","","","","","14",2,"isian"),
    ("KC-O03","Ketik jawabannya! 8 + 7 = ?","","","","","15",2,"isian"),
    ("KC-O03","9 + 9 = ...","16","17","18","19","c",2,"pilgan"),
    ("KC-O03","Ada 9 siswa 🧑 kelas A dan 8 siswa kelas B. Ada berapa siswa semuanya?","15","16","17","18","c",2,"pilgan"),
    ("KC-O03","Ketik jawabannya! 10 + 7 = ?","","","","","17",2,"isian"),
    ("KC-O03","Ibu beli 9 🥚 pagi dan 6 🥚 sore. Ada berapa telur semuanya?","13","14","15","16","c",2,"pilgan"),
    ("KC-O03","Ketik jawabannya! 7 + 8 = ?","","","","","15",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O04: Konsep pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O04","Ada 5 kue 🎂 di piring. Dimakan 2. Sisa berapa?","2","3","4","5","b",1,"pilgan"),
    ("KC-O04","Rani 🌸 punya 6 balon 🎈. 1 meletus 💥. Sisa berapa?","4","5","6","7","b",1,"pilgan"),
    ("KC-O04","Tanda ➖ artinya ...","tambah","kurang","kali","bagi","b",1,"pilgan"),
    ("KC-O04","Ketik jawabannya! 5 - 5 = ?","","","","","0",1,"isian"),
    ("KC-O04","Pengurangan artinya ...","menggabungkan","menambah","mengambil sebagian","melipatkan","c",1,"pilgan"),
    ("KC-O04","Ketik jawabannya! 8 - 0 = ?","","","","","8",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O05: Pengurangan dari bilangan sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O05","Klik kupu-kupu untuk menghitung! Ada 10 🦋. Bayangkan 3 terbang. Sisa?","🦋","7","","","7",1,"hitung"),
    ("KC-O05","Ketik jawabannya! 8 - 3 = ?","","","","","5",1,"isian"),
    ("KC-O05","Ketik jawabannya! 10 - 6 = ?","","","","","4",1,"isian"),
    ("KC-O05","9 - 4 = ...","4","5","6","7","b",1,"pilgan"),
    ("KC-O05","Ada 8 🍬 permen. Dimakan 5. Sisa berapa?","2","3","4","5","b",1,"pilgan"),
    ("KC-O05","Ketik jawabannya! 6 - 2 = ?","","","","","4",1,"isian"),
    ("KC-O05","10 - 3 = ...","5","6","7","8","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O06: Pengurangan dari bilangan sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O06","Ketik jawabannya! 15 - 7 = ?","","","","","8",2,"isian"),
    ("KC-O06","Ketik jawabannya! 18 - 9 = ?","","","","","9",2,"isian"),
    ("KC-O06","17 - 8 = ...","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Lani siapkan 15 🎈 balon. 6 meletus. Sisa berapa?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Ketik jawabannya! 20 - 6 = ?","","","","","14",2,"isian"),
    ("KC-O06","Ada 14 🍪 kue. Dimakan 5. Sisa berapa?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Ketik jawabannya! 16 - 7 = ?","","","","","9",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O07: Hubungan penjumlahan dan pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O07","4 + 5 = 9. Berarti 9 - 5 = ...","3","4","5","6","b",3,"pilgan"),
    ("KC-O07","Ketik jawabannya! 3 + ? = 10. Angka yang hilang?","","","","","7",3,"isian"),
    ("KC-O07","6 + 7 = 13. Berarti 13 - 7 = ...","5","6","7","8","b",3,"pilgan"),
    ("KC-O07","Ada 8 🍎. Diambil beberapa. Sisa 3. Berapa yang diambil?","3","4","5","6","c",3,"pilgan"),
    ("KC-O07","Ketik jawabannya! 12 - ? = 5. Angka yang hilang?","","","","","7",3,"isian"),
    ("KC-O07","9 + 8 = 17. Berarti 17 - 8 = ...","7","8","9","10","c",3,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G01: Mengenal bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G01","Roda sepeda 🚲 bentuknya ...","segitiga","persegi","lingkaran","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Buku tulis 📚 bentuknya ...","lingkaran","segitiga","persegi panjang","bintang","c",1,"pilgan"),
    ("KC-G01","Uang koin 🪙 bentuknya ...","segitiga","persegi","lingkaran","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Papan tulis di kelas 🏫 bentuknya ...","lingkaran","segitiga","persegi","persegi panjang","d",1,"pilgan"),
    ("KC-G01","Potongan pizza 🍕 biasanya berbentuk ...","persegi","lingkaran","segitiga","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Saputangan 🧣 bentuknya ...","lingkaran","segitiga","persegi","persegi panjang","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G02: Sifat bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G02","Segitiga 🔺 punya berapa sisi?","2","3","4","5","b",2,"pilgan"),
    ("KC-G02","Ketik jawabannya! Persegi punya berapa sudut?","","","","","4",2,"isian"),
    ("KC-G02","Lingkaran ⭕ punya berapa sudut?","1","2","4","tidak ada","d",2,"pilgan"),
    ("KC-G02","Ketik jawabannya! Persegi panjang punya berapa sisi?","","","","","4",2,"isian"),
    ("KC-G02","Bangun datar yang tidak punya sudut sama sekali adalah ...","persegi","segitiga","lingkaran","persegi panjang","c",2,"pilgan"),
    ("KC-G02","Ketik jawabannya! Segitiga punya berapa sudut?","","","","","3",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G03: Mengelompokkan bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G03","Uang koin 🪙, roda 🔵, jam dinding 🕐 semuanya berbentuk ...","segitiga","persegi","lingkaran","persegi panjang","c",2,"pilgan"),
    ("KC-G03","Buku 📚, papan tulis, dan pintu semuanya berbentuk ...","lingkaran","segitiga","persegi panjang","bintang","c",2,"pilgan"),
    ("KC-G03","Mana yang bentuknya berbeda dari teman-temannya?\n🪙 uang koin, 🔵 roda, 📚 buku, 🕐 jam","uang koin","roda","buku","jam","c",2,"pilgan"),
    ("KC-G03","Segitiga dan persegi sama-sama punya ...","tidak ada sudut","sudut","bentuk bulat","tidak ada sisi","b",2,"pilgan"),
    ("KC-G03","Mana yang berbentuk lingkaran?","penggaris 📏","buku 📚","piring 🍽️","pintu 🚪","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P01: Perbandingan panjang
    # ══════════════════════════════════════════════════════════════════
    ("KC-P01","✏️ Pensil atau 🧹 penghapus, yang lebih panjang adalah ...","penghapus","sama panjang","pensil","tidak tahu","c",1,"pilgan"),
    ("KC-P01","Ular 🐍 atau cacing 🪱, yang lebih panjang adalah ...","cacing","sama panjang","ular","tidak tahu","c",1,"pilgan"),
    ("KC-P01","Lawan kata PANJANG adalah ...","besar","tebal","pendek","tinggi","c",1,"pilgan"),
    ("KC-P01","Tali A lebih pendek dari tali B. Berarti tali B lebih ... dari tali A","pendek","sama","panjang","tidak tahu","c",1,"pilgan"),
    ("KC-P01","Meja 🪑 atau pensil ✏️, yang lebih panjang adalah ...","pensil","sama panjang","meja","tidak tahu","c",1,"pilgan"),
    ("KC-P01","Jalan raya 🛣️ atau gang kecil, yang lebih panjang adalah ...","gang kecil","sama panjang","jalan raya","tidak tahu","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P02: Perbandingan berat
    # ══════════════════════════════════════════════════════════════════
    ("KC-P02","🏈 Bola sepak atau 🏓 bola pingpong, yang lebih berat adalah ...","bola pingpong","sama berat","bola sepak","tidak tahu","c",1,"pilgan"),
    ("KC-P02","Gajah 🐘 atau kelinci 🐰, yang lebih berat adalah ...","kelinci","sama berat","gajah","tidak tahu","c",1,"pilgan"),
    ("KC-P02","Lawan kata BERAT adalah ...","kecil","tipis","ringan","pendek","c",1,"pilgan"),
    ("KC-P02","Semangka 🍉 atau anggur 🍇, yang lebih berat adalah ...","anggur","semangka","sama berat","tidak tahu","b",1,"pilgan"),
    ("KC-P02","🎒 Tas berisi buku atau 👜 tas kosong, yang lebih berat adalah ...","tas kosong","sama berat","tas berisi buku","tidak tahu","c",1,"pilgan"),
    ("KC-P02","Batu besar 🪨 atau bulu 🪶, yang lebih berat adalah ...","bulu","sama berat","batu","tidak tahu","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P03: Urutan kejadian dan waktu
    # ══════════════════════════════════════════════════════════════════
    ("KC-P03","🌅 Kegiatan yang dilakukan di PAGI hari adalah ...","tidur malam","makan malam","sarapan","nonton TV malam","c",1,"pilgan"),
    ("KC-P03","Yang dilakukan PERTAMA setiap pagi adalah ...","makan siang","berangkat sekolah","bangun tidur","bermain sore","c",1,"pilgan"),
    ("KC-P03","🌙 Kegiatan yang dilakukan di MALAM hari adalah ...","sarapan","berangkat sekolah","bermain siang","tidur","d",1,"pilgan"),
    ("KC-P03","Urutan yang benar setiap pagi: bangun → ... → sarapan → sekolah","tidur lagi","mandi","bermain","makan malam","b",1,"pilgan"),
    ("KC-P03","Hari ini Selasa 📅. Besok adalah hari ...","Senin","Selasa","Rabu","Kamis","c",1,"pilgan"),
    ("KC-P03","Hari ini Jumat 📅. Kemarin adalah hari ...","Kamis","Jumat","Sabtu","Rabu","a",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A01: Mengenal pola berulang
    # ══════════════════════════════════════════════════════════════════
    ("KC-A01","🔴🔵🔴🔵🔴🔵 — bagian yang diulang adalah ...","🔴🔴","🔵🔵","🔴🔵","🔵🔴","c",1,"pilgan"),
    ("KC-A01","⭐🌙⭐🌙⭐🌙 — ini adalah pola ...","AAAA","ABAB","AABB","ABBA","b",1,"pilgan"),
    ("KC-A01","🐱🐶🐱🐶🐱🐶 — satu bagian pola ada berapa gambar?","1","2","3","4","b",1,"pilgan"),
    ("KC-A01","Mana yang merupakan pola berulang? 🔄","1 2 3 4 5","🔴🔵🔴🔵🔴🔵","A B C D E","semua berbeda","b",1,"pilgan"),
    ("KC-A01","🟡🟢🟣🟡🟢🟣 — ada berapa warna dalam satu unit pola?","1","2","3","4","c",1,"pilgan"),
    ("KC-A01","Ketukan gendang: duk-tak-duk-tak 🥁. Bagian yang diulang adalah ...","duk saja","tak saja","duk-tak","tidak ada","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A02: Melanjutkan pola
    # ══════════════════════════════════════════════════════════════════
    ("KC-A02","🔴🔵🔴🔵🔴 ___ → selanjutnya?","🔴","🔵","🟡","🟢","b",1,"pilgan"),
    ("KC-A02","⭐🌙⭐🌙⭐ ___ → selanjutnya?","⭐","🌙","☀️","🌟","b",1,"pilgan"),
    ("KC-A02","🟡🟢🟣🟡🟢 ___ → selanjutnya?","🟡","🟢","🟣","🔵","c",1,"pilgan"),
    ("KC-A02","1 2 1 2 1 ___ → angka selanjutnya?","1","2","3","4","b",1,"pilgan"),
    ("KC-A02","🐱🐱🐶🐱🐱🐶🐱🐱 ___ → selanjutnya?","🐱","🐶","🐰","🐷","b",1,"pilgan"),
    ("KC-A02","besar - kecil - besar - kecil - besar ___ → selanjutnya?","besar","kecil","sedang","sangat besar","b",1,"pilgan"),
]


def seed():
    if count_questions() > 0:
        print(f"Soal sudah ada ({count_questions()} soal). Gunakan --force untuk reset.")
        return
    for q in QUESTIONS:
        insert_question(*q)
    total = count_questions()
    print(f"Selesai: {total} soal.\n")
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT kc_id, COUNT(*) as n FROM questions GROUP BY kc_id ORDER BY kc_id"
        ).fetchall()
        rows2 = conn.execute(
            "SELECT question_type, COUNT(*) as n FROM questions GROUP BY question_type"
        ).fetchall()
    for row in rows:
        print(f"  {row['kc_id']}: {row['n']} soal")
    print("\nPer tipe:")
    for row in rows2:
        print(f"  {row['question_type']}: {row['n']} soal")


if __name__ == "__main__":
    import sys as _sys
    if "--force" in _sys.argv:
        with get_conn() as conn:
            conn.execute("DELETE FROM questions")
        print("Bank soal dikosongkan.\n")
    seed()
