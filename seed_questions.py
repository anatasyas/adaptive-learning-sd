"""
seed_questions.py — Bank soal interaktif Matematika Kelas 1 SD
Tipe soal:
  pilgan      — 4 pilihan (a/b/c/d)
  benar_salah — 2 tombol Benar/Salah
  isian       — ketik jawaban angka

Referensi: Buku Matematika Kurikulum Merdeka Kelas 1 (Kemendikbud),
           Bimbel Brilian, ATP Matematika Fase A
"""

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from database import init_db, insert_question, count_questions, get_conn

init_db()

# insert_question(kc_id, question, a, b, c, d, answer, difficulty, type)
# benar_salah: a = pernyataan, b/c/d = '', answer = 'benar'/'salah'
# isian: a/b/c/d = '', answer = angka benar (string)

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # KC-B01: Mengenal bilangan 1–10
    # ══════════════════════════════════════════════════════════════════
    ("KC-B01","Angka ini dibaca apa? → 5 🖐️","tiga","empat","lima","enam","c",1,"pilgan"),
    ("KC-B01","Angka ini dibaca apa? → 8 ✋🤙","enam","tujuh","delapan","sembilan","c",1,"pilgan"),
    ("KC-B01","Bilangan TUJUH ditulis ...","5","6","7","8","c",1,"pilgan"),
    ("KC-B01","✅ BENAR atau ❌ SALAH?\nAngka 6 dibaca ENAM","6 = ENAM","","","","benar",1,"benar_salah"),
    ("KC-B01","✅ BENAR atau ❌ SALAH?\nAngka 9 dibaca TUJUH","9 = TUJUH","","","","salah",1,"benar_salah"),
    ("KC-B01","Ketik angkanya! 🔢\nAngka EMPAT ditulis ...","","","","","4",1,"isian"),
    ("KC-B01","Ketik angkanya! 🔢\nAngka DELAPAN ditulis ...","","","","","8",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B02: Membilang 1–10
    # ══════════════════════════════════════════════════════════════════
    ("KC-B02","Hitung buahnya! 🍎🍎🍎","2","3","4","5","b",1,"pilgan"),
    ("KC-B02","Hitung bintangnya! ⭐⭐⭐⭐⭐","3","4","5","6","c",1,"pilgan"),
    ("KC-B02","Ketik jawabannya! 🐥\nAda berapa anak ayam? 🐥🐥🐥🐥","","","","","4",1,"isian"),
    ("KC-B02","Ketik jawabannya! 🎈\nAda berapa balon? 🎈🎈🎈🎈🎈🎈🎈","","","","","7",1,"isian"),
    ("KC-B02","✅ BENAR atau ❌ SALAH?\n🐠🐠🐠🐠🐠🐠 ada 7 ikan","6 ikan","","","","salah",1,"benar_salah"),
    ("KC-B02","Hitung kupu-kupunya! 🦋🦋🦋🦋🦋🦋🦋🦋🦋","7","8","9","10","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B03: Mengenal bilangan 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B03","Angka 14 dibaca ...","tiga belas","empat belas","lima belas","enam belas","b",1,"pilgan"),
    ("KC-B03","Angka 17 dibaca ...","enam belas","tujuh belas","delapan belas","sembilan belas","b",1,"pilgan"),
    ("KC-B03","✅ BENAR atau ❌ SALAH?\nAngka 12 dibaca DUA BELAS","12 = dua belas","","","","benar",1,"benar_salah"),
    ("KC-B03","✅ BENAR atau ❌ SALAH?\nAngka 20 dibaca SEMBILAN BELAS","20 = sembilan belas","","","","salah",1,"benar_salah"),
    ("KC-B03","Ketik angkanya! 🔢\nSEMBILAN BELAS ditulis ...","","","","","19",1,"isian"),
    ("KC-B03","Ketik angkanya! 🔢\nEMPAT BELAS ditulis ...","","","","","14",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B04: Membilang 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B04","Hitung! 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟","10","11","12","13","c",2,"pilgan"),
    ("KC-B04","Di keranjang ada 10 telur 🥚. Ibu menaruh 5 telur lagi. Ada berapa telur?","13","14","15","16","c",2,"pilgan"),
    ("KC-B04","Ketik jawabannya! 🔢\nBudi punya 10 kelereng ⚪. Ayah memberi 7 lagi. Ada berapa?","","","","","17",2,"isian"),
    ("KC-B04","✅ BENAR atau ❌ SALAH?\n10 + 8 = 18","","","","","benar",2,"benar_salah"),
    ("KC-B04","Ketik jawabannya!\nHitung: 10 + 4 = ?","","","","","14",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B05: Membandingkan dua bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B05","Siti 🎀 punya 7 permen. Ani 🌸 punya 5 permen. Siapa yang lebih banyak?","Ani","Siti","sama banyak","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Mana yang lebih besar? 9 atau 6?","6","9","sama besar","tidak tahu","b",1,"pilgan"),
    ("KC-B05","✅ BENAR atau ❌ SALAH?\n8 lebih besar dari 5","8 > 5","","","","benar",1,"benar_salah"),
    ("KC-B05","✅ BENAR atau ❌ SALAH?\n12 lebih kecil dari 9","12 < 9","","","","salah",2,"benar_salah"),
    ("KC-B05","✅ BENAR atau ❌ SALAH?\n7 sama dengan 7","7 = 7","","","","benar",1,"benar_salah"),
    ("KC-B05","Mana yang lebih kecil? 4 🔵 atau 8 🔴?","8","4","sama kecil","tidak tahu","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B06: Urutan bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B06","Angka setelah 7 adalah ...","6","8","9","10","b",1,"pilgan"),
    ("KC-B06","Angka sebelum 10 adalah ...","8","9","11","12","b",1,"pilgan"),
    ("KC-B06","Ketik jawabannya! 🔢\nAngka yang ada di antara 5 dan 7 adalah ...","","","","","6",1,"isian"),
    ("KC-B06","✅ BENAR atau ❌ SALAH?\nUrutan yang benar: 1, 3, 2, 4","1 3 2 4","","","","salah",1,"benar_salah"),
    ("KC-B06","Urutkan dari kecil ke besar: 5, 2, 8, 1 🔢","1 2 5 8","8 5 2 1","5 2 8 1","2 5 1 8","a",1,"pilgan"),
    ("KC-B06","Ketik jawabannya! 🔢\nAngka setelah 15 adalah ...","","","","","16",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B07: Nilai tempat satuan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B07","Pada angka 13, angka 3 ada di tempat ...","puluhan","satuan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B07","Angka 16 terdiri dari 1 puluhan dan ... satuan","4","5","6","7","c",2,"pilgan"),
    ("KC-B07","✅ BENAR atau ❌ SALAH?\nPada angka 19, angka 9 adalah satuannya","","","","","benar",2,"benar_salah"),
    ("KC-B07","Ketik jawabannya! 🔢\nPada angka 18, berapa angka satuannya?","","","","","8",2,"isian"),
    ("KC-B07","Ketik jawabannya! 🔢\nPada angka 15, berapa angka satuannya?","","","","","5",2,"isian"),
    ("KC-B07","✅ BENAR atau ❌ SALAH?\nPada angka 20, angka satuannya adalah 0","","","","","benar",2,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B08: Nilai tempat puluhan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B08","Pada angka 17, angka 1 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B08","1 puluhan dan 5 satuan = angka ... 🔢","15","51","5","10","a",2,"pilgan"),
    ("KC-B08","✅ BENAR atau ❌ SALAH?\n1 puluhan dan 9 satuan = 19","","","","","benar",2,"benar_salah"),
    ("KC-B08","Ketik jawabannya! 🔢\n1 puluhan dan 3 satuan = ?","","","","","13",2,"isian"),
    ("KC-B08","Ketik jawabannya! 🔢\n1 puluhan dan 7 satuan = ?","","","","","17",2,"isian"),
    ("KC-B08","✅ BENAR atau ❌ SALAH?\n1 puluhan dan 6 satuan = 61","","","","","salah",2,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O01: Konsep penjumlahan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O01","🍎🍎 + 🍎 = berapa apel semuanya?","2","3","4","5","b",1,"pilgan"),
    ("KC-O01","Dito 🧒 punya 2 kue 🎂. Ibu memberi 1 kue lagi. Sekarang Dito punya berapa kue?","2","3","4","1","b",1,"pilgan"),
    ("KC-O01","Tanda ➕ artinya ...","kurang","tambah","bagi","sama dengan","b",1,"pilgan"),
    ("KC-O01","✅ BENAR atau ❌ SALAH?\nPenjumlahan artinya menggabungkan","","","","","benar",1,"benar_salah"),
    ("KC-O01","Ketik jawabannya! 🔢\n0 + 6 = ?","","","","","6",1,"isian"),
    ("KC-O01","✅ BENAR atau ❌ SALAH?\n3 + 0 = 0","","","","","salah",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O02: Penjumlahan hasil sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O02","🍎🍎🍎 + 🍊🍊🍊🍊 = ? 🍽️","5","6","7","8","c",1,"pilgan"),
    ("KC-O02","Ketik jawabannya! ✏️\n3 + 4 = ?","","","","","7",1,"isian"),
    ("KC-O02","Ketik jawabannya! ✏️\n5 + 5 = ?","","","","","10",1,"isian"),
    ("KC-O02","✅ BENAR atau ❌ SALAH?\n4 + 4 = 9","","","","","salah",1,"benar_salah"),
    ("KC-O02","✅ BENAR atau ❌ SALAH?\n6 + 3 = 9","","","","","benar",1,"benar_salah"),
    ("KC-O02","Ketik jawabannya! ✏️\n2 + 7 = ?","","","","","9",1,"isian"),
    ("KC-O02","Ada 4 🐟 dan 5 🐟. Ada berapa ikan semuanya?","7","8","9","10","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O03: Penjumlahan hasil sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O03","Ketik jawabannya! ✏️\n9 + 5 = ?","","","","","14",2,"isian"),
    ("KC-O03","Ketik jawabannya! ✏️\n8 + 7 = ?","","","","","15",2,"isian"),
    ("KC-O03","✅ BENAR atau ❌ SALAH?\n9 + 9 = 19","","","","","salah",2,"benar_salah"),
    ("KC-O03","✅ BENAR atau ❌ SALAH?\n8 + 8 = 16","","","","","benar",2,"benar_salah"),
    ("KC-O03","Ada 9 siswa 🧑 kelas A dan 8 siswa kelas B. Ada berapa siswa semuanya?","15","16","17","18","c",2,"pilgan"),
    ("KC-O03","Ketik jawabannya! ✏️\n10 + 7 = ?","","","","","17",2,"isian"),
    ("KC-O03","Ibu beli 9 🥚 pagi dan 6 🥚 sore. Ada berapa telur?","13","14","15","16","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O04: Konsep pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O04","🎂🎂🎂🎂🎂 dimakan 2. Sisa berapa kue? 🎂","2","3","4","5","b",1,"pilgan"),
    ("KC-O04","Rani 🌸 punya 6 balon 🎈. 1 meletus 💥. Sisa berapa?","4","5","6","7","b",1,"pilgan"),
    ("KC-O04","Tanda ➖ artinya ...","tambah","kurang","kali","bagi","b",1,"pilgan"),
    ("KC-O04","✅ BENAR atau ❌ SALAH?\nPengurangan artinya mengambil sebagian","","","","","benar",1,"benar_salah"),
    ("KC-O04","✅ BENAR atau ❌ SALAH?\n8 - 0 = 0","","","","","salah",1,"benar_salah"),
    ("KC-O04","Ketik jawabannya! ✏️\n5 - 5 = ?","","","","","0",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O05: Pengurangan dari bilangan sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O05","🦋🦋🦋🦋🦋🦋🦋🦋🦋🦋 ada 10 kupu-kupu. 3 terbang pergi ✈️. Sisa berapa?","5","6","7","8","c",1,"pilgan"),
    ("KC-O05","Ketik jawabannya! ✏️\n8 - 3 = ?","","","","","5",1,"isian"),
    ("KC-O05","Ketik jawabannya! ✏️\n10 - 6 = ?","","","","","4",1,"isian"),
    ("KC-O05","✅ BENAR atau ❌ SALAH?\n9 - 4 = 5","","","","","benar",1,"benar_salah"),
    ("KC-O05","✅ BENAR atau ❌ SALAH?\n7 - 3 = 3","","","","","salah",1,"benar_salah"),
    ("KC-O05","Ada 8 🍬 permen. Dimakan 5. Sisa berapa?","2","3","4","5","b",1,"pilgan"),
    ("KC-O05","Ketik jawabannya! ✏️\n6 - 2 = ?","","","","","4",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O06: Pengurangan dari bilangan sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O06","Ketik jawabannya! ✏️\n15 - 7 = ?","","","","","8",2,"isian"),
    ("KC-O06","Ketik jawabannya! ✏️\n18 - 9 = ?","","","","","9",2,"isian"),
    ("KC-O06","✅ BENAR atau ❌ SALAH?\n17 - 8 = 9","","","","","benar",2,"benar_salah"),
    ("KC-O06","✅ BENAR atau ❌ SALAH?\n16 - 7 = 10","","","","","salah",2,"benar_salah"),
    ("KC-O06","Lani 🌺 siapkan 15 🎈 balon. 6 meletus. Sisa berapa?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Ketik jawabannya! ✏️\n20 - 6 = ?","","","","","14",2,"isian"),
    ("KC-O06","Ada 14 🍪 kue. Dimakan 5. Sisa berapa?","7","8","9","10","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O07: Hubungan penjumlahan dan pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O07","4 + 5 = 9. Berarti 9 - 5 = ... 🔢","3","4","5","6","b",3,"pilgan"),
    ("KC-O07","Ketik jawabannya! ✏️\n3 + ... = 10. Angka yang hilang?","","","","","7",3,"isian"),
    ("KC-O07","✅ BENAR atau ❌ SALAH?\n6 + 7 = 13, berarti 13 - 7 = 6","","","","","benar",3,"benar_salah"),
    ("KC-O07","Ada 8 🍎. Diambil beberapa. Sisa 3 🍎. Berapa yang diambil?","3","4","5","6","c",3,"pilgan"),
    ("KC-O07","Ketik jawabannya! ✏️\n12 - ... = 5. Angka yang hilang?","","","","","7",3,"isian"),
    ("KC-O07","✅ BENAR atau ❌ SALAH?\n9 + 8 = 17, berarti 17 - 8 = 9","","","","","benar",3,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G01: Mengenal bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G01","Roda sepeda 🚲 bentuknya ...","segitiga","persegi","lingkaran","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Buku tulis 📚 bentuknya ...","lingkaran","segitiga","persegi panjang","bintang","c",1,"pilgan"),
    ("KC-G01","✅ BENAR atau ❌ SALAH?\nUang koin 🪙 berbentuk lingkaran","","","","","benar",1,"benar_salah"),
    ("KC-G01","✅ BENAR atau ❌ SALAH?\nPizza 🍕 biasanya dipotong berbentuk persegi","","","","","salah",1,"benar_salah"),
    ("KC-G01","Papan tulis 🖥️ di kelas berbentuk ...","lingkaran","segitiga","persegi","persegi panjang","d",1,"pilgan"),
    ("KC-G01","✅ BENAR atau ❌ SALAH?\nLayar perahu ⛵ berbentuk segitiga","","","","","benar",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G02: Sifat bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G02","Segitiga 🔺 punya berapa sisi?","2","3","4","5","b",2,"pilgan"),
    ("KC-G02","Ketik jawabannya! 🔢\nPersegi punya berapa sudut?","","","","","4",2,"isian"),
    ("KC-G02","✅ BENAR atau ❌ SALAH?\nLingkaran ⭕ tidak punya sudut","","","","","benar",2,"benar_salah"),
    ("KC-G02","✅ BENAR atau ❌ SALAH?\nSegitiga punya 4 sisi","","","","","salah",2,"benar_salah"),
    ("KC-G02","Ketik jawabannya! 🔢\nPersegi panjang punya berapa sisi?","","","","","4",2,"isian"),
    ("KC-G02","Bangun datar yang tidak punya sudut adalah ...","persegi","segitiga","lingkaran","persegi panjang","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G03: Mengelompokkan bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G03","Uang koin 🪙, roda 🔵, jam dinding 🕐 semuanya berbentuk ...","segitiga","persegi","lingkaran","persegi panjang","c",2,"pilgan"),
    ("KC-G03","✅ BENAR atau ❌ SALAH?\nBuku 📚, papan tulis, dan pintu semuanya berbentuk persegi panjang","","","","","benar",2,"benar_salah"),
    ("KC-G03","Mana yang bentuknya berbeda dari teman-temannya?\n🪙 uang koin, 🔵 roda, 📚 buku, 🕐 jam","uang koin","roda","buku","jam","c",2,"pilgan"),
    ("KC-G03","✅ BENAR atau ❌ SALAH?\nSegitiga dan persegi sama-sama punya sudut","","","","","benar",2,"benar_salah"),
    ("KC-G03","Mana yang berbentuk lingkaran? 🔍","penggaris","buku","piring 🍽️","pintu","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P01: Perbandingan panjang
    # ══════════════════════════════════════════════════════════════════
    ("KC-P01","✏️ Pensil atau 🧹 penghapus, yang lebih panjang adalah ...","penghapus","sama panjang","pensil","tidak tahu","c",1,"pilgan"),
    ("KC-P01","✅ BENAR atau ❌ SALAH?\nUlar 🐍 lebih panjang dari cacing 🪱","","","","","benar",1,"benar_salah"),
    ("KC-P01","Lawan kata PANJANG adalah ...","besar","tebal","pendek","tinggi","c",1,"pilgan"),
    ("KC-P01","✅ BENAR atau ❌ SALAH?\nPensil lebih pendek dari penggaris 📏","","","","","benar",1,"benar_salah"),
    ("KC-P01","Tali A lebih pendek dari tali B. Berarti tali B lebih ... dari tali A 🎀","pendek","sama","panjang","tidak tahu","c",1,"pilgan"),
    ("KC-P01","✅ BENAR atau ❌ SALAH?\nJalan tol lebih panjang dari gang kecil 🛣️","","","","","benar",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P02: Perbandingan berat
    # ══════════════════════════════════════════════════════════════════
    ("KC-P02","🏈 Bola sepak atau 🏓 bola pingpong, yang lebih berat adalah ...","bola pingpong","sama berat","bola sepak","tidak tahu","c",1,"pilgan"),
    ("KC-P02","✅ BENAR atau ❌ SALAH?\nGajah 🐘 lebih berat dari kelinci 🐰","","","","","benar",1,"benar_salah"),
    ("KC-P02","Lawan kata BERAT adalah ...","kecil","tipis","ringan","pendek","c",1,"pilgan"),
    ("KC-P02","✅ BENAR atau ❌ SALAH?\nSemangka 🍉 lebih berat dari anggur 🍇","","","","","benar",1,"benar_salah"),
    ("KC-P02","🎒 Tas berisi buku atau 👜 tas kosong, yang lebih berat adalah ...","tas kosong","sama berat","tas berisi buku","tidak tahu","c",1,"pilgan"),
    ("KC-P02","✅ BENAR atau ❌ SALAH?\nBatu besar 🪨 lebih ringan dari bulu 🪶","","","","","salah",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P03: Urutan kejadian dan waktu
    # ══════════════════════════════════════════════════════════════════
    ("KC-P03","🌅 Kegiatan yang dilakukan di PAGI hari adalah ...","tidur malam","makan malam","sarapan","nonton TV malam","c",1,"pilgan"),
    ("KC-P03","✅ BENAR atau ❌ SALAH?\nSebelum pergi ke sekolah 🏫, kita sarapan dulu","","","","","benar",1,"benar_salah"),
    ("KC-P03","🌙 Kegiatan yang dilakukan di MALAM hari adalah ...","sarapan","berangkat sekolah","bermain siang","tidur","d",1,"pilgan"),
    ("KC-P03","✅ BENAR atau ❌ SALAH?\nUrutannya benar: bangun tidur → mandi → sarapan → sekolah 📅","","","","","benar",1,"benar_salah"),
    ("KC-P03","Hari ini Selasa 📅. Besok adalah hari ...","Senin","Selasa","Rabu","Kamis","c",1,"pilgan"),
    ("KC-P03","✅ BENAR atau ❌ SALAH?\nSetelah Jumat adalah Sabtu 📆","","","","","benar",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A01: Mengenal pola berulang
    # ══════════════════════════════════════════════════════════════════
    ("KC-A01","🔴🔵🔴🔵🔴🔵 — bagian yang diulang adalah ...","🔴🔴","🔵🔵","🔴🔵","🔵🔴","c",1,"pilgan"),
    ("KC-A01","✅ BENAR atau ❌ SALAH?\n⭐🌙⭐🌙⭐🌙 adalah pola ABAB","","","","","benar",1,"benar_salah"),
    ("KC-A01","🐱🐶🐱🐶🐱🐶 — satu bagian pola ada berapa gambar?","1","2","3","4","b",1,"pilgan"),
    ("KC-A01","✅ BENAR atau ❌ SALAH?\n🟡🟢🟣🟡🟢🟣 memiliki 3 warna dalam satu unit pola","","","","","benar",1,"benar_salah"),
    ("KC-A01","Mana yang merupakan pola berulang? 🔄","1 2 3 4 5","🔴🔵🔴🔵🔴🔵","A B C D E","semua berbeda","b",1,"pilgan"),
    ("KC-A01","✅ BENAR atau ❌ SALAH?\nduk-tak-duk-tak adalah pola berulang 🥁","","","","","benar",1,"benar_salah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A02: Melanjutkan pola
    # ══════════════════════════════════════════════════════════════════
    ("KC-A02","🔴🔵🔴🔵🔴 ___ → selanjutnya? 🔄","🔴","🔵","🟡","🟢","b",1,"pilgan"),
    ("KC-A02","⭐🌙⭐🌙⭐ ___ → selanjutnya? ✨","⭐","🌙","☀️","🌟","b",1,"pilgan"),
    ("KC-A02","🟡🟢🟣🟡🟢 ___ → selanjutnya? 🎨","🟡","🟢","🟣","🔵","c",1,"pilgan"),
    ("KC-A02","✅ BENAR atau ❌ SALAH?\n1 2 1 2 1 → selanjutnya adalah 2","","","","","benar",1,"benar_salah"),
    ("KC-A02","🐱🐱🐶🐱🐱🐶🐱🐱 ___ → selanjutnya?","🐱","🐶","🐰","🐷","b",1,"pilgan"),
    ("KC-A02","✅ BENAR atau ❌ SALAH?\nbesar-kecil-besar-kecil → selanjutnya adalah BESAR","","","","","benar",1,"benar_salah"),
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
