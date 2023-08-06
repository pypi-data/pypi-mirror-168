import numpy as np
from faker import Faker
import random
fake = Faker('es-ES')

#Datos sinteticos de nombre y apellidos cuando no hay una columna que especifique el sexo
def spanish_name(row):

    name = ''
    sex = np.random.randint(0, 2, 1) 
    if sex==1: # female
        name = fake.last_name_female() + ' ' + fake.last_name_female() + '; ' + fake.first_name_female()
    if sex!=1: # male
        name = fake.last_name_male() + ' ' + fake.last_name_male() + '; ' + fake.first_name_male()
    
    # randomly determine if two first name should be used:
    if np.random.randint(0, 2, 1) == 1:
        name = name + ' ' + fake.first_name_nonbinary()
        
    return(name)

#Correo electronico
def safe_email(row):
    return(fake.ascii_safe_email())

#Numero de telefono
def phone_number_no_national_prefix(row):
    
    phone=fake.phone_number().replace(' ', '')
    phone=phone.replace('+34','')
    
    return(phone)

#Direccion completa
def fake_address(row):
      address = fake.street_address() + ', ' + fake.city()
    
      return(address) 

letter_map = {0:'T', 1:'R', 2:'W', 3:'A', 4:'G', 5:'M', 
              6:'Y', 7:'F', 8:'P', 9:'D', 10:'X', 11:'B', 
              12:'N', 13:'J', 14:'Z', 15:'S', 16:'Q', 
              17:'V', 18:'H', 19:'L', 20:'C', 21:'K', 22:'E'}

#DNI
def national_id_gen(row):
    id_num = "".join(["{}".format(np.random.randint(0, 9)) for i in range(8)])
    letter = letter_map[int(id_num) % 23]
    national_id = str(id_num) + str(letter)
       
    return(national_id)   

#Ciudad-localidad
def city(row):
      city = fake.city()
    
      return(city) 

#Portal   
def buildingNumber(row):
      buildingNumber = random.randint(1, 300)
    
      return(buildingNumber) 

#Nombre de la calle   
def street_name(row):
      street_name = fake.street_name() 
    
      return(street_name) 
    
    
types_street=['CL', 'AV', 'PG', 'AP', 'CR', 'LG', 'AC', 'UR', 'RD',
       'RO', 'AT', 'CM', 'ZO', 'CO', 'C1', 'PD', 'PZ', 'VA', 'PS', 'RB',
       'ED', 'CD', 'RU', 'TR', 'PQ', 'CA', 'PC', 'CI', 'BO', 'VD', 'CU',
       'CJ', 'PA', 'AU', 'VI', 'CZ', 'BD', 'GV', 'CC', 'PE', 'FN', 'GT',
       'CT', 'ST', 'AL', 'MO', 'CH', 'AB', 'CS', 'PO', 'PT', 'TU', 'SA',
       'EA', 'AR', 'MT', 'GR', 'PR', 'CE', 'AM', 'RA', 'ET', 'OT', 'EX',
       'AE', 'PB', 'AG', 'PJ', 'BC', 'CÑ', 'BL', 'ES', 'TV', 'PU', 'GA',
       'FU', 'RS', 'EN', 'TS', 'MC', 'TT', 'RM', 'QT', 'ER', 'GL', 'MN',
       'P1', 'SI', 'FT', 'NC', 'SN', 'EM', 'VN', 'SD', 'SC', 'CG']

#Tipo de via
def street_type(row):
      street_type = random.choice(types_street)
    
      return(street_type) 
       
#informacion ampliada. Piso y letra
door = {0:'B', 1:'D', 2:'F', 3:'A', 4:'G', 5:'C', 
              6:'E', 7:'F', 8:'H', 9:'IZQUIERDA', 10:'DERECHA', 11:'I'}

def infoampl(row):
    num = "".join(["{}".format(np.random.randint(0, 2)) for i in range(2)])
    letter = door[int(num) % 12]
    infoampl = str(num) +' '+ str(door)  
    return(infoampl) 

#Nombre y apellidos por separado cuando no hay una columna que especifique el sexo
def name(row):

    name = ''
    sex = np.random.randint(0, 2, 1) 
    if sex==1: # female
        name = fake.first_name_female()
    if sex!=1: # male
        name = fake.first_name_male()
    
    # randomly determine if two first name should be used:
    if np.random.randint(0, 2, 1) == 1:
        name = name + ' ' + fake.first_name_nonbinary()
        
    return(name)

def last_name(row):
    last_name = fake.last_name() 
            
    return(last_name)

#Nombre y apellidos pòr separado cuando hay una columna que especifique el sexo
def gender_HM(row):
    if row['gender'] == 'M':
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex

def gender(row):
    if row['gender'] == 1:
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex
       
def gender_MF(row):
    if row['gender'] == 'F':
        name_sex = fake.first_name_female()
    else:
        name_sex = fake.first_name_male()
    return name_sex   

#Nombre y apellidos juntos cuando existe una columna de sexo
def gender_HM(row):
    if row['gender'] == 'M':
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name_male() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex

def gender(row):
    if row['gender'] == 1:
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name_male() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex
       
def gender_MF(row):
    if row['gender'] == 'F':
        name_sex = fake.last_name() + ' ' + fake.last_name() + '; ' + fake.first_name_female()
    else:
        name_sex = fake.last_name_male() + ' '+ fake.last_name() + '; '+ fake.first_name_male()
    return name_sex