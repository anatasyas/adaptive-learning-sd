"""
seed_questions.py — Isi bank soal ke DB
5+ soal per KC, total 23 KC Matematika Kelas 1 SD

Format: kc_id, soal, opt_a, opt_b, opt_c, opt_d, jawaban ('a'/'b'/'c'/'d'), difficulty (1-3)
"""

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from database import init_db, insert_question, count_questions, get_conn

init_db()

QUESTIONS = [
    # KC-B01: Mengenal bilangan 1-10
    ("KC-B01","Manakah lambang bilangan ENAM?","8","6","9","7","b",1),
    ("KC-B01","Angka 3 dibaca...","dua","empat","tiga","lima","c",1),
    ("KC-B01","Manakah lambang bilangan SEMBILAN?","6","7","8","9","d",1),
    ("KC-B01","Angka 5 dibaca...","tiga","empat","lima","enam","c",1),
    ("KC-B01","Manakah lambang bilangan DUA?","1","2","3","4","b",1),
    ("KC-B01","Angka 10 dibaca...","sembilan","delapan","tujuh","sepuluh","d",1),

    # KC-B02: Membilang 1-10
    ("KC-B02","Ada bintang sebanyak ini: ⭐⭐⭐⭐⭐. Ada berapa?","4","5","6","7","b",1),
    ("KC-B02","Ada balon sebanyak ini: 🎈🎈🎈. Ada berapa?","2","3","4","5","b",1),
    ("KC-B02","Ada apel sebanyak ini: 🍎🍎🍎🍎🍎🍎🍎. Ada berapa?","6","7","8","9","b",1),
    ("KC-B02","Ada bebek sebanyak ini: 🦆🦆. Ada berapa?","1","2","3","4","b",1),
    ("KC-B02","Ada bunga sebanyak ini: 🌸🌸🌸🌸🌸🌸🌸🌸🌸. Ada berapa?","7","8","9","10","c",1),

    # KC-B03: Mengenal bilangan 11-20
    ("KC-B03","Manakah lambang bilangan DUA BELAS?","11","12","13","14","b",1),
    ("KC-B03","Angka 15 dibaca...","tiga belas","empat belas","lima belas","enam belas","c",1),
    ("KC-B03","Manakah lambang bilangan SEMBILAN BELAS?","16","17","18","19","d",1),
    ("KC-B03","Angka 20 dibaca...","dua puluh","delapan belas","sembilan belas","tujuh belas","a",1),
    ("KC-B03","Manakah lambang bilangan SEBELAS?","10","11","12","13","b",1),
    ("KC-B03","Angka 17 dibaca...","enam belas","tujuh belas","delapan belas","sembilan belas","b",1),

    # KC-B04: Membilang 11-20
    ("KC-B04","Ada 🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺. Berapa jumlahnya?","11","12","13","14","b",2),
    ("KC-B04","Ada ikan sebanyak 15. Jika kita hitung, berhenti di angka...","13","14","15","16","c",2),
    ("KC-B04","Ada 🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈. Berapa jumlahnya?","16","17","18","19","c",2),
    ("KC-B04","Membilang dari 11 sampai 15, ada berapa bilangan?","3","4","5","6","c",2),
    ("KC-B04","Bilangan 20 terdiri dari berapa puluhan?","1","2","3","4","b",2),

    # KC-B05: Membandingkan dua bilangan
    ("KC-B05","Manakah yang LEBIH BESAR: 7 atau 4?","4","7","sama besar","tidak tahu","b",1),
    ("KC-B05","Manakah yang LEBIH KECIL: 9 atau 3?","9","sama kecil","3","tidak tahu","c",1),
    ("KC-B05","5 ... 5. Tanda yang tepat adalah...",">","<","=","tidak ada","c",1),
    ("KC-B05","8 ... 6. Tanda yang tepat adalah...","<",">","=","tidak ada","b",1),
    ("KC-B05","Mana yang LEBIH BESAR: 12 atau 18?","12","sama besar","18","tidak tahu","c",2),
    ("KC-B05","3 ... 7. Tanda yang tepat adalah...","<",">","=","tidak ada","a",1),

    # KC-B06: Urutan bilangan
    ("KC-B06","Urutan terkecil ke terbesar: 5, 2, 8, 1 adalah...","1,2,5,8","8,5,2,1","2,1,5,8","5,8,1,2","a",1),
    ("KC-B06","Bilangan setelah 7 adalah...","6","8","9","10","b",1),
    ("KC-B06","Bilangan sebelum 5 adalah...","6","4","3","2","b",1),
    ("KC-B06","Urutan terbesar ke terkecil: 3, 9, 6, 1 adalah...","1,3,6,9","9,6,3,1","6,9,3,1","3,1,9,6","b",1),
    ("KC-B06","Di antara 10 dan 14, bilangan genap yang ada adalah...","11","12","13","15","b",2),
    ("KC-B06","Bilangan sebelum 20 adalah...","17","18","19","21","c",1),

    # KC-B07: Nilai tempat satuan
    ("KC-B07","Pada bilangan 13, angka 3 menempati tempat...","puluhan","ratusan","satuan","ribuan","c",2),
    ("KC-B07","Pada bilangan 27, angka 7 menempati tempat...","puluhan","satuan","ratusan","ribuan","b",2),
    ("KC-B07","Pada bilangan 45, angka di tempat satuan adalah...","4","5","45","0","b",2),
    ("KC-B07","Bilangan 18 memiliki angka satuan...","1","8","10","18","b",2),
    ("KC-B07","Angka satuan dari 30 adalah...","3","30","0","1","c",2),
    ("KC-B07","Bilangan 9 terletak di tempat...","puluhan","ratusan","satuan","ribuan","c",1),

    # KC-B08: Nilai tempat puluhan
    ("KC-B08","Pada bilangan 24, angka 2 menempati tempat...","satuan","puluhan","ratusan","ribuan","b",2),
    ("KC-B08","Pada bilangan 36, angka di tempat puluhan adalah...","6","36","3","0","c",2),
    ("KC-B08","Bilangan 50 memiliki angka puluhan...","0","50","5","10","c",2),
    ("KC-B08","Bilangan yang memiliki 1 puluhan dan 7 satuan adalah...","71","17","107","11","b",2),
    ("KC-B08","Bilangan yang memiliki 2 puluhan dan 3 satuan adalah...","32","23","203","302","b",2),
    ("KC-B08","Berapa puluhan pada bilangan 19?","9","19","0","1","d",2),

    # KC-O01: Konsep penjumlahan
    ("KC-O01","Penjumlahan artinya kita...","mengambil","menggabungkan","memisahkan","membagi","b",1),
    ("KC-O01","Ada 2 kucing, lalu datang 3 lagi. Sekarang ada berapa?","2","3","5","6","c",1),
    ("KC-O01","Simbol untuk penjumlahan adalah...","−","+","×","÷","b",1),
    ("KC-O01","Menggabungkan 4 merah dan 2 biru hasilnya...","2","4","6","8","c",1),
    ("KC-O01","Beni punya 1 buku, diberi 1 lagi. Beni punya...","1","2","3","0","b",1),
    ("KC-O01","3 ditambah 0 sama dengan...","0","1","2","3","d",1),

    # KC-O02: Penjumlahan hasil sampai 10
    ("KC-O02","3 + 4 = ?","6","7","8","9","b",1),
    ("KC-O02","5 + 5 = ?","8","9","10","11","c",1),
    ("KC-O02","2 + 6 = ?","7","8","9","10","b",1),
    ("KC-O02","1 + 9 = ?","8","9","10","11","c",1),
    ("KC-O02","4 + 3 = ?","6","7","8","9","b",1),
    ("KC-O02","6 + 2 = ?","7","8","9","10","b",1),
    ("KC-O02","0 + 7 = ?","6","7","8","9","b",1),

    # KC-O03: Penjumlahan hasil sampai 20
    ("KC-O03","8 + 7 = ?","13","14","15","16","c",2),
    ("KC-O03","9 + 9 = ?","16","17","18","19","c",2),
    ("KC-O03","6 + 8 = ?","12","13","14","15","c",2),
    ("KC-O03","7 + 7 = ?","12","13","14","15","c",2),
    ("KC-O03","5 + 9 = ?","13","14","15","16","b",2),
    ("KC-O03","10 + 8 = ?","17","18","19","20","b",2),
    ("KC-O03","9 + 6 = ?","13","14","15","16","c",2),

    # KC-O04: Konsep pengurangan
    ("KC-O04","Pengurangan artinya kita...","menggabungkan","menambah","mengambil","mengalikan","c",1),
    ("KC-O04","Ada 7 kue, dimakan 2. Sisa berapa?","4","5","6","7","b",1),
    ("KC-O04","Simbol untuk pengurangan adalah...","+","−","×","÷","b",1),
    ("KC-O04","Siti punya 5 permen, diberikan 1. Siti punya...","6","5","4","3","c",1),
    ("KC-O04","3 diambil dari 3 hasilnya...","1","2","3","0","d",1),
    ("KC-O04","8 dikurangi 0 sama dengan...","0","1","7","8","d",1),

    # KC-O05: Pengurangan dari bilangan sampai 10
    ("KC-O05","8 − 3 = ?","4","5","6","7","b",1),
    ("KC-O05","10 − 4 = ?","5","6","7","8","b",1),
    ("KC-O05","7 − 2 = ?","4","5","6","7","b",1),
    ("KC-O05","9 − 6 = ?","2","3","4","5","b",1),
    ("KC-O05","6 − 1 = ?","4","5","6","7","b",1),
    ("KC-O05","10 − 10 = ?","0","1","2","10","a",1),
    ("KC-O05","5 − 3 = ?","1","2","3","4","b",1),

    # KC-O06: Pengurangan dari bilangan sampai 20
    ("KC-O06","15 − 7 = ?","6","7","8","9","c",2),
    ("KC-O06","18 − 9 = ?","7","8","9","10","c",2),
    ("KC-O06","20 − 6 = ?","12","13","14","15","c",2),
    ("KC-O06","17 − 8 = ?","7","8","9","10","c",2),
    ("KC-O06","14 − 5 = ?","7","8","9","10","c",2),
    ("KC-O06","20 − 13 = ?","5","6","7","8","c",2),
    ("KC-O06","16 − 7 = ?","7","8","9","10","c",2),

    # KC-O07: Hubungan penjumlahan dan pengurangan
    ("KC-O07","Jika 3 + 5 = 8, maka 8 − 5 = ?","2","3","4","5","b",3),
    ("KC-O07","Jika 7 + 4 = 11, maka 11 − 4 = ?","5","6","7","8","c",3),
    ("KC-O07","Pengurangan adalah kebalikan dari...","perkalian","pembagian","penjumlahan","penjumlahan dan perkalian","c",3),
    ("KC-O07","Jika 6 + ? = 10, maka ? = ?","3","4","5","6","b",3),
    ("KC-O07","Jika 15 − 8 = 7, maka 7 + 8 = ?","13","14","15","16","c",3),
    ("KC-O07","Jika 9 + 3 = 12, maka 12 − 9 = ?","1","2","3","4","c",3),

    # KC-G01: Mengenal bangun datar
    ("KC-G01","Bentuk ini ⭕ disebut...","segitiga","persegi","lingkaran","persegi panjang","c",1),
    ("KC-G01","Bentuk ini 🔺 disebut...","lingkaran","segitiga","persegi","bintang","b",1),
    ("KC-G01","Uang koin berbentuk...","segitiga","persegi","lingkaran","bintang","c",1),
    ("KC-G01","Buku tulis berbentuk...","lingkaran","segitiga","persegi panjang","bintang","c",1),
    ("KC-G01","Sapu tangan biasanya berbentuk...","lingkaran","segitiga","persegi","oval","c",1),
    ("KC-G01","Pizza berbentuk...","segitiga","persegi","lingkaran","persegi panjang","c",1),

    # KC-G02: Sifat bangun datar
    ("KC-G02","Berapa banyak sisi segitiga?","2","3","4","5","b",2),
    ("KC-G02","Berapa banyak sudut persegi?","2","3","4","5","c",2),
    ("KC-G02","Berapa banyak sisi lingkaran?","0","1","2","4","a",2),
    ("KC-G02","Persegi panjang memiliki berapa sisi?","3","4","5","6","b",2),
    ("KC-G02","Bangun 4 sisi sama panjang dan 4 sudut disebut...","persegi panjang","segitiga","lingkaran","persegi","d",2),
    ("KC-G02","Berapa sudut yang dimiliki segitiga?","2","3","4","5","b",2),

    # KC-G03: Mengelompokkan bangun datar
    ("KC-G03","Uang koin, roda, dan piring termasuk kelompok...","persegi","segitiga","lingkaran","persegi panjang","c",2),
    ("KC-G03","Segitiga dan persegi memiliki kesamaan yaitu...","memiliki sudut","berbentuk bulat","tidak punya sisi","4 sisi","a",2),
    ("KC-G03","Manakah yang TIDAK termasuk bangun bersudut?","segitiga","persegi","lingkaran","persegi panjang","c",2),
    ("KC-G03","Pintu, buku, dan jendela dikelompokkan sebagai...","lingkaran","segitiga","persegi panjang","persegi","c",2),
    ("KC-G03","Bangun yang tidak memiliki sudut adalah...","persegi","segitiga","persegi panjang","lingkaran","d",2),

    # KC-P01: Perbandingan panjang
    ("KC-P01","Pensil atau penghapus, mana yang biasanya lebih panjang?","penghapus","pensil","sama panjang","tidak bisa dibandingkan","b",1),
    ("KC-P01","Ular atau semut, mana yang lebih panjang?","semut","sama panjang","ular","tidak tahu","c",1),
    ("KC-P01","Jika tali A lebih pendek dari tali B, maka tali B...","lebih pendek dari A","sama panjang dengan A","lebih panjang dari A","tidak bisa dibandingkan","c",1),
    ("KC-P01","Kebalikan dari kata panjang adalah...","tinggi","pendek","lebar","besar","b",1),
    ("KC-P01","Buku atau penggaris, mana yang biasanya lebih panjang?","buku","sama panjang","penggaris","tidak tahu","c",1),
    ("KC-P01","Jalan tol atau jalan gang, mana yang lebih panjang?","jalan gang","sama panjang","jalan tol","tidak bisa dibandingkan","c",1),

    # KC-P02: Perbandingan berat
    ("KC-P02","Bola sepak atau bola tenis, mana yang biasanya lebih berat?","bola tenis","sama berat","bola sepak","tidak tahu","c",1),
    ("KC-P02","Buku atau pensil, mana yang biasanya lebih berat?","pensil","buku","sama berat","tidak tahu","b",1),
    ("KC-P02","Kebalikan dari berat adalah...","kecil","ringan","pendek","tipis","b",1),
    ("KC-P02","Jika A lebih ringan dari B, maka B...","lebih ringan dari A","sama berat dengan A","lebih berat dari A","tidak bisa dibandingkan","c",1),
    ("KC-P02","Gajah atau kucing, mana yang lebih berat?","kucing","sama berat","gajah","tidak tahu","c",1),
    ("KC-P02","Semangka atau anggur, mana yang lebih berat?","anggur","semangka","sama berat","tidak tahu","b",1),

    # KC-P03: Urutan kejadian dan waktu
    ("KC-P03","Mana yang terjadi di pagi hari?","tidur malam","makan siang","sarapan pagi","makan malam","c",1),
    ("KC-P03","Urutan kegiatan yang benar adalah...","tidur lalu bangun lalu makan","bangun lalu sarapan lalu sekolah","sekolah lalu bangun lalu sarapan","makan malam lalu sekolah","b",1),
    ("KC-P03","Kegiatan yang dilakukan MALAM hari adalah...","sarapan","sekolah","bermain siang","tidur","d",1),
    ("KC-P03","Sebelum berangkat sekolah, biasanya kita...","makan malam","tidur siang","sarapan pagi","bermain malam","c",1),
    ("KC-P03","Hari ini Senin. Besok adalah hari...","Minggu","Senin","Selasa","Rabu","c",1),
    ("KC-P03","Setelah makan siang, waktu yang tepat untuk istirahat adalah...","pagi","siang","malam","subuh","b",1),

    # KC-A01: Mengenal pola berulang
    ("KC-A01","🔴🔵🔴🔵🔴🔵. Pola ini disebut pola...","AAAB","ABAB","AABB","ABBA","b",1),
    ("KC-A01","⭐🌙⭐🌙. Satu unit pola adalah...","⭐⭐","🌙🌙","⭐🌙","🌙⭐","c",1),
    ("KC-A01","🟡🟢🟣🟡🟢🟣. Ada berapa warna dalam satu unit pola?","1","2","3","4","c",1),
    ("KC-A01","Pola ABBA contohnya...","🔴🔵🔴🔵","🔴🔵🔵🔴","🔵🔵🔴🔴","🔴🔴🔵🔵","b",1),
    ("KC-A01","Manakah yang merupakan pola berulang?","1 2 3 4 5","🔴🔵🔴🔵🔴🔵","A B C D E","2 4 8 16","b",1),
    ("KC-A01","Pada pola AB, huruf apa yang diulang?","hanya A","hanya B","A dan B","tidak ada","c",1),

    # KC-A02: Melanjutkan pola
    ("KC-A02","🔴🔵🔴🔵🔴___. Apa selanjutnya?","🔴","🔵","🟡","🟢","b",1),
    ("KC-A02","⭐🌙⭐🌙⭐___. Apa selanjutnya?","⭐","☀️","🌙","🌟","c",1),
    ("KC-A02","🟡🟢🟣🟡🟢___. Apa selanjutnya?","🟡","🟢","🟣","🔵","c",1),
    ("KC-A02","1 2 1 2 1 ___. Angka selanjutnya...","1","2","3","4","b",1),
    ("KC-A02","A B B A B B ___. Huruf selanjutnya...","A","B","C","D","a",2),
    ("KC-A02","🔺🔷🔺🔷___. Apa selanjutnya?","🔺","🔷","🟡","⭕","a",1),
]

def seed():
    if count_questions() > 0:
        print(f"Soal sudah ada ({count_questions()} soal). Jalankan dengan --force untuk reset.")
        return
    for q in QUESTIONS:
        insert_question(*q)
    total = count_questions()
    print(f"Selesai: {total} soal ditambahkan ke DB.\n")
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT kc_id, COUNT(*) as n FROM questions GROUP BY kc_id ORDER BY kc_id"
        ).fetchall()
    for row in rows:
        print(f"  {row['kc_id']}: {row['n']} soal")

if __name__ == "__main__":
    import sys
    if "--force" in sys.argv:
        with get_conn() as conn:
            conn.execute("DELETE FROM questions")
        print("Question bank dikosongkan.")
    seed()
