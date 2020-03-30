"""
检查文件中是否出现重复的5位数
"""
import re

filename = "tset.txt"

with open(filename,'r')as f:
	s = f.read()
	nums = re.findall('[0-9]{5}',s)
	for i in range(0,len(nums)):
		nums[i] = int(nums[i])
	print("checking")
	rlt = 0
	for i in range(0,len(nums)):
		for j in range(i+1,len(nums)):
			if nums[i] == nums[j]:
				print("have conflict num "+str(nums[i]))	
				rlt += 1	
	if rlt == 0:
		print("no conflict num found")		
	print("job done")
