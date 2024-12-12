from cryptography.fernet import Fernet
import os

class SecuritySystem:
    def __init__(self):
        self.key_file = "secure_key.key"
        self._create_or_load_key()

    def _create_or_load_key(self):
        """Güvenlik anahtarı oluştur veya yükle"""
        if not os.path.exists(self.key_file):
            # Yeni anahtar oluştur
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(self.key)
        else:
            # Var olan anahtarı yükle
            with open(self.key_file, 'rb') as key_file:
                self.key = key_file.read()
        
        self.fernet = Fernet(self.key)

    def encrypt_file(self, file_path):
        """Dosyayı şifrele"""
        try:
            # Dosyayı oku
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            # Şifrele
            encrypted_data = self.fernet.encrypt(file_data)
            
            # Şifrelenmiş dosyayı kaydet
            with open(file_path + '.encrypted', 'wb') as file:
                file.write(encrypted_data)
            
            # Orijinal dosyayı sil
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Şifreleme hatası: {str(e)}")
            return False

    def decrypt_file(self, encrypted_file_path):
        """Şifrelenmiş dosyayı çöz"""
        try:
            # Şifrelenmiş dosyayı oku
            with open(encrypted_file_path, 'rb') as file:
                encrypted_data = file.read()
            
            # Şifreyi çöz
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Orijinal dosyayı oluştur
            original_file = encrypted_file_path.replace('.encrypted', '')
            with open(original_file, 'wb') as file:
                file.write(decrypted_data)
            
            # Şifrelenmiş dosyayı sil
            os.remove(encrypted_file_path)
            return True
        except Exception as e:
            print(f"Şifre çözme hatası: {str(e)}")
            return False

    def secure_directory(self, directory_path):
        """Bir klasördeki tüm dosyaları şifrele"""
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if not file.endswith('.encrypted') and not file.endswith('.key'):
                    file_path = os.path.join(root, file)
                    self.encrypt_file(file_path)

    def unsecure_directory(self, directory_path):
        """Bir klasördeki tüm şifrelenmiş dosyaların şifresini çöz"""
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.encrypted'):
                    file_path = os.path.join(root, file)
                    self.decrypt_file(file_path)