import re
import os
import json
import ctypes
import sqlite3
import simple_colors
from pyfiglet import Figlet
from base64 import b64decode

os.system('cls && title "Booktabz Patcher! By Kali <3"')
os.system('')
custom_fig = Figlet(font='graffiti')

print(simple_colors.green(custom_fig.renderText('Booktabz Patcher!'), 'bold'))
print("\n\t\t\tBy Kali <3\n")

if not ctypes.windll.shell32.IsUserAnAdmin():
    print(simple_colors.red("[-] Please run this script with admin rights!", "bold"))
    exit()

BASE_PATH = os.getenv('localappdata') + r'\Zanichelli\Booktabz'
BOOK_PATTERN = b"ZHIDDEN=:HIDDEN"
TITLE_PATTERN = b"Versione \00\00\00\00"
DEBUG_PATTERN = b"\x48\x8B\xC8\xE8..\xFD\xFF\x0F\xB6\xD8"

def update_zhidden_to_zero(database_path):
    try:
        username = b64decode(database_path.split("\\")[-2]).decode("latin-1")
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE ZVOLUME SET ZHIDDEN = 0")
        conn.commit()
        conn.close()
        print(simple_colors.green(f"[+] Removed hidden flag for the user {username}!", "bold"))
    except sqlite3.Error as e:
        return

def navigate_and_update(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "booktab.sqlite":
                database_path = os.path.join(root, file)
                update_zhidden_to_zero(database_path)

def find_offset(f, regex_pattern):
    regex = re.compile(regex_pattern)
    matches = list(regex.finditer(f))
    if matches:
        for match in matches:
            offset = match.start()
            print(simple_colors.green(f"[!] Offset found: {hex(offset)}", "dim"))
        return matches[0].start()
    else:
        print(simple_colors.red("[-] Offset not found!", "bold"))

def patch_book(f, offset):
    if offset == None:
        print(simple_colors.red("[-] Book protection", "bold"))
        return
    f.seek(offset)
    f.write(b'\x00'*15)
    print(simple_colors.green("[+] Book protection patched!", "bold"))

def enable_debug_mode(f, offset):
    if offset == None:
        print(simple_colors.red("[-] Debug mode", "bold"))
        return
    f.seek(offset + 4)
    wildcard_bytes = f.read(2)
    patch = b"\x90\x90\x90\xE8" + wildcard_bytes + b"\xFD\xFF\x0F\xB6\xD8"
    f.seek(offset)
    f.write(patch)
    print(simple_colors.green("[+] Debug mode enabled!", "bold"))

def patch_title(f, offset):
    if offset == None:
        print(simple_colors.red("[-] Title", "bold"))
        return
    text = b"Patched by Kali <3"
    f.seek(offset)
    f.write(b'\x00'*1024)
    f.seek(offset)
    f.write(text)
    print(simple_colors.green("[+] Title patched!", "bold"))

def disable_analytics():
    path = os.getenv('localappdata') + r'\Zanichelli\Booktabz\anconf.json'
    settings = json.load(open(path, 'r', encoding="utf-8"))
    settings['analytics'] = "false"
    json.dump(settings, open(path, 'w', encoding="utf-8"))
    print(simple_colors.green("[+] Analytics disabled!", "bold"))

if __name__ == '__main__':
    print(simple_colors.yellow("[*] Patching BooktabZ.exe...", "bold"))
    try:
        print(simple_colors.yellow("[*] Opening the exe..."))
        with open("C:\Program Files (x86)\BooktabZ\\BooktabZ.exe", 'rb+') as f:
            content = f.read()
            print(simple_colors.yellow("[*] Finding the book protection offset..."))
            book_offset = find_offset(content, BOOK_PATTERN)
            print(simple_colors.yellow("[*] Finding the app title offset..."))
            title_offset = find_offset(content, TITLE_PATTERN)
            print(simple_colors.yellow("[*] Finding the developer mode offset..."))
            debug_offset = find_offset(content, DEBUG_PATTERN)
            print(simple_colors.yellow("[*] Applying the patches..."))
            enable_debug_mode(f, debug_offset)
            patch_book(f, book_offset)
            patch_title(f, title_offset)
            print(simple_colors.yellow("[*] Disabling analytics..."))
            disable_analytics()
            print(simple_colors.yellow("[*] Removing book flags..."))
            navigate_and_update(BASE_PATH)
            print(simple_colors.green("[+] Done!", "bold"))
    except Exception as e:
        print(e)
        print(simple_colors.red("[-] Something went wrong!", "bold"))
    input("Press any key to exit...")
