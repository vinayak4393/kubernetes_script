def rotate_matrix(m):
	x = len(m)
	for i in range(x):
		for j in range(i+1,x):
			m[i][j], m[j][i] = m[j][i], m[i][j]
	
	for i in range(x):
		m[i].reverse()
		
	return m

m = [
	[1,2,3],
	[4,5,6],
	[7,8,9]
]	

rm_90 = rotate_matrix(m)
for k in rm_90:
	print(k)