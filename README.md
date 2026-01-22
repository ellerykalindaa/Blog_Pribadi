# Blog Pribadi

## I. Blog Pribadi
blog pribadi adalah sistem server-side yang mengelola data dan logika aplikasi blog. Tujuannya adalah menyediakan API untuk membuat, membaca, memperbarui, dan menghapus (CRUD) postingan blog, mengelola pengguna, komentar, dan autentikasi, sambil memastikan keamanan dan performa.
<hr>

## II. Daftar Anggota Kelompok 3
<br>1. I Putu Mahardika ( 240030041 ) --> username GitHub : putumahardika
<br>2. I NYOMAN REYNALD ADITYA PARMANDA ( 240030245 )  --> username GitHub : reynaldaditya 
<br>3. MADE ELLERY KALINDA ( 240030341 )  --> username GitHub : ellerykalindaa
<br>4. I MADE BAGUS SATRIA PAWANA KESUMA PUTRA ( 240030244 )  --> username GitHub : satriapawan
<br>5. ALIF DZULFIKAR BAGHIS ( 200030710 )  --> username GitHub : 

### Peran dan Tugas setiap Anggota :
1. I Putu Mahardika -> Membuat Dokumentasi Program Sistem Blog Pribadi di Readme, Membantu merancang Struktur, Diskusi awal dalam menentukan konsep pembuatan, Mengusulkan Frontend,Membantu menyelesaikan Backend dari Blog Pribadi, Membantu Membuat Frontend
2. I NYOMAN REYNALD ADITYA PARMANDA -> Diskusi awal dalam menentukan konsep pembuatan,Membantu merancang Struktur Program, Menyelesaikan Backend dari Blog Pribadi, Membuat Frontend
3. MADE ELLERY KALINDA -> Diskusi awal dalam menentukan konsep pembuatan, Membantu merancang Struktur Program, Menyelesaikan Backend dari Blog Pribadi, Membantu Membuat Frontend
4. I MADE BAGUS SATRIA PAWANA KESUMA PUTRA -> Diskusi awal dalam menentukan konsep pembuatan, Membantu merancang Struktur Program, Membuat PPT Materi dari Program Blog Pribadi untuk di persentasikan
# 5. ALIF DZULFIKAR BAGHIS -> Report : Gaguna, AFK, Menyusahkan Tim, Tidak ada Berkontribusi
    
<hr>
  
## III. Lingkungan Pengembangan dari Blog Pribadi
  ###  Alat dan Teknologi:
    * Laptop >> Digunakan untuk membuat atau mengeksekusi kode program, masing - masing orang menggunakan laptop untuk terlibat dalam pengerjaan project blog pribadi ini
    * Discord >> Kita menggunakan alat komunikasi yaitu app Discord, yang memudahkan kita untuk saling berinteraksi dari jarak jauh dalam pembuatan project blog pribadi ini
    * FastAPI
    * SQLAlchemy
    * SQLite
    * Pydantic
    * JWT Authentication
    * Python

## IV. Proses Bisnis dari Blog Pribadi
### 1. Registrasi Pengguna
Pengguna yang belum memiliki akun dapat melakukan registrasi dengan memasukkan data berupa username dan password.
Sistem akan:
  * Melakukan validasi data input
  * Mengenkripsi password menggunakan mekanisme hashing
  * Menyimpan data pengguna ke dalam database
  * Tahap ini bertujuan untuk memastikan hanya pengguna terdaftar yang dapat mengakses fitur utama aplikasi.

### 2. Login Pengguna
Pengguna yang telah terdaftar dapat melakukan login menggunakan kredensial yang valid.
Jika autentikasi berhasil:
  * Sistem akan menghasilkan JSON Web Token (JWT)
  * Token digunakan sebagai bukti otorisasi untuk mengakses endpoint tertentu
JWT ini wajib dikirimkan pada setiap request yang membutuhkan autentikasi, sehingga keamanan akses data tetap terjaga.

### 3. Manajemen Posting Blog
Setelah login, pengguna dapat mengelola posting blog dengan alur sebagai berikut:
  * Membuat posting baru
  * Melihat daftar seluruh posting
  * Melihat detail posting
  * Memperbarui posting
  * Menghapus posting

Saat pengguna membuat posting:
  * Sistem secara otomatis menetapkan pengguna yang sedang login sebagai author
  * Informasi author (username) akan ditampilkan saat data posting diambil (GET)

Selain itu, sistem menerapkan otorisasi, sehingga:
  * Pengguna hanya dapat mengedit dan menghapus posting miliknya sendiri
  * Pengguna tidak dapat mengubah posting milik pengguna lain

### 4. Manajemen Kategori
Kategori digunakan untuk mengelompokkan posting blog berdasarkan topik tertentu.
Setiap posting:
  * Dapat memiliki satu kategori
  * Kategori disimpan dalam tabel terpisah dan direlasikan dengan posting
Dengan adanya kategori, data posting menjadi lebih terstruktur dan mudah dikembangkan ke fitur pencarian atau filter di masa depan.

### 5. Manajemen Komentar
Pengguna dapat memberikan komentar pada posting blog yang tersedia.
Setiap komentar:
  * Terhubung dengan satu posting
  * Terhubung dengan satu pengguna
Menyimpan informasi waktu pembuatan komentar

Fitur komentar memungkinkan interaksi antar pengguna dalam aplikasi blog.

## V. ERD dari Database Blog Pribadi

![ERD Blog Pribadi](https://github.com/ellerykalindaa/Blog_Pribadi/blob/0f78d43abfaead781647fdabf4cbfd481b1debc7/blogPribadi.drawio.png)
### Entity :
#### User >> memiliki 2 Atribut :
                              ** Atribut user.id sebagai PrimaryKey nya
                              ** Atribut Nama 
  <br> *Dimana  User dapat melakukan Register terlebih dahulu untuk membuat akun, jika sudah mempunyai akun User langsung bisa Login
#### Register >> memiliki 3 Atribut :
                              ** Atribut Username sebagai PrimaryKey 
                              ** Atribut User.id sebagai ForeignKey 
                              ** Atribut Password
#### Login >> memiliki 3 Atribut :
                              ** Atribut Username sebagai PrimaryKey 
                              ** Atribut User.id sebagai ForeignKey 
                              ** Atribut Password 
  <br> *Untuk relasi User ke Register menggunakan One to One >> yang dimana  1 user.id memiliki 1 username atau bisa dibilang 1 user.id hanya bisa memiliki 1 akun saja.
  
  ---
  <br> *Untuk relasi User ke Login sama menggunakan One to One >> yang dimana 1 user.id memiliki 1 akun username saja untuk login.
#### Create_Post >> memiliki 4 Atribut :
                              ** Atribut Judul sebagai PrimaryKey
                              ** Atribut Username sebagai ForeignKey 
                              ** Atribut Isi
                              ** Atribut Kategori
#### Komentar >> memiliki 3 Atribut : 
                              ** Atribut Judul sebagai PrimaryKey
                              ** Atribut Username sebagai ForeignKey
                              ** Atribut Isi
  <br> *Untuk relasi User setelah melakukan Registrasi atau Login ke Create_Post yaitu One to Many >> yang dimana 1 User bisa membuat banyak postingan baru di Blog Pribadi ( bermacam judul ataupun kategori)
  
  ---
  <br> *Dan untuk User, relasi di dalam Create_Post ke Komentar yaitu One to Many >> yang dimana dalam 1 postingan blog bisa membuat banyak komentar, jadi dalam 1 postingan User bisa berkomentar banyak.

  ---
  <br> *Serta jika anda langsung melakukan login ataupun masuk dengan register, anda juga bisa langsung melakukan komentar di sebuah postingan >> dengan relasi One to Many >> yang dimana dalam 1 postingan blog bisa membuat banyak komentar

## VI. Struktur/Informasi Detail Tabel Database
### 1. User 
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT | Primary Key |
| name | VARCHAR(100) | Nama lengkap |
| username | VARCHAR(50) | Username login (unique) |
| email | VARCHAR(100) | Email user (unique) |
| password | VARCHAR(255) | Password terenkripsi |
| role | ENUM('admin','author') | Hak akses user |
| bio | TEXT | Deskripsi singkat penulis |
| password | TIMESTAMP | Tanggal dibuat |
| photo | VARCHAR(255) | Foto profil |
| created_at | TIMESTAMP | Tanggal dibuat |
| updated_at | TIMESTAMP | Tanggal diperbarui |

### 2. Tabel (categories)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT | Primary Key Kategori |
| name | VARCHAR(100) | Nama kategori |
| slug | VARCHAR(120) | URL kategori |
| created_at | TIMESTAMP | Tanggal dibuat |
| updated_at | TIMESTAMP | Tanggal diperbarui |

### 3. Tabel (post)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT | Primary Key Post |
| user.id |INT (FK) | Relasi ke users |
| category_id | INT (FK) | Relasi ke categories |
| title | VARCHAR(200) | Judul artikel |
| slug | VARCHAR(220) | URL artikel |
| content | TEXT | Isi artikel |
| thumbnail | VARCHAR(255) | Gambar artikel |
| status | ENUM('draft','published') | Status artikel |
| views | INT | Jumlah kunjungan |
| created_at | TIMESTAMP | Tanggal dibuat |
| updated_at | TIMESTAMP | Tanggal diperbarui |

### 4. Tabel (comments)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT | Primary Key Kategori |
| post_id |INT (FK) | Relasi ke posts |
| name | VARCHAR(100) | Nama komentator |
| email | VARCHAR(100) | Email komentator |
| comment | TEXT | Isi komentar |
| status | ENUM('pending','approved') | Status moderasi |
| created_at | TIMESTAMP | Tanggal komentar |

### 5. Tabel (tags)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT | Primary key tag |
| name | VARCHAR(50) | Nama tag |
| slug | VARCHAR(60) | URL tag |

### 6. Tabel Post (tags)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| post_id |INT (FK) | Relasi ke posts |
| tag_id | INT (FK) | Relasi ke tags |

### 7. Tabel (settings)
| Field | Tipe Data | Keterangan |
|------|----------|------------|
| id | INT (PK) | Primary key |
| site_name | VARCHAR(100) | Nama blog |
| description | TEXT | Deskripsi blog |
| logo | VARCHAR(255) | Logo blog |
| email | VARCHAR(100) | Email admin |

### Relasi Antar Tabel
  * users (1) —— (N) posts
  * categories (1) —— (N) posts
  * posts (1) —— (N) comments
  * posts (N) —— (N) tags melalui post_tags

## VII. Hasil Pengembangan 
### 1. Modul Autentikasi
Modul ini menangani seluruh proses keamanan pengguna, meliputi:
  * Registrasi pengguna
  * Login pengguna
  * Pembuatan dan validasi JWT
  * Proteksi endpoint menggunakan dependency FastAPI
Modul ini memastikan bahwa hanya pengguna yang terautentikasi yang dapat mengakses fitur tertentu.

### 2. Modul Post
Modul Post merupakan inti dari aplikasi blog, dengan fitur:
  * Create Post (posting otomatis memiliki author)
  * Get All Posts (menampilkan username author)
  * Get Post by ID
  * Update Post (hanya oleh author)
  * Delete Post (hanya oleh author)
Modul ini terhubung langsung dengan database melalui SQLAlchemy ORM dan menerapkan validasi data menggunakan Pydantic Schema.

### 3. Modul Kategori
Modul ini memungkinkan pengelolaan kategori posting, yang mencakup:
  * Menambahkan kategori baru
  * Menghubungkan kategori dengan posting
  * Menyimpan relasi kategori dalam database

### 4. Modul Komentar
  * Modul komentar berfungsi untuk:
  * Menambahkan komentar ke posting
  * Menampilkan komentar berdasarkan posting
  * Menyimpan relasi antara komentar, pengguna, dan posting

### 5. Database dan ORM
Aplikasi menggunakan:
  * SQLite sebagai database
  * SQLAlchemy ORM untuk pengelolaan data
  * Relasi antar tabel:
        ** User ↔ Post
        ** Post ↔ Category
        ** Post ↔ Comment
        ** User ↔ Comment
Pendekatan ORM mempermudah pengelolaan data dan menjaga konsistensi struktur database.

## VIII. Struktur Folder
```
app/
│
├── core/
│   └── security.py
│       # Mengatur hashing password dan JWT
│
├── database/
│   ├── db.py
│   │   # Konfigurasi koneksi database
│   └── models.py
│       # Definisi model SQLAlchemy
│
├── repositories/
│   └── post_repository.py
│       # Query database terkait post
│
├── routers/
│   ├── auth_router.py
│   │   # Endpoint autentikasi
│   ├── post_router.py
│   │   # Endpoint posting blog
│   ├── category_router.py
│   │   # Endpoint kategori
│   └── comment_router.py
│       # Endpoint komentar
│
├── schema/
│   ├── user_schema.py
│   │   # Schema User dan Author
│   └── post_schema.py
│       # Schema Post dan Comment
│
├── services/
│   └── post_service.py
│       # Logika bisnis posting
│
└── main.py
    # Entry point aplikasi
```

## IX. Cara Instalasi dan Menjalankan Informasi
### 1. Clone Repository
```
git clone <url-repository>
cd Blog_Pribadi
```
### 2. Membuat dan Mengaktifkan Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate
```
### 3. Instalasi Dependency
```
pip install -r requirements.txt
```
### 4. Menjalankan Server
```
uvicorn app.main:app --reload
```
### 5. Akses Dokumentasi API
FastAPI menyediakan dokumentasi otomatis:
  * Swagger UI
    ```
    http://127.0.0.1:8000/docs
    ```
  * ReDoc
    ```
    http://127.0.0.1:8000/redoc
    ```



