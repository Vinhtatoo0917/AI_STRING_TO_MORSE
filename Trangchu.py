import PySimpleGUI as sg
import pyodbc
from queue import PriorityQueue
from unidecode import unidecode
import time
import winsound 

import PySimpleGUI as sg

def am_thanh(morse_code):
    for char in morse_code:
        if char == ".":
            winsound.Beep(800, 100)
        elif char == "-":
            winsound.Beep(800, 300)
        elif char == " ":
            time.sleep(0.1)
        elif char == "/":
            time.sleep(0.2)

def form_chuyen_van_ban():
    #chuyển văn bản sang mã morse
    sg.theme('DarkTeal9')

    layout = [
        [sg.Text('🎯 Tool chuyển văn bản sang mã Morse', font=('Arial Bold', 16), justification='center', expand_x=True, text_color='yellow')],
        [sg.Text('Nhập văn bản:', font=('Arial', 12), size=(12, 1)), 
        sg.InputText(key='vanban', font=('Arial', 12), size=(35, 1), border_width=2)],
        [sg.Button('🔄 Chuyển đổi', font=('Arial', 12, 'bold'), button_color=('white', '#007ACC'), size=(12,1))],
        [sg.Text('🎵 Mã Morse:', font=('Arial', 12), size=(12, 1)), 
        sg.Multiline(size=(35, 6), key='morse', font=('Arial', 12), text_color='yellow', background_color='#222222', border_width=2)],
        [sg.Button('🗑️ Clear', font=('Arial', 12, 'bold'), button_color=('white', 'red'), size=(10,1)), 
        [sg.Button('🔊 Phát âm thanh', font=('Arial', 12, 'bold'), button_color=('white', 'green'), size=(20,1))], 
        sg.Exit('🚪 Thoát', font=('Arial', 12, 'bold'), button_color=('white', '#444444'), size=(10,1))]
    ]
    window = sg.Window('TVinh - Morse Converter', layout, element_justification='c', finalize=True)
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
        elif event == '🔊 Phát âm thanh':
            mamorse = value['morse'].strip()
            am_thanh(mamorse)

        
        

def form_chuyen_morse():
    #chuyển mã morse sang văn bản
    sg.theme('DarkTeal9')
    layout = [
        [sg.Text('Nhập mã Morse:', font=('Arial', 12))],
        [sg.InputText(key='-INPUT-', font=('Arial', 12))],
        [sg.Button('Chuyển đổi', font=('Arial', 12, 'bold'), button_color=('white', 'blue')),
         sg.Button('Thoát', font=('Arial', 12, 'bold'), button_color=('white', 'red'))]
    ]
    window = sg.Window('Chuyển mã Morse sang văn bản', layout, element_justification='c', finalize=True)
    while True:
        event, value = window.read()
        if event in (sg.WINDOW_CLOSED, '🚪 Thoát'):
            window.close(),
            return trangchu()


def trangchu():
    #trang chủ
    sg.theme('DarkTeal9')
    layout = [
        [sg.Button('🎯 Chuyển văn bản sang mã Morse', font=('Arial', 12, 'bold'), button_color=('white', 'green')), 
        sg.Button('🎯 Chuyển mã Morse sang văn bản', font=('Arial', 12, 'bold'), button_color=('white', 'blue'))]
    ]

    window = sg.Window('TVinh - Morse Converter', layout, element_justification='c', finalize=True)

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

conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-9BNK57A; Database=MAMORSE; UID=Trituenhantao; PWD=12345678;')
cursor = conx.cursor()

class nodecon:
    def __init__(node):
        node.con = {} # nó sẽ chứa mã morse của từ vựng
        node.ma_morse = None # Nó sẽ chứa từ vựng 
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
        nut.ma_morse = kytu
        nut.chi_phi = chi_phi

    def tim_ma_morse_ucs(node, ky_tu):
        if ky_tu == " ":
            return "/"
        hang_doi_uu_tien = PriorityQueue()
        hang_doi_uu_tien.put((0, "", node.goc))  # (Chi phí, đường đi, nút hiện tại)

        while not hang_doi_uu_tien.empty():
            chi_phi, duong_di, nut_hien_tai = hang_doi_uu_tien.get()
            
            if nut_hien_tai.ma_morse == ky_tu:
                return duong_di 

            for ky_hieu, nut_con in nut_hien_tai.con.items():
                hang_doi_uu_tien.put((chi_phi + nut_con.chi_phi, duong_di + ky_hieu, nut_con))
        return None



cay = caynode()
for row in cursor.execute("select * from BangMorse"):
    kytu = row.KyTu
    ma_morse = row.MaMorse
    cay.themnode(kytu, ma_morse)

def duyet_trie(nut, duong_di=""):
    if nut.ma_morse:
        print(f"{nut.ma_morse}: {duong_di} (Chi phí: {nut.chi_phi})")

    for ky_hieu, nut_con in nut.con.items():
        duyet_trie(nut_con, duong_di + ky_hieu)

def chuyen_doi_van_ban_sang_ma_morse(van_ban):
    ket_qua_morse = []
    for ky_tu in van_ban.upper():
            ma_morse = cay.tim_ma_morse_ucs(ky_tu)
            ket_qua_morse.append(ma_morse if ma_morse else "?")
    return " ".join(ket_qua_morse)

trangchu()
