
dic = {}
with open('aa.txt', 'r') as the_file:
    for line in the_file:
        print(line.split(' ')[1])
        x = int(line.split(' ')[1])
        if x-1520660043 in dic:
            dic[x-1520660043] = dic[x-1520660043] + 1
        else:
            dic[x-1520660043] = 1

with open('aa.csv', 'w') as the_file:
    for i in range(0,1520660251-1520660043+1):
        if i in dic:
            the_file.write(str(i) + "," + str(dic[i]) + "\n")
        else:
            the_file.write(str(i) + ",0" + "\n")