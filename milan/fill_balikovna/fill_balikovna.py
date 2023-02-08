# https://selenium-python.readthedocs.io/index.html
# web driver chrome 105.0.5195.52 

#add path envrioment
#control panel/user accounts/user account/change my enviroment variables/Path edit new 

#bat add var enviroment selenium 
# C:\Users\11tom\OneDrive\Dokumenty\DAYS_IN_LOVE_AUTOMATION\add_selenium.bat

#copy
# https://stackoverflow.com/questions/20573990/how-can-i-copy-a-string-to-the-windows-clipboard-python-3
# https://medium.com/analytics-vidhya/clipboard-operations-in-python-3cf2b3bd998c

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import pyperclip as pc
import os, datetime, csv
from termcolor import colored
import class_order
import set_up

def fill_form(sender_first_name,sender_second_name,sender_email,sender_phone_phone,receiver_first_name,
    receiver_second_name,receiver_email,receiver_phone,balikovna):
    """
    Function open new window balikovna.cz and input sender end receiver inforamtion, then wait for manual input address of
    post after enter close window 
    """
    balikovna_web = "https://www.balikovna.cz/cs/poslat-balik/muj-balik?utm_source=poslat-balik&utm_medium=button_HeroBanner_cz"
    service = Service(executable_path=set_up.chrome_path)
    driver = webdriver.Chrome(service=service)
    driver.get(balikovna_web)   #open balikovna web to send package
    
    text_box = driver.find_element(value="my-package_senderFirstName")
    text_box.send_keys(sender_first_name)

    text_box = driver.find_element(value="my-package_senderLastName")
    text_box.send_keys(sender_second_name)

    text_box = driver.find_element(value="my-package_senderEmail")
    text_box.send_keys(sender_email)

    text_box = driver.find_element(value="my-package_senderPhone")
    text_box.send_keys(sender_phone_phone)

    text_box = driver.find_element(value="my-package_recipientFirstName")
    text_box.send_keys(receiver_first_name)

    text_box = driver.find_element(value="my-package_recipientLastName")
    text_box.send_keys(receiver_second_name)

    text_box = driver.find_element(value="my-package_recipientEmail")
    text_box.send_keys(receiver_email)

    text_box = driver.find_element(value="my-package_recipientPhone")
    text_box.send_keys(receiver_phone)

    pc.copy(balikovna)
    a = pc.paste()

    print("Dopln adresu posty. Staci stlacit (ctrl + v) do policka.")
    print("Po zaplateni stlac enter v prikazovom riadku pre dalsiu objednavku.")

    if False:
    # in progress not working with out manual clicking on website, did not work with out manual click on website
        a = input()

        submit_button = driver.find_element(by="class name",value="my-package__button__text")

        submit_button.click()

        a = input()
        
        text_box = driver.find_element(by="class name",value="select-balikovna-form__form__input")
        text_box.send_keys("51246")

    a = input()
    driver.close()

def get_date_name():
    today = datetime.datetime.now()
    day = "0" + str(today.day) if len(str(today.day)) == 1 else str(today.day)  #change format single numbers to 2 digits numbers
    month = "0" + str(today.month) if len(str(today.month)) == 1 else str(today.month)#change format single numbers to 2 digits numbers
    return f"{day}_{month}_{today.year}.csv"

def find_file():
    dir_path = set_up.dir_path #path to downloads dir
    ref_name = get_date_name() 
    print(ref_name)
    file_path = os.path.join(dir_path,ref_name)
    input_file_name = ref_name

    while(True):
        os.system("cls")
        if ref_name != input_file_name:
            print(colored(f"Subor {file_path} nema spravne meno!!!\n","red") + f"Dopln cestu k csv suboru s dnesnym datum {input_file_name}: ",end="")
        elif os.path.isfile(file_path):
            print(colored(f"Subor {file_path} bol najdeny.","green"))
            return file_path
        else:
            print(colored(f"Subor {file_path} nebol najdeny!!!\n","red") + "Dopln cestu k csv suboru: ",end="")

        file_path = input()
        input_file_name = file_path.split("\"")[-1]

def get_orders(file_path):
    first_row = True
    cz_orders = []
    with open(file_path, "r", encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',')
        for row in spamreader:
            if first_row:
                first_row = False
                continue
            else:
                if row[16] == "CZ" :
                    objednavka = class_order.Order(number=row[0], first_name=row[3], second_name = row[4], address=row[5] + " " + row[6] + 
                    " " + row[7], email=row[9], phone=row[13], product=row[21], balikovna=row[22], first_date="")
                    cz_orders.append(objednavka)
    print(f"Pocet nacitanych objednavok {len(cz_orders)}.")
    return cz_orders

def del_number(number):
    if len(number) > 9:
        del_dig = len(number) - 9
        return number[del_dig:]
    else:
        return number

#-----------------------------------------------------------------------------------------------------

sender_info = {
    "sender_first_name" : "Tomáš",
    "sender_second_name" : "Kotian",
    "sender_email" : "11tomas16@gmail.com",
    "sender_phone_phone" : "602110829"
}

file_path = find_file()
orders = get_orders(file_path)

for order in orders:
    fill_form(sender_info["sender_first_name"],sender_info["sender_second_name"],sender_info["sender_email"], 
        sender_info["sender_phone_phone"],order.first_name,order.second_name,order.email, del_number(order.phone),order.balikovna)
