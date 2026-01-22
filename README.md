# Blog Pribadi

## Blog Pribadi
blog pribadi adalah sistem server-side yang mengelola data dan logika aplikasi blog. Tujuannya adalah menyediakan API untuk membuat, membaca, memperbarui, dan menghapus (CRUD) postingan blog, mengelola pengguna, komentar, dan autentikasi, sambil memastikan keamanan dan performa.
<hr>

## Daftar Anggota Kelompok 3
<br>1. I Putu Mahardika ( 240030041 ) --> username GitHub : putumahardika
<br>2. I NYOMAN REYNALD ADITYA PARMANDA ( 240030245 )  --> username GitHub : reynaldaditya 
<br>3. MADE ELLERY KALINDA ( 240030341 )  --> username GitHub : ellerykalindaa
<br>4. I MADE BAGUS SATRIA PAWANA KESUMA PUTRA ( 240030244 )  --> username GitHub :
<br>5. ALIF DZULFIKAR BAGHIS ( 200030710 )  --> username GitHub :
<hr>

## Lingkungan Pengembangan dari Blog Pribadi
  ###  Alat dan Teknologi:
    * Laptop >> Digunakan untuk membuat atau mengeksekusi kode program, masing - masing orang menggunakan laptop untuk terlibat dalam pengerjaan project blog pribadi ini
    * Discord >> Kita menggunakan alat komunikasi yaitu app Discord, yang memudahkan kita untuk saling berinteraksi dari jarak jauh dalam pembuatan project blog pribadi ini
    * FastAPI
    * SQLAlchemy
    * SQLite
    * Pydantic
    * JWT Authentication
    * Python

## Proses Bisnis dari Blog Pribadi
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

## ERD dari Database Blog Pribadi

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

## Struktur/Informasi Detail Tabel Database
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

## Hasil Pengembangan 
### 1. Modul Autentikasi
Modul ini menangani seluruh proses keamanan pengguna, meliputi:
  * Registrasi pengguna
  * Login pengguna
  * Pembuatan dan validasi JWT
  * Proteksi endpoint menggunakan dependency FastAPI
Modul ini memastikan bahwa hanya pengguna yang terautentikasi yang dapat mengakses fitur tertentu.

### 2. Modul Post
Modul Post merupakan inti dari aplikasi blog, dengan fitur:

Create Post (posting otomatis memiliki author)
Get All Posts (menampilkan username author)
Get Post by ID
Update Post (hanya oleh author)
Delete Post (hanya oleh author)
Modul ini terhubung langsung dengan database melalui SQLAlchemy ORM dan menerapkan validasi data menggunakan Pydantic Schema.








