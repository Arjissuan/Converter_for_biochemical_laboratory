import PySimpleGUI as sg
import os
import pasing


def gui():
    sg.theme("DarkAmber")

    file_list_column = [
        [
            sg.Text("Folder"),
            sg.In(size=(30, 3), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(45, 24), key="-FILE LIST-")],
        [sg.Button("Exit")]
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Chosen text file from list on left:", size=(40, 1))],
        [sg.Text("File name", size=(70, 1), key="-TOUT-")],
        [sg.Multiline(size=(70, 20), key="-TEXT-")],
        [
            sg.Text("Name to conversion:"),
            sg.Input(enable_events=True, key="-TIN-")
        ],
        [
            sg.Text("New folder"),
            sg.Input(enable_events=True, key="-END FOLDER-"),
            sg.FolderBrowse()
        ],
        [
            sg.Button("Save"),
            sg.Button("Convert to excel file", enable_events=True, key="-CONVERT-"),
            sg.Text(key="-CONVERSION EVENT-")
        ]
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]

    window = sg.Window("Text file converter", layout)

    folder_location = ""

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == "-FOLDER-":
            folder_location = values["-FOLDER-"]
            try:
                files_names = os.listdir(folder_location)
            except:
                files_names = []

            fnames = [
                f for f in files_names
                if os.path.isfile(os.path.join(folder_location, f))
                and f.lower().endswith((".txt", ".TXT", ".py", ".json"))
            ]
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-" and len(values["-FILE LIST-"]) > 0:
            fselection = values["-FILE LIST-"][0]

            with open(os.path.join(folder_location, fselection)) as file:
                content = file.read()
                window["-TOUT-"].update(os.path.join(folder_location, fselection))
                window["-TEXT-"].update(content)

        elif event == "-CONVERT-":
            fselection = values["-FILE LIST-"][0]
            try:
                pasing.parsing(folder_location, fselection, values["-END FOLDER-"], values["-TIN-"])
                window["-CONVERSION EVENT-"].update("Conversion to excel file done")
            except:
                window["-CONVERSION EVENT-"].update("Not all neccesary fields are filled up")

        elif event == "Save":
            try:
                fselection = values["-FILE LIST-"][0]
            except:
                window["-CONVERSION EVENT-"].update("File is not chosen")
            try:
                with open(os.path.join(folder_location, fselection), "w") as myfile:
                    myfile.write(values["-TEXT-"])
                    window["-CONVERSION EVENT-"].update("Changes to file saved")
            except:
                window["-CONVERSION EVENT-"].update("File is not chosen")
    window.close()
