import os,sys

test_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\data_citaty.txt"
prispevky_path = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\citaty\\prispevky"
data_path = "\\".join(prispevky_path.split("\\")[:-1])
file_name = "data_citaty.txt"

def get_citaty(prispevky_path,data_path,file_name):
    """
    function scan text from all generted svg, and create data_citatt.txt and backup data_citaty if already exists to old_data_citaty.txt
    """
    data = ""
    temp = ""

    def to_int(num):
        return int(num.split(".")[0])

    svg_path = []
    for path in os.listdir(prispevky_path):
        if path.endswith(".svg") and not path.startswith("temp"):
            svg_path.append(path) 
    svg_path.sort(key=to_int)

    for path in svg_path:
        with open(f"{prispevky_path}\\{path}", encoding="utf8")as FR:
            temp = ""
            for line in FR:
                if "</tspan><" in line:
                    citat = line.split(">")[1].split("<")[0]
                    temp += citat 
                    
            data += ".".join(temp.split(".")[:-1]) + ".>>" + temp.split(".")[-1] +"\n"

    if file_name in os.listdir(data_path):
        os.rename(data_path +  "\\" + file_name, data_path +  "\\" + f"old_{file_name}")

    with open(data_path + "\\" + file_name, "w")as FW:
        FW.write(data)
        print(f"NEW {file_name} was created")

get_citaty(prispevky_path,data_path,file_name)

    # with open(test_path, "r")as FR:
    #     print(FR.read())