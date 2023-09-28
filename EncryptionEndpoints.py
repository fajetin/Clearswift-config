# Clearswift - dodawanie Mail Encryption Endpoints

# Importy
import os
import gzip
import shutil
import csv

# Parametry systemowe #
folder = 'C:\\Users\\duda.m\\Desktop\\Python\\Clearswift\\'
configgz = 'backup\\config.xml.gz'
configxml = 'backup\\config.xml'
csvmailhaslo = 'csv\\maile-hasla.csv'
array = []

# Szukanie pliku backupu w pobranych
listaplikow = os.listdir(folder + 'backup')
plik = listaplikow[0]
print(plik)

# Zmiana rozszerzenia na .xml.gz, rozpakowanie targz, usunięcie pliku oryginalnego
#os.rename(folder + 'backup\\' + plik, folder + configgz)
#with gzip.open(folder + configgz, 'rb') as gzip_in:
#    with open(folder + configxml, 'wb') as xml_out:
#        shutil.copyfileobj(gzip_in, xml_out)
### USUNAĆ ### os.remove(folder + 'backup\\' + plik)

# Parsowanie csvki z danymi, Dodawanie wpisów do pliku XML w pętli
with open(folder + csvmailhaslo, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        array.append(row)
        

# Zapakowanie pliku do formatu .xml.gz, zmiana rozszerzenia do .bk


# Uruchomienie AHK w celu wgrania pliku do konsoli Clearswift