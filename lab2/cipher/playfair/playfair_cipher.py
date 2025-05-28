class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        seen = set()
        matrix = []
        # Thêm các ký tự trong key nếu chưa xuất hiện
        for ch in key:
            if ch not in seen and ch.isalpha():
                seen.add(ch)
                matrix.append(ch)

        # Bổ sung các ký tự còn thiếu trong bảng chữ cái (trừ J)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for ch in alphabet:
            if ch not in seen:
                matrix.append(ch)
                if len(matrix) == 25:
                    break

        # Chia ma trận thành 5x5
        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I").upper()
        encrypted_text = ""

        i = 0
        while i < len(plain_text):
            a = plain_text[i]
            b = ''
            if i + 1 < len(plain_text):
                b = plain_text[i + 1]
                if a == b:
                    b = 'X'
                    i += 1
                else:
                    i += 2
            else:
                b = 'X'
                i += 1

            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            a = cipher_text[i]
            b = cipher_text[i + 1]
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        # Loại bỏ 'X' nếu là padding
        banro = ""
        i = 0
        while i < len(decrypted_text) - 2:
            if decrypted_text[i] == decrypted_text[i + 2] and decrypted_text[i + 1] == 'X':
                banro += decrypted_text[i]
                i += 2
            else:
                banro += decrypted_text[i]
                i += 1
        banro += decrypted_text[-2:]
        if banro.endswith("X"):
            banro = banro[:-1]

        return banro
