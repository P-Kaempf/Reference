# This is a Python script.
import os
import csv
import traceback
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.polynomial.chebyshev import chebfit
import pandas
import pandas as pd
from operator import add
from datetime import date
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
import classes
import data
import plot
import ui

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon   = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

#
#******************************************************************************
#

def readFolders(fullname):
#
#  Reads a list of the files and subfolders contained in a folder
#
    listOfFolders = []
    listOfNames = os.listdir(fullname)
    for name in listOfNames:
        new_fullname = os.path.join(fullname, name)
        if os.path.isdir(new_fullname):
            listOfFolders.append(new_fullname)
            listOfFolders.extend(readFolders(new_fullname))   # recursive call to capture all branches below
    return listOfFolders

#
#******************************************************************************
#

def td_fill(td, listOfFolders, lastFolder):
#
#  Fills the Treedata list with file or folder names.
#
    for fullname in listOfFolders:
        name = os.path.basename(fullname)
        if name[0] == '.':
            continue

        ui.progressUpdate("-stdout-", "added item "+name)
        listOfNames = os.listdir(fullname)
        n = len(listOfNames)
        td.insert(parent = '',
                  key = fullname,
                  text = name,
                  values = [str(n)+" items"],
                  icon=folder_icon)
#
#  Add the files inside the folder:
#
        for filename in listOfNames:
            if filename[0] == '.':
                continue
            fullFileName = os.path.join(fullname, filename)
            size = os.path.getsize(fullFileName)
            try:
                td.insert(parent=fullname,
                          key=fullFileName,
                          text=filename,
                          values=[str(round(size / 1024.0, 2)) + " KB"],
                          icon=file_icon)
            except Exception as e:
                tb = traceback.format_exc()
                print(f'Something went wrong. Here is the error message:', e, tb)
#
#  Read the results.csv file into a dataframe and pack them all in a single list.
#
            if filename == "results.csv":
                try:
                    data.dfList.append(classes.makeDFfrom(name, fullFileName))
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f'Something went wrong. Here is the error message:', e, tb)
                
    ui.progressUpdate("-stdout-", "\n"+str(len(listOfFolders))+" directories were added.\n")

    return

#
#******************************************************************************
#

def splitStream(listOfFolders):
#
#  Divide the StreamData file into the single exercises according to the labels in labels.csv.
#
    for fullname in listOfFolders:
        name = os.path.basename(fullname)
        if name[0] == '.':
            continue
#
#  Get the files inside this one folder:
#
        listOfNames = os.listdir(fullname)
        hasResults  = False
#
#  Loop through the files inside the folder:
#
        for filename in listOfNames:
            fullFileName = os.path.join(fullname, filename)
            if filename[0] == '.':
                continue
            elif filename.__contains__("results.csv"):
                hasResults = True
            elif filename.startswith("labels"):
                with open(fullFileName, 'r', encoding='utf-8', newline='') as labels:
                    zeile     = labels.readline()           #  the first line contains the column headers.
                    zeile     = labels.readline()           #  only the second and further lines are interesting.
                    exerList  = []
                    startList = []
                    stopList  = []
                    while not zeile == "":
                        items = zeile.split(";")
                        exerList.append(items[0])
                        startList.append(items[1])
                        stopList.append(items[2])
                        zeile = labels.readline()
                    labels.close()
            elif filename.startswith("Stream"):
                streamDF = pd.read_csv(fullFileName, sep=";", header=0)
            else:
                continue
#
#  Do the splitting:
#
        for exercise, start, end in zip(exerList, startList, stopList):
            startIndex = streamDF.index[streamDF['MILLIS']==int(start)].tolist()
            endIndex   = streamDF.index[streamDF['MILLIS']==int(end)].tolist()
            if len(startIndex) > 0 and len(endIndex) > 0:
                newFileName = os.path.join(fullname, exercise+".csv")
                exerciseDF  = streamDF.loc[startIndex[0]:endIndex[-1]]
                with open(newFileName, 'w', encoding='utf-8', newline='') as csvDatei:
                    exerciseDF.to_csv(csvDatei, sep=";", index=False)

#
#******************************************************************************
#

def writeToFile(path, statisticsList, rowList, df_Stats):
#
#  Create a pickle file for eoch Dataframe list and save them separately.
#
    try:
        with open(os.path.join(path, "statistics.pkl"), 'wb') as output:     # Overwrites any existing file.
            pickle.dump(2, output)
            pickle.dump(statisticsList, output)
            pickle.dump(rowList, output)
        output.close()
        with open(os.path.join(path, "timeslices.pkl"), 'wb') as output:     # Overwrites any existing file.
            df_Stats.to_pickle(output)
        output.close()
        return 0

    except Exception as e:
        tb = traceback.format_exc()
        ui.progressUpdate("-stdout-",
                           'Something went wrong. Here is the error message:\n'+str(e)+"\n"+str(tb))
        return (e, tb)

#
#******************************************************************************
#

def readPickledData(path, window):
#
#  Read a DataFrame from a pickle file.
#
    try:
        with open(os.path.join(path, "statistics.pkl"), 'rb') as input:
            number = pickle.load(input)
            statisticsList = pickle.load(input)
            rowList = pickle.load(input)
        input.close()
        window["-stdout-"].print("File "+path+"/statistics.pkl read successfully")
        with open(os.path.join(path, "timeslices.pkl"), 'rb') as input:
            df_Stats = pandas.read_pickle(input)
        input.close()
        window["-stdout-"].print("File "+path+"/timeslices.pkl read successfully")
        return statisticsList, rowList, df_Stats

    except Exception as e:
        tb = traceback.format_exc()
        ui.progressUpdate("-stdout-",
                                   'Something went wrong. Here is the error message:\n'+str(e)+"\n"+str(tb))
        return [], [], pandas.DataFrame()

#
#******************************************************************************
#

def writeStandard(path, df_Stats, rowList):
#
#  Write the Statistics output to a CSV file.
#
#  Input: Tuple with 2 lists:
#        1. List of 20 lists of age brackets, each with the output from statistics (48 Parameters-Instances).
#        2. List of 7 lists, one for each task, with the number of entries in each age bracket.
#
#  First step: Smooth statistics results over age.
#
    result = plot.smoothData(df_Stats)
    jump   = len(classes.measuredData)
#
#  result is the list of smoothed runs over age and has 49 (7 items x 7 tasks) sublists.
#  Each sublist is a list of statistical results (min, max, mean, q1, median, q3).
#
    dateToday = date.today()
    filePath  = os.path.join(path, "Standard_"+dateToday.strftime("%y%m%d")+".csv")
    try:
        with open(filePath, 'w', newline='') as output:     # Overwrites any existing file.
            output.write("minAge,datasets,testTask,durationMin,durationMax,writingPressureMin,writingPressureMax,"+ \
                         "gripPressureMin,gripPressureMax,velocityMin,velocityMax,frequencyMin,frequencyMax,nivMin,"+ \
                         "nivMax,angleMin,angleMax,formMin,formMax\n")
            writer = csv.writer(output, dialect='unix', delimiter=",", quoting=csv.QUOTE_MINIMAL)
#
            for task in classes.relevantRows:
                taskIndex   = classes.relevantRows.index(task)
                taskRowList = rowList[taskIndex]
#
                for age in classes.ageStarts:
                    ageIndex = classes.ageStarts.index(age)
                    lineList = [age, len(taskRowList[ageIndex]), task,
                                result[taskIndex][0][ageIndex], result[taskIndex][1][ageIndex],
                                result[3*jump + taskIndex][0][ageIndex], result[3*jump + taskIndex][1][ageIndex],
                                result[4*jump + taskIndex][0][ageIndex], result[4*jump + taskIndex][1][ageIndex],
                                result[jump   + taskIndex][0][ageIndex], result[jump   + taskIndex][1][ageIndex],
                                result[2*jump + taskIndex][0][ageIndex], result[2*jump + taskIndex][1][ageIndex],
                                result[5*jump + taskIndex][0][ageIndex], result[5*jump + taskIndex][1][ageIndex],
                                result[6*jump + taskIndex][0][ageIndex], result[6*jump + taskIndex][1][ageIndex],
                                0.0, 1.0]
                    writer.writerow(lineList)
            output.close()
    
    except Exception as e:
       tb = traceback.format_exc()
       ui.progressUpdate("-stdout-",
                                  'Something went wrong. Here is the error message:\n'+str(e)+"\n"+str(tb))
#
#  Write the scaling of the EduPen output graphs to file.
#
    filePath  = os.path.join(path, "proportions_"+dateToday.strftime("%y%m%d")+".csv")
#
    timeMaximumList = result[1][1]           #  Time is only taken from the Sentence task.
    timeMedianList  = result[1][4]           #  Time is only taken from the Sentence task.
    maximumDict = {}
    quart1Dict  = {}
    quart3Dict  = {}
#
    for item in classes.measuredData:
        maximumDict[item] = [0.0] * len(classes.relevantRows)
        quart1Dict[item]  = [0.0] * len(classes.relevantRows)
        quart3Dict[item]  = [0.0] * len(classes.relevantRows)
        index = classes.measuredData.index(item) * len(classes.relevantRows)
        for task in classes.relevantRows:
            taskCounter = classes.relevantRows.index(task)
            maximumDict[item] = list(map(add, maximumDict[item], result[index + taskCounter][1]))
            quart1Dict[item]  = list(map(add, quart1Dict[item] , result[index + taskCounter][3]))
            quart3Dict[item]  = list(map(add, quart3Dict[item] , result[index + taskCounter][5]))
#
    try:
        with open(filePath, 'w', newline='') as output:     # Overwrites any existing file.
            output.write("ResultType,NormCenter,NormMin,NormMax,Invert,GraphCenter\n")
            writer = csv.writer(output, dialect='unix', delimiter=",", quoting=csv.QUOTE_MINIMAL)
            medianSentenceTime  = sum(timeMedianList)
            maximumSentenceTime = sum(timeMaximumList)
            normMax = medianSentenceTime / maximumSentenceTime
            writer.writerow(["duration", 0.5*normMax, 0.0, normMax, 1.0, normMax])
    
            normMin, normMax = relativeToMax(quart1Dict["Pressure"], quart3Dict["Pressure"], maximumDict["Pressure"])
            normMed = 0.5 * (normMax + normMin)
            writer.writerow(["writingPressure", normMed, normMin, normMax, 1.0, normMax])
    
            normMin, normMax = relativeToMax(quart1Dict["GripPressure"], quart3Dict["GripPressure"], maximumDict["GripPressure"])
            normMed = 0.5 * (1.0 + normMin)
            writer.writerow(["gripPressure", 0.22, 0.02, 0.42, 1.0, 0.42])
    
            normMin, normMax = relativeToMax(quart1Dict["Speed"], quart3Dict["Speed"], maximumDict["Speed"])
            normMed = 0.5 * (1.0 + normMin)
            writer.writerow(["velocity", normMed, normMin, 1.0, 0.0, normMin])
    
            normMin, normMax = relativeToMax(quart1Dict["Frequency"], quart3Dict["Frequency"], maximumDict["Frequency"])
            normMed = 0.5 * (1.0 + normMin)
            writer.writerow(["frequency", normMed, normMin, 1.0, 0.0, normMin])
    
            normMin, normMax = relativeToMax(quart1Dict["AutomationIndex"], quart3Dict["AutomationIndex"], maximumDict["AutomationIndex"])
            normDiff = normMax - normMin
            writer.writerow(["niv", 0.5*normDiff, 0.0, normDiff, 1.0, normDiff])
    
            normMin, normMax = relativeToMax(quart1Dict["PenTilt"], quart3Dict["PenTilt"], maximumDict["PenTilt"])
            normDiff = normMax - normMin
            writer.writerow(["angle", 0.5, 0.5 - normDiff, 0.5 + normDiff, 0.0, 0.5])
            writer.writerow(["form", 0.75, 0.5, 1.0, 0.0, 0.5])
    
            output.close()

    except Exception as e:
        tb = traceback.format_exc()
        ui.progressUpdate("-stdout-",
                                   'Something went wrong. Here is the error message:\n'+str(e)+"\n"+str(tb))
#
#  Polynomial fit over age runs
#
#    ageArray = np.array(classes.ageStarts)
#    order    = 5
#    print("rowList")
#    exIndex = 0
#    for exerciseList in rowList:
#        ageIndex = 0
#        print("Übung: ", classes.relevantRows[exIndex])
#        for entry in exerciseList:
#           print("Für Altersgruppe", ageArray[ageIndex], " gibt es", len(entry), " Einträge")
#           ageIndex += 1
#        exIndex += 1
#
#    for sublist in result:
#        newArray = np.array([np.array(sublist_i) for sublist_i in sublist])
#        coeffs = []
#        cheby  = []
#        for i in range(len(newArray)):
#            coeffs.append(polyfit(ageArray, newArray[i], order))
#            cheby.append(chebfit(ageArray, newArray[i], order))
#        print(coeffs)
#        print(cheby)
#        print(" ")
#
    return

#
#******************************************************************************
#

def relativeToMax(q1, q3, max):
#
#  Get the average rsp. maximum from all tasks.
#  q1, q3, max: List of ages built by summing up all task lists.
#
    sumQ1 = sum(q1)
    sumQ3 = sum(q3)
    maximum = sum(max)

    return (sumQ1 / maximum, sumQ3 / maximum)

#
#******************************************************************************
#

def rebase(listOfLists):
#
#  Rebase lists of smothed values on the same list of ages.
#
    newAge = np.array(classes.ageStarts)
    result = [classes.ageStarts]
    for counter in list(range(0, len(listOfLists), 2)):
        rebasedY = np.interp(newAge, listOfLists[counter], listOfLists[counter+1])
        result.append(rebasedY.tolist())

    return result
