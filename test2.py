from queue import PriorityQueue

class TrieNode:
    def __init__(self):
        self.con = {}
        self.ma_morse = None

class Trie:
    def __init__(self):
        self.goc = TrieNode()  # Nút gốc

    def chen_vao_trie(self, ky_tu, ma_morse):
        """Thêm ký tự và mã Morse vào cây Trie"""
        nut = self.goc
        for ky_hieu in ma_morse:
            if ky_hieu not in nut.con:
                nut.con[ky_hieu] = TrieNode()
            nut = nut.con[ky_hieu]
        nut.ma_morse = ma_morse  # Lưu mã Morse

    def tim_kiem_ucs(self, ky_tu):
        """Tìm kiếm ký tự và trả về mã Morse bằng UCS"""
        hang_doi = PriorityQueue()
        chi_so = 0
        hang_doi.put((0, chi_so, self.goc, ""))

        while not hang_doi.empty():
            chi_phi, _, nut, duong_di = hang_doi.get()

            # ✅ Nếu tìm thấy ký tự
            if nut.ma_morse and ky_tu == du_lieu_morse.get(ky_tu):
                return nut.ma_morse

            # ✅ Duyệt các nhánh con
            for ky_hieu, nut_con in nut.con.items():
                chi_so += 1
                hang_doi.put((chi_phi + 1, chi_so, nut_con, duong_di + ky_hieu))

        return None  # Không tìm thấy

    def chuyen_doi_van_ban(self, van_ban):
        """Chuyển đổi văn bản thành mã Morse"""
        ket_qua = []
        for ky_tu in van_ban.upper():  # Chuyển chữ thường thành chữ hoa
            if ky_tu in du_lieu_morse:
                ket_qua.append(du_lieu_morse[ky_tu])
            else:
                ket_qua.append('?')  # Ký tự không hợp lệ
        return ' '.join(ket_qua)

# ✅ Dữ liệu Morse
du_lieu_morse = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',  
    'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
    'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',  
    'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',  
    'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',  
    'Z': '--..',   

    '0': '-----',  '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',
    '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',  

    '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', ':': '---...',
    ';': '-.-.-.', '(': '-.--.',  ')': '-.--.-', '&': '.-...',  '=': '-...-',  
    '+': '.-.-.',  '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-',
    '@': '.--.-.', ' ': '/'
}

# ✅ Tạo cây Trie và thêm dữ liệu
trie = Trie()
for ky_tu, ma_morse in du_lieu_morse.items():
    trie.chen_vao_trie(ky_tu, ma_morse)

# ✅ Nhập văn bản và chuyển đổi
van_ban = input("Nhập văn bản: ")
morse_code = trie.chuyen_doi_van_ban(van_ban)
print("Mã Morse:", morse_code)
