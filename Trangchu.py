import PySimpleGUI as sg
import pyodbc
from queue import PriorityQueue
from unidecode import unidecode
import time
import winsound

import PySimpleGUI as sg

MORSE_CODE = {
    'A': ".-", 'B': "-...", 'C': "-.-.", 'D': "-..", 'E': ".",
    'F': "..-.", 'G': "--.", 'H': "....", 'I': "..", 'J': ".---",
    'K': "-.-", 'L': ".-..", 'M': "--", 'N': "-.", 'O': "---",
    'P': ".--.", 'Q': "--.-", 'R': ".-.", 'S': "...", 'T': "-",
    'U': "..-", 'V': "...-", 'W': ".--", 'X': "-..-", 'Y': "-.--", 'Z': "--..",
    '1': ".----", '2': "..---", '3': "...--", '4': "....-", '5': ".....",
    '6': "-....", '7': "--...", '8': "---..", '9': "----.", '0': "-----",
    ' ': "|"
}

def am_thanh(morse_code, window):
    khungdoimau = window['doimau']
    for char in morse_code:
        if char == ".":
            khungdoimau.update(button_color=('black', 'white'))
            window.refresh()
            winsound.Beep(800, 100)
            khungdoimau.update(button_color=('gray', 'gray'))
            window.refresh()
        elif char == "-":
            khungdoimau.update(button_color=('white', 'black')),
            window.refresh()
            winsound.Beep(800, 300)
            khungdoimau.update(button_color=('gray', 'gray'))
            window.refresh()
        elif char == " ":
            time.sleep(0.1)
        elif char == "/":
            time.sleep(0.3)

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
        [
            sg.Button('🔊 Phát âm thanh', key='play_button', font=('Arial', 12, 'bold'), button_color=('white', '#007ACC')),
            sg.Button(key='doimau', font=('Arial', 12, 'bold'), button_color=('black', 'white'), size=(3,1)),
        ],
        sg.Exit('🚪 Thoát', font=('Arial', 12, 'bold'), button_color=('white', '#444444'), size=(10,1))]
    ]
    window = sg.Window('Nhóm 12 - Morse Converter', layout, element_justification='c', finalize=True)
    while True:
        event, value = window.read()
        if event in (sg.WINDOW_CLOSED, '🚪 Thoát'):
            window.close(),
            return trangchu()
        elif event == '🔄 Chuyển đổi':
            van_ban_nhap = value['vanban']
            van_ban_khong_dau = unidecode(van_ban_nhap)
            xuatmamorse = chuyen_doi_van_ban_sang_ma_morse(van_ban_khong_dau)
            window['morse'].update(xuatmamorse)
        elif event == 'play_button':
            khungdoimau = window['doimau']
            mamorse = value['morse'].strip()
            am_thanh(mamorse, window)
        elif event == '🗑️ Clear':
            window['vanban'].update("")
            window['morse'].update("")


def form_chuyen_morse():
    sg.theme('DarkGrey5')

    layout = [
        [sg.Text('🔹 Chuyển mã morse sang văn bản 🔹', font=('Arial', 18, 'bold'), text_color='#00CCFF', background_color='#1E1E1E', justification='center', expand_x=True)],
        [sg.Text('📥 Nhập mã Morse:', font=('Arial', 12, 'bold'), text_color='#DDDDDD', background_color='#1E1E1E')],
        [sg.InputText(key='-INPUT-', font=('Arial', 14), size=(50,1), background_color='#2E2E2E', text_color='white', border_width=2, justification='center')],
        [sg.Button('🔄 Chuyển đổi', font=('Arial', 12, 'bold'), button_color=('white', '#0078D7'), size=(15, 1), border_width=1, pad=(5, 15))],
        [sg.Text('📜 Kết quả:', font=('Arial', 12, 'bold'), text_color='#DDDDDD', background_color='#1E1E1E')],
        [sg.Multiline(size=(50, 5), key='-OUTPUT-', font=('Arial', 14), text_color='#00FF00', background_color='#1E1E1E', border_width=2, disabled=True, autoscroll=True)],
        [sg.Button('❌ Thoát', font=('Arial', 12, 'bold'), button_color=('white', '#D70000'), size=(15, 1), border_width=1, pad=(5, 15))]
    ]

    window = sg.Window('Nhóm 12 - Morse Converter', layout, element_justification='c', finalize=True, background_color='#1E1E1E')

    while True:
        event, value = window.read()
        if event in (sg.WINDOW_CLOSED, '❌ Thoát'):
            window.close()
            break
        elif event == '🔄 Chuyển đổi':
            Kytumorse = value['-INPUT-']
            vanbansaukhichuyendoi = chuyen_doi_morse_sang_van_ban(Kytumorse)
            window['-OUTPUT-'].update(vanbansaukhichuyendoi)


def trangchu():
    #trang chủ
    sg.theme('DarkTeal9')
    layout = [
        [sg.Button('🎯 Chuyển văn bản sang mã Morse', font=('Arial', 12, 'bold'), button_color=('white', 'green')),
        sg.Button('🎯 Chuyển mã Morse sang văn bản', font=('Arial', 12, 'bold'), button_color=('white', 'blue'))]
    ]

    window = sg.Window('Nhóm 12 - Morse Converter', layout, element_justification='c', finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '🎯 Chuyển văn bản sang mã Morse':
            window.close()
            form_chuyen_van_ban()
            break
        elif event == '🎯 Chuyển mã Morse sang văn bản':
            window.close()
            form_chuyen_morse()
            break
    window.close()


class nodecon:
    def __init__(node):
        node.con = {} # nó sẽ chứa mã morse của từ vựng
        node.tuvung = None # Đã đổi thành tuvung - Nó sẽ chứa từ vựng
        node.chi_phi = 0 # Chứa chi phí


class caynode:
    def __init__(node):
        node.goc = nodecon()

    def themnode(node, kytu, ma_morse):
        nut = node.goc
        chi_phi = ma_morse.count('.') * 1 + ma_morse.count('-') * 2
        for i in ma_morse:
            if i not in nut.con:
                nut.con[i] =  nodecon()
            nut = nut.con[i]
        nut.tuvung = kytu # Thay vì node.kytu = kytu, giờ là node.tuvung = kytu
        nut.chi_phi = chi_phi

    def tim_ma_morse_ucs(node, ky_tu):
        if ky_tu == " ": # Nếu ký tự là khoảng trắng sẽ trả về là /
            return "/"
        hang_doi_uu_tien = PriorityQueue()
        hang_doi_uu_tien.put((0, "", node.goc))  # (Chi phí, đường đi, nút hiện tại)

        while not hang_doi_uu_tien.empty():
            chi_phi, duong_di, nut_hien_tai = hang_doi_uu_tien.get()

            if nut_hien_tai.tuvung == ky_tu: 
                return duong_di

            for ky_hieu, nut_con in nut_hien_tai.con.items():
                hang_doi_uu_tien.put((chi_phi + nut_con.chi_phi, duong_di + ky_hieu, nut_con))
        return None

    def tim_ky_tu_tu_morse(node, ma_morse): #Hàm chuyển mã morse sang văn bản ( cụ thể sẽ sử dụng thuật toán dfs )
        nut = node.goc
        stack = [(nut, 0)]
        while stack:
            nut_hien_tai, index = stack.pop()
            if index == len(ma_morse):
                return nut_hien_tai.tuvung if nut_hien_tai.tuvung else "?"
            ky_hieu = ma_morse[index]
            if ky_hieu in nut_hien_tai.con:
                stack.append((nut_hien_tai.con[ky_hieu], index+1))
        return "?"


cay = caynode()
for kytu, ma_morse in MORSE_CODE.items():
    cay.themnode(kytu, ma_morse)

def chuyen_doi_van_ban_sang_ma_morse(van_ban):
    ket_qua_morse = []
    for ky_tu in van_ban.upper():
            ma_morse = cay.tim_ma_morse_ucs(ky_tu)
            ket_qua_morse.append(ma_morse if ma_morse else "?")
    return " ".join(ket_qua_morse)

def chuyen_doi_morse_sang_van_ban(ma_morse):
    ket_qua = []
    tu_morse = ma_morse.split(" / ")
    for tu in tu_morse:
        ky_tu_morse = tu.split(" ")
        tu_giai_ma = "".join(cay.tim_ky_tu_tu_morse(ky_tu) for ky_tu in ky_tu_morse)
        ket_qua.append(tu_giai_ma)
    return " ".join(ket_qua)

trangchu()