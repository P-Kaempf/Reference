# This is a Python script.
import numpy as np
import platform
import matplotlib.pyplot as plt
import matplotlib
import classes
import data
from scipy.signal import savgol_filter

matplotlib.use('TKAgg')

if "Darwin" in platform.uname():
    defaultFont = {'family' : 'Lucida Grande', 'size' : 9}
elif "Linux" in platform.uname():
    defaultFont = {'family' : 'Bitstream Charter', 'size' : 10}
elif "Windows" in platform.uname():
    defaultFont = {'family' : 'Calibri', 'size' : 10}

#
#******************************************************************************
#

def show(plotstring, df_Stats, rowList):

    global plot_fig
    global time_ax
    global freq_ax
    global speed_ax
    global pres_ax
    global niv_ax
    global tilt_ax
#
# 6 fields with different contents
#
    plot_fig = plt.figure("Results", figsize=(10, 5.5))
    plot_fig.set_dpi(144)
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('legend', fontsize=8)
#
# Writing Time
#
    time_ax = plt.subplot(231, adjustable='datalim')
    plt.yscale('linear')
    plt.title('Writing Time for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('Time [s]', font=defaultFont)
    plt.grid(True)
    time_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    time_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    time_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[time_qua1, time_mean, time_qua3], loc='upper left')
#
# Writing Frequency
#
    freq_ax = plt.subplot(232)
    plt.yscale('linear')
    plt.title('Writing Frequency for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('Frequency [Hz]', font=defaultFont)
    plt.grid(True)
    freq_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    freq_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    freq_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[freq_qua1, freq_mean, freq_qua3], loc='upper left')
#
# Writing Speed
#
    speed_ax = plt.subplot(233)
    plt.yscale('linear')
    plt.title('Writing Speed for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('Speed [cm/s]', font=defaultFont)
    plt.grid(True)
    speed_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    speed_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    speed_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[speed_qua1, speed_mean, speed_qua3], loc='upper left')
#
# Writing Pressure
#
    pres_ax = plt.subplot(234)
    plt.yscale('linear')
    plt.title('Writing Pressure for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('Pressure [N]', font=defaultFont)
    plt.grid(True)
    pres_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    pres_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    pres_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[pres_qua1, pres_mean, pres_qua3], loc='upper left')
#
# Automation Index
#
    niv_ax = plt.subplot(235)
    plt.yscale('linear')
    plt.title('Automation Index for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('NIV', font=defaultFont)
    plt.grid(True)
    niv_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    niv_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    niv_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[niv_qua1, niv_mean, niv_qua3], loc='upper left')
#
# Pen Tilt
#
    tilt_ax = plt.subplot(236)
    plt.yscale('linear')
    plt.title('Pen Tilt Angle for exercise '+plotstring, font=defaultFont)
    plt.xlabel('Age [years]', font=defaultFont)
    plt.ylabel('Angle [degrees]', font=defaultFont)
    plt.grid(True)
    tilt_qua1 = matplotlib.lines.Line2D([], [], color='darkgreen', label='1st quartil')
    tilt_mean = matplotlib.lines.Line2D([], [], color='black',   label='median')
    tilt_qua3 = matplotlib.lines.Line2D([], [], color='darkred', label='3rd quartil')
    plt.legend(handles=[tilt_qua1, tilt_mean, tilt_qua3], loc='upper left')
    
    plt.subplots_adjust(top=0.95, bottom=0.08, left=0.08, right=0.98, hspace=0.28, wspace=0.2)

    graph = plt.show(block=False)
#
#  df_Stats:
#         0         1          2            3            4            5
#  0 [min_time  max_time  mean_time  quart1_time  median_time  quart3_time
#  6  min_speed max_speed mean_speed quart1_speed median_speed quart3_speed
# 12  min_freq  max_freq  mean_freq  quart1_freq  median_freq  quart3_freq
# 18  min_force max_force mean_force quart1_force median_force quart3_force
# 24  min_grip  max_grip  mean_grip  quart1_grip  median_grip  quart3_grip
# 30  min_niv   max_niv   mean_niv   quart1_niv   median_niv   quart3_niv
# 36  min_tilt  max_tilt  mean_tilt  quart1_tilt  median_tilt  quart3_tilt]
#
#  agelists:
#
#    ageList_5  = ageList[0]
#    ageList_6  = ageList[1]
#    ageList_7  = ageList[2]
#    ageList_8  = ageList[3]
#    ageList_9  = ageList[4]
#    ageList_10 = ageList[5]
#    ageList_11 = ageList[6]
#    ageList_12 = ageList[7]
#    ageList_13 = ageList[8]
#    ageList_14 = ageList[9]
#    ageList_15 = ageList[10]
#    ageList_16 = ageList[11]
#    ageList_17 = ageList[12]
#    ageList_21 = ageList[13]
#    ageList_31 = ageList[14]
#    ageList_41 = ageList[15]
#    ageList_51 = ageList[16]
#    ageList_61 = ageList[17]
#    ageList_71 = ageList[18]
#    ageList_76 = ageList[19]
#
#  rowLists:
#
#    nameRowList     = rowList[0]
#    sentenceRowList = rowList[1]
#    wordRowList     = rowList[2]
#    eleRowList      = rowList[3]
#    lateralRowList  = rowList[4]
#    frontalRowList  = rowList[5]
#    loopsRowList    = rowList[6]
#
    x1List  = []
    y11List = []
    y12List = []
    y13List = []
    x2List  = []
    y21List = []
    y22List = []
    y23List = []
    x3List  = []
    y31List = []
    y32List = []
    y33List = []
    x4List  = []
    y41List = []
    y42List = []
    y43List = []
    x5List  = []
    y51List = []
    y52List = []
    y53List = []
    x6List  = []
    y61List = []
    y62List = []
    y63List = []
#
#  Loop over age groups:
#
    for counter in list(range(len(classes.ageValues))):
        if len(rowList[1][counter]) > 4:
            tuple = collectValues(df_Stats, counter,3, 4, 5, plotstring)
            if len(tuple) == 4:
                x1List.append(tuple[0])
                y11List.append(tuple[1])
                y12List.append(tuple[2])
                y13List.append(tuple[3])
            
            tuple = collectValues(df_Stats, counter,15, 16, 17, plotstring)
            if len(tuple) == 4:
                x2List.append(tuple[0])
                y21List.append(tuple[1])
                y22List.append(tuple[2])
                y23List.append(tuple[3])
            
            tuple = collectValues(df_Stats, counter,9, 10, 11, plotstring)
            if len(tuple) == 4:
                x3List.append(tuple[0])
                y31List.append(tuple[1])
                y32List.append(tuple[2])
                y33List.append(tuple[3])
            
            tuple = collectValues(df_Stats, counter,21, 22, 23, plotstring)
            if len(tuple) == 4:
                x4List.append(tuple[0])
                y41List.append(tuple[1])
                y42List.append(tuple[2])
                y43List.append(tuple[3])
            
            tuple = collectValues(df_Stats, counter,33, 34, 35, plotstring)
            if len(tuple) == 4:
                x5List.append(tuple[0])
                y51List.append(tuple[1])
                y52List.append(tuple[2])
                y53List.append(tuple[3])
            
            tuple = collectValues(df_Stats, counter,39, 40, 41, plotstring)
            if len(tuple) == 4:
                x6List.append(tuple[0])
                y61List.append(tuple[1])
                y62List.append(tuple[2])
                y63List.append(tuple[3])
#
#  Plot the true values first with linewidth 1, then the smoothed lines with linewidth 2.
#
    small_y11List = []
    for item in y11List:
        if data.checkForNumeric(item):
            small_y11List.append(item / 1000.0)
        else:
            small_y11List.append(item)
    small_y12List = []
    for item in y12List:
        if data.checkForNumeric(item):
            small_y12List.append(item / 1000.0)
        else:
            small_y12List.append(item)
    small_y13List = []
    for item in y13List:
        if data.checkForNumeric(item):
            small_y13List.append(item / 1000.0)
        else:
            small_y13List.append(item)
#
    drawLines(time_ax, x1List, small_y11List, small_y12List, small_y13List)
    drawLines(freq_ax, x2List, y21List, y22List, y23List)
    drawLines(speed_ax, x3List, y31List, y32List, y33List)
    drawLines(pres_ax, x4List, y41List, y42List, y43List)
    drawLines(niv_ax, x5List, y51List, y52List, y53List)
    drawLines(tilt_ax, x6List, y61List, y62List, y63List)

#
#******************************************************************************
#

def collectValues(df_Stats, counter, column1, column2, column3, string) -> tuple:
#
#  Collect the values for the different plots from the DataFrame df_Stats.
#  Filter for Nan, None and negative values:
#
    value1 = getattr(df_Stats.iat[counter,column1], string)
    value2 = getattr(df_Stats.iat[counter,column2], string)
    value3 = getattr(df_Stats.iat[counter,column3], string)
    if data.checkForNumeric(value1) and \
       data.checkForNumeric(value1) and \
       data.checkForNumeric(value1) :
        if value1 > 0.0 and value2 > 0.0 and value3 > 0.0:
            return (classes.ageValues[counter], value1, value2, value3)
        else:
            return ()
    else:
        return ()

#
#******************************************************************************
#

def drawLines(plot_ax, xList, y1List, y2List, y3List):
#
#  does the plotting work.
#
    for line in plot_ax.lines:
        line.remove()

    y_arr1 = np.array(y1List)
    y_arr2 = np.array(y2List)
    y_arr3 = np.array(y3List)
    plot_ax.plot(np.array(xList), y_arr1, color='darkgreen', lw=1.0)
    plot_ax.plot(np.array(xList), y_arr2, color='black', lw=1.0)
    plot_ax.plot(np.array(xList), y_arr3, color='darkred', lw=1.0)
    if len(xList) > 4:
        x_array1, y_array1 = savgol_filter((np.array(xList), y_arr1), 5, 3)
        x_array2, y_array2 = savgol_filter((np.array(xList), y_arr2), 5, 3)
        x_array3, y_array3 = savgol_filter((np.array(xList), y_arr3), 5, 3)
        plot_ax.plot(x_array1, y_array1, color='darkgreen', lw=2.0)
        plot_ax.plot(x_array2, y_array2, color='black', lw=2.0)
        plot_ax.plot(x_array3, y_array3, color='darkred', lw=2.0)

    plot_ax.figure.canvas.draw()

#
#******************************************************************************
#

def smoothData(df_Stats) -> list:
#
#  Input: DataFrame with age as index and the output from statistics (42 Parameters-Instances) as columns.
#
#  Output: Smoothed runs over age, because of possible gaps now as list of pairs of x and y lists.
#          The required values are Minimum, Maximum, Quartil1, Median and Quartil3 of all exercises.
#
    smoothedList = []
    startColumn  = 0

    for item in classes.measuredData:
#        print("\n Meßwert: ", item)

        for task in classes.relevantRows:
#            print("\n Aufgabe: ", task)
#
#  We cannot just grab a column of the DataFrame, but must check every single entry
#  for -1, Nan, None and such. Therefore, we go into a loop over age:
#
            smoothedList.append(collectRow(df_Stats, startColumn, task))
            
        startColumn += 6            #  min, max, mean, q1, median, q3: Six statistics results
#
    return smoothedList

#
#******************************************************************************
#

def collectRow(df_Stats, startColumn, task):
#
#  We cannot just get a column of the DataFrame, but must check every single entry
#  for -1, Nan, None and such. Therefore, we go into a loop over age:
#
    outputList = []

    xMinMaxList = []
    yMinList    = []
    yMaxList    = []
    yMeanList   = []
    xQuartList  = []
    yQuart1List = []
    yMedianList = []
    yQuart3List = []
#
    for counter in list(range(len(classes.ageValues))):
        tuple = collectValues(df_Stats, counter,startColumn, startColumn+1, startColumn+2, task)
        if len(tuple) == 4:
            xMinMaxList.append(tuple[0])
            yMinList.append(tuple[1])
            yMaxList.append(tuple[2])
            yMeanList.append(tuple[3])
#
        tuple = collectValues(df_Stats, counter, startColumn+3, startColumn+4, startColumn+5, task)
        if len(tuple) == 4:
            xQuartList.append(tuple[0])
            yQuart1List.append(tuple[1])
            yMedianList.append(tuple[2])
            yQuart3List.append(tuple[3])
#
#  Now smooth the filtered run of values over age ...
#  (We need to put the x and y sequences into the filter because x has an uneven distribution)
#
    if len(xMinMaxList) > 4:
        xArray, yMinArray  = savgol_filter((np.array(xMinMaxList), np.array(yMinList)), 5, 3)
        xArray, yMaxArray  = savgol_filter((np.array(xMinMaxList), np.array(yMaxList)), 5, 3)
        xArray, yMeanArray = savgol_filter((np.array(xMinMaxList), np.array(yMeanList)), 5, 3)
    elif len(xMinMaxList) > 0:
        xArray = np.array(xMinMaxList)
        yMinArray  = np.array(yMinList)
        yMaxArray  = np.array(yMaxList)
        yMeanArray = np.array(yMeanList)
    else:
        xArray = np.empty(shape=1)
        yMinArray  = np.empty(shape=1)
        yMaxArray  = np.empty(shape=1)
        yMeanArray = np.empty(shape=1)
#
#  ... and base it on the full age range again. Rememeber, the columns might be missing some values!
#
    rebasedY = np.interp(np.array(classes.ageStarts), xArray, yMinArray)
#    print("Min: ", rebasedY.tolist())
    outputList.append(rebasedY.tolist())
    rebasedY = np.interp(np.array(classes.ageStarts), xArray, yMaxArray)
#    print("Max: ", rebasedY.tolist())
    outputList.append(rebasedY.tolist())
    rebasedY = np.interp(np.array(classes.ageStarts), xArray, yMeanArray)
#    print("Mean:", rebasedY.tolist())
    outputList.append(rebasedY.tolist())
#
#  Same for the second triplet of values:
#
    if len(xQuartList) > 4:
        xQuartArray, yQuart1Array = savgol_filter((np.array(xQuartList), np.array(yQuart1List)), 5, 3)
        xQuartArray, yMedianArray = savgol_filter((np.array(xQuartList), np.array(yMedianList)), 5, 3)
        xQuartArray, yQuart3Array = savgol_filter((np.array(xQuartList), np.array(yQuart3List)), 5, 3)
    elif len(xMinMaxList) > 0:
        xQuartArray  = np.array(xQuartList)
        yQuart1Array = np.array(yQuart1List)
        yMedianArray = np.array(yMedianList)
        yQuart3Array = np.array(yQuart3List)
    else:
        xQuartArray  = np.empty(shape=1)
        yQuart1Array = np.empty(shape=1)
        yMedianArray = np.empty(shape=1)
        yQuart3Array = np.empty(shape=1)
#
    rebasedY = np.interp(np.array(classes.ageStarts), xQuartArray, yQuart1Array)
#    print("Q1:  ", rebasedY.tolist())
    outputList.append(rebasedY.tolist())
    rebasedY = np.interp(np.array(classes.ageStarts), xQuartArray, yMedianArray)
#    print("Med: ", rebasedY.tolist())
    outputList.append(rebasedY.tolist())
    rebasedY = np.interp(np.array(classes.ageStarts), xQuartArray, yQuart3Array)
#    print("Q3:  ", rebasedY.tolist())
    outputList.append(rebasedY.tolist())

    return outputList
    
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
