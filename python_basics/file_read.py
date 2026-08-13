input_file = input("Provide file path to read: ")

f = open(input_file,"r")
for line in f.readlines():
    print(line.strip())

f.close()