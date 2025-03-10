import PySimpleGUI as sg
from unidecode import unidecode

# Hàm chuyển đổi văn bản sang mã Morse
def chuyen_doi_van_ban_sang_ma_morse(text):
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'
    }
    text = text.upper()
    return ' '.join(morse_code_dict.get(char, '?') for char in text)

# Form giao diện
def form_chuyen_van_ban():
    sg.theme('DarkTeal9')

    layout = [
        [sg.Text('🎯 Tool chuyển văn bản sang mã Morse', font=('Arial Bold', 16), justification='center', expand_x=True, text_color='yellow')],
        [sg.Text('Nhập văn bản:', font=('Arial', 12), size=(12, 1)), 
        sg.InputText(key='vanban', font=('Arial', 12), size=(35, 1), border_width=2)],
        [sg.Button('🔄 Chuyển đổi', font=('Arial', 12, 'bold'), button_color=('white', '#007ACC'), size=(12,1))],
        [sg.Text('🎵 Mã Morse:', font=('Arial', 12), size=(12, 1)), 
        sg.Multiline(size=(35, 6), key='morse', font=('Arial', 12), text_color='yellow', background_color='#222222', border_width=2)],
        [sg.Button('🗑️ Clear', font=('Arial', 12, 'bold'), button_color=('white', 'red'), size=(10,1)), 
        sg.Exit('🚪 Thoát', font=('Arial', 12, 'bold'), button_color=('white', '#444444'), size=(10,1))]
    ]
    
    window = sg.Window('TVinh - Morse Converter', layout, element_justification='c', finalize=True)
    
    while True:
        event, value = window.read()
        if event in (sg.WINDOW_CLOSED, '🚪 Thoát'):
            window.close()
            break
        elif event == '🔄 Chuyển đổi':
            van_ban_nhap = value['vanban']
            van_ban_khong_dau = unidecode(van_ban_nhap)
            xuat_morse = chuyen_doi_van_ban_sang_ma_morse(van_ban_khong_dau)
            window['morse'].update(xuat_morse)
        elif event == '🗑️ Clear':
            window['vanban'].update('')
            window['morse'].update('')

# Chạy chương trình
if __name__ == "__main__":
    form_chuyen_van_ban()
