file = open('something.txt', 'a+')
out = file.write("kubernetes")
file.seek(0)
y = file.read()
print(y)