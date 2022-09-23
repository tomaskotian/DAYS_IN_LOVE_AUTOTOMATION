#!/usr/bin/env python3
#-------------------------------
# version 1.0
# 14.9.2022
#-------------------------------

import csv, os
import datetime
import sys
from typing import _ProtocolMeta 

class InfoEPH:
    def __init__(self,pocet_zasielok,meno_priezvisko, ulica, obec, psc):
        self.pocet_zasielok = pocet_zasielok
        self.meno_priezvisko = meno_priezvisko
        self.ulica = ulica
        self.obec = obec
        self.psc = psc 
        
    def get_InfoEPH(self):
        return f"""
<?xml version="1.0"?>
<EPH verzia="3.0">
    <InfoEPH>
        <Mena>EUR</Mena> 
        <TypEPH>1</TypEPH>
        <EPHID/>
        <Datum></Datum>
        <PocetZasielok>{self.pocet_zasielok}</PocetZasielok>
        <Uhrada>
            <SposobUhrady>9</SposobUhrady>
            <SumaUhrady>0.00</SumaUhrady>
        </Uhrada><DruhPPP/>
        <DruhZasielky>1</DruhZasielky>
        <SposobSpracovania>3</SposobSpracovania>
        <Odosielatel>
            <OdosielatelID/>
            <Meno>{self.meno_priezvisko}</Meno>
            <Organizacia/><Ulica>{self.ulica}</Ulica>
            <Mesto>{self.obec}</Mesto>
            <PSC>{self.psc}</PSC>
            <Krajina>SK</Krajina>
            <Telefon/>
            <Email>11tomas16@gmail.com</Email>
            <CisloUctu></CisloUctu>
        </Odosielatel>
    </InfoEPH>
    
    <Zasielky>"""

def get_days_count(first_date):
    splited_date = first_date.split(".")
    f_date = datetime.date(int(splited_date[-1]),int(splited_date[1]),int(splited_date[0]))
    l_date = datetime.date.today()
    delta = l_date - f_date
    return delta.days

class Zasielka():
    def __init__(self,obj,meno_priezvisko, ulica, obec, psc, mobil, email, produkt,balikovna,first_date):
        self.obj = obj
        self.meno_priezvisko = meno_priezvisko
        self.ulica = ulica
        self.obec = obec
        self.psc = psc 
        self.krajina = "SK"
        self.mobil = mobil
        self.email = email
        self.hmotnost = "0.4"
        self.trieda = "1"
        self.produkt = produkt
        self.balikovna = balikovna
        self.first_date = first_date

    def get_list(self):
        fotka = ""
        adresa = self.ulica + " " + self.obec + " " + self.psc
        if "PLUS" in self.produkt:
            fotka = str(self.obj)
        if self.krajina == "CZ":
            adresa = self.balikovna

        days_count = ""
        if self.first_date:
            days_count = get_days_count(self.first_date)
        
        return [self.obj,self.meno_priezvisko,adresa,self.produkt,fotka,self.first_date,days_count,""]

    def get_Zasielka(self):
        return f"""
        <Zasielka>
            <Adresat>
            <Meno>{self.meno_priezvisko}</Meno>
            <Organizacia/>
            <Ulica>{self.ulica}</Ulica>
            <Mesto>{self.obec}</Mesto>
            <PSC>{self.psc}</PSC>
            <Krajina>SK</Krajina>
            <Telefon>{self.mobil}</Telefon>
            <Email>{self.email}</Email>
            </Adresat>
            <Info>
            <CiarovyKod/>
            <ZasielkaID></ZasielkaID>
            <Hmotnost>0.4</Hmotnost>
            <CenaDobierky>0</CenaDobierky>
            <CenaPoistneho/>
            <CenaVyplatneho/>
            <Trieda>1</Trieda>
            <CisloUctu/>
            <SymbolPrevodu></SymbolPrevodu>
            <Poznamka/>
            <DruhPPP/>
            <DruhZasielky>1</DruhZasielky>
            <PocetKusov/>
            <ObsahZasielky/>
            </Info>
        </Zasielka>"""

def get_end():
    return """
    </Zasielky>
</EPH>
        """

def get_column_name(row):
    for cell in row:
        print(f"{row.index(cell)} {cell}")


csv_columns = ["objednavka","meno priezvisko","adresa","prudukt","fotka","datum k nastaveniu","pocet dni spolu","stav"]
sk_list_objednavok = []
cz_list_objednavok = []

#-----------------------------------------------------------------------------------------------------------------------
# Main  
#-----------------------------------------------------------------------------------------------------------------------
print("Zadaj cestu k csv suboru:")
path_file = input()

if path_file.endswith("\""):
    path_file = path_file[:-1]
if path_file.endswith("\""):
    path_file = path_file[0:]


if not(os.path.isfile(path_file) and path_file.endswith(".csv")):
    print(f"File {path_file} was not found")
    sys.exit()

dyl_objednavky_database = "C:\\Users\\11tom\\OneDrive\\Dokumenty\\DAYS_IN_LOVE\\DAYS IN LOVE\\dyl_objednavky_database"

actual_date = datetime.date.today().strftime(r"%d_%m_%Y")
act_day, act_month, act_year = actual_date.split("_")
dir_name = actual_date
save_path = os.path.join(dyl_objednavky_database,act_year,act_month,dir_name)

if not(os.path.isdir(save_path)):
    os.makedirs(save_path)
    print(f"Directory was created {dir_name}")

first_row = True
if os.path.isfile(path_file) and path_file.endswith(".csv"):
    with open(path_file, "r", encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',')
        for row in spamreader:
            if first_row:
                # get_column_name(row) # column names
                first_row = False
                continue
            else:
                if row[16] == "SK" :
                    objednavka = Zasielka(obj=row[0],meno_priezvisko=row[10]+" "+row[11],ulica=row[12],obec=row[14],psc=row[15], \
                                                    mobil=row[13],email=row[9],produkt=row[21],balikovna="",first_date=row[23])
                    sk_list_objednavok.append(objednavka)
                elif row[16] == "CZ" :
                    objednavka = Zasielka(obj=row[0],meno_priezvisko=row[10]+" "+row[11],ulica=row[12],obec=row[14],psc=row[15], \
                                                    mobil=row[13],email=row[9],produkt=row[21],balikovna=row[22],first_date=row[23])
                    cz_list_objednavok.append(objednavka)

first_row = True
today = datetime.datetime.now()
path_save_xml = f"{save_path}\\{today.day}_{today.month}_{today.year}.xml"
info = InfoEPH(meno_priezvisko="Tomas Kotian",obec="Jalovec",ulica="SNP 102/94",pocet_zasielok=str(len(sk_list_objednavok)),psc="97231")

path_save_csv_sk = f"{save_path}\\{today.day}_{today.month}_{today.year}_sk.csv"
path_save_csv_cz = f"{save_path}\\{today.day}_{today.month}_{today.year}_cz.csv"

# with open(path_save_xml,"w", encoding="utf8") as FW:
#     xml_str = info.get_InfoEPH()[1:] # remove new line from first line
#     for x in sk_list_objednavok:
#         xml_str += x.get_Zasielka()
#     FW.write(xml_str + get_end())
        
# with open(path_save_csv_sk,"w",newline='', encoding="utf8",) as FW:
#     write = csv.writer(FW)  
#     write.writerow(csv_columns)
#     for x in sk_list_objednavok:
#         print(x.get_list())
#         write.writerow(x.get_list())

with open(path_save_csv_cz,"w",newline='', encoding="utf8",) as FW:
    write = csv.writer(FW)  
    write.writerow(csv_columns)
    for x in cz_list_objednavok:
        print(x.get_list())
        write.writerow(x.get_list())