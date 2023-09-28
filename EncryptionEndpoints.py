# Clearswift - dodawanie Mail Encryption Endpoints

# Importy
import os
import gzip
import shutil
import csv

# Parametry systemowe #
# folder = 'C:\\Users\\duda.m\\Desktop\\Python\\Clearswift\\'
configgz = 'backup\\config.xml.gz'
configxml = 'backup\\config.xml'
csvmailhaslo = 'csv\\maile-hasla.csv'
array = []
gzipfinal = 'backup\\forupload.xml.gz'

# Szukanie pliku backupu w pobranych
listaplikow = os.listdir('backup')
for pliki in listaplikow:
    if pliki[len(pliki)-3:len(pliki)] == '.bk':
        plik = pliki
print(plik)

# Zmiana rozszerzenia na .xml.gz, rozpakowanie targz, usunięcie pliku oryginalnego
os.rename('backup\\' + plik, configgz)
with gzip.open(configgz, 'rb') as gzip_in:
    with open(configxml, 'wb') as xml_out:
        shutil.copyfileobj(gzip_in, xml_out)
os.remove(configgz)

# Parsowanie csvki z danymi, Dodawanie wpisów do pliku XML w pętli
with open(csvmailhaslo, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        array.append(row)
        

# Zapakowanie pliku do formatu .xml.gz, zmiana rozszerzenia do .bk
with open(configxml, 'rb') as xml_in:
    with gzip.open(gzipfinal, 'wb') as gzip_out:
        gzip_out.writelines(xml_in)
os.rename(gzipfinal, 'backup\\forupload.bk')
os.remove(configxml)
# Uruchomienie AHK w celu wgrania pliku do konsoli Clearswift