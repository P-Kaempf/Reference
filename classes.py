from dataclasses import dataclass
import pandas as pd
from datetime import date
#
@dataclass
class parameters:
    Name: float
    TestSentence: float
    TestWord: float
    TestEle: float
#    TestAna: float
    HatchLateral: float
    HatchFrontal: float
    Loops: float
#    GarlandsUUU: float
#    GarlandsNNN: float
    
eduPenData:bool = True

relevantColumns = ["Label", "IsValidData", "WritingTime", "WritingSpeed", "WritingFrequency",
                   "WritingPressure", "GripPressureTotal", "AutomationIndex", "PenTilt", "Form"]
measuredData = ["Time", "Speed", "Frequency", "Pressure", "GripPressure", "AutomationIndex", "PenTilt"]
relevantRows = ["Name", "TestSentence", "TestWord", "TestEle", "HatchLateral", "HatchFrontal", "Loops"]
ageGroups = [" 5.0 to  6.0 years"," 6.0 to  7.0 years"," 7.0 to  8.0 years"," 8.0 to  9.0 years",
             " 9.0 to 10.0 years", "10.0 to 11.0 years", "11.0 to 12.0 years", "11.5 to 13.0 years",
             "13.0 to 14.0 years", "14.0 to 15.0 years", "15.0 to 16.0 years", "16.0 to 17.0 years",
             "17.0 to 21.0 years", "21.0 to 30.0 years", "31.0 to 40.0 years", "41.0 to 50.0 years",
             "51.0 to 60.0 years", "61.0 to 70.0 years", "71.0 to 76.0 years", "76.0 to 80.0 years"]
ageValues = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 25, 35, 45, 55, 65, 75, 78]
ageStarts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 31, 41, 51, 61, 71, 76]

def makeDFfrom(folder, file):
#
#  Reads the metadata from the folder name and the results from the file and puts them in a Dataframe
#
    global actualColumns

    metalist = folder.split("_")
    handed = str(metalist[-1])
    gender = str(metalist[-2])
    if gender == "f":
        gender = "w"
#
#  The birthday is the third item from the end and in itself delineated by simple dashes.
#
    birthday = metalist[-3].split("-")
    if len(birthday) == 3:
        yearOfBirth  = int(birthday[0])
        monthOfBirth = int(birthday[1])
        dayOfBirth   = int(birthday[2])
    elif len(birthday) == 2:
        yearOfBirth  = int(birthday[0])
        monthOfBirth = int(birthday[1])
        dayOfBirth   = 15           # 15 is the mid of the month
    else:
        yearOfBirth  = int(birthday[0])
        monthOfBirth = 6
        dayOfBirth   = 30           # 6-30 is the mid of the year
    birthdate = date(yearOfBirth, monthOfBirth, dayOfBirth)
#
#  Date of test is at the start of the foldername. It could be ahead or after the name - so much for consistency.
#
    testdate = date(1903, 1, 1)
    for element in metalist:
        if element.isdigit() & (len(element) == 8):
            yearOfTest  = int(element[0:4])
            monthOfTest = int(element[4:6])
            dayOfTest   = int(element[6:8])
            testdate = date(yearOfTest, monthOfTest, dayOfTest)
            break
    if testdate != date(1903, 1, 1):
        age = testdate - birthdate
    else:
        age = -365.24
    
    df = pd.read_csv(file, sep=";", header=0, index_col=False)
    actualColumns = []
    for columnTitle in relevantColumns:
        if columnTitle in df.columns:
            actualColumns.append(columnTitle)
    df = df[actualColumns]
#
    df['Age'] = float(age.days) / 365.24        # with the non-leap-year in 2000, this is the
                                                #  most precise way to convert days into years.
    df['Handed'] = handed
    df['Gender'] = gender

    return df
