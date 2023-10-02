# Clearswift - dodawanie Mail Encryption Endpoints

# Importy
import os
import gzip
import shutil
import csv
import xml.etree.ElementTree as ET
import uuid
import datetime
import subprocess

# Definicje
def writeerrorlog(errorlog):
    with open('logs\\errorlog.log', 'a', encoding='utf-8') as log:
        log.write(str(datetime.datetime.now()) + errorlog + '\n')

# Parametry systemowe #
folder = 'C:\\Users\\Mateusz\\Downloads\\'
gzipiputfile = 'config\\config.xml.gz'
xmlfile = 'config\\config.xml'
csvmailhaslo = 'csv\\maile-hasla.csv'
array = []
gzipfinal = 'config\\forupload.xml.gz'

# Szukanie pliku backupu w pobranych
try:
    listaplikow = os.listdir(folder)
    for pliki in listaplikow:
        if pliki[len(pliki)-3:len(pliki)] == '.bk':
            plik = pliki
except:
    writeerrorlog(' Bląd podczas przeszukiwania folderu' + folder + ' z plikami wejsciowymi')
        
# Zmiana rozszerzenia na .xml.gz, rozpakowanie targz, usunięcie pliku oryginalnego
try:
    os.rename(folder + plik, gzipiputfile)
    with gzip.open(gzipiputfile, 'rb') as gzip_in:
        with open(xmlfile, 'wb') as xml_out:
            shutil.copyfileobj(gzip_in, xml_out)
    os.remove(gzipiputfile)
except:
    writeerrorlog(' Bląd zmiany nazwy pliku z ' + folder + ' na ' + gzipiputfile)
        
# Parsowanie csvki z danymi, Dodawanie wpisów do pliku XML w pętli
try:
    with open(csvmailhaslo, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            array.append(row)
except:
    writeerrorlog(' Błąd związanym z plikiem CSV w lokalizacji: ' + csvmailhaslo)

# Przygotowanie XML
tree = ET.parse(xmlfile)
root = tree.getroot()
addresstable = tree.find('AddressListTable')
encryptionendpoint = tree.find('EncryptionPolicyList')

# Częsć dotycząca AddressList
for user in array:
    NewAddressList = ET.Element('AddressList')
    ET.SubElement(NewAddressList, 'Address')
    addressuuid = str(uuid.uuid4())
    NewAddressList.set('name', user[0])
    NewAddressList.set('type', 'static')
    NewAddressList.set('uuid', addressuuid)
    NewAddressList.find('Address').text = user[0]
    addresstable.append(NewAddressList)
    user.append(addressuuid)
        
# Częsć dotycząca EncryptionPolicy
for user in array:
    policycount = int(encryptionendpoint.get('count')) + 1
    encryptionendpoint.set('count', str(policycount))
    NewEncryptionPolicy = ET.Element('EncryptionPolicy')
    NewEncryptionPolicy.set('enabled', 'true')
    NewEncryptionPolicy.set('expandedName', 'To user:' + user[0])
    NewEncryptionPolicy.set('name', 'To user:' + user[0])
    NewEncryptionPolicy.set('uuid', str(uuid.uuid4()))
    RouteList = ET.SubElement(NewEncryptionPolicy, 'RouteList')
    RouteItem = ET.SubElement(RouteList, 'RouteItem')
    target = ET.SubElement(RouteItem, 'target')
    target.text = user[2]
    source = ET.SubElement(RouteItem, 'source')
    source.text = '2a5efa7c-82ca-4f1e-9170-8c408f08f4f4'
    PasswordOptions = ET.SubElement(NewEncryptionPolicy, 'PasswordOptions')
    PasswordOptions.set('autogeneratePassword', 'static')
    PasswordOptions.set('encryptFileFormat', 'PASSWORD')
    PasswordOptions.set('language', 'en')
    PasswordOptions.set('logPassword', 'true')
    PasswordOptions.set('overrideEncryptFileFormat', 'true')
    PasswordOptions.set('overrideLanguage', 'true')
    PasswordOptions.set('overrideLogPassword', 'true')
    PasswordOptions.set('overridePassword', 'true')
    PasswordOptions.set('overrideProtectSubjectLine', 'true')
    PasswordOptions.set('overrideSamePassword', 'false')
    PasswordOptions.set('overrideWhatToEncrypt', 'true')
    PasswordOptions.set('password', user[1])
    PasswordOptions.set('passwordStrength', '2')
    PasswordOptions.set('protectSubjectLine', 'false')
    PasswordOptions.set('samePassword', 'true')
    PasswordOptions.set('whatToEncrypt', 'attachments_only')
    encryptionendpoint.append(NewEncryptionPolicy)

# Zapisywanie wynikowego pliku XML
tree.write(xmlfile)
        
# Zapakowanie pliku do formatu .xml.gz, zmiana rozszerzenia do .bk
with open(xmlfile, 'rb') as xml_in:
    with gzip.open(gzipfinal, 'wb') as gzip_out:
        gzip_out.writelines(xml_in)
os.rename(gzipfinal, 'config\\forupload.bk')
os.remove(xmlfile)

# Uruchomienie AHK w celu wgrania pliku do konsoli Clearswift
try:
    subprocess.call(['C:\\Program Files\\AutoHotkey\\v2\\AutoHotkey.exe', 'Clearswift-UploadBackup.ahk'])
except:
    writeerrorlog(' Błąd przy uruchamianiu pliku Clearswift-UploadBackup.ahk')
