###Comments###

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
		450: [16, 28],
		500: [16, 28]		
		}
		return HP_dict[si]	
	elif ty == 'P':
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
	else:
		return [-1, -1]

#Check extra infos (modifications because of high distances)
#The pipe diameter between the indoor unit and the branch
def iu_branch (si, ty): #size of the connected indoor unit, and the type of the system (based on the data, now this second variable negigible)
	if ty == 'EP':
		EP_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
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
		250: [10, 22],
		}
		return EP_dict[si]
	elif ty == 'HP':
		HP_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
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
		250: [10, 22],
		}
		return HP_dict[si]
	elif ty == 'P':
		P_dict = {
		15: [6, 12],
		18: [6, 12],
		20: [6, 12],
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
		250: [10, 22],
		}
		return P_dict[si]
	else:
		return [-1, -1]
		
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
	elif ty == 'P':
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
	else:
		return [-1, -1]

###Import data###		
import xml.etree.ElementTree as ET
tree = ET.parse('ndtv.xml')
root = tree.getroot()

###var
elemtyp = list() #Outdoor / Indoorunit, Branch
size = list() #The capacity of the units
joker1 = list() #Mitsubitsi system type; P, EP, HP
parentid = list()
a = 0 #Where a = ID (a = NDT_ID - 1)

###Valus from string###

while True:
	try:
		root[0][2][a]
	except IndexError:
		a -= 1
		break
	s = str(root[0][2][a].attrib)
	if s.find('Outdoor') > 0:
		elemtyp.append('Outdoor')
		#pareintID
		parentid.append(-1)
		#HP, P, EP -> joker1
		#joker1.append('')
		if s.find('PUHY') > 0:
			pos = s.find('PUHY')
		else:
			print("This system not allowed") #Crete a better sys mess
		if s[pos+5:pos+7] == 'EP':
			joker1.append('EP')
		elif s[pos+5:pos+7] == 'HP':
			joker1.append('HP')
		else:
			joker1.append('P')
		#outdoor unit size -> size
		pos = s.find('PUHY')
		for i in range(6, 8, 1):
			if len(size) > a:
				break
			try:
				int(s[pos+i:pos+i+3])
				size.append(int(s[pos+i:pos+i+3]))
			except ValueError:
				continue
			try:
				int(s[pos+i:pos+i+4])
				size[a] = (int(s[pos+i:pos+i+4]))
			except ValueError:
				continue
		#print('The size of the found outdoor unit is: ' + str(size[a]))
	elif s.find('Indoor') > 0:
		elemtyp.append('Indoor')
		joker1.append('')
		#pareintID
		pos = s.find('ParentUnitID')
		try:
			int(s[pos+16:pos+18])
			parentid.append(int(s[pos+16:pos+18])-1)
		except ValueError:
			parentid.append(int((s[pos+16]))-1)
		#indoor unit size -> size
		pos = s.find('ModelName')
		if s.find('PWFY') > 0:
			print('Error, bad construction')#Create correct err mess
		for i in range(18, 21):
			if len(size) > a:
				break
			try:
				int(s[pos+i:pos+i+2])
				size.append(int(s[pos+i:pos+i+2]))
			except ValueError:
				pass
			try:
				int(s[pos+i:pos+i+3])
				if len(size) > a:
					size[a] = int(s[pos+i:pos+i+3])
				else:
					size.append(int(s[pos+i:pos+i+3]))
			except ValueError:
				pass
		#print('The size of the indoor unit is: ' + str(size[a]))
	elif s.find('Branch') > 0:
		elemtyp.append('Branch')
		size.append(-1)
		#Catch joker1
		pos = s.find('CMY-Y')
		joker1.append(s[pos:pos+13])
		#print('The type of the joint is: ' + joker1[a])
		#pareintID
		pos = s.find('ParentUnitID')
		try:
			int(s[pos+16:pos+18])
			parentid.append(int(s[pos+16:pos+18])-1)
		except ValueError:
			parentid.append(int((s[pos+16]))-1)
	else:
		print(a)
	a += 1

###Building the tree###
###var
leftsize = [0] * (a + 1) #give the capacity connected on the 1st side 
rightsize = [0] * (a + 1) #give the capacity connected on the 2nd side
leftchild = [-1] * (a + 1)  #give the just for the branch-IU connection
rightchild = [-1] * (a + 1) #just for the branch-IU connection

i = a
for i in range(a, -1, -1):
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
num_join = 1 #Number of joints (int, but bool may enoug later?)


for i in range (0, a + 1):
	if elemtyp[i] == 'Outdoor':
		pipdia[i] = [0, 0]
		pass #later
	elif elemtyp[i] == 'Indoor':
		pipdia[i] = iu_branch(size[i], joker1[0])
	else:
		if num_join == 1: #Not consecvent, other places the ID = 0 means OU, ID = 1 => branch
			pipdia[i] = ou_branch(size[0], joker1[0])
		else:
			pipdia[i] = branch_branch(size[i], joker1[0])
		num_join += 1

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
print(str(len(joint_s)+1))
print(joint_s)
print(j)
for i in range (1, len(joint)):
	exist = False
	for j in range(0, len(joint_s)):
		print(j)
		print("current i is: " + str(i))
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
'''print('****Test section start here******')

print('****End******')
'''

print(joint)
print(joint_s)
print(joint_num)