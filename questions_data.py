# -*- coding: utf-8 -*-

MINAT_BELAJAR = {
    "title": "ANGKET MINAT BELAJAR MAHASISWA",
    "subtitle": "PENDIDIKAN PROFESI GURU (PPG)",
    "biodata_title": "Data Responden",
    "biodata_fields": [
        {"id": "nama", "label": "Nama", "type": "text"},
        {"id": "lembaga_ppg", "label": "Lembaga PPG", "type": "text"},
        {"id": "program_studi", "label": "Program Studi", "type": "text"},
        {"id": "semester", "label": "Semester", "type": "select", "options": ["1", "2", "3", "4", "5", "6", "7", "8", ">8"]}
    ],
    "likert_aspects": {
        "Aspek: Perasaan Senang dan Ketertarikan (Kognitif & Afektif)": [
            "Saya merasa antusias dan bersemangat ketika memulai perkuliahan atau workshop PPG.",
            "Materi yang dipelajari dalam PPG sangat relevan dengan bidang studi yang akan saya ajarkan.",
            "Saya senang menggali lebih dalam materi pedagogik dan profesional, meskipun di luar tuntutan tugas.",
            "Saya merasa penasaran dan tertantang untuk memecahkan studi kasus yang diberikan dalam perkuliahan.",
            "Proses belajar di PPG memberikan saya kepuasan intelektual."
        ],
        "Aspek: Perasaan Penting dan Bermakna (Relevansi)": [
            "Saya yakin bahwa semua yang saya pelajari di PPG akan sangat berguna bagi karir saya sebagai guru.",
            "Saya melihat langsung hubungan antara teori yang diajarkan dengan praktik mengajar di sekolah.",
            "Keikutsertaan saya dalam PPG adalah langkah penting untuk mewujudkan cita-cita menjadi guru profesional.",
            "Saya termotivasi untuk belajar karena ingin menjadi pendidik yang berkualitas bagi siswa.",
            "Saya merasa bahwa profesi guru adalah panggilan jiwa, dan PPG adalah proses untuk menyempurnakannya."
        ],
        "Aspek: Keterlibatan dan Perhatian (Perilaku)": [
            "Saya aktif bertanya dan berpendapat selama sesi perkuliahan atau diskusi berlangsung.",
            "Saya berusaha menyelesaikan semua tugas (teori dan praktik) dengan sungguh-sungguh dan tepat waktu.",
            "Saya sering mencari sumber belajar tambahan (buku, jurnal, video) untuk mendukung pemahaman saya.",
            "Saya tidak mudah menyerah ketika menghadapi kesulitan dalam memahami materi atau dalam praktik mengajar.",
            "Saya memanfaatkan waktu di luar jam kuliah untuk berdiskusi dengan rekan atau dosen tentang materi PPG."
        ],
        "Aspek: Dorongan Ekstrinsik dan Lingkungan": [
            "Dosen/instruktur PPG mampu menciptakan suasana belajar yang menarik dan memotivasi.",
            "Metode pembelajaran yang variatif (simulasi, PBL, microteaching) meningkatkan minat belajar saya.",
            "Dukungan dari rekan sejawat dalam kelompok belajar sangat membantu semangat belajar saya.",
            "Saya termotivasi untuk belajar dengan baik agar lulus PPG dan mendapatkan sertifikat pendidik.",
            "Fasilitas dan sumber belajar yang disediakan lembaga mendukung proses belajar saya."
        ]
    },
    "open_questions": [
        "Menurut Anda, aspek atau materi apa dalam PPG yang paling Anda minati? Jelaskan alasannya!",
        "Menurut Anda, hal apa atau situasi seperti apa yang dapat meningkatkan minat belajar Anda selama mengikuti PPG?",
        "Apakah ada saran atau kritik konstruktif untuk dosen/lembaga penyelenggara PPG agar proses pembelajaran lebih menarik dan bermakna?"
    ]
}

SIKAP_SOSIAL = {
    "title": "ANGKET SIKAP SOSIAL",
    "subtitle": "MAHASISWA PPG CALON GURU SEKOLAH DASAR",
    "biodata_title": "Bagian A: Data Responden",
    "biodata_fields": [
        {"id": "nama", "label": "Nama", "type": "text"},
        {"id": "lembaga_ppg", "label": "Lembaga PPG", "type": "text"},
        {"id": "semester", "label": "Semester", "type": "select", "options": ["1", "2", "3", "4", "5", "6", "7", "8", ">8"]},
        {"id": "usia", "label": "Usia", "type": "text"}
    ],
    "likert_aspects": {
        "A. Tanggung Jawab dan Komitmen": [
            "Saya menyelesaikan semua tugas mengajar dan administratif dengan tepat waktu",
            "Saya merasa bertanggung jawab atas perkembangan belajar semua siswa di kelas",
            "Kehadiran saya mengajar di sekolah adalah prioritas yang tidak bisa ditawar",
            "Saya bersedia mengorbankan waktu pribadi untuk memastikan siswa memahami pelajaran"
        ],
        "B. Empati dan Kepedulian": [
            "Saya dapat merasakan perasaan siswa ketika mereka mengalami kesulitan belajar",
            "Saya memperlakukan semua siswa dengan kasih sayang seperti anak sendiri",
            "Saya peka terhadap perubahan perilaku atau mood siswa di kelas",
            "Saya aktif menanyakan kabar siswa yang tampak tidak bersemangat atau sedih"
        ],
        "C. Kerja Sama dan Kolaborasi": [
            "Saya aktif berkomunikasi dengan guru lain untuk koordinasi pembelajaran",
            "Saya terbuka menerima masukan dan saran dari rekan sejawat",
            "Saya bersedia berbagi sumber belajar dan strategi mengajar dengan guru lain",
            "Saya dapat bekerja dalam tim untuk menyelesaikan program sekolah"
        ],
        "D. Hormat dan Menghargai": [
            "Saya menghormati pendapat orang tua siswa meskipun berbeda dengan pandangan saya",
            "Saya memperlakukan semua siswa secara adil tanpa memandang latar belakang mereka",
            "Saya menghargai perbedaan kemampuan dan gaya belajar setiap siswa",
            "Saya mendengarkan dengan seksama ketika siswa menyampaikan pendapatnya"
        ],
        "E. Keteladanan dan Integritas": [
            "Saya konsisten antara perkataan dan perbuatan dalam interaksi dengan siswa",
            "Saya mengakui kesalahan dan meminta maaf ketika melakukan kekeliruan di kelas",
            "Saya menjaga tutur kata dan perilaku agar layak diteladani oleh siswa",
            "Saya menjunjung tinggi nilai-nilai kejujuran dalam menilai hasil belajar siswa"
        ],
        "F. Komunikasi dan Interaksi Sosial": [
            "Saya mampu berkomunikasi secara efektif dengan orang tua dari berbagai latar belakang",
            "Saya dapat menyampaikan kritik kepada rekan sejawat dengan cara yang santun",
            "Saya aktif membangun hubungan positif dengan seluruh warga sekolah",
            "Saya mampu menyesuaikan gaya komunikasi sesuai dengan usia dan pemahaman siswa"
        ],
        "G. Adaptasi dan Fleksibilitas": [
            "Saya dapat menyesuaikan diri dengan budaya dan norma yang berlaku di sekolah",
            "Saya terbuka terhadap perubahan kurikulum dan kebijakan pendidikan baru",
            "Saya mampu menghadapi orang tua dengan karakter yang berbeda-beda",
            "Saya fleksibel dalam menerapkan strategi mengajar sesuai kebutuhan siswa"
        ]
    },
    "scenarios": [
        "Skenario 1: Seorang siswa menangis karena diejek temannya tidak bisa mengerjakan soal matematika. Bagaimana sikap dan tindakan Anda?",
        "Skenario 2: Orang tua siswa mengeluh bahwa nilai anaknya tidak sesuai harapan dan menyalahkan metode mengajar Anda. Bagaimana respons Anda?",
        "Skenario 3: Rekan guru mengajak bekerja sama memalsukan nilai ujian sekolah untuk meningkatkan prestise sekolah. Apa yang akan Anda lakukan?"
    ],
    "reflections": [
        "Menurut Anda, aspek sikap sosial apa yang paling penting bagi guru SD? Mengapa?",
        "Aspek sikap sosial mana yang paling Anda kuasai? Berikan contoh!",
        "Aspek sikap sosial mana yang masih perlu Anda tingkatkan? Bagaimana rencana pengembangannya?"
    ]
}

LIKERT_OPTIONS_MINAT = {
    5: "SS (Sangat Setuju)",
    4: "S (Setuju)",
    3: "RR (Ragu-ragu)",
    2: "TS (Tidak Setuju)",
    1: "STS (Sangat Tidak Setuju)"
}

LIKERT_OPTIONS_SIKAP = {
    5: "SS (Sangat Setuju)",
    4: "S (Setuju)",
    3: "RG (Ragu-ragu)",
    2: "TS (Tidak Setuju)",
    1: "STS (Sangat Tidak Setuju)"
}

BERPIKIR_KRITIS = {
    "title": "SOAL BERPIKIR KRITIS",
    "subtitle": "PENDIDIKAN PROFESI GURU (PPG)",
    "biodata_title": "Data Responden",
    "questions": [
        "Pak Roni ketika akan melakukan kegiatan pembelajaran dengan topik Tata Surya melakukan pre tes terlebih dahulu, Jika anda sebagai Pak Roni, analisislah apa yang akan anda lakukan selanjutnya dalam pembelajaran!",
        "Ketika melakukan proses pembelajaran Pak Beni selalu menggunakan media, kadang memutar video pembelajaran, kadang memutar CD audio, kadang menggunakan poster berwarna, agar peserta didiknya memperhatikan dan tertarik terhadap apa yang dibahasnya serta senang mengikuti pelajarannya. Buatlah rancangan media pembelajaran yang paling sesuai untuk mengajarkan tentang kebudayaan Indonesia di kelas 4 SD!",
        "Dalam sebuah sekolah, seorang guru SD yang dituntut mengarahkan proses pembelajaran ke arah karakteristik pembelajaran Abad ke-21. Untuk memenuhi hal tersebut, sekolah dalam melaksanakan rekruitmen guru telah menetapkan standar kualifikasi yang sesuai. Ibu Ani adalah salah satu calon guru yang mengikuti kegiatan rekruitmen tersebut. Ibu Ani memiliki kualifikasi pendidikan S1 dalam bidang pendidikan dan telah memiliki sertifikasi pendidik. Selain itu, Ibu Ani juga memiliki kemampuan yang mendalam dalam mengintegrasikan teknologi dalam pembelajaran, mengelola kelas dengan efektif, serta menerapkan strategi pembelajaran yang kreatif. Berdasarkan cerita tersebut, analisislah apa saja yang sudah dimiliki oleh Ibu Ani sebagai modal untuk menjadi guru dalam pembelajaran Abad ke-21!",
        "Seorang guru ingin menganalisis hasil belajar siswa setelah sebuah pembelajaran berlangsung. Guru tersebut memilih untuk menggunakan metode penilaian berupa tes tertulis dengan pilihan ganda dan esai. Setelah mengumpulkan hasil penilaian, guru tersebut akan melakukan analisis statistik untuk melihat tingkat pemahaman siswa secara keseluruhan. Analisislah tujuan dari metode penilaian yang dilakukan oleh guru tersebut!",
        "Seorang guru SD yang profesional harus memenuhi persyaratan, kualifikasi, dan kompetensi tertentu. Pak Budi, seorang guru SD yang profesional, memiliki pengalaman mengajar selama 5 tahun di tingkat SD dan telah mengikuti berbagai pelatihan terkait pengembangan kurikulum dan evaluasi pembelajaran. Selain itu, Pak Budi memiliki kemampuan dalam mendesain dan mengimplementasikan pembelajaran berbasis proyek yang melibatkan siswa secara aktif. Berdasarkan cerita tersebut, nilailah apa saja kompetensi yang dimiliki oleh Pak Budi?",
        "Seorang guru di suatu sekolah mempublikasikan informasi pribadi siswa di media sosial tanpa izin dan membagikan soal ujian kepada siswa sebelum ujian dilaksanakan. Dalam konteks ini, evaluasilah sanksi yang mungkin diterapkan terhadap guru tersebut!",
        "Pak Larso melaksanakan pembelajaran dengan menggunakan masalah sebagai langkah awal dalam mengumpulkan dan mengintergrasikan pengetahuan baru berdasarkan pengalamannya, dimulai dengan memunculkan pertanyaan penuntun (a guiding question) dan membimbing peserta didik berkolaboratif yang mengintegrasikan berbagai subjek (materi) dalam kurikulum. Analisislah model pembelajaran yang dilaksanakan oleh Pak Larso!",
        "Ketika ada siswa yang mengajukan “protes” atas jawaban ulangan yang diyakini benar tetapi dinyatakan salah oleh guru, dan terbukti bahwa jawaban yang dimaksud adalah benar, Dari kasus diatas, buatlah rancangan tindakan yang sebaiknya dilakukan oleh guru!",
        "Peserta didik dalam suatu kelas gaya belajarnya beragam ada yang visual, auditori, dan kinestetik. Namun kegiatan pembelajaran selama ini masih banyak yang konvensional- klasikal. Buatlah rancangan pembelajran yang memungkinkan dapat memenuhi ketiga gaya belajar tersebut!",
        "Tulislah beberapa hal yang perlu dipertimbangkan oleh seorang guru dalam mengembangkan kurikulum!"
    ]
}

