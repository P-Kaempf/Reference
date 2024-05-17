# This is a Python script.
import os.path
import shutil
import PySimpleGUI as sg
import platform
import traceback
import file
import data
import plot
import classes

sg.theme('SystemDefault1')

if "Darwin" in platform.uname():
    defaultFont      = ("Lucida Grande", 14)
    defaultFontLarge = ("Lucida Grande", 18)
    defaultFontSmall = ("Lucida Grande", 12)
    sg.set_options(font=defaultFont, use_ttk_buttons=True, ttk_theme='aqua',
                   background_color='grey95',
                   element_background_color='grey95',
                   text_element_background_color='grey95',
                   input_elements_background_color='white',
                   scrollbar_color='white',
                   input_text_color='black',
                   text_color='black',
                   element_text_color='black')
elif "Linux" in platform.uname():
    defaultFont      = ("Bitstream Charter", 14)
    defaultFontLarge = ("Bitstream Charter", 18)
    defaultFontSmall = ("Bitstream Charter", 12)
    sg.set_options(font=defaultFont, use_ttk_buttons=True, ttk_theme='clearlooks',
                   background_color='grey95',
                   element_background_color='grey95',
                   text_element_background_color='grey95',
                   input_elements_background_color='white',
                   scrollbar_color='white',
                   input_text_color='black',
                   text_color='black',
                   element_text_color='black')
elif "Windows" in platform.uname():
    defaultFont      = ("Calibri", 10)
    defaultFontLarge = ("Calibri", 12)
    defaultFontSmall = ("Calibri", 9)
    sg.set_options(font=defaultFont, use_ttk_buttons=True, ttk_theme='winnative',
                   dpi_awareness=True, border_width=8, element_padding=(5, 5),
                   background_color='grey95',
                   element_background_color='grey95',
                   text_element_background_color='grey95',
                   input_elements_background_color='white',
                   scrollbar_color='white',
                   input_text_color='black',
                   text_color='black',
                   element_text_color='black')

#
# *************************************************************************************
#

def get_scaling():
# called before window created
    root = sg.tk.Tk()
    scaling = root.winfo_fpixels('1i')/144
    root.destroy()
    return scaling

#
# *************************************************************************************
#

def askStartingDirectory() -> str:
#
#  Displays a file dialog and expects to read the top directory of the recordings
#
    try:
        path: str = sg.popup_get_folder('Select root directory', title='Select root directory', no_window=True)
        if path == None:
            path = ""
        return path

    except Exception as e:
        tb = traceback.format_exc()
        sg.Print(f'Something went wrong. Here is the error message:', e, tb)
        sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb, font=defaultFont)
        return ""

#
# *************************************************************************************
#

def makeDefaultFolder(targetPath):
    
    try:
        os.mkdir(targetPath)
    except FileExistsError:
        fileList = os.listdir(targetPath)
        print("Number of files to be deleted: ", len(fileList))
        if len(fileList) > 0:
            layout  = [[sg.Text("The content of the existing folder will be overwritten", pad=(4, 10))],
                       [sg.Button("Don't do it!", size=(10,1), pad=(12, 10), key='-Cancel-'), sg.Push(),
                        sg.Button('OK', size=(10,1), pad=(12, 10), key='-OK-')]]
            warning = sg.Window('Warning', layout)
            event, values = warning.read()
            if event == '-Cancel-':
                targetPath = ""
            else:
                for file in fileList:
                    fullName = os.path.join(targetPath, file)
                    if os.path.isdir(fullName):
                        shutil.rmtree(fullName)
                    else:
                        os.remove(fullName)
            warning.close()
    return targetPath

#
# *************************************************************************************
#

def progressUpdate(key, action):
    
    global window
    
    if key == "-stdout-":
        window[key].print(str(action))
    elif key == '-Pro-':
        window[key].update(current_count=int(action))

#
# *************************************************************************************
#
def start():
#
#  Runs first and contains the event loop
#
#  Open one window with all UI elements
#
    global window
    global df_Stats

    statisticsList = []
    ageList    = []
    handedList = []
    genderList = []
#
#  Get scaling for consistency with Matplotlib.
#  Find the number in original screen when GUI designed.
#
    my_width, my_height = 1160, 642     #  call sg.Window.get_screen_size()
    scaling_old = get_scaling()         #  Get the number for new screen
    width, height = sg.Window.get_screen_size()
    scaling = 0.75 * scaling_old * min(width / my_width, height / my_height)
#
#  Definition of UI elements
#
    layout = [[sg.Frame(title="", layout=[
                [sg.Frame(title="List of Directories", font=defaultFontLarge, layout=[
                   [sg.Tree(data=sg.TreeData(), headings=[" Size "], auto_size_columns=True, num_rows=24, col0_width=32,
                            select_mode=sg.TABLE_SELECT_MODE_EXTENDED, key='_TREE_', enable_events=True, show_expanded=False,
                            expand_x=True, expand_y=True)]])]]),
            sg.Frame(title="", layout=[
                [sg.Radio("EduPen data",  group_id=1, default=True,  key="-edu-", size=(16, 1), pad=(18, 8),
                          enable_events=True, font=defaultFont),
                 sg.Radio("ErgoPen data", group_id=1, default=False, key="-ergo-", size=(16, 1), pad=(18, 8),
                          enable_events=True, font=defaultFont),
                 sg.Button(button_text="Read pickled data", key='-read-', size=(15, 1), pad=(12, 10))],
                [sg.Frame(title="Root Directory", font=defaultFontLarge, layout=[
                    [sg.InputText(" ", size=(60,1), key='-root-', pad=(12, 5))],
                    [sg.Button(button_text="Open root directory", key='-rootFolder-', size=(18, 1), pad=(18, 8))]])],
                [sg.Button(button_text="Compute", key='-Rechnen-', size=(9, 1), pad=(12, 10), disabled=True),
                 sg.ProgressBar(max_value=10000, orientation="horizontal", key='-Pro-', pad=(12, 10), expand_x=True,
                                expand_y=True)],
                [sg.Frame(title="Target Directory", font=defaultFontLarge, layout=[
                    [sg.InputText(" ", size=(60,1), key='-target-', pad=(12, 5))],
                    [sg.Button(button_text="Create in parallel", key='-parallel-', size=(18, 1), pad=(12, 8), disabled=True),
                     sg.Button(button_text="Enter new directory", key='-newFolder-', size=(18, 1), pad=(18, 8), disabled=True)]])],
                  [sg.Multiline(size=(32,12), background_color='white', key="-stdout-", font=defaultFontSmall,
                             expand_x=True, expand_y=True, auto_refresh=True, write_only=True, pad=(12,8))],
                  [sg.HorizontalSeparator(pad=(10, 10))],
                  [sg.Text(text="Exercise", size=(8, 1), pad=((24, 2), (10, 10))),
                   sg.Combo(values=classes.relevantRows, default_value="TestSentence", key='-parm-',
                            size=(12, 1), auto_size_text=False, pad=(0, 10)),
                   sg.Button(button_text="Plot", enable_events=True, key='-plot-', size=(8, 1), disabled=True),
                   sg.Push(), sg.Push(),
                   sg.Button(button_text="Quit", key='-OK-', size=(8, 1), pad=(24, 10))]])]]
    window = sg.Window('Digipen Reference Data Tool', layout, resizable=True, alpha_channel=1.0, no_titlebar=False,
                       scaling=scaling, return_keyboard_events=True)
    window.Finalize()
#
#  * * *  Eventloop  * * *
#
    while True:
        event, values = window.read()
#        print(event, values)

        if event == '-OK-':
            window.close()
            return

        elif event == sg.WIN_CLOSED:
            return

        elif event == '-edu-':
            classes.eduPenData = True

        elif event == '-ergo-':
            classes.ergoPenData = True

        elif event == '-read-':
            path = askStartingDirectory()
            if not path == "":
                statisticsList, rowList, df_Stats = file.readPickledData(path, window)
                window['-plot-'].update(disabled=False)

        elif event == '-rootFolder-':
            path = askStartingDirectory()
#            path = "/Users/peter/Schwan/digitaler Stift/Software/Referenzdaten/Daten_2022"
            if not path == "":
                window["-stdout-"].print(path+"\n")
                listOfFolders = file.readFolders(path)
                if len(listOfFolders) != 0:
                    td = sg.TreeData()
                    file.td_fill(td, listOfFolders, '')
#                    file.splitStream(listOfFolders)
                    window['_TREE_'].update(values=td)
                    window['-root-'].update(value=path)
                    window['-Rechnen-'].update(disabled=False)
 
        elif event == '-parallel-':
            targetFolder = path+"_result"
            targetFolder = makeDefaultFolder(targetFolder)
            window['-target-'].update(value=targetFolder)
            if len(statisticsList) > 0:
                file.writeStandard(targetFolder, df_Stats, rowList)
                returnCode = file.writeToFile(targetFolder, statisticsList, rowList, df_Stats)
                if isinstance(returnCode, int):
                    sg.Popup("Data has been written successfully!", title="Done!", auto_close=True, auto_close_duration=3)
                else:
                    sg.Popup("\nSomething went wrong! Here is the error message:\n",
                             str(returnCode[0])+"\n\n", str(returnCode[1]), title="Error during writing")
            else:
                sg.Popup("Please calculate results first!", title="Not yet!")

        elif event == '-newFolder-':
            targetFolder = sg.popup_get_folder('Select directory', title='Select Directory', default_path=path,
                                               no_window=True)
            targetFolder = makeDefaultFolder(targetFolder)
            window['-target-'].update(value=targetFolder)
            if len(statisticsList) > 0:
                file.writeStandard(targetFolder, df_Stats, rowList)
                returnCode = file.writeToFile(targetFolder, statisticsList, ageList, handedList, genderList)
                if isinstance(returnCode, int):
                    sg.Popup("Data has been written successfully!", title="Done!", auto_close=True, auto_close_duration=3)
                else:
                    sg.Popup("\nSomething went wrong! Here is the error message:\n",
                             str(returnCode[0])+"\n\n", str(returnCode[1]), title="Error during writing")
            else:
                sg.Popup("Please calculate results first!", title="Not yet!")

        elif event == '-Rechnen-':
            data.runCollateDataframes()
            statisticsList = data.runStatistics()
            df_Stats, rowList = data.runTimeslices()
            handedList = data.runSplitHanded()
            genderList = data.runSplitGenders()
            window['-plot-'].update(disabled=False)
            window['-parallel-'].update(disabled=False)
            window['-newFolder-'].update(disabled=False)

            progressUpdate('-Pro-', int(10000))

        elif event == '-plot-':
            if len(statisticsList) > 0:
                plotString = values['-parm-']
                plot.show(plotString, df_Stats, rowList)
            else:
                sg.Popup("Please calculate results first!", title="Not yet!")

