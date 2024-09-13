import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from datetime import datetime

# Fungsi untuk memastikan panjang kunci yang valid (16, 24, atau 32 byte)
def adjust_key_length(key):
    if len(key) not in [16, 24, 32]:
        key = key.ljust(32)[:32]  # Membuat kunci tepat 32 karakter
    return key

# Fungsi substitusi berdasarkan kunci substitusi (mengenkripsi semua karakter termasuk angka dan simbol)
def key_based_substitution(text, sub_key):
    random.seed(sub_key)  # Menggunakan kunci substitusi sebagai seed
    substitution = {}
    # Menggabungkan huruf, angka, dan simbol untuk disubstitusi
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    shuffled_chars = list(characters)
    random.shuffle(shuffled_chars)  # Mengacak semua karakter berdasarkan kunci substitusi
    
    # Membuat peta substitusi untuk semua karakter
    for i, char in enumerate(characters):
        substitution[char] = ''.join(random.choices(shuffled_chars, k=3))  # 3 karakter acak menggantikan 1 karakter
    
    substituted_text = ''.join(substitution[char] if char in substitution else char for char in text)
    return substituted_text, substitution  # Mengembalikan teks yang sudah disubstitusi dan map substitusi

# Enkripsi AES
def aes_encrypt(text, key):
    key = adjust_key_length(key)  # Memastikan panjang kunci benar
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return iv + ct

# Dekripsi AES
def aes_decrypt(encrypted_text, key):
    key = adjust_key_length(key)  # Memastikan panjang kunci benar
    iv = b64decode(encrypted_text[:24])
    ct = b64decode(encrypted_text[24:])
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted.decode('utf-8')

# Fungsi untuk membalikkan substitusi berdasarkan kunci substitusi (mengenkripsi semua karakter)
def reverse_substitution(decrypted_text_1, sub_key):
    random.seed(sub_key)  # Pastikan kunci yang sama digunakan untuk membalikkan substitusi
    substitution_map = {}
    # Menggabungkan huruf, angka, dan simbol untuk dibalikkan
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    shuffled_chars = list(characters)
    random.shuffle(shuffled_chars)
    
    # Pemetaan karakter acak ke karakter asli
    for i, char in enumerate(characters):
        substitution_map[''.join(random.choices(shuffled_chars, k=3))] = char

    # Membalikkan substitusi
    original_text = ''
    i = 0
    while i < len(decrypted_text_1):
        block = decrypted_text_1[i:i+3]
        if block in substitution_map:
            original_text += substitution_map[block]
        else:
            original_text += decrypted_text_1[i]  # Jika tidak ditemukan (misalnya spasi), tambahkan karakter asli
            i += 1
            continue
        i += 3  # Lanjutkan iterasi setiap 3 karakter
    
    return original_text

# Fungsi untuk menyimpan hasil ke file
def save_to_file(content):
    # Membuat nama file dengan format "encrypted-tanggal-dan-waktu.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"encrypted-{timestamp}.txt"
    
    # Menyimpan ke file
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Hasil enkripsi berhasil disimpan ke file: {filename}")

# Fungsi untuk enkripsi dengan jumlah putaran dinamis
def encrypt_text():
    original_text = input("Masukkan teks yang akan dienkripsi: ")
    num_layers = int(input("Masukkan berapa kali ingin mengenkripsi teks: "))
    
    # Substitusi huruf berdasarkan kunci
    sub_key = input("Masukkan kunci untuk mengacak substitusi: ")  # Kunci untuk substitusi acak
    substituted_text, substitution_map = key_based_substitution(original_text, sub_key)
    print(f"Hasil Substitusi: {substituted_text}")
    
    encrypted_text = substituted_text
    encryption_keys = []
    
    # Lakukan enkripsi sebanyak yang diinginkan user
    for i in range(num_layers):
        aes_key = input(f"Masukkan kunci AES untuk enkripsi ke-{i+1} (16/24/32 karakter): ")
        encrypted_text = aes_encrypt(encrypted_text, aes_key)
        encryption_keys.append(aes_key)
        print(f"Hasil Enkripsi ke-{i+1}: {encrypted_text}")

    # Tanya user apakah ingin menyimpan hasilnya ke file
    save_choice = input("Apakah Anda ingin menyimpan hasil enkripsi ke file? (y/n): ").lower()
    if save_choice == 'y':
        content = f"Teks Asli: {original_text}\nHasil Enkripsi: {encrypted_text}\nKunci Substitusi: {sub_key}\nKunci AES yang digunakan: {encryption_keys}"
        save_to_file(content)
    else:
        print("Hasil enkripsi tidak disimpan.")

    return encrypted_text, encryption_keys, sub_key, num_layers

# Fungsi untuk dekripsi dengan jumlah putaran dinamis
def decrypt_text():
    encrypted_text = input("Masukkan teks yang akan didekripsi: ")
    num_layers = int(input("Masukkan berapa kali teks dienkripsi: "))
    
    # Dekripsi AES dengan jumlah putaran sesuai input pengguna
    decryption_keys = []
    for i in range(num_layers):
        aes_key = input(f"Masukkan kunci AES untuk dekripsi ke-{num_layers-i}: ")
        encrypted_text = aes_decrypt(encrypted_text, aes_key)
        decryption_keys.append(aes_key)
        print(f"Hasil Dekripsi ke-{num_layers-i}: {encrypted_text}")
    
    # Masukkan kunci untuk membalikkan substitusi
    sub_key = input("Masukkan kunci yang digunakan untuk mengacak substitusi: ")
    original_text = reverse_substitution(encrypted_text, sub_key)
    
    print(f"Teks asli setelah dekripsi: {original_text}")

# Fungsi menu utama
def main_menu():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Enkripsi teks")
        print("2. Dekripsi teks")
        print("3. Keluar")
        pilihan = input("Pilih opsi (1/2/3): ")
        
        if pilihan == "1":
            encrypt_text()  # Panggil fungsi enkripsi
        elif pilihan == "2":
            decrypt_text()  # Panggil fungsi dekripsi
        elif pilihan == "3":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Jalankan menu utama
if __name__ == "__main__":
    main_menu()