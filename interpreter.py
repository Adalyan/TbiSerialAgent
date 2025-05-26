import os
import sys

from fnc import check_int, resource_path

keys = ["remove_text", "exclude_line", "sub_string", "crop_line","split_line"]
directives = ["device", "start", "end"]
constants = ["first", "last"]
banned_chars = "ÜĞİŞÇÖüğşçöıİ"


def crop_line(raw, index):
    lines = raw.splitlines()
    return lines[index]

def read_lines():
    lines = []
    with open(os.path.join(sys.path[0], 'settings.conf'), "rt") as fin:
        for line in fin:
            lines.append(line)
        fin.close()
    return lines

def split_line(raw,index):
    lines = raw.split(' ')
    counter = 0
    for line in lines:
        if line != '' and  counter >index :
            return line
        counter +=1

def sub_string(raw, n1, n2):
    print(raw)
    raw = raw[int(n1):int(n2)]
    print(raw)
    return raw

def remove_text(raw, chr):
    raw = raw.replace(chr.strip(), "")
    return raw

def process_command_on_raw(raw, line):
    if line.split(" ")[0].strip() == "sub_string":
        raw = sub_string(raw, line.split(" ")[1].split(",")[0], line.split(" ")[1].split(",")[1])
    if line.split(" ")[0].strip() == "remove_text":
        raw = remove_text(raw, line.split(" ")[1])
        print("remove", line.split(" ")[1])
    if line.split(" ")[0].strip() == "crop_line":
        raw = crop_line(raw, int(line.split(" ")[1]))
    if line.split(" ")[0].strip() == "split_line":
        raw = split_line(raw, int(line.split(" ")[1]))

    return raw

def read_lines_for_device(device_name):
    lines = []
    is_in_device = False
    with open(resource_path('scripts.tsc'), "rt") as fin:
        for line in fin:
            if len(line.split(" ")) == 3 \
                    and line.split(" ")[0].strip() == "device" \
                    and line.split(" ")[1].strip() == device_name \
                    and line.split(" ")[2].strip() == "start":
                is_in_device = True
            if len(line.split(" ")) == 3 \
                    and line.split(" ")[0].strip() == "device" \
                    and line.split(" ")[1].strip() == device_name \
                    and line.split(" ")[2].strip() == "end":
                is_in_device = False
            if is_in_device:
                lines.append(line)
        fin.close()
    return lines

def read_settings_for_device(device_name):
    settings = {
        "baud_rate": "9600",
        "ssl": "off"
    }
    with open(resource_path('settings.conf'), "rt") as fin:
        for line in fin:
            if len(line.split(" ")) == 3 \
                    and line.split(" ")[0].strip() == "baud_rate" \
                    and line.split(" ")[1].strip() == device_name:
                settings["baud_rate"] = line.split(" ")[2].strip()
            if len(line.split(" ")) == 3 \
                    and line.split(" ")[0].strip() == "ssl" \
                    and line.split(" ")[1].strip() == device_name:
                settings["ssl"] = line.split(" ")[2].strip()
        fin.close()
    return settings

def check_line(words):
    error = ""

    if len(words) > 0 and words[0] in keys and len(words) > 2:
        error = "Çok fazla argüman"

    if len(words) > 0 and words[0] in directives and len(words) > 3:
        error = "Çok fazla argüman"

    if len(words) > 0 and words[0] not in directives and words[0] not in keys:
        error = "Geçerli bir komut girin"

    if len(words) > 0 and words[0] == "device" and words[2] not in ["start", "end"]:
        error = """device, cihaz ismi, start/end sırasıyla yazılmalıdır"""

    if len(words) == 2 and words[0] == "exclude_line" and not (check_int(words[1]) or words[1] in constants):
        error = "geçerli bir sayı girilmelidir"

    if len(words)>0 and words[0].startswith('#'):
        error = ""

    for word in words:
        for char in word:
            if char in banned_chars:
                error = "Türkçe karakter kullanılmamalıdır"

    return error


def is_argument(word, words):
    if len(words) == 3 and word == words[1]:
        return True
    else:
        return False
