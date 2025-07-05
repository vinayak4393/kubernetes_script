def flatten_list(x):
	list1=[]
	for num in x:
		if isinstance (num,list):
			list1.extend(flatten_list(num))
		else:
			list1.append(num)
	return list1
		
x = [1, [2, [3, 4], 5], [6, 7]]		
m = flatten_list(x)
print(m)