def flatten_list(x):
	list1=[]
	for i in x:
		if type(i) is list:
			list1.extend(flatten_list(i))
		else:
			list1.append(i)
	return list1
		
x = [1, [2, [3, 4], 5], [6, 7]]		
m = flatten_list(x)
print(m)