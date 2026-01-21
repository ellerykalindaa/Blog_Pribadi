# Blog Pribadi

## Blog Pribadi
blog pribadi adalah sistem server-side yang mengelola data dan logika aplikasi blog. Tujuannya adalah menyediakan API untuk membuat, membaca, memperbarui, dan menghapus (CRUD) postingan blog, mengelola pengguna, komentar, dan autentikasi, sambil memastikan keamanan dan performa.
<hr>

## Daftar Anggota Kelompok 3
<br>1. I Putu Mahardika ( 240030041 ) --> username GitHub : putumahardika
<br>2. I NYOMAN REYNALD ADITYA PARMANDA ( 240030245 )  --> username GitHub : 
<br>3. MADE ELLERY KALINDA ( 240030341 )  --> username GitHub : ellerykalindaa
<br>4. I MADE BAGUS SATRIA PAWANA KESUMA PUTRA ( 240030244 )  --> username GitHub :
<br>5. ALIF DZULFIKAR BAGHIS ( 200030710 )  --> username GitHub :
<hr>

## Lingkungan Pengembangan dari Blog Pribadi
  ### Alat dan Teknologi:
    * Laptop >> Digunakan untuk membuat atau mengeksekusi kode program, masing - masing orang menggunakan laptop untuk terlibat dalam pengerjaan project blog pribadi ini
    * Discord >> Kita menggunakan alat komunikasi yaitu app Discord, yang memudahkan kita untuk saling berinteraksi dari jarak jauh dalam pembuatan project blog pribadi ini
  #### Bahasa Peemrograman

## Proses Bisnis dari Blog Pribadi


## ERD dari Database Blog Pribadi

![ERD Blog Pribadi](https://github.com/ellerykalindaa/Blog_Pribadi/blob/0f78d43abfaead781647fdabf4cbfd481b1debc7/blogPribadi.drawio.png)
### Entity :
#### User >> memiliki 2 Atribut :
                              ** Atribut user.id sebagai PrimaryKey nya
                              ** Atribut Nama 
    <br> Dimana  User dapat melakukan Register terlebih dahulu untuk membuat akun, jika sudah mempunyai akun User langsung bisa Login
#### Register >> memiliki 3 Atribut :
                              ** Atribut Username sebagai PrimaryKey 
                              ** Atribut User.id sebagai ForeignKey 
                              ** Atribut Password
#### Login >> memiliki 3 Atribut :
                              ** Atribut Username sebagai PrimaryKey 
                              ** Atribut User.id sebagai ForeignKey 
                              ** Atribut Password 
  <br> Untuk relasi User ke Register menggunakan One to One >> yang dimana  1 user.id memiliki 1 username atau bisa dibilang 1 user.id hanya bisa memiliki 1 akun saja.
  <br> Untuk relasi User ke Login sama menggunakan One to One >> yang dimana 1 user.id memiliki 1 akun username saja untuk login.
#### Create_Post >> memiliki 4 Atribut :
                              ** Atribut Judul sebagai PrimaryKey
                              ** Atribut Username sebagai ForeignKey 
                              ** Atribut Isi
                              ** Atribut Kategori
#### Komentar >> memiliki 3 Atribut : 
                              ** Atribut Judul sebagai PrimaryKey
                              ** Atribut Username sebagai ForeignKey
                              ** Atribut Isi
  <br> Untuk relasi User setelah melakukan Registrasi atau Login ke Create_Post yaitu One to Many >> yang dimana 1 User bisa membuat banyak postingan baru di Blog Pribadi ( bermacam judul ataupun kategori)
  
  ---
  <br> Dan untuk User, relasi di dalam Create_Post ke Komentar yaitu One to Many >> yang dimana dalam 1 postingan blog bisa membuat banyak komentar, jadi dalam 1 postingan User bisa berkomentar banyak.

  ---
  <br> Serta jika anda langsung melakukan login ataupun masuk dengan register, anda juga bisa langsung melakukan komentar di sebuah postingan >> dengan relasi One to Many >> yang dimana dalam 1 postingan blog bisa membuat banyak komentar














