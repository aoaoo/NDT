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
elemtyp = list()
size = list()

print('****Test section start here******')
int('200')
print(len(size))
print('****End******')


a = 0 #Where a = ID
while True:
	try:
		root[0][2][a]
	except IndexError:
		a -= 1
		break
	s = str(root[0][2][a].attrib)
	if s.find('Outdoor') > 0:
		elemtyp.append('Outdoor')
		pos = s.find('PUHY')
			for i in range(6, 7)
				try:
					int(s[pos+i:pos+i+2])
				except ValueError:
				if len(size) = a: #Empty and P200 or P1000
					size.append(int(s[pos+i:pos+i+2])
				elif size[a] < int(s[pos+i:pos+i+2] and len(size) > a: #Delete after debugging
					Print('Error')
				try:
					int(s[pos+i:pos+i+3])
				except ValueError:
				if size[a] < int(s[pos+i:pos+i+3] and len(size) > a: #Second statement is just for check the code
					size.append(int(s[pos+i:pos+i+3])
		print(str(pos))#
		print(s[pos+6:pos+11])#
		print(s[pos+6:pos+11])#
	elif s.find('Indoor') > 0:
		elemtyp.append('Indoor')
	elif s.find('Branch') > 0:
		elemtyp.append('Branch')
	else:
		print(a)
	a += 1

print(elemtyp) 
print(a)
#print(root[0][2][a].attrib)