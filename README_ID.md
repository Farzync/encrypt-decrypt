
# AES File Encryption & Decryption Script

Skrip Python ini digunakan untuk melakukan enkripsi dan dekripsi file menggunakan algoritma **AES** dengan mode **CBC** (Cipher Block Chaining). Skrip ini mendukung penggunaan melalui **CLI (Command Line Interface)** dengan argumen, atau dapat dijalankan dalam **mode interaktif** di mana pengguna akan diminta untuk memasukkan input secara langsung.

## Fitur
- **Enkripsi File**: Melakukan enkripsi file dengan menggunakan AES dan key yang dihasilkan dari password.
- **Dekripsi File**: Melakukan dekripsi file yang sebelumnya dienkripsi menggunakan skrip ini.
- **CLI Mode**: Dapat dijalankan langsung dengan argumen dari command line.
- **Interactive Mode**: Jika tidak ada argumen yang diberikan, skrip akan meminta input dari pengguna melalui interaksi di terminal.
- **Keamanan**: Menggunakan algoritma AES-256 dengan **Scrypt** untuk key derivation yang aman, serta `getpass` untuk input password yang aman (tidak ditampilkan di layar).

## Teknologi dan Library yang Digunakan

- **Python**: Versi 3.7 atau lebih baru
- **Cryptography Library**: Digunakan untuk enkripsi dan dekripsi.
  
  Anda dapat menginstalnya dengan menjalankan:
  
  ```bash
  pip install cryptography
  ```

## Prasyarat

Pastikan Python versi 3.7 atau lebih baru telah terpasang di sistem Anda. Jika belum, Anda dapat mengunduh dan menginstal Python dari [situs resmi Python](https://www.python.org/downloads/).

## Instalasi

1. Clone repositori atau unduh skrip ini ke komputer Anda.
2. Instal dependensi dengan menjalankan perintah berikut:

   ```bash
   pip install cryptography
   ```

## Cara Penggunaan

### 1. Menggunakan Argumen (CLI Mode)

Anda dapat menggunakan skrip ini dengan memberikan argumen langsung melalui command line. Berikut adalah format argumen yang harus digunakan:

- **Encrypt (Enkripsi File)**:

  ```bash
  python encrypt-decrypt.py encrypt <password> <input_file> <output_file>
  ```

  Contoh:

  ```bash
  python encrypt-decrypt.py encrypt passwordku file_input.txt file_encrypted.enc
  ```

- **Decrypt (Dekripsi File)**:

  ```bash
  python encrypt-decrypt.py decrypt <password> <input_file> <output_file>
  ```

  Contoh:

  ```bash
  python encrypt-decrypt.py decrypt passwordku file_encrypted.enc file_decrypted.txt
  ```

### 2. Tanpa Argumen (Interactive Mode)

Jika Anda menjalankan skrip tanpa argumen, maka skrip akan masuk ke mode interaktif dan meminta Anda memasukkan informasi yang diperlukan seperti mode (enkripsi atau dekripsi), password, file input, dan file output.

- Jalankan skrip tanpa argumen:

  ```bash
  python encrypt-decrypt.py
  ```

- Anda akan diminta untuk memasukkan informasi berikut:
  - **Mode**: Pilih `encrypt` atau `decrypt`.
  - **Password**: Masukkan password yang ingin digunakan untuk enkripsi atau dekripsi.
  - **File Input**: Path ke file yang ingin dienkripsi atau didekripsi.
  - **File Output**: Path untuk menyimpan file yang dienkripsi atau didekripsi.

Contoh:

```
Pilih mode (encrypt/decrypt): encrypt
Masukkan password: ********
Masukkan path file input: file_input.txt
Masukkan path file output: file_encrypted.enc
File berhasil dienkripsi: file_input.txt -> file_encrypted.enc
```

## Struktur Kode

- **derive_key(password, salt)**: Fungsi untuk menghasilkan kunci AES dari password yang diberikan menggunakan algoritma **Scrypt**.
- **encrypt_file(password, input_file, output_file)**: Fungsi untuk mengenkripsi file menggunakan AES-256.
- **decrypt_file(password, input_file, output_file)**: Fungsi untuk mendekripsi file yang sudah dienkripsi.
- **interactive_mode()**: Fungsi untuk menjalankan skrip dalam mode interaktif jika tidak ada argumen yang diberikan.
- **main()**: Fungsi utama yang memproses argumen dari CLI atau memanggil `interactive_mode()` jika tidak ada argumen yang diberikan.

## Error Handling

Skrip ini menangani berbagai error seperti:

- **FileNotFoundError**: Jika file input tidak ditemukan.
- **IOError**: Jika terjadi kesalahan saat membaca atau menulis file.
- **ValueError**: Jika terjadi kesalahan saat menghasilkan kunci atau mode tidak valid.

Jika ada kesalahan, pesan yang jelas akan ditampilkan ke terminal, sehingga pengguna bisa lebih mudah memahami masalah yang terjadi.

## Lisensi

Skrip ini bebas digunakan dan didistribusikan untuk keperluan non-komersial. Silakan modifikasi dan gunakan sesuai kebutuhan Anda.
