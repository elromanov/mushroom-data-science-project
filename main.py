from typing import NewType
from numpy import double
import pandas as pd
import sys

# Test data: x,f,g,f,c,f,c,n,n,e,b,s,s,w,w,p,w,o,p,k,v,d,?

knn = 1

def csvParser(pathToCSV):
    df = pd.read_csv(pathToCSV)
    return df

def showStats(dataSet, fileName, dataTypeName, collumnIndex):
    print("Loaded file:", fileName, "containing", dataTypeName)
    print(len(dataSet), dataTypeName)
    print(len(dataSet[0]), "attributes")
    nbEdible = 0
    nbPoisonous = 0
    for item in dataSet:
        if item[22] == "e":
            nbEdible += 1
        else:
            nbPoisonous += 1
    print("prediction: edible(e:",nbEdible,"p:",nbPoisonous,")\n") 

def chooseKNN():
    global knn
    knn = int(input("Please choose a value for K\n--> "))
    print("K's value:", knn, "\n")

# EUCLIDIENNE
# SI '?' -> Distance = 1
def calculDistance(i, dataset, newItem, columnToPredict):
    itemToCompare = dataset[i]
    distance = 0
    for n in range(len(itemToCompare) - 1):
        if '?' not in newItem[n]:
            if(n != columnToPredict):
                if(itemToCompare[n] != newItem[n]):
                    distance += 1
        else:
            distance += 1
    distance = distance ** 0.5
    return (i, distance)    

def findKNN(dataset, newItem, dataNames, columnToPredict):
    closestNeighbours = []
    toutesLesDistances = []
    for n in range(len(dataset)):
        nDistance = calculDistance(n, dataset, newItem, columnToPredict)
        toutesLesDistances.append(nDistance[1])
        if(len(closestNeighbours) < knn):
            closestNeighbours.append(nDistance)
            #print(closestNeighbours)
            closestNeighbours.sort(key=lambda y: y[1], reverse=True)
            #print(closestNeighbours)
        else:
            # print(nDistance[1])
            if(nDistance[1] <= closestNeighbours[0][1]):
                closestNeighbours.pop(0)
                closestNeighbours.append(nDistance)
                closestNeighbours.sort(key=lambda y: y[1], reverse=True)
    options = [["a",0,0],["b",0,0]]
    i = 0
    for n in closestNeighbours:
        if i == 0:
            options[0][1] += 1
            options[0][0] = dataset[n[0]][columnToPredict]
            options[0][2] += (1/float(n[1]))
        elif i == 1:
            if options[0][0] != dataset[n[0]][columnToPredict]:
                options[1][0] = dataset[n[0]][columnToPredict]
                options[1][1] += 1
                options[1][2] += (1/float(n[1]))
            else:
                options[0][1] += 1
                options[0][2] += (1/float(n[1]))
        else:
            if options[0][0] == dataset[n[0]][columnToPredict]:
                options[0][1] += 1
                options[0][2] += (1/float(n[1]))
            else:
                options[1][1] += 1
                options[1][2] += (1/float(n[1]))
        i += 1
        # weightedTotalOpt1 += (1/float(n[1]))
        print("Neighbour N°" + str(n[0]) + ". Distance = " + str(n[1]) + "; " + dataNames[columnToPredict] + ": "+ dataset[n[0]][columnToPredict])
    print("\n")
    if options[0][1] > 0:
        print("Total " + str(options[0][0]) + ": " + str(options[0][1]) + "/" + str(options[0][1]+options[1][1]))
        print("Weighted total ("+ options[0][0] +"): " + str(options[0][2]))
    if options[1][1] > 0:
        print("Total " + str(options[1][0]) + ": " + str(options[1][1]) + "/" + str(options[0][1]+options[1][1]))
        print("Weighted total ("+ options[0][0] +"): " + str(options[1][2]))
    print("\n")
    # print("Weighted total: " + str(weightedTotalOpt1))
    # pondéré inversement proportionnel aux voisins proches (pour chaque classe)



def menu(dataNames, dataSet, args):
    userInput = input("What do you want to do (enter option's number)?\n1 - Choose K's value\n2 - Compare items\n3 - Show stats\nE - Exit\n--> ")
    if userInput == "1":
        chooseKNN()
    elif userInput == "2":
        # itemToCompare = int(input('Please enter the index of the item you want to compare\n--> '))
        thingsToCompareString = input('Please enter the item you want to compare (separate the values with comas as in the loaded file, leave an interogation mark on the collumns you don\'t have informations)\n--> ')
        thingsToCompareList = thingsToCompareString.split(',')
        # print(thingsToCompareList)
        # calculDistance(itemToCompare, dataSet, thingsToCompareList)
        findKNN(dataSet, thingsToCompareList, dataNames, args[2])
    elif userInput == "3":
        showStats(dataSet, args[0], args[1], args[2])
    elif userInput == 'E' or userInput == "e":
        exit()
    else:
        print("Invalid input !\n")
    menu(dataNames, dataSet, args)

def main():
    #userInput = input("Please enter: CSV path, item type & column to predict index (please separat args with a space)\n-> ")
    args = []
    for element in sys.argv:
        args.append(element)
    args.pop(0)
    print(args)

    loadedData = csvParser(args[0])
    dataNames = loadedData.head()
    dataSet = csvParser(args[0]).values
    headers = list(dataNames.columns.values.tolist())
    args[2] = int(args[2])
    menu(headers, dataSet, args)

main()