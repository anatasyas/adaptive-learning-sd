"""
seed_questions.py — Bank soal Matematika Kelas 1 SD
Tipe soal:
  pilgan        — 4 pilihan teks
  isian         — numpad angka interaktif
  hitung        — klik emoji satu per satu
  visual_pilgan — lihat deretan emoji, pilih angka
  jodohkan      — kotak emoji di kiri, pilih angka yang cocok di kanan
  hitung_warna  — kotak emoji campur, hitung warna/jenis tertentu
  visual_tambah — A emoji + B emoji = ? (numpad)

Schema kolom:
  pilgan:        (kc, soal, a, b, c, d, 'a'/'b'/'c'/'d', diff, 'pilgan')
  isian:         (kc, soal, '','','','', angka, diff, 'isian')
  hitung:        (kc, soal, emoji, jumlah, '','', jumlah, diff, 'hitung')
  visual_pilgan: (kc, soal, emoji, jumlah, salah1, salah2, jumlah, diff, 'visual_pilgan')
  jodohkan:      (kc, soal, emoji, jumlah, salah1, salah2, jumlah, diff, 'jodohkan')
  hitung_warna:  (kc, soal, emoji_campur_str, target_emoji, '','', count, diff, 'hitung_warna')
  visual_tambah: (kc, soal, emoji1, jml1, emoji2, jml2, total, diff, 'visual_tambah')
"""

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from database import init_db, insert_question, count_questions, get_conn

init_db()

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # KC-B01: Mengenal bilangan 1–10
    # Layout: konteks (baris 1) \n\n pertanyaan (baris 2)
    # ══════════════════════════════════════════════════════════════════
    ("KC-B01","Perhatikan angka berikut.\n\nAngka 5 dibaca ...","tiga","empat","lima","enam","c",1,"pilgan"),
    ("KC-B01","Perhatikan angka berikut.\n\nAngka 8 dibaca ...","enam","tujuh","delapan","sembilan","c",1,"pilgan"),
    ("KC-B01","Perhatikan angka berikut.\n\nAngka 3 dibaca ...","satu","dua","tiga","empat","c",1,"pilgan"),
    ("KC-B01","Bilangan TUJUH ditulis dengan angka ...","5","6","7","8","c",1,"pilgan"),
    ("KC-B01","Bilangan SEMBILAN ditulis dengan angka ...","7","8","9","10","c",1,"pilgan"),
    ("KC-B01","Tekan angka EMPAT pada tombol di bawah!","","","","","4",1,"isian"),
    ("KC-B01","Tekan angka ENAM pada tombol di bawah!","","","","","6",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B02: Membilang 1–10
    # ══════════════════════════════════════════════════════════════════
    ("KC-B02","Klik setiap 🍎 satu per satu.\n\nAda berapa apel?","🍎","4","","","4",1,"hitung"),
    ("KC-B02","Klik setiap 🌸 satu per satu.\n\nAda berapa bunga?","🌸","6","","","6",1,"hitung"),
    ("KC-B02","Klik setiap ⭐ satu per satu.\n\nAda berapa bintang?","⭐","7","","","7",1,"hitung"),
    ("KC-B02","Klik setiap 🐥 satu per satu.\n\nAda berapa anak ayam?","🐥","3","","","3",1,"hitung"),
    ("KC-B02","Lihat kelompok hewan di bawah ini.\n\nAda berapa 🦋 kupu-kupu?","🦋","5","3","8","5",1,"jodohkan"),
    ("KC-B02","Lihat kelompok buah di bawah ini.\n\nAda berapa 🎈 balon?","🎈","8","5","10","8",1,"jodohkan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B03: Mengenal bilangan 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B03","Perhatikan angka berikut.\n\nAngka 14 dibaca ...","tiga belas","empat belas","lima belas","enam belas","b",1,"pilgan"),
    ("KC-B03","Perhatikan angka berikut.\n\nAngka 17 dibaca ...","enam belas","tujuh belas","delapan belas","sembilan belas","b",1,"pilgan"),
    ("KC-B03","Perhatikan angka berikut.\n\nAngka 20 dibaca ...","delapan belas","sembilan belas","dua puluh","dua belas","c",1,"pilgan"),
    ("KC-B03","Bilangan DUA BELAS ditulis dengan angka ...\n\nTekan jawabanmu!","","","","","12",1,"isian"),
    ("KC-B03","Bilangan SEMBILAN BELAS ditulis dengan angka ...\n\nTekan jawabanmu!","","","","","19",1,"isian"),
    ("KC-B03","Perhatikan angka berikut.\n\nAngka 11 dibaca ...","sepuluh","sebelas","dua belas","tiga belas","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B04: Membilang 11–20
    # ══════════════════════════════════════════════════════════════════
    ("KC-B04","Klik setiap 🌟 satu per satu.\n\nAda berapa bintang?","🌟","12","","","12",2,"hitung"),
    ("KC-B04","Klik setiap 🍊 satu per satu.\n\nAda berapa jeruk?","🍊","15","","","15",2,"hitung"),
    ("KC-B04","Lihat kelompok benda di bawah ini.\n\nAda berapa ❤️?","❤️","13","11","16","13",2,"jodohkan"),
    ("KC-B04","Di keranjang ada 10 telur. Ibu menaruh 5 telur lagi.\n\nAda berapa telur sekarang?","13","14","15","16","c",2,"pilgan"),
    ("KC-B04","Hitunglah!\n\n10 + 7 = ?","","","","","17",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B05: Membandingkan dua bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B05","Siti punya 7 permen 🍬. Ani punya 5 permen 🍬.\n\nSiapa yang punya lebih banyak?","Ani","Siti","sama banyak","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Perhatikan dua bilangan ini.\n\nMana yang lebih besar: 9 atau 6?","6","9","sama besar","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Perhatikan dua bilangan ini.\n\nMana yang lebih kecil: 4 atau 8?","8","4","sama kecil","tidak tahu","b",1,"pilgan"),
    ("KC-B05","Di kelas ada 12 anak laki-laki dan 15 anak perempuan.\n\nMana yang lebih banyak?","anak laki-laki","sama banyak","anak perempuan","tidak tahu","c",2,"pilgan"),
    ("KC-B05","Perhatikan dua bilangan ini.\n\nMana yang lebih kecil: 11 atau 15?","15","sama kecil","11","tidak tahu","c",2,"pilgan"),
    ("KC-B05","Perhatikan dua bilangan ini.\n\nMana yang lebih besar: 7 atau 3?","3","7","sama besar","tidak tahu","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B06: Urutan bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B06","Perhatikan bilangan berikut.\n\nAngka setelah 7 adalah ...","6","8","9","10","b",1,"pilgan"),
    ("KC-B06","Perhatikan bilangan berikut.\n\nAngka sebelum 10 adalah ...","8","9","11","12","b",1,"pilgan"),
    ("KC-B06","Di antara 5 dan 7 ada satu angka.\n\nTekan angka itu!","","","","","6",1,"isian"),
    ("KC-B06","Angka sesudah 15 adalah ...\n\nTekan jawabanmu!","","","","","16",1,"isian"),
    ("KC-B06","Urutkan dari yang paling kecil.\n\n5, 2, 8, 1 → urutan yang benar?","1 2 5 8","8 5 2 1","5 2 8 1","2 5 1 8","a",1,"pilgan"),
    ("KC-B06","Angka yang ada di antara 12 dan 14 adalah ...","11","13","15","16","b",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B07: Nilai tempat satuan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B07","Perhatikan angka 13.\n\nAngka 3 ada di tempat ...","puluhan","satuan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B07","Perhatikan angka 18.\n\nAngka 8 ada di tempat ...","puluhan","ratusan","satuan","ribuan","c",2,"pilgan"),
    ("KC-B07","Perhatikan angka 16.\n\n16 terdiri dari 1 puluhan dan ... satuan","4","5","6","7","c",2,"pilgan"),
    ("KC-B07","Perhatikan angka 15.\n\nBerapa angka satuannya? Tekan jawabanmu!","","","","","5",2,"isian"),
    ("KC-B07","Perhatikan angka 19.\n\nBerapa angka satuannya? Tekan jawabanmu!","","","","","9",2,"isian"),
    ("KC-B07","Perhatikan angka 20.\n\nAngka 0 ada di tempat ...","satuan","puluhan","ratusan","ribuan","a",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-B08: Nilai tempat puluhan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B08","Perhatikan angka 17.\n\nAngka 1 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B08","Perhatikan angka 20.\n\nAngka 2 ada di tempat ...","satuan","puluhan","ratusan","ribuan","b",2,"pilgan"),
    ("KC-B08","1 puluhan dan 5 satuan sama dengan angka ...","51","15","5","10","b",2,"pilgan"),
    ("KC-B08","1 puluhan dan 3 satuan sama dengan angka berapa?\n\nTekan jawabanmu!","","","","","13",2,"isian"),
    ("KC-B08","1 puluhan dan 7 satuan sama dengan angka berapa?\n\nTekan jawabanmu!","","","","","17",2,"isian"),
    ("KC-B08","1 puluhan dan 9 satuan sama dengan angka ...","91","19","9","10","b",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O01: Konsep penjumlahan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O01","Dito punya 2 kue 🎂. Ibu memberi 1 kue lagi.\n\nSekarang Dito punya berapa kue?","2","3","4","1","b",1,"pilgan"),
    ("KC-O01","Ada 3 anak laki-laki 🧒 dan 2 anak perempuan 👧.\n\nAda berapa anak semuanya?","3","4","5","6","c",1,"pilgan"),
    ("KC-O01","Perhatikan tanda berikut.\n\nTanda ➕ artinya ...","kurang","tambah","bagi","sama dengan","b",1,"pilgan"),
    ("KC-O01","Hitunglah!\n\n0 + 6 = ?","","","","","6",1,"isian"),
    ("KC-O01","Penjumlahan artinya kita ...\n\nPilih jawaban yang benar!","mengambil","menghitung mundur","menggabungkan","memotong","c",1,"pilgan"),
    # visual_tambah: siswa lihat emoji, jawab total dengan numpad
    ("KC-O01","Hitung semua buah!\n\n🍎🍎🍎 ditambah 🍊🍊 = ?","🍎","3","🍊","2","5",1,"visual_tambah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O02: Penjumlahan hasil sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O02","Lihat gambar berikut.\n\nAda berapa 🐟 ikan semuanya?","🐟","7","5","9","7",1,"jodohkan"),
    ("KC-O02","Hitunglah!\n\n3 + 4 = ?","","","","","7",1,"isian"),
    ("KC-O02","Hitunglah!\n\n5 + 5 = ?","","","","","10",1,"isian"),
    ("KC-O02","Hitunglah!\n\n4 + 4 = ?","6","7","8","9","c",1,"pilgan"),
    ("KC-O02","Hitunglah!\n\n2 + 7 = ?","","","","","9",1,"isian"),
    ("KC-O02","Hitung semua buah!\n\n🍎🍎🍎🍎 ditambah 🍊🍊🍊 = ?","🍎","4","🍊","3","7",1,"visual_tambah"),
    ("KC-O02","Hitung semua bintang!\n\n⭐⭐ ditambah ⭐⭐⭐⭐ = ?","⭐","2","⭐","4","6",1,"visual_tambah"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O03: Penjumlahan hasil sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O03","Hitunglah!\n\n9 + 5 = ?","","","","","14",2,"isian"),
    ("KC-O03","Hitunglah!\n\n8 + 7 = ?","","","","","15",2,"isian"),
    ("KC-O03","Hitunglah!\n\n9 + 9 = ?","16","17","18","19","c",2,"pilgan"),
    ("KC-O03","Ada 9 siswa di kelas A dan 8 siswa di kelas B.\n\nAda berapa siswa semuanya?","15","16","17","18","c",2,"pilgan"),
    ("KC-O03","Hitunglah!\n\n10 + 7 = ?","","","","","17",2,"isian"),
    ("KC-O03","Hitung semua bola!\n\n🏀🏀🏀🏀🏀🏀 ditambah ⚽⚽⚽⚽⚽⚽⚽⚽ = ?","🏀","6","⚽","8","14",2,"visual_tambah"),
    ("KC-O03","Hitunglah!\n\n7 + 8 = ?","","","","","15",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O04: Konsep pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O04","Ada 5 kue 🎂 di piring. Dimakan 2.\n\nSisa berapa kue?","2","3","4","5","b",1,"pilgan"),
    ("KC-O04","Rani punya 6 balon 🎈. 1 balon meletus 💥.\n\nSisa berapa balon?","4","5","6","7","b",1,"pilgan"),
    ("KC-O04","Perhatikan tanda berikut.\n\nTanda ➖ artinya ...","tambah","kurang","kali","bagi","b",1,"pilgan"),
    ("KC-O04","Hitunglah!\n\n5 - 5 = ?","","","","","0",1,"isian"),
    ("KC-O04","Pengurangan artinya kita ...\n\nPilih jawaban yang benar!","menggabungkan","menambah","mengambil sebagian","melipatkan","c",1,"pilgan"),
    ("KC-O04","Hitunglah!\n\n8 - 0 = ?","","","","","8",1,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O05: Pengurangan dari bilangan sampai 10
    # ══════════════════════════════════════════════════════════════════
    ("KC-O05","Ada 10 🦋 kupu-kupu. 3 terbang pergi ✈️.\n\nSisa berapa kupu-kupu?","5","6","7","8","c",1,"pilgan"),
    ("KC-O05","Hitunglah!\n\n8 - 3 = ?","","","","","5",1,"isian"),
    ("KC-O05","Hitunglah!\n\n10 - 6 = ?","","","","","4",1,"isian"),
    ("KC-O05","Hitunglah!\n\n9 - 4 = ?","4","5","6","7","b",1,"pilgan"),
    ("KC-O05","Ada 8 permen 🍬. Dimakan 5 permen.\n\nSisa berapa?","2","3","4","5","b",1,"pilgan"),
    ("KC-O05","Hitunglah!\n\n6 - 2 = ?","","","","","4",1,"isian"),
    ("KC-O05","Hitunglah!\n\n10 - 3 = ?","5","6","7","8","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O06: Pengurangan dari bilangan sampai 20
    # ══════════════════════════════════════════════════════════════════
    ("KC-O06","Hitunglah!\n\n15 - 7 = ?","","","","","8",2,"isian"),
    ("KC-O06","Hitunglah!\n\n18 - 9 = ?","","","","","9",2,"isian"),
    ("KC-O06","Hitunglah!\n\n17 - 8 = ?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Lani menyiapkan 15 balon 🎈. 6 balon meletus.\n\nSisa berapa balon?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Hitunglah!\n\n20 - 6 = ?","","","","","14",2,"isian"),
    ("KC-O06","Ada 14 kue 🍪. Dimakan 5 kue.\n\nSisa berapa kue?","7","8","9","10","c",2,"pilgan"),
    ("KC-O06","Hitunglah!\n\n16 - 7 = ?","","","","","9",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-O07: Hubungan penjumlahan dan pengurangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-O07","Perhatikan hubungan ini.\n\n4 + 5 = 9, berarti 9 - 5 = ?","3","4","5","6","b",3,"pilgan"),
    ("KC-O07","Cari angka yang hilang!\n\n3 + ? = 10","","","","","7",3,"isian"),
    ("KC-O07","Perhatikan hubungan ini.\n\n6 + 7 = 13, berarti 13 - 7 = ?","5","6","7","8","b",3,"pilgan"),
    ("KC-O07","Ada 8 apel 🍎. Diambil beberapa. Sisa 3 apel.\n\nBerapa apel yang diambil?","3","4","5","6","c",3,"pilgan"),
    ("KC-O07","Cari angka yang hilang!\n\n12 - ? = 5","","","","","7",3,"isian"),
    ("KC-O07","Perhatikan hubungan ini.\n\n9 + 8 = 17, berarti 17 - 8 = ?","7","8","9","10","c",3,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G01: Mengenal bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G01","Roda sepeda 🚲 berbentuk bulat sempurna.\n\nBentuk itu disebut ...","segitiga","persegi","lingkaran","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Buku tulis 📚 memiliki 4 sudut, panjang dan lebar berbeda.\n\nBentuk itu disebut ...","lingkaran","segitiga","persegi panjang","bintang","c",1,"pilgan"),
    ("KC-G01","Uang koin 🪙 berbentuk bulat sempurna.\n\nBentuk itu disebut ...","segitiga","persegi","lingkaran","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Papan tulis di kelas berbentuk empat persegi dengan panjang dan lebar berbeda.\n\nBentuk itu disebut ...","lingkaran","segitiga","persegi","persegi panjang","d",1,"pilgan"),
    ("KC-G01","Potongan pizza memiliki 3 sudut.\n\nBentuk itu disebut ...","persegi","lingkaran","segitiga","persegi panjang","c",1,"pilgan"),
    ("KC-G01","Saputangan memiliki 4 sudut dengan panjang dan lebar sama.\n\nBentuk itu disebut ...","lingkaran","segitiga","persegi","persegi panjang","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G02: Sifat bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G02","Perhatikan bangun datar segitiga 🔺.\n\nSegitiga punya berapa sisi?","2","3","4","5","b",2,"pilgan"),
    ("KC-G02","Perhatikan bangun datar persegi.\n\nBerapa jumlah sudutnya? Tekan jawabanmu!","","","","","4",2,"isian"),
    ("KC-G02","Perhatikan bangun datar lingkaran ⭕.\n\nLingkaran punya berapa sudut?","1","2","4","tidak ada","d",2,"pilgan"),
    ("KC-G02","Perhatikan bangun datar persegi panjang.\n\nBerapa jumlah sisinya? Tekan jawabanmu!","","","","","4",2,"isian"),
    ("KC-G02","Di antara bangun datar ini, mana yang tidak punya sudut sama sekali?","persegi","segitiga","lingkaran","persegi panjang","c",2,"pilgan"),
    ("KC-G02","Perhatikan bangun datar segitiga 🔺.\n\nBerapa jumlah sudutnya? Tekan jawabanmu!","","","","","3",2,"isian"),

    # ══════════════════════════════════════════════════════════════════
    # KC-G03: Mengelompokkan bangun datar
    # ══════════════════════════════════════════════════════════════════
    ("KC-G03","Uang koin 🪙, roda, jam dinding — semuanya berbentuk bulat.\n\nBentuk itu disebut ...","segitiga","persegi","lingkaran","persegi panjang","c",2,"pilgan"),
    ("KC-G03","Buku 📚, papan tulis, dan pintu — semuanya memiliki 4 sudut dengan sisi tidak sama panjang.\n\nBentuk itu disebut ...","lingkaran","segitiga","persegi panjang","bintang","c",2,"pilgan"),
    ("KC-G03","Di antara benda-benda berikut, mana yang bentuknya berbeda?\n\nUang koin 🪙, roda, piring, buku tulis","uang koin","roda","piring","buku tulis","d",2,"pilgan"),
    ("KC-G03","Segitiga dan persegi sama-sama memiliki ...\n\nPilih yang benar!","tidak ada sudut","sudut","bentuk bulat","tidak ada sisi","b",2,"pilgan"),
    ("KC-G03","Di antara benda-benda berikut, mana yang berbentuk lingkaran?\n\nPilih yang benar!","penggaris 📏","buku 📚","piring 🍽️","pintu 🚪","c",2,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P01: Perbandingan panjang (tanpa soal ambigu)
    # ══════════════════════════════════════════════════════════════════
    ("KC-P01","Sebuah jalan raya sangat panjang. Sebuah gang kecil sangat pendek.\n\nMana yang lebih panjang?","gang kecil","sama panjang","jalan raya","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P01","Seekor ular 🐍 panjangnya bisa mencapai beberapa meter. Seekor cacing 🪱 hanya beberapa cm.\n\nMana yang lebih panjang?","cacing","sama panjang","ular","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P01","Lawan kata dari PANJANG adalah ...","besar","tebal","pendek","tinggi","c",1,"pilgan"),
    ("KC-P01","Tali A lebih pendek dari tali B.\n\nBerarti tali B lebih ... dari tali A","pendek","sama","panjang","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P01","Sebuah lapangan bola lebih panjang dari sebuah ruangan kelas.\n\nMana yang lebih pendek?","lapangan bola","sama panjang","ruang kelas","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P01","Truk besar 🚛 lebih panjang dari motor 🏍️.\n\nMana yang lebih pendek?","truk","sama panjang","motor","tidak bisa dibanding","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P02: Perbandingan berat
    # ══════════════════════════════════════════════════════════════════
    ("KC-P02","Seekor gajah 🐘 beratnya bisa ribuan kilogram. Seekor kelinci 🐰 hanya beberapa kilogram.\n\nMana yang lebih berat?","kelinci","sama berat","gajah","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P02","Sebuah batu besar 🪨 lebih berat dari selembar bulu 🪶.\n\nMana yang lebih ringan?","batu besar","sama berat","bulu","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P02","Lawan kata dari BERAT adalah ...","kecil","tipis","ringan","pendek","c",1,"pilgan"),
    ("KC-P02","Sebuah semangka utuh 🍉 beratnya bisa 5 kg. Sebutir anggur 🍇 hanya beberapa gram.\n\nMana yang lebih berat?","anggur","semangka","sama berat","tidak bisa dibanding","b",1,"pilgan"),
    ("KC-P02","Tas sekolah yang berisi buku-buku lebih berat dari tas yang kosong.\n\nMana yang lebih ringan?","tas berisi buku","sama berat","tas kosong","tidak bisa dibanding","c",1,"pilgan"),
    ("KC-P02","Sebuah kulkas 🧊 jauh lebih berat dari sebuah gelas 🥤.\n\nMana yang lebih berat?","gelas","sama berat","kulkas","tidak bisa dibanding","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-P03: Urutan kejadian dan waktu
    # ══════════════════════════════════════════════════════════════════
    ("KC-P03","Biasanya setelah bangun tidur di pagi hari, kita melakukan beberapa kegiatan.\n\nKegiatan mana yang dilakukan di PAGI hari?","tidur malam","makan malam","sarapan pagi","nonton TV malam","c",1,"pilgan"),
    ("KC-P03","Setiap pagi ada urutan kegiatan yang biasa dilakukan.\n\nUrutan yang benar adalah ...","tidur → mandi → bangun","bangun → mandi → sarapan → sekolah","sekolah → bangun → mandi","makan malam → sekolah → tidur","b",1,"pilgan"),
    ("KC-P03","Matahari sudah terbenam, langit menjadi gelap.\n\nKegiatan yang tepat dilakukan saat itu adalah ...","sarapan","berangkat sekolah","bermain siang","tidur malam","d",1,"pilgan"),
    ("KC-P03","Hari Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu berurutan.\n\nHari ini Selasa. Besok adalah hari ...","Senin","Selasa","Rabu","Kamis","c",1,"pilgan"),
    ("KC-P03","Hari Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu berurutan.\n\nHari ini Jumat. Kemarin adalah hari ...","Kamis","Jumat","Sabtu","Rabu","a",1,"pilgan"),
    ("KC-P03","Setelah matahari terbit, kita mulai hari dengan kegiatan pagi.\n\nYang pertama dilakukan saat bangun adalah ...","makan siang","berangkat sekolah","bangun dan rapikan tempat tidur","bermain sore","c",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A01: Mengenal pola berulang
    # ══════════════════════════════════════════════════════════════════
    ("KC-A01","Perhatikan urutan warna berikut.\n\n🔴🔵🔴🔵🔴🔵 → bagian yang diulang adalah ...","🔴🔴","🔵🔵","🔴🔵","🔵🔴","c",1,"pilgan"),
    ("KC-A01","Perhatikan urutan simbol berikut.\n\n⭐🌙⭐🌙⭐🌙 → ini adalah pola ...","AAAA","ABAB","AABB","ABBA","b",1,"pilgan"),
    ("KC-A01","Perhatikan urutan hewan berikut.\n\n🐱🐶🐱🐶🐱🐶 → satu bagian pola ada berapa gambar?","1","2","3","4","b",1,"pilgan"),
    ("KC-A01","Dari pilihan berikut, mana yang merupakan pola berulang?\n\nPilih jawabanmu!","1 2 3 4 5","🔴🔵🔴🔵🔴🔵","A B C D E","semua berbeda","b",1,"pilgan"),
    ("KC-A01","Perhatikan urutan warna berikut.\n\n🟡🟢🟣🟡🟢🟣 → ada berapa warna dalam satu bagian pola?","1","2","3","4","c",1,"pilgan"),
    # hitung_warna
    ("KC-A01","Perhatikan urutan berikut.\n\nHitung ada berapa 🔴 dalam: 🔴🔵🔴🔵🔴🔵🔴",
     "🔴🔵🔴🔵🔴🔵🔴","🔴","","","4",1,"hitung_warna"),

    # ══════════════════════════════════════════════════════════════════
    # KC-A02: Melanjutkan pola
    # ══════════════════════════════════════════════════════════════════
    ("KC-A02","Perhatikan pola berikut.\n\n🔴🔵🔴🔵🔴 ___ → selanjutnya?","🔴","🔵","🟡","🟢","b",1,"pilgan"),
    ("KC-A02","Perhatikan pola berikut.\n\n⭐🌙⭐🌙⭐ ___ → selanjutnya?","⭐","🌙","☀️","🌟","b",1,"pilgan"),
    ("KC-A02","Perhatikan pola berikut.\n\n🟡🟢🟣🟡🟢 ___ → selanjutnya?","🟡","🟢","🟣","🔵","c",1,"pilgan"),
    ("KC-A02","Perhatikan pola angka berikut.\n\n1 2 1 2 1 ___ → selanjutnya?","1","2","3","4","b",1,"pilgan"),
    ("KC-A02","Perhatikan pola berikut.\n\n🐱🐱🐶🐱🐱🐶🐱🐱 ___ → selanjutnya?","🐱","🐶","🐰","🐷","b",1,"pilgan"),
    ("KC-A02","Perhatikan pola berikut.\n\nbesar - kecil - besar - kecil - besar ___ → selanjutnya?","besar","kecil","sedang","sangat besar","b",1,"pilgan"),

    # ══════════════════════════════════════════════════════════════════
    # TAMBAHAN hitung_warna untuk KC operasi & bilangan
    # ══════════════════════════════════════════════════════════════════
    ("KC-B02",
     "Perhatikan kotak benda-benda berikut.\n\nHitung ada berapa 🍎 apel merah?",
     "🍎🍊🍎🍊🍎🍊🍎","🍎","","","4",1,"hitung_warna"),

    ("KC-O02",
     "Perhatikan kotak buah berikut.\n\nHitung ada berapa 🍊 jeruk?",
     "🍎🍊🍊🍎🍊🍎🍊🍊","🍊","","","5",1,"hitung_warna"),

    ("KC-O03",
     "Perhatikan kotak bola berikut.\n\nHitung ada berapa ⚽ bola hitam-putih?",
     "🏀⚽🏀⚽⚽🏀⚽⚽🏀⚽⚽⚽","⚽","","","7",2,"hitung_warna"),
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
