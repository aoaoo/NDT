"""tree = ET.parse('ndtv1.0.xml')
root = tree.getroot()"""
#tree = ET.parse('ndtv.xml')
'''infil = open('ndtv.xml')
st = (infil.read())
print(st)
print(type(st))'''
'''import xml.etree.ElementTree as ET
tree = ET.parse('ndtv.xml')
root = tree.getroot()
print(type(root))
print(root.attrib)'''
'''for child in root
	print (child.tag)
	print(child.attrib)'''


import xml.etree.ElementTree as ET
tree = ET.parse('ndtv.xml')
root = tree.getroot()

#var
elemtyp = list() #Outdoor / Indoorunit, Branch
size = list() #The capacity of the units
joker1 = list() #Mitsu joint type
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
		joker1.append('')
		#pareintID
		parentid.append(-1)
		#Catch the outdoor unit size
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
		#Catch the indoor unit size
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


'''print('****Test section start here******')
int('200')
print(len(size))
print('****End******')
'''


print('****End of code****')