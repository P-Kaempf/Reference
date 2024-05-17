# This is a Python script.
import numpy as np
import pandas
import classes
from classes import parameters
import ui

dfList = []
dfSubList = []

#
#******************************************************************************
#

def get_group(group, key):
#
#  Get a sub-DataFrame with all entries having the desired key.
#
    if key in group.groups:
        return group.get_group(key)
    else:
        return pandas.DataFrame()

#
#******************************************************************************
#

def runCollateDataframes():
    
    global dfList
    global dfSubList

    ui.progressUpdate("-stdout-", "Now collecting data from all files.\n")

    result = collateDataframes(dfList)
    dfSubList = result[1]

    ui.progressUpdate("-stdout-", "Done with "+str(7*len(dfList))+" exercises, "
                               + str(result[0])+" of which were not valid.")
    for df, rowName in zip(dfSubList, classes.relevantRows):
        ui.progressUpdate("-stdout-",
                             "The "+rowName+" exercise has "+str(len(df.index))+" valid entries")

#
#******************************************************************************
#

def collateDataframes(localList):
#
#  Collect the individual lines of all dataframes in new dataframes
#
#   localList :   List of Pandas.DataFrames
#
    total = len(localList)
#
    counter  = 0
    invalid  = 0
    nameList = []
    sentList = []
    wordList = []
    eleList  = []
    lateList = []
    fronList = []
    loopsList = []
    loopList = [nameList, sentList, wordList, eleList, lateList, fronList, loopsList]
#
    for line in localList:
        ui.progressUpdate('-Pro-', int(5000 * float(counter) / float(total)))
#
        for subList, exercise in zip(loopList, classes.relevantRows):
            row_array = np.where(line["Label"] == exercise)[0]
            if row_array.size > 0:
                row = int(row_array[0])
                if int(line.at[row, 'IsValidData']) == 1 and line.at[row, 'WritingTime'] > 0:
                    subList.append(line.iloc[[row]])
                else:
                    invalid += 1
            else:
                invalid += 1
        counter += 1
#
#  Older recordings do not have a name exercise. Therefore ...
#
    if len(nameList) > 0:
        df_name = pandas.concat(nameList, axis=0, ignore_index=True)
    else:
        df_name = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid name recording could be found!')
    if len(sentList) > 0:
        df_sent = pandas.concat(sentList, axis=0, ignore_index=True)
    else:
        df_sent = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid sentence recording could be found!')
    if len(wordList) > 0:
        df_word = pandas.concat(wordList, axis=0, ignore_index=True)
    else:
        df_word = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid AUTO recording could be found!')
    if len(eleList) > 0:
        df_ele  = pandas.concat(eleList,  axis=0, ignore_index=True)
    else:
        df_ele = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid ele recording could be found!')
    if len(lateList) > 0:
        df_late = pandas.concat(lateList, axis=0, ignore_index=True)
    else:
        df_late = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid wrist hatch recording could be found!')
    if len(fronList) > 0:
        df_fron = pandas.concat(fronList, axis=0, ignore_index=True)
    else:
        df_fron = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid finger hatch recording could be found!')
    if len(loopsList) > 0:
        df_loops = pandas.concat(loopsList, axis=0, ignore_index=True)
    else:
        df_loops = pandas.DataFrame()
        ui.progressUpdate("-stdout-",
            'Not a single instance of a valid loops recording could be found!')

    return (invalid, [df_name, df_sent, df_word, df_ele, df_late, df_fron, df_loops])

#
#******************************************************************************
#

def runTimeslices():
#
#  Divide the data in those age groups:
# <5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-75 and 76-80-year olds.
#
    global dfSubList

    resultTuple = timeslices(dfSubList)

    df_Stats = pandas.DataFrame([],
         columns = ["min_time",  "max_time",  "mean_time",  "quart1_time",  "median_time",  "quart3_time",
                    "min_speed", "max_speed", "mean_speed", "quart1_speed", "median_speed", "quart3_speed",
                    "min_freq",  "max_freq",  "mean_freq",  "quart1_freq",  "median_freq",  "quart3_freq",
                    "min_force", "max_force", "mean_force", "quart1_force", "median_force", "quart3_force",
                    "min_grip",  "max_grip",  "mean_grip",  "quart1_grip",  "median_grip",  "quart3_grip",
                    "min_niv",   "max_niv",   "mean_niv",   "quart1_niv",   "median_niv",   "quart3_niv",
                    "min_tilt",  "max_tilt",  "mean_tilt",  "quart1_tilt",  "median_tilt",  "quart3_tilt"])
    for ageList, lineIndex in zip(resultTuple[0], list(range(len(resultTuple[0])))):
        df_Stats.loc[lineIndex] = ageList
    
    ui.progressUpdate("-stdout-", "Done splitting into "+str(len(resultTuple[0]))+" age groups.")

    return df_Stats, resultTuple[1]

#
#******************************************************************************
#
def timeslices(localList):
#
#  Divide the data into those age groups:
# <5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-75 and 76-80-year olds.
#
    df_name  = localList[0]
    df_name.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_sent = localList[1]
    df_sent.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_word = localList[2]
    df_word.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_ele  = localList[3]
    df_ele.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_late = localList[4]
    df_late.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_fron = localList[5]
    df_fron.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
    df_loops = localList[6]
    df_loops.sort_values(by=['Age'], axis=0, inplace=True, ignore_index=True)
#
    df_name_5  = df_name.query('Age <  6')
    df_name_6  = df_name.query(' 6.0 <= Age <  7')
    df_name_7  = df_name.query(' 7.0 <= Age <  8')
    df_name_8  = df_name.query(' 8.0 <= Age <  9')
    df_name_9  = df_name.query(' 9.0 <= Age < 10')
    df_name_10 = df_name.query('10.0 <= Age < 11.0')
    df_name_11 = df_name.query('11.0 <= Age < 12.0')
    df_name_12 = df_name.query('12.0 <= Age < 13.0')
    df_name_13 = df_name.query('13.0 <= Age < 14.0')
    df_name_14 = df_name.query('14.0 <= Age < 15.0')
    df_name_15 = df_name.query('15.0 <= Age < 16.0')
    df_name_16 = df_name.query('16.0 <= Age < 17.0')
    df_name_17 = df_name.query('17.0 <= Age < 21.0')
    df_name_21 = df_name.query('30.0 <= Age < 31.0')
    df_name_31 = df_name.query('40.0 <= Age < 41.0')
    df_name_41 = df_name.query('50.0 <= Age < 51.0')
    df_name_51 = df_name.query('60.0 <= Age < 61.0')
    df_name_61 = df_name.query('70.0 <= Age < 71.0')
    df_name_71 = df_name.query('75.0 <= Age < 76.0')
    df_name_76 = df_name.query('76.0 <= Age')

    nameRowList = [df_name_5.index,  df_name_6.index,  df_name_7.index,  df_name_8.index,
                   df_name_9.index,  df_name_10.index, df_name_11.index, df_name_12.index,
                   df_name_13.index, df_name_14.index, df_name_15.index, df_name_16.index,
                   df_name_17.index, df_name_21.index, df_name_31.index, df_name_41.index,
                   df_name_51.index, df_name_61.index, df_name_71.index, df_name_76.index]
#
    df_sent_5  = df_sent.query('Age <  6')
    df_sent_6  = df_sent.query(' 6.0 <= Age <  7')
    df_sent_7  = df_sent.query(' 7.0 <= Age <  8')
    df_sent_8  = df_sent.query(' 8.0 <= Age <  9')
    df_sent_9  = df_sent.query(' 9.0 <= Age < 10')
    df_sent_10 = df_sent.query('10.0 <= Age < 11.0')
    df_sent_11 = df_sent.query('11.0 <= Age < 12.0')
    df_sent_12 = df_sent.query('12.0 <= Age < 13.0')
    df_sent_13 = df_sent.query('13.0 <= Age < 14.0')
    df_sent_14 = df_sent.query('14.0 <= Age < 15.0')
    df_sent_15 = df_sent.query('15.0 <= Age < 16.0')
    df_sent_16 = df_sent.query('16.0 <= Age < 17.0')
    df_sent_17 = df_sent.query('17.0 <= Age < 21.0')
    df_sent_21 = df_sent.query('30.0 <= Age < 31.0')
    df_sent_31 = df_sent.query('40.0 <= Age < 41.0')
    df_sent_41 = df_sent.query('50.0 <= Age < 51.0')
    df_sent_51 = df_sent.query('60.0 <= Age < 61.0')
    df_sent_61 = df_sent.query('70.0 <= Age < 71.0')
    df_sent_71 = df_sent.query('75.0 <= Age < 76.0')
    df_sent_76 = df_sent.query('76.0 <= Age')

    ui.progressUpdate('-Pro-', int(5200))

    sentRowList = [df_sent_5.index,  df_sent_6.index,  df_sent_7.index,  df_sent_8.index,
                   df_sent_9.index,  df_sent_10.index, df_sent_11.index, df_sent_12.index,
                   df_sent_13.index, df_sent_14.index, df_sent_15.index, df_sent_16.index,
                   df_sent_17.index, df_sent_21.index, df_sent_31.index, df_sent_41.index,
                   df_sent_51.index, df_sent_61.index, df_sent_71.index, df_sent_76.index]

    df_word_5  = df_word.query('Age <  6')
    df_word_6  = df_word.query(' 6.0 <= Age <  7')
    df_word_7  = df_word.query(' 7.0 <= Age <  8')
    df_word_8  = df_word.query(' 8.0 <= Age <  9')
    df_word_9  = df_word.query(' 9.0 <= Age < 10')
    df_word_10 = df_word.query('10.0 <= Age < 11.0')
    df_word_11 = df_word.query('11.0 <= Age < 12.0')
    df_word_12 = df_word.query('12.0 <= Age < 13.0')
    df_word_13 = df_word.query('13.0 <= Age < 14.0')
    df_word_14 = df_word.query('14.0 <= Age < 15.0')
    df_word_15 = df_word.query('15.0 <= Age < 16.0')
    df_word_16 = df_word.query('16.0 <= Age < 17.0')
    df_word_17 = df_word.query('17.0 <= Age < 21.0')
    df_word_21 = df_word.query('30.0 <= Age < 31.0')
    df_word_31 = df_word.query('40.0 <= Age < 41.0')
    df_word_41 = df_word.query('50.0 <= Age < 51.0')
    df_word_51 = df_word.query('60.0 <= Age < 61.0')
    df_word_61 = df_word.query('70.0 <= Age < 71.0')
    df_word_71 = df_word.query('75.0 <= Age < 76.0')
    df_word_76 = df_word.query('76.0 <= Age')

    wordRowList = [df_word_5.index,  df_word_6.index,  df_word_7.index,  df_word_8.index,
                   df_word_9.index,  df_word_10.index, df_word_11.index, df_word_12.index,
                   df_word_13.index, df_word_14.index, df_word_15.index, df_word_16.index,
                   df_word_17.index, df_word_21.index, df_word_31.index, df_word_41.index,
                   df_word_51.index, df_word_61.index, df_word_71.index, df_word_76.index]

    df_ele_5  = df_ele.query('Age <  6')
    df_ele_6  = df_ele.query(' 6.0 <= Age <  7')
    df_ele_7  = df_ele.query(' 7.0 <= Age <  8')
    df_ele_8  = df_ele.query(' 8.0 <= Age <  9')
    df_ele_9  = df_ele.query(' 9.0 <= Age < 10')
    df_ele_10 = df_ele.query('10.0 <= Age < 11.0')
    df_ele_11 = df_ele.query('11.0 <= Age < 12.0')
    df_ele_12 = df_ele.query('12.0 <= Age < 13.0')
    df_ele_13 = df_ele.query('13.0 <= Age < 14.0')
    df_ele_14 = df_ele.query('14.0 <= Age < 15.0')
    df_ele_15 = df_ele.query('15.0 <= Age < 16.0')
    df_ele_16 = df_ele.query('16.0 <= Age < 17.0')
    df_ele_17 = df_ele.query('17.0 <= Age < 21.0')
    df_ele_21 = df_ele.query('30.0 <= Age < 31.0')
    df_ele_31 = df_ele.query('40.0 <= Age < 41.0')
    df_ele_41 = df_ele.query('50.0 <= Age < 51.0')
    df_ele_51 = df_ele.query('60.0 <= Age < 61.0')
    df_ele_61 = df_ele.query('70.0 <= Age < 71.0')
    df_ele_71 = df_ele.query('75.0 <= Age < 76.0')
    df_ele_76 = df_ele.query('76.0 <= Age')

    ui.progressUpdate('-Pro-', int(5400))

    eleRowList = [df_ele_5.index,  df_ele_6.index,  df_ele_7.index,  df_ele_8.index,
                  df_ele_9.index,  df_ele_10.index, df_ele_11.index, df_ele_12.index,
                  df_ele_13.index, df_ele_14.index, df_ele_15.index, df_ele_16.index,
                  df_ele_17.index, df_ele_21.index, df_ele_31.index, df_ele_41.index,
                  df_ele_51.index, df_ele_61.index, df_ele_71.index, df_ele_76.index]

    df_late_5  = df_late.query('Age <  6')
    df_late_6  = df_late.query(' 6.0 <= Age <  7')
    df_late_7  = df_late.query(' 7.0 <= Age <  8')
    df_late_8  = df_late.query(' 8.0 <= Age <  9')
    df_late_9  = df_late.query(' 9.0 <= Age < 10')
    df_late_10 = df_late.query('10.0 <= Age < 11.0')
    df_late_11 = df_late.query('11.0 <= Age < 12.0')
    df_late_12 = df_late.query('12.0 <= Age < 13.0')
    df_late_13 = df_late.query('13.0 <= Age < 14.0')
    df_late_14 = df_late.query('14.0 <= Age < 15.0')
    df_late_15 = df_late.query('15.0 <= Age < 16.0')
    df_late_16 = df_late.query('16.0 <= Age < 17.0')
    df_late_17 = df_late.query('17.0 <= Age < 21.0')
    df_late_21 = df_late.query('30.0 <= Age < 31.0')
    df_late_31 = df_late.query('40.0 <= Age < 41.0')
    df_late_41 = df_late.query('50.0 <= Age < 51.0')
    df_late_51 = df_late.query('60.0 <= Age < 61.0')
    df_late_61 = df_late.query('70.0 <= Age < 71.0')
    df_late_71 = df_late.query('75.0 <= Age < 76.0')
    df_late_76 = df_late.query('76.0 <= Age')

    lateRowList = [df_late_5.index,  df_late_6.index,  df_late_7.index,  df_late_8.index,
                   df_late_9.index,  df_late_10.index, df_late_11.index, df_late_12.index,
                   df_late_13.index, df_late_14.index, df_late_15.index, df_late_16.index,
                   df_late_17.index, df_late_21.index, df_late_31.index, df_late_41.index,
                   df_late_51.index, df_late_61.index, df_late_71.index, df_late_76.index]

    df_fron_5  = df_fron.query('Age <  6')
    df_fron_6  = df_fron.query(' 6.0 <= Age <  7')
    df_fron_7  = df_fron.query(' 7.0 <= Age <  8')
    df_fron_8  = df_fron.query(' 8.0 <= Age <  9')
    df_fron_9  = df_fron.query(' 9.0 <= Age < 10')
    df_fron_10 = df_fron.query('10.0 <= Age < 11.0')
    df_fron_11 = df_fron.query('11.0 <= Age < 12.0')
    df_fron_12 = df_fron.query('12.0 <= Age < 13.0')
    df_fron_13 = df_fron.query('13.0 <= Age < 14.0')
    df_fron_14 = df_fron.query('14.0 <= Age < 15.0')
    df_fron_15 = df_fron.query('15.0 <= Age < 16.0')
    df_fron_16 = df_fron.query('16.0 <= Age < 17.0')
    df_fron_17 = df_fron.query('17.0 <= Age < 21.0')
    df_fron_21 = df_fron.query('30.0 <= Age < 31.0')
    df_fron_31 = df_fron.query('40.0 <= Age < 41.0')
    df_fron_41 = df_fron.query('50.0 <= Age < 51.0')
    df_fron_51 = df_fron.query('60.0 <= Age < 61.0')
    df_fron_61 = df_fron.query('70.0 <= Age < 71.0')
    df_fron_71 = df_fron.query('75.0 <= Age < 76.0')
    df_fron_76 = df_fron.query('76.0 <= Age')

    ui.progressUpdate('-Pro-', int(5600))

    fronRowList = [df_fron_5.index,  df_fron_6.index,  df_fron_7.index,  df_fron_8.index,
                   df_fron_9.index,  df_fron_10.index, df_fron_11.index, df_fron_12.index,
                   df_fron_13.index, df_fron_14.index, df_fron_15.index, df_fron_16.index,
                   df_fron_17.index, df_fron_21.index, df_fron_31.index, df_fron_41.index,
                   df_fron_51.index, df_fron_61.index, df_fron_71.index, df_fron_76.index]

    df_loops_5  = df_loops.query('Age <  6')
    df_loops_6  = df_loops.query(' 6.0 <= Age <  7')
    df_loops_7  = df_loops.query(' 7.0 <= Age <  8')
    df_loops_8  = df_loops.query(' 8.0 <= Age <  9')
    df_loops_9  = df_loops.query(' 9.0 <= Age < 10')
    df_loops_10 = df_loops.query('10.0 <= Age < 11.0')
    df_loops_11 = df_loops.query('11.0 <= Age < 12.0')
    df_loops_12 = df_loops.query('12.0 <= Age < 13.0')
    df_loops_13 = df_loops.query('13.0 <= Age < 14.0')
    df_loops_14 = df_loops.query('14.0 <= Age < 15.0')
    df_loops_15 = df_loops.query('15.0 <= Age < 16.0')
    df_loops_16 = df_loops.query('16.0 <= Age < 17.0')
    df_loops_17 = df_loops.query('17.0 <= Age < 21.0')
    df_loops_21 = df_loops.query('30.0 <= Age < 31.0')
    df_loops_31 = df_loops.query('40.0 <= Age < 41.0')
    df_loops_41 = df_loops.query('50.0 <= Age < 51.0')
    df_loops_51 = df_loops.query('60.0 <= Age < 61.0')
    df_loops_61 = df_loops.query('70.0 <= Age < 71.0')
    df_loops_71 = df_loops.query('75.0 <= Age < 76.0')
    df_loops_76 = df_loops.query('76.0 <= Age')

    loopsRowList = [df_loops_5.index,  df_loops_6.index,  df_loops_7.index,  df_loops_8.index,
                    df_loops_9.index,  df_loops_10.index, df_loops_11.index, df_loops_12.index,
                    df_loops_13.index, df_loops_14.index, df_loops_15.index, df_loops_16.index,
                    df_loops_17.index, df_loops_21.index, df_loops_31.index, df_loops_41.index,
                    df_loops_51.index, df_loops_61.index, df_loops_71.index, df_loops_76.index]
    ageList_5  = statistics([df_name_5 , df_sent_5 , df_word_5 , df_ele_5 , df_late_5 , df_fron_5 , df_loops_5 ])
    ageList_6  = statistics([df_name_6 , df_sent_6 , df_word_6 , df_ele_6 , df_late_6 , df_fron_6 , df_loops_6 ])
    ui.progressUpdate('-Pro-', int(5900))
    ageList_7  = statistics([df_name_7 , df_sent_7 , df_word_7 , df_ele_7 , df_late_7 , df_fron_7 , df_loops_7 ])
    ageList_8  = statistics([df_name_8 , df_sent_8 , df_word_8 , df_ele_8 , df_late_8 , df_fron_8 , df_loops_8 ])
    ui.progressUpdate('-Pro-', int(6200))
    ageList_9  = statistics([df_name_9 , df_sent_9 , df_word_9 , df_ele_9 , df_late_9 , df_fron_9 , df_loops_9 ])
    ui.progressUpdate('-Pro-', int(6500))
    ageList_10 = statistics([df_name_10, df_sent_10, df_word_10, df_ele_10, df_late_10, df_fron_10, df_loops_10])
    ageList_11 = statistics([df_name_11, df_sent_11, df_word_11, df_ele_11, df_late_11, df_fron_11, df_loops_11])
    ui.progressUpdate('-Pro-', int(6800))
    ageList_12 = statistics([df_name_12, df_sent_12, df_word_12, df_ele_12, df_late_12, df_fron_12, df_loops_12])
    ageList_13 = statistics([df_name_13, df_sent_13, df_word_13, df_ele_13, df_late_13, df_fron_13, df_loops_13])
    ui.progressUpdate('-Pro-', int(7100))
    ageList_14 = statistics([df_name_14, df_sent_14, df_word_14, df_ele_14, df_late_14, df_fron_14, df_loops_14])
    ageList_15 = statistics([df_name_15, df_sent_15, df_word_15, df_ele_15, df_late_15, df_fron_15, df_loops_15])
    ui.progressUpdate('-Pro-', int(7400))
    ageList_16 = statistics([df_name_16, df_sent_16, df_word_16, df_ele_16, df_late_16, df_fron_16, df_loops_16])
    ageList_17 = statistics([df_name_17, df_sent_17, df_word_17, df_ele_17, df_late_17, df_fron_17, df_loops_17])
    ui.progressUpdate('-Pro-', int(7700))
    ageList_21 = statistics([df_name_21, df_sent_21, df_word_21, df_ele_21, df_late_21, df_fron_21, df_loops_21])
    ageList_31 = statistics([df_name_31, df_sent_31, df_word_31, df_ele_31, df_late_31, df_fron_31, df_loops_31])
    ui.progressUpdate('-Pro-', int(8000))
    ageList_41 = statistics([df_name_41, df_sent_41, df_word_41, df_ele_41, df_late_41, df_fron_41, df_loops_41])
    ageList_51 = statistics([df_name_51, df_sent_51, df_word_51, df_ele_51, df_late_51, df_fron_51, df_loops_51])
    ui.progressUpdate('-Pro-', int(8300))
    ageList_61 = statistics([df_name_61, df_sent_61, df_word_61, df_ele_61, df_late_61, df_fron_61, df_loops_61])
    ageList_71 = statistics([df_name_71, df_sent_71, df_word_71, df_ele_71, df_late_71, df_fron_71, df_loops_71])
    ui.progressUpdate('-Pro-', int(8600))
    ageList_76 = statistics([df_name_76, df_sent_76, df_word_76, df_ele_76, df_late_76, df_fron_76, df_loops_76])

    for count, rowName in zip(nameRowList, classes.ageGroups):
        ui.progressUpdate("-stdout-",
                             "The age group of "+rowName+" contains "+str(len(count))+" valid entries")
#
    return ([ageList_5,  ageList_6,  ageList_7,  ageList_8,  ageList_9,
             ageList_10, ageList_11, ageList_12, ageList_13, ageList_14,
             ageList_15, ageList_16, ageList_17, ageList_21, ageList_31,
             ageList_41, ageList_51, ageList_61, ageList_71, ageList_76],
            [nameRowList, sentRowList, wordRowList, eleRowList,
             lateRowList, fronRowList, loopsRowList])
#
#******************************************************************************
#

def runSplitGenders():
#
#  split the dataframe in two, one for female and one for male users.
#
    global dfSubList

    genderList = splitGenders(dfSubList)

    numberOfFemales = 0
    for df in genderList[0]:
        numberOfFemales += df.shape[0]
    numberOfMales = 0
    for df in genderList[1]:
        numberOfMales += df.shape[0]
    numberOfUnknown = 0
    for df in genderList[2]:
        numberOfUnknown += df.shape[0]

    ui.progressUpdate('-Pro-', int(9500))

    ui.progressUpdate("-stdout-", "Data split into "+str(numberOfFemales)+" female, "
          +str(numberOfMales)+" male and "+str(numberOfUnknown)+" unknown datasets.")
    return genderList

#
#******************************************************************************
#

def splitGenders(localList):
#
#  Makes it possible to call statistics from everywhere
#
    sorted = localList[0].groupby(localList[0].Gender)
    dfFemaName = get_group(sorted, "w")
    dfMaleName = get_group(sorted, "m")
    dfUnknName = get_group(sorted, "u")

    sorted = localList[1].groupby(localList[1].Gender)
    dfFemaSentence = get_group(sorted, "w")
    dfMaleSentence = get_group(sorted, "m")
    dfUnknSentence = get_group(sorted, "u")

    sorted = localList[2].groupby(localList[2].Gender)
    dfFemaWord = get_group(sorted, "w")
    dfMaleWord = get_group(sorted, "m")
    dfUnknWord = get_group(sorted, "u")

    sorted = localList[3].groupby(localList[3].Gender)
    dfFemaEle = get_group(sorted, "w")
    dfMaleEle = get_group(sorted, "m")
    dfUnknEle = get_group(sorted, "u")

    sorted = localList[4].groupby(localList[4].Gender)
    dfFemaLateral = get_group(sorted, "w")
    dfMaleLateral = get_group(sorted, "m")
    dfUnknLateral = get_group(sorted, "u")

    sorted = localList[5].groupby(localList[5].Gender)
    dfFemaFrontal = get_group(sorted, "w")
    dfMaleFrontal = get_group(sorted, "m")
    dfUnknFrontal = get_group(sorted, "u")

    sorted = localList[6].groupby(localList[6].Gender)
    dfFemaLoops = get_group(sorted, "w")
    dfMaleLoops = get_group(sorted, "m")
    dfUnknLoops = get_group(sorted, "u")
    
    femaList = [dfFemaName, dfFemaSentence, dfFemaWord, dfFemaEle, dfFemaLateral, dfFemaFrontal, dfFemaLoops]
    maleList = [dfMaleName, dfMaleSentence, dfMaleWord, dfMaleEle, dfMaleLateral, dfMaleFrontal, dfMaleLoops]
    unknList = [dfUnknName, dfUnknSentence, dfUnknWord, dfUnknEle, dfUnknLateral, dfUnknFrontal, dfUnknLoops]

    return [femaList, maleList, unknList]

#
#******************************************************************************
#

def runSplitHanded():
#
#  split the dataframe in two, one for right- and one for lefthanded users.
#
    global dfSubList

    handedList = splitHanded(dfSubList)

    numberOfRighthanded = 0
    for df in handedList[0]:
        numberOfRighthanded += df.shape[0]
    numberOfLefthanded = 0
    for df in handedList[1]:
        numberOfLefthanded += df.shape[0]
    numberOfUnknown = 0
    for df in handedList[2]:
        numberOfUnknown += df.shape[0]

    ui.progressUpdate('-Pro-', int(9000))

    ui.progressUpdate("-stdout-", "\nData split into "+str(numberOfRighthanded)+" righthanded, "
          +str(numberOfLefthanded)+" lefthanded and "+str(numberOfUnknown)+" unknown datasets.")
    return handedList

#
#******************************************************************************
#

def splitHanded(localList):
#
#  Makes it possible to call statistics from everywhere
#
    sorted = localList[0].groupby(localList[0].Handed)
    dfRightName = get_group(sorted, "r")
    dfLeftName  = get_group(sorted, "l")
    dfUnknName  = get_group(sorted, "u")

    sorted = localList[1].groupby(localList[1].Handed)
    dfRightSentence = get_group(sorted, "r")
    dfLeftSentence  = get_group(sorted, "l")
    dfUnknSentence  = get_group(sorted, "u")

    sorted = localList[2].groupby(localList[2].Handed)
    dfRightWord = get_group(sorted, "r")
    dfLeftWord  = get_group(sorted, "l")
    dfUnknWord  = get_group(sorted, "u")

    sorted = localList[3].groupby(localList[3].Handed)
    dfRightEle = get_group(sorted, "r")
    dfLeftEle  = get_group(sorted, "l")
    dfUnknEle  = get_group(sorted, "u")

    sorted = localList[4].groupby(localList[4].Handed)
    dfRightLateral = get_group(sorted, "r")
    dfLeftLateral  = get_group(sorted, "l")
    dfUnknLateral  = get_group(sorted, "u")

    sorted = localList[5].groupby(localList[5].Handed)
    dfRightFrontal = get_group(sorted, "r")
    dfLeftFrontal  = get_group(sorted, "l")
    dfUnknFrontal  = get_group(sorted, "u")

    sorted = localList[6].groupby(localList[6].Handed)
    dfRightLoops = get_group(sorted, "r")
    dfLeftLoops  = get_group(sorted, "l")
    dfUnknLoops  = get_group(sorted, "u")
    
    rightList = [dfRightName, dfRightSentence, dfRightWord, dfRightEle, dfRightLateral, dfRightFrontal, dfRightLoops]
    leftList  = [dfLeftName, dfLeftSentence, dfLeftWord, dfLeftEle, dfLeftLateral, dfLeftFrontal, dfLeftLoops]
    unknList  = [dfUnknName, dfUnknSentence, dfUnknWord, dfUnknEle, dfUnknLateral, dfUnknFrontal, dfUnknLoops]

    return [rightList, leftList, unknList]

#
#******************************************************************************
#

def runStatistics():
#
#  Makes it possible to call statistics from everywhere
#
    global dfSubList

    statisticsList = statistics(dfSubList)

    ui.progressUpdate("-stdout-", "\nDone with splitting into exercises"+
                             " and computing statistical parameters.")
    return statisticsList

#
#******************************************************************************
#

def statistics(localList):
#
#  Now comes the justification for using those awkward dataframes!
#
#  Input: List of 6 DataFrames (df_name, df_sent, df_word, df_ele, df_late, df_fron, df_loops)
#
#  Output: List of 48 Parameters-Instances with one value from each of the 7 DataFrames inside.
#
    df_name = localList[0]
    if df_name.empty:
        df_nameWritingTime  = pandas.Series(dtype=object)
        df_nameWritingSpeed = pandas.Series(dtype=object)
        df_nameWritingFreq  = pandas.Series(dtype=object)
        df_nameWritingPress = pandas.Series(dtype=object)
        df_nameGripPressure = pandas.Series(dtype=object)
        df_nameNIVindex     = pandas.Series(dtype=object)
        df_namePenTilt      = pandas.Series(dtype=object)
        print("\ndf_name ist leer")
    else:
        df_nameWritingTime  = checkForNegatives('WritingTime', df_name)
        df_nameWritingSpeed = checkForNegatives('WritingSpeed', df_name)
        df_nameWritingFreq  = checkForNegatives('WritingFrequency', df_name)
        df_nameWritingPress = checkForNegatives('WritingPressure', df_name)
        df_nameGripPressure = checkForNegatives('GripPressureTotal', df_name)
        df_nameNIVindex     = checkForNegatives('AutomationIndex', df_name)
        df_namePenTilt      = checkForNegatives('PenTilt', df_name)

    df_sent = localList[1]
    if df_sent.empty:
        df_sentWritingTime  = pandas.Series(dtype=object)
        df_sentWritingSpeed = pandas.Series(dtype=object)
        df_sentWritingFreq  = pandas.Series(dtype=object)
        df_sentWritingPress = pandas.Series(dtype=object)
        df_sentGripPressure = pandas.Series(dtype=object)
        df_sentNIVindex     = pandas.Series(dtype=object)
        df_sentPenTilt      = pandas.Series(dtype=object)
        print("\ndf_sent ist leer")
    else:
        df_sentWritingTime  = checkForNegatives('WritingTime', df_sent)
        df_sentWritingSpeed = checkForNegatives('WritingSpeed', df_sent)
        df_sentWritingFreq  = checkForNegatives('WritingFrequency', df_sent)
        df_sentWritingPress = checkForNegatives('WritingPressure', df_sent)
        df_sentGripPressure = checkForNegatives('GripPressureTotal', df_sent)
        df_sentNIVindex     = checkForNegatives('AutomationIndex', df_sent)
        df_sentPenTilt      = checkForNegatives('PenTilt', df_sent)

    df_word = localList[2]
    if df_word.empty:
        df_wordWritingTime  = pandas.Series(dtype=object)
        df_wordWritingSpeed = pandas.Series(dtype=object)
        df_wordWritingFreq  = pandas.Series(dtype=object)
        df_wordWritingPress = pandas.Series(dtype=object)
        df_wordGripPressure = pandas.Series(dtype=object)
        df_wordNIVindex     = pandas.Series(dtype=object)
        df_wordPenTilt      = pandas.Series(dtype=object)
        print("\ndf_word ist leer")
    else:
        df_wordWritingTime  = checkForNegatives('WritingTime', df_word)
        df_wordWritingSpeed = checkForNegatives('WritingSpeed', df_word)
        df_wordWritingFreq  = checkForNegatives('WritingFrequency', df_word)
        df_wordWritingPress = checkForNegatives('WritingPressure', df_word)
        df_wordGripPressure = checkForNegatives('GripPressureTotal', df_word)
        df_wordNIVindex     = checkForNegatives('AutomationIndex', df_word)
        df_wordPenTilt      = checkForNegatives('PenTilt', df_word)
        
    df_ele = localList[3]
    if df_ele.empty:
        df_ele_WritingTime  = pandas.Series(dtype=object)
        df_ele_WritingSpeed = pandas.Series(dtype=object)
        df_ele_WritingFreq  = pandas.Series(dtype=object)
        df_ele_WritingPress = pandas.Series(dtype=object)
        df_ele_GripPressure = pandas.Series(dtype=object)
        df_ele_NIVindex     = pandas.Series(dtype=object)
        df_ele_PenTilt      = pandas.Series(dtype=object)
        print("\ndf_ele  ist leer")
    else:
        df_ele_WritingTime  = checkForNegatives('WritingTime', df_ele)
        df_ele_WritingSpeed = checkForNegatives('WritingSpeed', df_ele)
        df_ele_WritingFreq  = checkForNegatives('WritingFrequency', df_ele)
        df_ele_WritingPress = checkForNegatives('WritingPressure', df_ele)
        df_ele_GripPressure = checkForNegatives('GripPressureTotal', df_ele)
        df_ele_NIVindex     = checkForNegatives('AutomationIndex', df_ele)
        df_ele_PenTilt      = checkForNegatives('PenTilt', df_ele)

    df_late = localList[4]
    if df_late.empty:
        df_lateWritingTime  = pandas.Series(dtype=object)
        df_lateWritingSpeed = pandas.Series(dtype=object)
        df_lateWritingFreq  = pandas.Series(dtype=object)
        df_lateWritingPress = pandas.Series(dtype=object)
        df_lateGripPressure = pandas.Series(dtype=object)
        df_lateNIVindex     = pandas.Series(dtype=object)
        df_latePenTilt      = pandas.Series(dtype=object)
        print("\ndf_late ist leer")
    else:
        df_lateWritingTime  = checkForNegatives('WritingTime', df_late)
        df_lateWritingSpeed = checkForNegatives('WritingSpeed', df_late)
        df_lateWritingFreq  = checkForNegatives('WritingFrequency', df_late)
        df_lateWritingPress = checkForNegatives('WritingPressure', df_late)
        df_lateGripPressure = checkForNegatives('GripPressureTotal', df_late)
        df_lateNIVindex     = checkForNegatives('AutomationIndex', df_late)
        df_latePenTilt      = checkForNegatives('PenTilt', df_late)
        
    df_fron = localList[5]
    if df_fron.empty:
        df_fronWritingTime  = pandas.Series(dtype=object)
        df_fronWritingSpeed = pandas.Series(dtype=object)
        df_fronWritingFreq  = pandas.Series(dtype=object)
        df_fronWritingPress = pandas.Series(dtype=object)
        df_fronGripPressure = pandas.Series(dtype=object)
        df_fronNIVindex     = pandas.Series(dtype=object)
        df_fronPenTilt      = pandas.Series(dtype=object)
        print("\ndf_fron ist leer")
    else:
        df_fronWritingTime  = checkForNegatives('WritingTime', df_fron)
        df_fronWritingSpeed = checkForNegatives('WritingSpeed', df_fron)
        df_fronWritingFreq  = checkForNegatives('WritingFrequency', df_fron)
        df_fronWritingPress = checkForNegatives('WritingPressure', df_fron)
        df_fronGripPressure = checkForNegatives('GripPressureTotal', df_fron)
        df_fronNIVindex     = checkForNegatives('AutomationIndex', df_fron)
        df_fronPenTilt      = checkForNegatives('PenTilt', df_fron)

    df_loops = localList[6]
    if df_loops.empty:
        df_loopWritingTime   = pandas.Series(dtype=object)
        df_loopsWritingSpeed = pandas.Series(dtype=object)
        df_loopsWritingFreq  = pandas.Series(dtype=object)
        df_loopsWritingPress = pandas.Series(dtype=object)
        df_loopsGripPressure = pandas.Series(dtype=object)
        df_loopsNIVindex     = pandas.Series(dtype=object)
        df_loopsPenTilt      = pandas.Series(dtype=object)
        print("\ndf_loops ist leer")
    else:
        df_loopWritingTime   = checkForNegatives('WritingTime', df_loops)
        df_loopsWritingSpeed = checkForNegatives('WritingSpeed', df_loops)
        df_loopsWritingFreq  = checkForNegatives('WritingFrequency', df_loops)
        df_loopsWritingPress = checkForNegatives('WritingPressure', df_loops)
        df_loopsGripPressure = checkForNegatives('GripPressureTotal', df_loops)
        df_loopsNIVindex     = checkForNegatives('AutomationIndex', df_loops)
        df_loopsPenTilt      = checkForNegatives('PenTilt', df_loops)
#
#  Now we have series of data, all cleanded up for statistical analysis.
#
    min_time = parameters(-1.0 if len(df_nameWritingTime) == 0 else df_nameWritingTime.min(),
                          -1.0 if len(df_sentWritingTime) == 0 else df_sentWritingTime.min(),
                          -1.0 if len(df_wordWritingTime) == 0 else df_wordWritingTime.min(),
                          -1.0 if len(df_ele_WritingTime) == 0 else df_ele_WritingTime.min(),
                          -1.0 if len(df_lateWritingTime) == 0 else df_lateWritingTime.min(),
                          -1.0 if len(df_fronWritingTime) == 0 else df_fronWritingTime.min(),
                          -1.0 if len(df_loopWritingTime) == 0 else df_loopWritingTime.min())

    min_speed = parameters(-1.0 if len(df_nameWritingSpeed) == 0 else df_nameWritingSpeed.min(),
                           -1.0 if len(df_sentWritingSpeed) == 0 else df_sentWritingSpeed.min(),
                           -1.0 if len(df_wordWritingSpeed) == 0 else df_wordWritingSpeed.min(),
                           -1.0 if len(df_ele_WritingSpeed) == 0 else df_ele_WritingSpeed.min(),
                           -1.0 if len(df_lateWritingSpeed) == 0 else df_lateWritingSpeed.min(),
                           -1.0 if len(df_fronWritingSpeed) == 0 else df_fronWritingSpeed.min(),
                           -1.0 if len(df_loopsWritingSpeed) == 0 else df_loopsWritingSpeed.min())

    min_freq = parameters(-1.0 if len(df_nameWritingFreq) == 0 else df_nameWritingFreq.min(),
                          -1.0 if len(df_sentWritingFreq) == 0 else df_sentWritingFreq.min(),
                          -1.0 if len(df_wordWritingFreq) == 0 else df_wordWritingFreq.min(),
                          -1.0 if len(df_ele_WritingFreq) == 0 else df_ele_WritingFreq.min(),
                          -1.0 if len(df_lateWritingFreq) == 0 else df_lateWritingFreq.min(),
                          -1.0 if len(df_fronWritingFreq) == 0 else df_fronWritingFreq.min(),
                          -1.0 if len(df_loopsWritingFreq) == 0 else df_loopsWritingFreq.min())

    min_force = parameters(-1.0 if len(df_nameWritingPress) == 0 else df_nameWritingPress.min(),
                           -1.0 if len(df_sentWritingPress) == 0 else df_sentWritingPress.min(),
                           -1.0 if len(df_wordWritingPress) == 0 else df_wordWritingPress.min(),
                           -1.0 if len(df_ele_WritingPress) == 0 else df_ele_WritingPress.min(),
                           -1.0 if len(df_lateWritingPress) == 0 else df_lateWritingPress.min(),
                           -1.0 if len(df_fronWritingPress) == 0 else df_fronWritingPress.min(),
                           -1.0 if len(df_loopsWritingPress) == 0 else df_loopsWritingPress.min())
 
    min_grip = parameters(-1.0 if len(df_nameGripPressure) == 0 else df_nameGripPressure.min(),
                          -1.0 if len(df_sentGripPressure) == 0 else df_sentGripPressure.min(),
                          -1.0 if len(df_wordGripPressure) == 0 else df_wordGripPressure.min(),
                          -1.0 if len(df_ele_GripPressure) == 0 else df_ele_GripPressure.min(),
                          -1.0 if len(df_lateGripPressure) == 0 else df_lateGripPressure.min(),
                          -1.0 if len(df_fronGripPressure) == 0 else df_fronGripPressure.min(),
                          -1.0 if len(df_loopsGripPressure) == 0 else df_loopsGripPressure.min())

    min_niv = parameters(-1.0 if len(df_nameNIVindex) == 0 else df_nameNIVindex.min(),
                         -1.0 if len(df_sentNIVindex) == 0 else df_sentNIVindex.min(),
                         -1.0 if len(df_wordNIVindex) == 0 else df_wordNIVindex.min(),
                         -1.0 if len(df_ele_NIVindex) == 0 else df_ele_NIVindex.min(),
                         -1.0 if len(df_lateNIVindex) == 0 else df_lateNIVindex.min(),
                         -1.0 if len(df_fronNIVindex) == 0 else df_fronNIVindex.min(),
                         -1.0 if len(df_loopsNIVindex) == 0 else df_loopsNIVindex.min())

    min_tilt = parameters(-1.0 if len(df_namePenTilt) == 0 else df_namePenTilt.min(),
                          -1.0 if len(df_sentPenTilt) == 0 else df_sentPenTilt.min(),
                          -1.0 if len(df_wordPenTilt) == 0 else df_wordPenTilt.min(),
                          -1.0 if len(df_ele_PenTilt) == 0 else df_ele_PenTilt.min(),
                          -1.0 if len(df_latePenTilt) == 0 else df_latePenTilt.min(),
                          -1.0 if len(df_fronPenTilt) == 0 else df_fronPenTilt.min(),
                          -1.0 if len(df_loopsPenTilt) == 0 else df_loopsPenTilt.min())
#
#  Next round for the maximum
#
    max_time = parameters(-1.0 if len(df_nameWritingTime) == 0 else df_nameWritingTime.max(),
                          -1.0 if len(df_sentWritingTime) == 0 else df_sentWritingTime.max(),
                          -1.0 if len(df_wordWritingTime) == 0 else df_wordWritingTime.max(),
                          -1.0 if len(df_ele_WritingTime) == 0 else df_ele_WritingTime.max(),
                          -1.0 if len(df_lateWritingTime) == 0 else df_lateWritingTime.max(),
                          -1.0 if len(df_fronWritingTime) == 0 else df_fronWritingTime.max(),
                          -1.0 if len(df_loopWritingTime) == 0 else df_loopWritingTime.max())

    max_speed = parameters(-1.0 if len(df_nameWritingSpeed) == 0 else df_nameWritingSpeed.max(),
                           -1.0 if len(df_sentWritingSpeed) == 0 else df_sentWritingSpeed.max(),
                           -1.0 if len(df_wordWritingSpeed) == 0 else df_wordWritingSpeed.max(),
                           -1.0 if len(df_ele_WritingSpeed) == 0 else df_ele_WritingSpeed.max(),
                           -1.0 if len(df_lateWritingSpeed) == 0 else df_lateWritingSpeed.max(),
                           -1.0 if len(df_fronWritingSpeed) == 0 else df_fronWritingSpeed.max(),
                           -1.0 if len(df_loopsWritingSpeed) == 0 else df_loopsWritingSpeed.max())

    max_freq = parameters(-1.0 if len(df_nameWritingFreq) == 0 else df_nameWritingFreq.max(),
                          -1.0 if len(df_sentWritingFreq) == 0 else df_sentWritingFreq.max(),
                          -1.0 if len(df_wordWritingFreq) == 0 else df_wordWritingFreq.max(),
                          -1.0 if len(df_ele_WritingFreq) == 0 else df_ele_WritingFreq.max(),
                          -1.0 if len(df_lateWritingFreq) == 0 else df_lateWritingFreq.max(),
                          -1.0 if len(df_fronWritingFreq) == 0 else df_fronWritingFreq.max(),
                          -1.0 if len(df_loopsWritingFreq) == 0 else df_loopsWritingFreq.max())

    max_force = parameters(-1.0 if len(df_nameWritingPress) == 0 else df_nameWritingPress.max(),
                           -1.0 if len(df_sentWritingPress) == 0 else df_sentWritingPress.max(),
                           -1.0 if len(df_wordWritingPress) == 0 else df_wordWritingPress.max(),
                           -1.0 if len(df_ele_WritingPress) == 0 else df_ele_WritingPress.max(),
                           -1.0 if len(df_lateWritingPress) == 0 else df_lateWritingPress.max(),
                           -1.0 if len(df_fronWritingPress) == 0 else df_fronWritingPress.max(),
                           -1.0 if len(df_loopsWritingPress) == 0 else df_loopsWritingPress.max())
 
    max_grip = parameters(-1.0 if len(df_nameGripPressure) == 0 else df_nameGripPressure.max(),
                          -1.0 if len(df_sentGripPressure) == 0 else df_sentGripPressure.max(),
                          -1.0 if len(df_wordGripPressure) == 0 else df_wordGripPressure.max(),
                          -1.0 if len(df_ele_GripPressure) == 0 else df_ele_GripPressure.max(),
                          -1.0 if len(df_lateGripPressure) == 0 else df_lateGripPressure.max(),
                          -1.0 if len(df_fronGripPressure) == 0 else df_fronGripPressure.max(),
                          -1.0 if len(df_loopsGripPressure) == 0 else df_loopsGripPressure.max())

    max_niv = parameters(-1.0 if len(df_nameNIVindex) == 0 else df_nameNIVindex.max(),
                         -1.0 if len(df_sentNIVindex) == 0 else df_sentNIVindex.max(),
                         -1.0 if len(df_wordNIVindex) == 0 else df_wordNIVindex.max(),
                         -1.0 if len(df_ele_NIVindex) == 0 else df_ele_NIVindex.max(),
                         -1.0 if len(df_lateNIVindex) == 0 else df_lateNIVindex.max(),
                         -1.0 if len(df_fronNIVindex) == 0 else df_fronNIVindex.max(),
                         -1.0 if len(df_loopsNIVindex) == 0 else df_loopsNIVindex.max())

    max_tilt = parameters(-1.0 if len(df_namePenTilt) == 0 else df_namePenTilt.max(),
                          -1.0 if len(df_sentPenTilt) == 0 else df_sentPenTilt.max(),
                          -1.0 if len(df_wordPenTilt) == 0 else df_wordPenTilt.max(),
                          -1.0 if len(df_ele_PenTilt) == 0 else df_ele_PenTilt.max(),
                          -1.0 if len(df_latePenTilt) == 0 else df_latePenTilt.max(),
                          -1.0 if len(df_fronPenTilt) == 0 else df_fronPenTilt.max(),
                          -1.0 if len(df_loopsPenTilt) == 0 else df_loopsPenTilt.max())
#
#  Next round for the mean
#
    mean_time = parameters(-1.0 if len(df_nameWritingTime) == 0 else df_nameWritingTime.mean(),
                           -1.0 if len(df_sentWritingTime) == 0 else df_sentWritingTime.mean(),
                           -1.0 if len(df_wordWritingTime) == 0 else df_wordWritingTime.mean(),
                           -1.0 if len(df_ele_WritingTime) == 0 else df_ele_WritingTime.mean(),
                           -1.0 if len(df_lateWritingTime) == 0 else df_lateWritingTime.mean(),
                           -1.0 if len(df_fronWritingTime) == 0 else df_fronWritingTime.mean(),
                           -1.0 if len(df_loopWritingTime) == 0 else df_loopWritingTime.mean())

    mean_speed = parameters(-1.0 if len(df_nameWritingSpeed) == 0 else df_nameWritingSpeed.mean(),
                            -1.0 if len(df_sentWritingSpeed) == 0 else df_sentWritingSpeed.mean(),
                            -1.0 if len(df_wordWritingSpeed) == 0 else df_wordWritingSpeed.mean(),
                            -1.0 if len(df_ele_WritingSpeed) == 0 else df_ele_WritingSpeed.mean(),
                            -1.0 if len(df_lateWritingSpeed) == 0 else df_lateWritingSpeed.mean(),
                            -1.0 if len(df_fronWritingSpeed) == 0 else df_fronWritingSpeed.mean(),
                            -1.0 if len(df_loopsWritingSpeed) == 0 else df_loopsWritingSpeed.mean())

    mean_freq = parameters(-1.0 if len(df_nameWritingFreq) == 0 else df_nameWritingFreq.mean(),
                           -1.0 if len(df_sentWritingFreq) == 0 else df_sentWritingFreq.mean(),
                           -1.0 if len(df_wordWritingFreq) == 0 else df_wordWritingFreq.mean(),
                           -1.0 if len(df_ele_WritingFreq) == 0 else df_ele_WritingFreq.mean(),
                           -1.0 if len(df_lateWritingFreq) == 0 else df_lateWritingFreq.mean(),
                           -1.0 if len(df_fronWritingFreq) == 0 else df_fronWritingFreq.mean(),
                           -1.0 if len(df_loopsWritingFreq) == 0 else df_loopsWritingFreq.mean())

    mean_force = parameters(-1.0 if len(df_nameWritingPress) == 0 else df_nameWritingPress.mean(),
                            -1.0 if len(df_sentWritingPress) == 0 else df_sentWritingPress.mean(),
                            -1.0 if len(df_wordWritingPress) == 0 else df_wordWritingPress.mean(),
                            -1.0 if len(df_ele_WritingPress) == 0 else df_ele_WritingPress.mean(),
                            -1.0 if len(df_lateWritingPress) == 0 else df_lateWritingPress.mean(),
                            -1.0 if len(df_fronWritingPress) == 0 else df_fronWritingPress.mean(),
                            -1.0 if len(df_loopsWritingPress) == 0 else df_loopsWritingPress.mean())
 
    mean_grip = parameters(-1.0 if len(df_nameGripPressure) == 0 else df_nameGripPressure.mean(),
                           -1.0 if len(df_sentGripPressure) == 0 else df_sentGripPressure.mean(),
                           -1.0 if len(df_wordGripPressure) == 0 else df_wordGripPressure.mean(),
                           -1.0 if len(df_ele_GripPressure) == 0 else df_ele_GripPressure.mean(),
                           -1.0 if len(df_lateGripPressure) == 0 else df_lateGripPressure.mean(),
                           -1.0 if len(df_fronGripPressure) == 0 else df_fronGripPressure.mean(),
                           -1.0 if len(df_loopsGripPressure) == 0 else df_loopsGripPressure.mean())

    mean_niv = parameters(-1.0 if len(df_nameNIVindex) == 0 else df_nameNIVindex.mean(),
                          -1.0 if len(df_sentNIVindex) == 0 else df_sentNIVindex.mean(),
                          -1.0 if len(df_wordNIVindex) == 0 else df_wordNIVindex.mean(),
                          -1.0 if len(df_ele_NIVindex) == 0 else df_ele_NIVindex.mean(),
                          -1.0 if len(df_lateNIVindex) == 0 else df_lateNIVindex.mean(),
                          -1.0 if len(df_fronNIVindex) == 0 else df_fronNIVindex.mean(),
                          -1.0 if len(df_loopsNIVindex) == 0 else df_loopsNIVindex.mean())

    mean_tilt = parameters(-1.0 if len(df_namePenTilt) == 0 else df_namePenTilt.mean(),
                           -1.0 if len(df_sentPenTilt) == 0 else df_sentPenTilt.mean(),
                           -1.0 if len(df_wordPenTilt) == 0 else df_wordPenTilt.mean(),
                           -1.0 if len(df_ele_PenTilt) == 0 else df_ele_PenTilt.mean(),
                           -1.0 if len(df_latePenTilt) == 0 else df_latePenTilt.mean(),
                           -1.0 if len(df_fronPenTilt) == 0 else df_fronPenTilt.mean(),
                           -1.0 if len(df_loopsPenTilt) == 0 else df_loopsPenTilt.mean())
#
#  Next round for the quartiles
#
    nameTimeQuant = df_nameWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameSpeeQuant = df_nameWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameFreqQuant = df_nameWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameForceQuant = df_nameWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameGripQuant = df_nameGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameNIVQuant  = df_nameNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameTiltQuant = df_namePenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    nameTimeQuant.fillna(value = -1.0, inplace = True)
    nameSpeeQuant.fillna(value = -1.0, inplace = True)
    nameFreqQuant.fillna(value = -1.0, inplace = True)
    nameForceQuant.fillna(value = -1.0, inplace = True)
    nameGripQuant.fillna(value = -1.0, inplace = True)
    nameNIVQuant.fillna(value = -1.0, inplace = True)
    nameTiltQuant.fillna(value = -1.0, inplace = True)

    sentTimeQuant = df_sentWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentSpeeQuant = df_sentWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentFreqQuant = df_sentWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentForceQuant = df_sentWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentGripQuant = df_sentGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentNIVQuant  = df_sentNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentTiltQuant = df_sentPenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    sentTimeQuant.fillna(value = -1.0, inplace = True)
    sentSpeeQuant.fillna(value = -1.0, inplace = True)
    sentFreqQuant.fillna(value = -1.0, inplace = True)
    sentForceQuant.fillna(value = -1.0, inplace = True)
    sentGripQuant.fillna(value = -1.0, inplace = True)
    sentNIVQuant.fillna(value  = -1.0, inplace = True)
    sentTiltQuant.fillna(value = -1.0, inplace = True)

    wordTimeQuant = df_wordWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordSpeeQuant = df_wordWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordFreqQuant = df_wordWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordForceQuant = df_wordWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordGripQuant = df_wordGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordNIVQuant  = df_wordNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordTiltQuant = df_wordPenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    wordTimeQuant.fillna(value = -1.0, inplace = True)
    wordSpeeQuant.fillna(value = -1.0, inplace = True)
    wordFreqQuant.fillna(value = -1.0, inplace = True)
    wordForceQuant.fillna(value = -1.0, inplace = True)
    wordGripQuant.fillna(value = -1.0, inplace = True)
    wordNIVQuant.fillna(value  = -1.0, inplace = True)
    wordTiltQuant.fillna(value = -1.0, inplace = True)

    ele_TimeQuant = df_ele_WritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_SpeeQuant = df_ele_WritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_FreqQuant = df_ele_WritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_ForceQuant = df_ele_WritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_GripQuant = df_ele_GripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_NIVQuant  = df_ele_NIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_TiltQuant = df_ele_PenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    ele_TimeQuant.fillna(value = -1.0, inplace = True)
    ele_SpeeQuant.fillna(value = -1.0, inplace = True)
    ele_FreqQuant.fillna(value = -1.0, inplace = True)
    ele_ForceQuant.fillna(value = -1.0, inplace = True)
    ele_GripQuant.fillna(value = -1.0, inplace = True)
    ele_NIVQuant.fillna(value = -1.0, inplace = True)
    ele_TiltQuant.fillna(value = -1.0, inplace = True)

    lateTimeQuant = df_lateWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateSpeeQuant = df_lateWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateFreqQuant = df_lateWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateForceQuant = df_lateWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateGripQuant = df_lateGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateNIVQuant  = df_lateNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateTiltQuant = df_latePenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    lateTimeQuant.fillna(value = -1.0, inplace = True)
    lateSpeeQuant.fillna(value = -1.0, inplace = True)
    lateFreqQuant.fillna(value = -1.0, inplace = True)
    lateForceQuant.fillna(value = -1.0, inplace = True)
    lateGripQuant.fillna(value = -1.0, inplace = True)
    lateNIVQuant.fillna(value = -1.0, inplace = True)
    lateTiltQuant.fillna(value = -1.0, inplace = True)

    fronTimeQuant = df_fronWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronSpeeQuant = df_fronWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronFreqQuant = df_fronWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronForceQuant = df_fronWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronGripQuant = df_fronGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronNIV_Quant = df_fronNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronTiltQuant = df_fronPenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    fronTimeQuant.fillna(value = -1.0, inplace = True)
    fronSpeeQuant.fillna(value = -1.0, inplace = True)
    fronFreqQuant.fillna(value = -1.0, inplace = True)
    fronForceQuant.fillna(value = -1.0, inplace = True)
    fronGripQuant.fillna(value = -1.0, inplace = True)
    fronNIV_Quant.fillna(value = -1.0, inplace = True)
    fronTiltQuant.fillna(value = -1.0, inplace = True)

    loopsTimeQuant = df_loopWritingTime.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsSpeeQuant = df_loopsWritingSpeed.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsFreqQuant = df_loopsWritingFreq.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsForceQuant = df_loopsWritingPress.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsGripQuant = df_loopsGripPressure.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsNIVQuant  = df_loopsNIVindex.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsTiltQuant = df_loopsPenTilt.quantile(q=[0.25, 0.5, 0.75], interpolation='linear').astype(float)
    loopsTimeQuant.fillna(value = -1.0, inplace = True)
    loopsSpeeQuant.fillna(value = -1.0, inplace = True)
    loopsFreqQuant.fillna(value = -1.0, inplace = True)
    loopsForceQuant.fillna(value = -1.0, inplace = True)
    loopsGripQuant.fillna(value = -1.0, inplace = True)
    loopsNIVQuant.fillna(value  = -1.0, inplace = True)
    loopsTiltQuant.fillna(value = -1.0, inplace = True)
#
    quart1_time = parameters(nameTimeQuant.get(key = 0.25), sentTimeQuant.get(key = 0.25),
                             wordTimeQuant.get(key = 0.25), ele_TimeQuant.get(key = 0.25),
                             lateTimeQuant.get(key = 0.25), fronTimeQuant.get(key = 0.25),
                             loopsTimeQuant.get(key = 0.25))
    median_time = parameters(nameTimeQuant.get(key = 0.5), sentTimeQuant.get(key = 0.5),
                             wordTimeQuant.get(key = 0.5), ele_TimeQuant.get(key = 0.5),
                             lateTimeQuant.get(key = 0.5), fronTimeQuant.get(key = 0.5),
                             loopsTimeQuant.get(key = 0.5))
    quart3_time = parameters(nameTimeQuant.get(key = 0.75), sentTimeQuant.get(key = 0.75),
                             wordTimeQuant.get(key = 0.75), ele_TimeQuant.get(key = 0.75),
                             lateTimeQuant.get(key = 0.75), fronTimeQuant.get(key = 0.75),
                             loopsTimeQuant.get(key = 0.75))

    quart1_speed = parameters(nameSpeeQuant.get(key = 0.25), sentSpeeQuant.get(key = 0.25),
                              wordSpeeQuant.get(key = 0.25), ele_SpeeQuant.get(key = 0.25),
                              lateSpeeQuant.get(key = 0.25), fronSpeeQuant.get(key = 0.25),
                              loopsSpeeQuant.get(key = 0.25))
    median_speed = parameters(nameSpeeQuant.get(key = 0.5), sentSpeeQuant.get(key = 0.5),
                              wordSpeeQuant.get(key = 0.5), ele_SpeeQuant.get(key = 0.5),
                              lateSpeeQuant.get(key = 0.5), fronSpeeQuant.get(key = 0.5),
                              loopsSpeeQuant.get(key = 0.5))
    quart3_speed = parameters(nameSpeeQuant.get(key = 0.75), sentSpeeQuant.get(key = 0.75),
                              wordSpeeQuant.get(key = 0.75), ele_SpeeQuant.get(key = 0.75),
                              lateSpeeQuant.get(key = 0.75), fronSpeeQuant.get(key = 0.75),
                              loopsSpeeQuant.get(key = 0.75))

    quart1_freq = parameters(nameFreqQuant.get(key = 0.25), sentFreqQuant.get(key = 0.25),
                             wordFreqQuant.get(key = 0.25), ele_FreqQuant.get(key = 0.25),
                             lateFreqQuant.get(key = 0.25), fronFreqQuant.get(key = 0.25),
                             loopsFreqQuant.get(key = 0.25))
    median_freq = parameters(nameFreqQuant.get(key = 0.5), sentFreqQuant.get(key = 0.5),
                             wordFreqQuant.get(key = 0.5), ele_FreqQuant.get(key = 0.5),
                             lateFreqQuant.get(key = 0.5), fronFreqQuant.get(key = 0.5),
                             loopsFreqQuant.get(key = 0.5))
    quart3_freq = parameters(nameFreqQuant.get(key = 0.75), sentFreqQuant.get(key = 0.75),
                             wordFreqQuant.get(key = 0.75), ele_FreqQuant.get(key = 0.75),
                             lateFreqQuant.get(key = 0.75), fronFreqQuant.get(key = 0.75),
                             loopsFreqQuant.get(key = 0.75))

#    print("\nQuartile", quart1_freq)
#    print("        ", median_freq)
#    print("        ", quart3_freq)

    quart1_force = parameters(nameForceQuant.get(key = 0.25), sentForceQuant.get(key = 0.25),
                              wordForceQuant.get(key = 0.25), ele_ForceQuant.get(key = 0.25),
                              lateForceQuant.get(key = 0.25), fronForceQuant.get(key = 0.25),
                              loopsForceQuant.get(key = 0.25))
    median_force = parameters(nameForceQuant.get(key = 0.5), sentForceQuant.get(key = 0.5),
                              wordForceQuant.get(key = 0.5), ele_ForceQuant.get(key = 0.5),
                              lateForceQuant.get(key = 0.5), fronForceQuant.get(key = 0.5),
                              loopsForceQuant.get(key = 0.5))
    quart3_force = parameters(nameForceQuant.get(key = 0.75), sentForceQuant.get(key = 0.75),
                              wordForceQuant.get(key = 0.75), ele_ForceQuant.get(key = 0.75),
                              lateForceQuant.get(key = 0.75), fronForceQuant.get(key = 0.75),
                              loopsForceQuant.get(key = 0.75))

    quart1_grip = parameters(nameGripQuant.get(key = 0.25), sentGripQuant.get(key = 0.25),
                             wordGripQuant.get(key = 0.25), ele_GripQuant.get(key = 0.25),
                             lateGripQuant.get(key = 0.25), fronGripQuant.get(key = 0.25),
                             loopsGripQuant.get(key = 0.25))
    median_grip = parameters(nameGripQuant.get(key = 0.5), sentGripQuant.get(key = 0.5),
                             wordGripQuant.get(key = 0.5), ele_GripQuant.get(key = 0.5),
                             lateGripQuant.get(key = 0.5), fronGripQuant.get(key = 0.5),
                             loopsGripQuant.get(key = 0.5))
    quart3_grip = parameters(nameGripQuant.get(key = 0.75), sentGripQuant.get(key = 0.75),
                             wordGripQuant.get(key = 0.75), ele_GripQuant.get(key = 0.75),
                             lateGripQuant.get(key = 0.75), fronGripQuant.get(key = 0.75),
                             loopsGripQuant.get(key = 0.75))

    quart1_niv = parameters(nameNIVQuant.get(key = 0.25), sentNIVQuant.get(key = 0.25),
                            wordNIVQuant.get(key = 0.25), ele_NIVQuant.get(key = 0.25),
                            lateNIVQuant.get(key = 0.25), fronNIV_Quant.get(key = 0.25),
                            loopsNIVQuant.get(key = 0.25))
    median_niv = parameters(nameNIVQuant.get(key = 0.5), sentNIVQuant.get(key = 0.5),
                            wordNIVQuant.get(key = 0.5), ele_NIVQuant.get(key = 0.5),
                            lateNIVQuant.get(key = 0.5), fronNIV_Quant.get(key = 0.5),
                            loopsNIVQuant.get(key = 0.5))
    quart3_niv = parameters(nameNIVQuant.get(key = 0.75), sentNIVQuant.get(key = 0.75),
                            wordNIVQuant.get(key = 0.75), ele_NIVQuant.get(key = 0.75),
                            lateNIVQuant.get(key = 0.75), fronNIV_Quant.get(key = 0.75),
                            loopsNIVQuant.get(key = 0.75))

    quart1_tilt = parameters(nameTiltQuant.get(key = 0.25), sentTiltQuant.get(key = 0.25),
                             wordTiltQuant.get(key = 0.25), ele_TiltQuant.get(key = 0.25),
                             lateTiltQuant.get(key = 0.25), fronTiltQuant.get(key = 0.25),
                             loopsTiltQuant.get(key = 0.25))
    median_tilt = parameters(nameTiltQuant.get(key = 0.5), sentTiltQuant.get(key = 0.5),
                             wordTiltQuant.get(key = 0.5), ele_TiltQuant.get(key = 0.5),
                             lateTiltQuant.get(key = 0.5), fronTiltQuant.get(key = 0.5),
                             loopsTiltQuant.get(key = 0.5))
    quart3_tilt = parameters(nameTiltQuant.get(key = 0.75), sentTiltQuant.get(key = 0.75),
                             wordTiltQuant.get(key = 0.75), ele_TiltQuant.get(key = 0.75),
                             lateTiltQuant.get(key = 0.75), fronTiltQuant.get(key = 0.75),
                             loopsTiltQuant.get(key = 0.75))
#
#  Now create a list of Parameters-Instances with statistical results.
#
    return([min_time, max_time, mean_time, quart1_time, median_time, quart3_time,
            min_speed, max_speed, mean_speed, quart1_speed, median_speed, quart3_speed,
            min_freq, max_freq, mean_freq, quart1_freq, median_freq, quart3_freq,
            min_force, max_force, mean_force, quart1_force, median_force, quart3_force,
            min_grip, max_grip, mean_grip, quart1_grip, median_grip, quart3_grip,
            min_niv,  max_niv,  mean_niv,  quart1_niv,  median_niv,  quart3_niv,
            min_tilt, max_tilt, mean_tilt, quart1_tilt, median_tilt, quart3_tilt])

#
#******************************************************************************
#

def checkForNegatives(col, df) -> pandas.Series:
#
#  Eliminate impossible entries in a DataFrame.
#
    if not df.empty:
        if col in df:
            df_clean = pandas.Series(df[col])
            minValue = df_clean.min()
            while minValue <= 0.0:
                minIndex = df_clean.idxmin()
                df_clean.drop(minIndex, inplace=True)
                minValue = df_clean.min()
            return df_clean
        else:
            return pandas.Series(dtype=object)
    else:
        return pandas.Series(dtype=object)

#
#******************************************************************************
#

def checkForNumeric(entry) -> bool:
    
    if isinstance(entry, np.integer) or isinstance(entry, float):
        return True
    else:
        return False
