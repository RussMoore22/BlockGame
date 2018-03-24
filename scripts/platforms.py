import pygame as pyg
Platforms = []

with open('map.txt') as file:
    data = file.read()
    data = data.strip()
    data = data.replace('\n', '')
    dataList = data.split("'")
    usableData = dataList[-1]
    usableData= usableData.split("-")


for list in usableData:
    tempList = []
    tempList2 = list.split(",")
    for num in tempList2:
        try:
            tempList.append(int(num))
        except:
            break
    Platforms.append(tempList)
i = 0
for list in Platforms:
    if len(list)<6:
        del Platforms[i]
    i += 1


print(Platforms)


