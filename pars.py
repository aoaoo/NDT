###Comments###
#Python v3.5.0
#openpyxl v2.5.3
print('***Ez a kód a PUHY-HP, P és EP szériák esetében számolja össze a beltéri egységekhez szükséges jointokat (azaz a kültéri egységek összekötéséhez szükséges darabokat ehhez hozzá kell venni, ha van ilyen.***')
print('***Jelenleg beta verzióban működik, az eredmények ellenőrzése szükséges.***')
print('***A jelenlegi verzió nem számolja a szükséges szűkítők és az azokhoz szükséges extra csőmennyiségek mértékét. Ezzel összhangban nem a Mitsubishi szabványos elágazásait adja meg.***')
print('***A végleges verzió esetén az eredmények ellenőrzése kimerülhet a Design Tool-ból exportálható és az innen számolt csőmennyiségek és gázrátöltés összehasonlításával.***')
print('***Amennyiben a G11-nél vagy a Mitsubishi New Design Tool v1.90 frissebb megjelenik, úgy ellenőrizni kell a kódba égetett adatokat.***')
print('***Használat ... in progress***')
print('***Forráskód: https://github.com/aoaoo/NDT***')
print()
print("***Begin***")
print()

#import modules
import string
import re

###Functions###

#Check extra infos (modifications because of high distances)
#The pipe diameter between the outdoor unit and the first branch
def ou_branch (si, ty): #size and type of the outdoor unit
	if ty == 'EP':
		EP_dict = {
		200: [10, 22],
		250: [10, 22],
		300: [10, 28],
		350: [12, 28],
		400: [12, 28],
		450: [16, 28],
		500: [16, 28],
		550: [16, 28],
		600: [16, 28],
		650: [16, 28],
		700: [20, 35],
		750: [20, 35],
		800: [20, 35],
		850: [20, 42],
		900: [20, 42],
		950: [20, 42],
		1000: [20, 42],
		1050: [20, 42],
		1100: [20, 42],
		1150: [20, 42],
		1200: [20, 42],
		1250: [20, 42],
		1300: [20, 42],
		1350: [20, 42]		
		}
		return EP_dict[si]
	elif ty == 'HP':
		HP_dict = {
		200: [12, 20],
		250: [12, 22],
		400: [16, 28],
		500: [16, 28]		
		}
		return HP_dict[si]	
	else: #ty == 'P'
		P_dict = {
		200: [10, 22],
		250: [10, 22],
		300: [10, 22],
		350: [12, 28],
		400: [12, 28],
		450: [16, 28],
		500: [16, 28],
		550: [16, 28],
		600: [16, 28],
		650: [16, 28],
		700: [20, 35],
		750: [20, 35],
		800: [20, 35],
		850: [20, 42],
		900: [20, 42],
		950: [20, 42],
		1000: [20, 42],
		1050: [20, 42],
		1100: [20, 42],
		1150: [20, 42],
		1200: [20, 42],
		1250: [20, 42],
		1300: [20, 42],
		1350: [20, 42]		
		}
		return P_dict[si]


#Check extra infos (modifications because of high distances)
#The pipe diameter between the indoor unit and the branch
def iu_branch (si, ty): #size of the connected indoor unit, and the type of the system (based on the data, now this second variable negigible)
	if ty == 'EP':
		EP_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
		22: [6, 12],
		25: [6, 12],
		32: [6, 12],
		35: [6, 12],
		40: [6, 12],
		42: [6, 12],
		50: [6, 12],
		63: [10, 16],
		71: [10, 16],
		80: [10, 16],
		100: [10, 16],
		125: [10, 16],
		140: [10, 16],
		200: [10, 20],
		250: [10, 22]
		}
		return EP_dict[si]
	elif ty == 'HP':
		HP_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
		22: [6, 12],
		25: [6, 12],
		32: [6, 12],
		35: [6, 12],
		40: [6, 12],
		42: [6, 12],
		50: [6, 12],
		63: [10, 16],
		71: [10, 16],
		80: [10, 16],
		100: [10, 16],
		125: [10, 16],
		140: [10, 16],
		200: [10, 20],
		250: [10, 22]
		}
		return HP_dict[si]
	else: #ty == 'P'
		P_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
		22: [6, 12],
		25: [6, 12],
		32: [6, 12],
		35: [6, 12],
		40: [6, 12],
		42: [6, 12],
		50: [6, 12],
		63: [10, 16],
		71: [10, 16],
		80: [10, 16],
		100: [10, 16],
		125: [10, 16],
		140: [10, 16],
		200: [10, 20],
		250: [10, 22]
		}
		return P_dict[si]

		
#Check extra infos (modifications because of high distances)
#The pipe diameter between two branches
def branch_branch (si, ty): #size of the total down-stream indoor capacity (and the outdoor unit type)
	if ty == 'EP':
		if si <= 140:
			return [10, 16]
		elif si <= 200:
			return [10, 20]
		elif si <= 300:
			return [10, 22]
		elif si <= 400:
			return [12, 28]
		elif si <= 650:
			return [16, 28]
		elif si <= 800:
			return [20, 35]
		else:
			return [20, 42]
	elif ty == 'HP':
		if si <= 140:
			return [10, 16]
		elif si <= 200:
			return [10, 20]
		elif si <= 300:
			return [10, 22]
		elif si <= 400:
			return [12, 28]
		elif si <= 650:
			return [16, 28]
		else:
			return [-1,-1]
	else: #ty == 'P'
		if si <= 140:
			return [10, 16]
		elif si <= 200:
			return [10, 20]
		elif si <= 300:
			return [10, 22]
		elif si <= 400:
			return [12, 28]
		elif si <= 650:
			return [16, 28]
		elif si <= 800:
			return [20, 35]
		else:
			return [20, 42]

###Values from string###
def get_num (s, typ): #String and type of the expected value; need: 'import re'
	if typ == 'float':
		return float(re.search(r'[-]?\d+[.]?\d{0,3}', s.replace(',' , '.')).group(0))
	elif typ == 'int':
		return int(re.search(r'[-]?\d+', s).group(0))
	else: #positive int
		return int(re.search(r'\d+', s).group(0))

#bend length correction
def bend_len_corr (si, ty): #size of the connected indoor unit, and the type of the system
	if ty == 'EP':
		EP_dict = {
			200: 0.42,
			250: 0.42,
			300: 0.47,
			350: 0.47,
			400: 0.50,
			450: 0.50,
			500: 0.50,
			550: 0.50,
			600: 0.50,
			650: 0.50,
			700: 0.70,
			750: 0.70,
			800: 0.70,
			850: 0.80,
			900: 0.80,
			950: 0.80,
			1000: 0.80,
			1050: 0.80,
			1100: 0.80,
			1150: 0.80,
			1200: 0.80,
			1250: 0.80,
			1300: 0.80,
			1350: 0.80
		}
		return EP_dict[si]
	elif ty == 'HP':
		HP_dict = {
			200: 0.30,
			250: 0.35,
			400: 0.50,
			500: 0.50
		}
		return HP_dict[si]
	else: #ty == 'P'
		P_dict = {
			200: 0.42,
			250: 0.42,
			300: 0.47,
			350: 0.47,
			400: 0.50,
			450: 0.50,
			500: 0.50,
			550: 0.50,
			600: 0.50,
			650: 0.50,
			700: 0.70,
			750: 0.70,
			800: 0.70,
			850: 0.80,
			900: 0.80,
			950: 0.80,
			1000: 0.80,
			1050: 0.80,
			1100: 0.80,
			1150: 0.80,
			1200: 0.80,
			1250: 0.80,
			1300: 0.80,
			1350: 0.80
		}
		return P_dict[si]

###Import data###
import xml.etree.ElementTree as ET
tree = ET.parse('ndtv.xml')
root = tree.getroot()

###var
elemtyp = list() #Outdoor / Indoor, Branch
size = list() #The capacity of the units
joker1 = list() #Random joker
parentid = list()
piplen = list() #Pipe length before the unit #Expect outdoor unit
c_piplen = list() #The equivalent pipe length
numbend	= list() #Number of bent before the unit #Expect the outdoort unit
a = 0 #Where a = ID (a = NDT_ID - 1)
systyp = '' #system type: P, HP, EP
dbou_unit = 1
#lenA lenB lenC nenD lenE bendA bendB bendC bendD bendE #Tho outdoor units piping length

for unit in root.iter('Unit'):
	elemtyp.append(unit.get('Model'))
	if elemtyp[a] == 'Outdoor':
		size.append(get_num(unit.get('ModelName'),'pint'))
		parentid.append(-1)
		piplen.append(0)
		numbend.append(0)
		systyp = (re.search(r'[-][E,H]?[P]', unit.get('ModelName')).group(0)).replace('-', '')
		lenA = get_num(unit.get('PipeLengthA'),'float')
		bendA = get_num(unit.get('BendA'), 'pint')
		piplen.append(lenA)
		numbend.append(bendA)
		try:
			lenB = get_num(unit.get('PipeLengthB'),'float'); lenB
			bendB = get_num(unit.get('BendB'), 'pint')
			piplen.append(lenB)
			numbend.append(bendB)
			dbou_unit += 1
			lenC = get_num(unit.get('PipeLengthC'),'float')
			bendC = get_num(unit.get('BendC'), 'pint')
			piplen.append(lenC)
			numbend.append(bendC)
			dbou_unit += 1
			lenD = get_num(unit.get('PipeLengthD'),'float')
			bendD = get_num(unit.get('BendD'), 'pint')
			piplen.append(lenD)
			numbend.append(bendD)
			dbou_unit += 1
			lenE = get_num(unit.get('PipeLengthE'),'float')
			bendE = get_num(unit.get('BendE'), 'pint')
			piplen.append(lenE)
			numbend.append(bendE)
		except AttributeError:
			pass
	elif elemtyp[a] == 'Indoor':
		size.append(get_num(unit.get('ModelName'),'pint'))
		parentid.append(int(unit.get('ParentUnitID')) - 1)
		piplen.append(get_num(unit.get('PipeLength'),'float'))
		numbend.append(get_num(unit.get('Bend'),'pint'))
	elif elemtyp[a] == 'Branch': #Jump the frist branch pilength, and bend values, use lenA;;lenE and bendA;;bendE
		size.append(0)
		parentid.append(int(unit.get('ParentUnitID')) - 1)
		if a != 1:
			piplen.append(get_num(unit.get('PipeLength'),'float'))
			numbend.append(get_num(unit.get('Bend'),'pint'))
	else:
		print('Unknown device type in sequence (0;;unit): ' + str(a))#Err mess
	bend_len_corr(200, 'EP')
	c_piplen.append(float(numbend[a]*bend_len_corr(size[0], systyp) + piplen[a]))
	a += 1
a -= 1
	
###Building the tree###
###var
leftsize = [0] * (a + 1) #give the capacity connected on the 1st side 
rightsize = [0] * (a + 1) #give the capacity connected on the 2nd side
leftchild = [-1] * (a + 1)  #give the just for the branch-IU connection
rightchild = [-1] * (a + 1) #just for the branch-IU connection

i = a
for i in range(a, 0, -1):
	if elemtyp[i] == 'Branch':
		size[i] = leftsize[i] + rightsize[i]
	if leftchild[parentid[i]] == -1:
		leftchild[parentid[i]] = i
		leftsize[parentid[i]] = size[i]	
	else:
		rightchild[parentid[i]] = i
		rightsize[parentid[i]] = size[i]

###Branch size calculating###
#This code calculate the amount of additional refirigent gas, and the length of the required copper pipe
#For theese feature, need to get the pipe length, and the set of the model (when two or more block are need)
#After it this code can calculate the 0th branch sizes (which connect the outdoor units if it necessary)

###var
pipdia = [[]] * (a + 1) #give diameter before of the equipment
pipdia_len = [0, 0, 0, 0, 0, 0, 0, 0, 0] #6, 10 12, 16, 20, 22, 28, 35, 42 #To summarize the total pipe length group by diameter
knowndia = { #known diameters to create pipdia_len vector
		6: 0,
		0: 0, #delete the zero value
		10: 1,
		12: 2,
		16: 3,
		20: 4,
		22: 5,
		28: 6,
		35: 7,
		42: 8
		}
num_join = 1 #Number of joints (int, but bool may enoug later?)

for i in range (0, a + 1):
	if elemtyp[i] == 'Outdoor':
		pipdia[i] = [0, 0]
		pass #later
	elif elemtyp[i] == 'Indoor':
		pipdia[i] = iu_branch(size[i], systyp)
	else:
		if num_join == 1: #Not consecvent, other places the ID = 0 means OU, ID = 1 => branch
			pipdia[i] = ou_branch(size[0], systyp)
		else:
			pipdia[i] = branch_branch(size[i], systyp)
		num_join += 1

#In case of P250-300, EP250-300 if the max equvivalent distance between the outdoor unit and the indoor unit is equal or more then 90/40 m, the outdoor unit liquid pipe has to reselect
if (size[0] == 300 or size[0] == 250) and (systyp == 'P' or systyp == 'EP'): 
	sumlen = c_piplen
	if size[0] == 300:
		crit = 40
	else:
		crit = 90
	#Mert bugos az NDT XML exportja, és az 1. joint távolsága néha fals (lenA-val redundánsan ugyan az kéne, hogy legyen)
	if rightchild[1] != -1:
		sumlen[rightchild[1]] += lenA
	if leftchild[1] != -1:
		sumlen[leftchild[1]] += lenA
	for i in range(2, a + 1):
		if rightchild[i] != -1:
			sumlen[rightchild[i]] += c_piplen[i]
		if leftchild[i] != -1:
			sumlen[leftchild[i]] += c_piplen[i]
		if sumlen[i] >= crit:
			if size[0] == 300:
				pipdia[1][0] = 12
			else:
				pipdia[1][0] = 12
			break

#correction of the pipe diameter (if the upper one is smaller)
for i in range(1, a + 1):
	for j in range(0, 2):
		if pipdia[leftchild[i]][j] > pipdia[i][j] and elemtyp[leftchild[i]] != 'Indoor':
			pipdia[leftchild[i]][j] = pipdia[i][j]
		elif pipdia[rightchild[i]][j] > pipdia[i][j] and elemtyp[rightchild[i]] != 'Indoor':
			pipdia[rightchild[i]][j] = pipdia[i][j]

#pipelength
for i in range(0, a + 1):
	pipdia_len[knowndia[pipdia[i][0]]] += piplen[i]
	pipdia_len[knowndia[pipdia[i][1]]] += piplen[i]

###var
b = 0 #Temp variable, joint ID (0::num_join-1)
joint = [[]] * (num_join*2) #joints
joint_s = list()
joint_num = list()

#Get the joints
joint[b] = [0,0,0]
joint[b+1] = [0,0,0]
b += 2
if size[0] >= 400:
	print('0th joint may need')#->output file
for i in range (0, a + 1):
	if elemtyp[i] == 'Branch':
		for j in range (0, 2):
			joint[b+j] = sorted([pipdia[i][j], pipdia[leftchild[i]][j], pipdia[rightchild[i]][j]], reverse=True)
		b += 2

#summarize joints
joint_s.append(joint[0])
joint_num.append(1)
for i in range (1, len(joint)):
	exist = False
	for j in range(0, len(joint_s)):
		if joint_s[j] == joint[i]:
			joint_num[j] += 1
			exist = True
			break
	if exist == True:
		continue
	else:
		joint_s.append(joint[i])
		joint_num.append(1)
	
print()
print('***End***')
print()

print("joints: " + str(joint_s))
print('number of joints: ' + str(joint_num))
print('pipe length 6, 10 12, 16, 20, 22, 28, 35, 42: ' + str(pipdia_len))

print('****Test section starts here******')

'''
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
print('A' + str(i))
ws.cell(row=4, column=2, value=10)
ws['A2'] = 2
print(ws['B2'])
wb.save('NDT_eport.xlsx')

from openpyxl import load_workbook
wb = load_workbook(filename = 'empty_book.xlsx')
sheet_ranges = wb['Sheet']
print(sheet_ranges['D18'].value)'''

print('****End******')
#bent -> pipe length in the export?
#outdoor unit joint calculate
#calculate the special cases
#create export file
#Summarize more export files
#Check from the NDT .xlsx export file
#a (new)index error correction
#-1 return value -> error message; + do not cause error
#check the 1st bend xml bug