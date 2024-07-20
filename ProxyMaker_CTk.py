#region Setup

import os
import subprocess
import platform
import shlex
import json
import re
import tkinter
import tkinter.filedialog
import tkinter.ttk
import customtkinter

# Window Setup
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.minsize(width=600, height=250)
root.title("Proxy Maker")

headerFrame = customtkinter.CTkFrame(master=root)
headerFrame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "NEW")

frame = customtkinter.CTkFrame(master=root)
frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "NSEW")

optionFrame = customtkinter.CTkFrame(master=root)
optionFrame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

execFrame = customtkinter.CTkFrame(master=root)
execFrame.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "NSEW")

tableFrame = customtkinter.CTkFrame(master=root)
tableFrame.grid(row=4, column=0, padx = 10, pady = 10, sticky = "NSEW")

#footerFrame = customtkinter.CTkFrame(master=root)
#footerFrame.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "SEW")

#Table Setup
columns = ["#1", "#2", "#3"]
tree = tkinter.ttk.Treeview(master=tableFrame, columns=columns, show="headings")
tree.pack(fill="both", expand=True)
tree.heading("#1", text="File Name")
tree.heading("#2", text="Proxy Level")
tree.heading("#3", text="Proxy Location")

tree.column("#1", width=150)
tree.column("#2", width=50)
tree.column("#3", width=300)

def add_table_data(data):
    tree.insert("", tkinter.END, values=data)

#endregion

# POINT YOUR DIRECTORY to sources and proxy destination
contentSource = tkinter.StringVar()
proxyDepot = tkinter.StringVar()
proxyRes = tkinter.StringVar()

#Folder Dialog Buttons
def directoryBrowseButton():
    folderName = tkinter.filedialog.askdirectory()
    contentSource.set(folderName)
    return folderName

def depotBrowseButton():
    folderName = tkinter.filedialog.askdirectory()
    proxyDepot.set(folderName)
    return folderName

#Proxy creator function
def createProxies(content_directory, proxy_depot):
    for dirpath, dirnames, filenames in os.walk(content_directory):
        for filename in filenames:
            if filename.endswith('.mov'):
                file_path = os.path.join(dirpath, filename)
                print(f"step 1 File path: {file_path}")
                createProxy(file_path, proxy_depot)

    print("Finished processing files")

def createProxy(file_path, proxy_depot):
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        resFactor = proxyRes.get()
        proxy_file_name = f"{file_name}_proxy{resFactor}.mov"
        print(f"File Name: {file_name}")
        print(f"File Path: {file_path}")
        print(f"Proxy Name: {proxy_file_name}")
        proxy_path = os.path.join(proxy_depot, proxy_file_name)
        print(f"Proxy path: {proxy_path}")

        cmd = 'ffmpeg -i ' + file_path + ' -vf "scale=iw/' + resFactor + ':ih/' + resFactor + '" -c:v hap ' + proxy_path

        print(f"command: {cmd}")
        if platform.system() == "Darwin":
            args = shlex.split(cmd)
            subprocess.run(args, check=True, stderr=subprocess.PIPE)
        if platform.system() == "Windows":
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE)

        
        tableData = (file_name, resFactor, proxy_path)
        add_table_data(tableData)
        
        
    except Exception as e:
        print(f"Error creating proxy for file '{file_path}': {str(e)}")

def proxyMakerButton():
    sourceDir = contentSource.get()
    proxyDir = proxyDepot.get()
    createProxies(sourceDir, proxyDir)

#region Window elements
headerLabel = customtkinter.CTkLabel(master=headerFrame, text="Proxy Maker")
contentLabel =customtkinter.CTkLabel(master=frame, text="Content Directory:")
depotLabel = customtkinter.CTkLabel(master=frame, text="Proxy Storage Location:")
resLabel = customtkinter.CTkLabel(master=optionFrame, text="Proxy Level:")

headerLabel.pack(anchor="n")
contentLabel.grid(row=1, column=0, sticky="e")
depotLabel.grid(row=2, column=0, sticky="e")

contentField = customtkinter.CTkEntry(master=frame, width=150, textvariable= contentSource)
contentField.grid(row=1, column=1)
depotField = customtkinter.CTkEntry(master=frame, width=150, textvariable= proxyDepot)
depotField.grid(row=2, column=1)

dirButton1 = customtkinter.CTkButton(master=frame, text="Browse", command=directoryBrowseButton, width=40)
dirButton1.grid(row=1, column=2)

dirButton2 = customtkinter.CTkButton(master=frame, text="Browse", command=depotBrowseButton, width=40)
dirButton2.grid(row=2, column=2)

resLabel.grid(row=3, column=1, sticky="e")
proxyRes.set("2")
resDropdown = customtkinter.CTkOptionMenu(master=optionFrame, values=["2", "4"], variable=proxyRes)
resDropdown.grid(row=3, column=2, sticky="w")

execButton = customtkinter.CTkButton(master=execFrame, text="Create Proxies",command=proxyMakerButton, width=80)
execButton.pack(anchor="center")


#endregion

root.mainloop()
