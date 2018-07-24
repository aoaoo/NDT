'''infil = open('ndtv.xml')
st = (infil.read())
print(st)
print(type(st))'''

'''#function
def pipesel (x):
  return 5 * x

print(pipesel(3))
'''

#Check extra infos (modifications because of high distances)
#The pipe diameter between the outdoor unit and the first branch
def ou (si, ty): #size and type of the outdoor unit
	if ty == 'EP':
		EP_dict = {
		200: (10, 22),
		250: (10, 22),
		300: (10, 28),
		350: (12, 28),
		400: (12, 28),
		450: (16, 28),
		500: (16, 28),
		550: (16, 28),
		600: (16, 28),
		650: (16, 28),
		700: (20, 35),
		750: (20, 35),
		800: (20, 35),
		850: (20, 42),
		900: (20, 42),
		950: (20, 42),
		1000: (20, 42),
		1050: (20, 42),
		1100: (20, 42),
		1150: (20, 42),
		1200: (20, 42),
		1250: (20, 42),
		1300: (20, 42),
		1350: (20, 42)		
		}
		return EP_dict[si]
	elif ty == 'HP':
		HP_dict = {
		200: (12, 20),
		250: (12, 22),
		400: (16, 28),
		450: (16, 28),
		500: (16, 28)		
		}
		return HP_dict[si]	
	elif ty == 'P':
		P_dict = {
		200: (10, 22),
		250: (10, 22),
		300: (10, 22),
		350: (12, 28),
		400: (12, 28),
		450: (16, 28),
		500: (16, 28),
		550: (16, 28),
		600: (16, 28),
		650: (16, 28),
		700: (20, 35),
		750: (20, 35),
		800: (20, 35),
		850: (20, 42),
		900: (20, 42),
		950: (20, 42),
		1000: (20, 42),
		1050: (20, 42),
		1100: (20, 42),
		1150: (20, 42),
		1200: (20, 42),
		1250: (20, 42),
		1300: (20, 42),
		1350: (20, 42)		
		}
		return P_dict[si]
	else:
		return (-1, -1)

import xml.etree.ElementTree as ET
tree = ET.parse('ndtv.xml')
root = tree.getroot()

#var
elemtyp = list() #Outdoor / Indoorunit, Branch
size = list() #The capacity of the units
joker1 = list() #Mitsu joint type; P, EP, HP
parentid = list()
a = 0 #Where a = ID (a = NDT_ID - 1)

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
		print('The size of the found outdoor unit is: ' + str(size[a]))
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
		print('The size of the indoor unit is: ' + str(size[a]))
	elif s.find('Branch') > 0:
		elemtyp.append('Branch')
		size.append(-1)
		#Catch joker1
		pos = s.find('CMY-Y')
		joker1.append(s[pos:pos+13])
		print('The type of the joint is: ' + joker1[a])
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

#Building the tree
#var
leftsize = [0] * (a+1)
rightsize = [0] * (a+1)

i = a
for i in range(a, -1, -1):
	if elemtyp[i] == 'Branch':
		size[i] = leftsize[i] + rightsize[i]
	if leftsize[parentid[i]] == 0:
		leftsize[parentid[i]] = size[i]
	else:
		rightsize[parentid[i]] = size[i]

#Branch size calculating
#var
bsize = list()


'''print('****Test section start here******')
int('200')
print(len(size))
print('****End******')
'''


print('****End of code****')