'''
Generate a list of rand numbers
'''
from random import randint

s = input("Enter List length ")
length = int(s)
s = input("Enter val Upper ")
upper = int(s)
s = input("enter val Lower ")
lower = int(s)
ll = []
for i in range(0,length):
	ll.append(randint(lower,upper))
content = '{\n'
for l in range(0,len(ll)):
	content += str(ll[l])+', '
	if l % 10 == 9:
		content += '\n'
content += '\n}'
print(content)
