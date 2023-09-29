import csv
import xml.etree.ElementTree as ET
import uuid

csvmailhaslo = 'csv\\maile-hasla.csv'
xmlfile = 'backup\\forupload.xml'
array = []

# Parsowanie csvki z danymi, Dodawanie wpisów do pliku XML w pętli
with open(csvmailhaslo, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        array.append(row)
        
tree = ET.parse(xmlfile)
root = tree.getroot()
addresstable = tree.find('AddressListTable')

for address in addresstable:
    print(address.tag, address.attrib)
    emails = address.findall('Address')
    for email in emails:
        print(email.tag, email.text)
    
XMLAddressList = ET.Element('AddressList')
XMLAddress = ET.SubElement(XMLAddressList, 'Address')
print(ET.dump(XMLAddressList))

addressuuid = uuid.uuid4()
XMLAddressList.set('name', 'Mateusz')
XMLAddressList.set('type', 'static')
XMLAddressList.set('uuid', str(addressuuid))
XMLAddressList.find('Address').text = 'test'

print(ET.dump(XMLAddressList))
