import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

# Fungsi untuk memastikan panjang kunci yang valid (16, 24, atau 32 byte)
def adjust_key_length(key):
    if len(key) not in [16, 24, 32]:
        key = key.ljust(32)[:32]  # Membuat kunci tepat 32 karakter
    return key

# Fungsi substitusi berdasarkan kunci substitusi
def key_based_substitution(text, sub_key):
    random.seed(sub_key)  # Menggunakan kunci substitusi sebagai seed
    substitution = {}
    letters = string.ascii_uppercase + string.ascii_lowercase
    shuffled_letters = list(letters)
    random.shuffle(shuffled_letters)  # Mengacak huruf berdasarkan kunci substitusi
    for i, letter in enumerate(letters):
        substitution[letter] = ''.join(random.choices(shuffled_letters, k=3))  # 3 huruf acak menggantikan 1 huruf
    
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

# Fungsi untuk enkripsi
def encrypt_text():
    original_text = input("Masukkan teks yang akan dienkripsi: ")
    aes_key = input("Masukkan kunci AES (16/24/32 karakter): ")
    sub_key = input("Masukkan kunci untuk mengacak substitusi: ")  # Kunci untuk substitusi acak

    # Substitusi huruf berdasarkan kunci
    substituted_text, substitution_map = key_based_substitution(original_text, sub_key)
    print(f"Hasil Substitusi: {substituted_text}")
    
    # Enkripsi pertama
    encrypted_text_1 = aes_encrypt(substituted_text, aes_key)
    print(f"Hasil Enkripsi Pertama: {encrypted_text_1}")
    
    # Enkripsi kedua
    encrypted_text_2 = aes_encrypt(encrypted_text_1, aes_key)
    print(f"Hasil Enkripsi Kedua: {encrypted_text_2}")
    
    # Enkripsi ketiga
    encrypted_text_3 = aes_encrypt(encrypted_text_2, aes_key)
    print(f"Hasil Enkripsi Ketiga: {encrypted_text_3}")
    
    return encrypted_text_3, aes_key, sub_key

# Fungsi untuk dekripsi
def decrypt_text():
    encrypted_text = input("Masukkan teks yang akan didekripsi: ")
    aes_key = input("Masukkan kunci AES (16/24/32 karakter): ")
    sub_key = input("Masukkan kunci yang digunakan untuk mengacak substitusi: ")  # Kunci substitusi

    # Dekripsi AES
    try:
        # Dekripsi ketiga
        decrypted_text_3 = aes_decrypt(encrypted_text, aes_key)
        print(f"Hasil Dekripsi Ketiga: {decrypted_text_3}")
        
        # Dekripsi kedua
        decrypted_text_2 = aes_decrypt(decrypted_text_3, aes_key)
        print(f"Hasil Dekripsi Kedua: {decrypted_text_2}")
        
        # Dekripsi pertama
        decrypted_text_1 = aes_decrypt(decrypted_text_2, aes_key)
        print(f"Hasil Dekripsi Pertama: {decrypted_text_1}")
        
        # Membalikkan substitusi berdasarkan kunci substitusi
        random.seed(sub_key)  # Pastikan kunci yang sama digunakan untuk membalikkan substitusi
        substitution_map = {}
        letters = string.ascii_uppercase + string.ascii_lowercase
        shuffled_letters = list(letters)
        random.shuffle(shuffled_letters)
        for i, letter in enumerate(letters):
            substitution_map[''.join(random.choices(shuffled_letters, k=3))] = letter
        
        original_text = ''.join(substitution_map[decrypted_text_1[i:i+3]] if decrypted_text_1[i:i+3] in substitution_map else decrypted_text_1[i:i+3] for i in range(0, len(decrypted_text_1), 3))
        
        print(f"Teks asli setelah dekripsi: {original_text}")
    except (ValueError, KeyError):
        print("Dekripsi gagal. Pastikan kunci AES dan substitusi benar.")

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
