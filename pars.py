###Comments###
#Python v3.5.0
#openpyxl v2.5.3
print('***Ez a kód a PUHY-HP, P és EP szériák esetében számolja össze a beltéri egységekhez szükséges jointokat (azaz a kültéri egységek összekötéséhez szükséges darabokat ehhez hozzá kell venni, ha van ilyen.***')
print('***Jelenleg beta verzióban működik, az eredmények ellenőrzése szükséges.***')
print('***A jelenlegi verzió nem számolja a szükséges szűkítők és az azokhoz szükséges extra csőmennyiségek mértékét. Ezzel összhangban nem a Mitsubishi szabványos elágazásait adja meg.***')
print('***A végleges verzió esetén az eredmények ellenőrzése kimerülhet a Design Tool-ból exportálható és az innen számolt csőmennyiségek összehasonlításával.***')
print('***Az ellenőrzésnél figyelni kell, hogy a kültériek összecsövezésére szolgáló csőmennyiség nincs benne ennek a programnak a kimenetében.***')
print('***Ezek mellett a kültériek összekötésére szolgáló csövekből a NDT jellemzően az egyik géptől érkező "gáz" csövet nem számolja.***')
print('***Amennyiben a G11-nél vagy a Mitsubishi New Design Tool v1.90 frissebb megjelenik, úgy ellenőrizni kell a kódba égetett adatokat.***')
print('***A program a kültéri egységek összekötéséhez szükséges csőmennyiséget és jointo(ka)t nem számítja, ezt kézzel hozzá kell adni!***')
print('***Használat ... in progress***')
print('***Forráskód: https://github.com/aoaoo/NDT***')
print()
print("***Begin***")
print()

#import modules
import string #string
import re #regexp
import sys #system exit
import time #wait

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
#The pipe diameter between the indoor unit and the branch, in case of VRF indoor unit (use Miu_branch function in case of PAC-LV11)
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

#The pipe diameter between the indoor unit and the branch, in case of M series indoor unit (with PAC-LV11): MSZ-SF, EF, FH and MFZ-KJ
def Miu_branch (si): #In this case system type is not important
	M_dict = {
	15: [6, 10],
	18: [6, 10],
	20: [6, 10],
	22: [6, 10],
	25: [6, 10],
	30: [6, 10],
	40: [6, 10],
	45: [6, 12], #unit 50, because of the size correction
	60: [6, 16],
	71: [10, 16],
	80: [10, 16]
	}
	return M_dict[si]

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

#Find if M serie (MSZ-EF/SF/FH or MFZ-KJ) (PAC-LV11 connection, to use smaller liquid pipe size)
def get_M_series (s): #String, the type of the indoor unit; need 'import re'
		if re.search(r'[M][SF][Z][-][ESFK][FHJ]', s) == None:
			return('VRF')
		else:
			return('M')

#M size correction (Because the total capacity in case of M series IU is eq or less than the number in the type designation)
def M_size_corr (size): #Size is an integer; No information for EF-18
	if size == 20 or size == 35 or size == 50:
		return size - 5
	elif size == 22 or size == 42:
		return size - 2
	else:
		return size
	
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

#Eqvivalent distance from the first joint; Leftchild, rightchild, pipe length
def dist_1st_joint (lchild, rchild, eqlen): 
	a = len(lchild) - 1
	eqdis = [0] * (a + 1)
	for i in range (2, a + 1):
		eqdis[i] += eqlen[i]
		if lchild[i] != -1:
			eqdis[lchild[i]] += eqdis[i]
		if rchild[i] != -1:
			eqdis[rchild[i]] += eqdis[i]
	return eqdis

###Import data###
print('Írd be az importálandó .xml fájl nevét, ami ebben a mappában van: ')
while True:
	try:
		infil = str(input())
		if len(infil) > 4:
			if infil[len(infil)-4:len(infil)+1] != '.xml':
				infil = infil + '.xml'
		else:
			infil = infil + '.xml'

		import xml.etree.ElementTree as ET
		tree = ET.parse(infil)
		root = tree.getroot()
		break
	except FileNotFoundError:
		print('Írd be helyesen az importálandó .xml fájl nevét, ami ebben a mappában van: ')
	
###var
elemtyp = list() #Outdoor / Indoor, Branch
size = list() #The capacity of the units
joker1 = list() #Random joker
parentid = list()
piplen = list() #Pipe length before the unit #Expect outdoor unit
c_piplen = list() #The equivalent pipe length
numbend	= list() #Number of bent before the unit #Expect the outdoort unit
height = list() #Height of the devices
a = 0 #Where a = ID (a = NDT_ID - 1)
systyp = '' #system type: P, HP, EP
iutyp = list() #VRF or M 
dbou = 1 #Number of the outdoor unit
minh = 0 #Minimum height by the IU-s
maxh = 0 #Maximum height by the IU-s
#lenA lenB lenC nenD lenE bendA bendB bendC bendD bendE #Tho outdoor units piping length

for unit in root.iter('Unit'):
	elemtyp.append(unit.get('Model'))
	if elemtyp[a] == 'Outdoor':
		size.append(get_num(unit.get('ModelName'),'pint'))
		parentid.append(-1)
		piplen.append(0)
		numbend.append(0)
		systyp = (re.search(r'[-][E,H]?[P]', unit.get('ModelName')).group(0)).replace('-', '')
		lenA = get_num(unit.get('PipeLengthA'),'float') #Because getnum change the ',' to '.' too
		bendA = get_num(unit.get('BendA'), 'pint')
		piplen.append(lenA)
		numbend.append(bendA)
		iutyp.append('VRF')
		try:
			lenB = get_num(unit.get('PipeLengthB'),'float'); lenB
			bendB = get_num(unit.get('BendB'), 'pint')
			dbou += 1
			lenC = get_num(unit.get('PipeLengthC'),'float')
			bendC = get_num(unit.get('BendC'), 'pint')
			piplen[1] = lenC
			numbend[1] = bendC
			lenD = get_num(unit.get('PipeLengthD'),'float')
			bendD = get_num(unit.get('BendD'), 'pint')
			dbou += 1
			lenE = get_num(unit.get('PipeLengthE'),'float')
			bendE = get_num(unit.get('BendE'), 'pint')
			piplen[1] =  lenE
			numbend[1] = bendE
		except AttributeError:
			pass
		height.append(get_num(unit.get('Height'), 'float'))
		if dbou == 2:
			height[0] = max(height[0], get_num(unit.get('Height2'), 'float'))
		elif dbou == 3:
			height[0] = max(height[0], get_num(unit.get('Height2'), 'float'), get_num(unit.get('Height3'), 'float'))
	elif elemtyp[a] == 'Indoor':
		iutyp.append(get_M_series(unit.get('ModelName')))
		if iutyp[a] == 'M': #Size correction for PAC-LV and M series
			size.append(M_size_corr(get_num(unit.get('ModelName'),'pint')))
		else:
			size.append(get_num(unit.get('ModelName'),'pint'))
		parentid.append(int(unit.get('ParentUnitID')) - 1)
		piplen.append(get_num(unit.get('PipeLength'),'float'))
		numbend.append(get_num(unit.get('Bend'),'pint'))
		height.append(get_num(unit.get('Height'), 'float'))
		if minh == 0: #To get an existing height value for initial condition to the min and max searching method
			minh = get_num(unit.get('Height'), 'float')
			maxh = get_num(unit.get('Height'), 'float')
	elif elemtyp[a] == 'Branch': #Jump the frist branch pilength, and bend values, use lenA;;lenE and bendA;;bendE
		size.append(0)
		parentid.append(int(unit.get('ParentUnitID')) - 1)
		iutyp.append('VRF')
		if a != 1:
			piplen.append(get_num(unit.get('PipeLength'),'float'))
			numbend.append(get_num(unit.get('Bend'),'pint'))
		height.append(get_num(unit.get('Height'), 'float'))
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
incdia = [False] * (a + 1) #Increased the liquid pipe diameter, because height limitation or exceeding the 40m
bunit = 0 #The height of the base unit
#act_paid  actual parendtID (by function height limit test)
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

knowndia_inv = { #known diameters to create increase pipe diameter
		0: 6,
		1: 10,
		2: 12,
		3: 16,
		4: 20,
		5: 22,
		6: 28,
		7: 35,
		8: 42
		}

num_join = 1 #Number of joints (int, but bool may enoug later?)

for i in range (0, a + 1):
	if elemtyp[i] == 'Outdoor':
		pipdia[i] = [0, 0]
		pass #later
	elif elemtyp[i] == 'Indoor':
		if iutyp[i] == 'M': #M serie Pipe size
			pipdia[i] = Miu_branch(size[i])
		else: #VRF pipe size
			pipdia[i] = iu_branch(size[i], systyp)
	else:
		if num_join == 1: #Not consecvent, other places the ID = 0 means OU, ID = 1 => branch
			pipdia[i] = ou_branch(size[0], systyp)
		else:
			pipdia[i] = branch_branch(size[i], systyp)
		num_join += 1

#Get the distance for every element from the first joint 
eqdist = dist_1st_joint(leftchild, rightchild, c_piplen)
#In case of P250-300, EP250-300 if the max equvivalent distance between the outdoor unit and the indoor unit is equal or more then 90/40 m, the outdoor unit liquid pipe has to reselect
if  size[0] == 250 and (systyp == 'P' or systyp == 'EP'):
	for i in eqdist:
		if i + lenA + bendA * bend_len_corr(size[0], systyp) >= 90: #Mert bugos az NDT XML exportja, és az 1. joint távolsága néha fals (lenA-val redundánsan ugyan az kéne, hogy legyen)
			pipdia[1][0] = 12
			break
if  size[0] == 300 and (systyp == 'P' or systyp == 'EP'):
	for i in eqdist:
		if i + lenA + bendA * bend_len_corr(size[0], systyp) >= 40:
			pipdia[1][0] = 12
			break

#correction of the pipe diameter (if the upper one is smaller)
for i in range(1, a + 1):
	for j in range(0, 2):
		if pipdia[leftchild[i]][j] > pipdia[i][j] and elemtyp[leftchild[i]] != 'Indoor':
			pipdia[leftchild[i]][j] = pipdia[i][j]
		elif pipdia[rightchild[i]][j] > pipdia[i][j] and elemtyp[rightchild[i]] != 'Indoor':
			pipdia[rightchild[i]][j] = pipdia[i][j]

#Correction the liquid pipe diameter, because the equvivalent distance from the first joint exceed 40m
for i in range (2, a + 1):
	if eqdist[i] > 40:
		pipdia[i][0] = knowndia_inv[knowndia[pipdia[i][0]] + 1]
		incdia[i] = True

#Correction the liquid pipe diameter, because the height difference from the mase (IU) unit is more than 15 m (and no correction was because the 40 m)
#First find the min and max value of the IU height
for i in range (2, a + 1):
	if elemtyp[i] == 'Indoor':
		if height[i] < minh:
			minh = height[i]
		elif height[i] > maxh:
			maxh = height[i]
#Choose the base IU height
if minh >= height[0]:
	bunit = minh
else:
	bunit = maxh

#Update the liquid pipe diameters
for i in range (2, a + 1):
	if elemtyp[i] == 'Indoor' and abs(height[i] - bunit) > 15 and incdia[i] == False:
		pipdia[i][0] = knowndia_inv[knowndia[pipdia[i][0]] + 1]
		incdia[i] = True
		act_paid = parentid[i]
		while abs(height[act_paid] - bunit) > 15 and act_paid != 0:
			if incdia[act_paid] == False:
				pipdia[act_paid][0] = knowndia_inv[knowndia[pipdia[act_paid][0]] + 1]
				incdia[act_paid] = True
			act_paid = parentid[act_paid]

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

print(size)
print("joints: " + str(joint_s))
print('number of joints: ' + str(joint_num))
print('pipe length 6, 10 12, 16, 20, 22, 28, 35, 42: ' + str(pipdia_len))


from openpyxl import Workbook
from openpyxl import load_workbook
infil = infil[0:len(infil)-4] + '_joint.xlsx' #Give a similar name to the output file
try:
	wb_load = load_workbook(filename = infil)
	print('\n***\n A futás sikertelen.\n')
	print(infil + ' néven létezik már fájl a mappában, ennek felülírására a programnak nincs jogosultsága. Kérlek nevezd vagy helyezd át a ' + infil +' nevű fájlt (vagy töröld), majd utána futtasd újra a kódot!')
	time.sleep(10)
	sys.exit()
except FileNotFoundError:
	print('Hello')
	pass
	
wb = Workbook()
ws = wb.active
ws['A1'] = 1
wb.save(infil)

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


print('****Test section starts here******')
print('****End******')
#Find/ask the input xml file
#bent -> pipe length in the export?
#outdoor unit joint calculate #Bug: In case of two (or more?) OU one of them pipe doesent calculate properly (just the liquid pipe summarize in the excell export, but the gas pipe is not summarized)
#calculate the special cases
#create export file
#Summarize more export files
#Check from the NDT .xlsx export file
#-1 return value -> error message; + do not cause error
#piplenA, piplenB.... create and calculate
#reducer might have to use in case of PAC-LV (because of the PAC has D10 and D12 diameters)