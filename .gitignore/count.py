def freq(text):
    char_count = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1
    return char_count    

text = "kubernetes"
n = freq(text)
print(f"frequency: {n}")