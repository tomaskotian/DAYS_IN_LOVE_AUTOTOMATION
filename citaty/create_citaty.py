import shutil, os, sys, base64

"""
TASKS:
-solve encoding problem change_text()
-implement read_punctuation.py
-create main menu 
"""

def copy_svg(template_path,save_path, number):
    new_path = os.path.join(save_path,f"{number}.svg")
    shutil.copy(template_path,new_path)
    print(f"Copied >> {new_path}")

def to_int(num):
  return int(num.split(".")[0])

def last_svg(save_path):
    files = os.listdir(save_path)
    svg_files = []
    for file in files:
        if file.endswith(".svg"):
            svg_files.append(file)
    
    svg_files.sort(key=to_int)
    return int(svg_files[-1].split(".")[0])

def change_export_name(svg_path,new_name,ready_path):
    svg_content = ""
    with open(svg_path,"r") as FR:
        for line in FR:
            if "inkscape:export-filename=" in line:
                svg_content += f"\t\t inkscape:export-filename=\"{ready_path}\{new_name}.png\"\n"
            else:
                svg_content += line
    
    with open(svg_path,"w") as FW:
        FW.write(svg_content)

def format_len(string,lenght):
    count = 0
    buf_st = ""
    for c in string:
        if count == lenght:
            buf_st += c + "\n"
            count = 1
        else:
            buf_st += c
            count += 1

    return buf_st

def change_text(svg_path,new_text,new_autor):
    svg_content = ""
    with open(svg_path,"r") as FR:
        for line in FR:
            if ">citat" in line:
                svg_content += "\t\t id=\"tspan842\">" + new_text + "</tspan></text>\n"
            elif ">autor" in line:
                svg_content += f"\t\t id=\"tspan866-9\">{new_autor}</tspan></text>\n"
            else:
                svg_content += line
    
    with open(svg_path,"wb") as FW:
        FW.write(svg_content.encode(encoding="UTF-8"))

def format_len(string,lenght):
    count = 0
    buf_st = ""
    for c in string:
        if count == lenght:
            buf_st += c + "\n"
            count = 1
        else:
            buf_st += c
            count += 1

    return buf_st

def change_image(svg_path,jpg_path,save_path):
    svg_content = ""
    jpg_content = ""
    img_flag = False

    with open(jpg_path, "rb") as FR:
        jpg_content = base64.b64encode(FR.read())
    encoded_jpg = format_len(str(jpg_content)[2:-1],76)

    with open(svg_path,"r")as FR:
        for line in FR:
            if "xlink:href=" in line:
                svg_content += f"xlink:href=\"data:image/jpeg;base64,{encoded_jpg}\"\n"
                img_flag = True
            elif img_flag:
                if "\"" in line:
                    img_flag = False
            else:
                svg_content += line

    with open(save_path, "w")as FW:
        FW.write(svg_content)

def scan_data(path):
    jpg_path = []
    svg_path = []

    if not(os.path.isdir(path)):
        print("Directory was not found!")
        sys.exit()

    for path in os.listdir(path):
        if path.endswith(".jpg"):
            jpg_path.append(path)
        elif path.endswith(".svg"):
            svg_path.append(path)

    last_jpg = len(jpg_path)+1
    for n in range(1,len(jpg_path)+1):
        if not(f"{n}.jpg" in jpg_path):
            print(f"{n}.jpg Was not found in directory!")
            last_jpg = n
            break

    last_svg = len(svg_path)+1
    for n in range(1,len(svg_path)+1):
        if not(f"{n}.svg" in svg_path):
            print(f"{n-1}.svg Last svg found in directory!")
            last_svg = n
            break

    print("---------------------------------------")
    return last_jpg, last_svg

def open_inkscape(path,num):
    os.system(f"inkscape \"{path}\\{num}.svg\"")  
    print("press any key")
    a = input()      

def load_text(citaty_path):
    text = {}
    x = 1
    with open(citaty_path,"r") as FR:
        for line in FR:
            text[x]= [line.split(">>")[0],line.split(">>")[-1][:-1]]
            x += 1

    return text


#---------------------------#
# MAIN CODE
#---------------------------#
test = False # path to test directory

if test:
    root_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\test"
    save_path = root_path
    template_path = f"{root_path}\\template.svg"
    ready_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\prispevky_ready"
    citaty_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\data_citaty.txt"
else:
    root_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\prispevky"
    save_path = root_path
    template_path = f"{root_path}\\template.svg"
    ready_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\prispevky_ready"
    citaty_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\data_citaty.txt"


citaty = load_text(citaty_path)
last_jpg,last_sv  = scan_data(root_path)

print(last_sv)

for num in range(last_sv,last_jpg):
    copy_svg(template_path,save_path,num)
    change_export_name(f"{save_path}\\{num}.svg",num,ready_path)  
    change_text(f"{save_path}\\{num}.svg",citaty[num][0],citaty[num][1])
    change_image(f"{save_path}\\{num}.svg",f"{root_path}\\{num}.jpg",f"{save_path}\\{num}.svg")
    open_inkscape(root_path,num)
