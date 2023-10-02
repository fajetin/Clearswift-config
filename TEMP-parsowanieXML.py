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
    print(ET.dump(NewEncryptionPolicy))

# Zapisywanie wynikowego pliku XML
tree.write('backup\\encryptiontests.xml')