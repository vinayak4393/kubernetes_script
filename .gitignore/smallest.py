list1 = [1,45,86,2,5,56,58]
smallest = list1[0]
for num in list1:
    if num < smallest:
        smallest = num
print (f"The smallest number is {smallest}")        