import json
import os
import maya.cmds as cmds

USER_DIR = os.environ['USERPROFILE'].replace('\\','/')

current_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

OfficefrontPath = f"{current_dir}/texture/office1.jpg"
OfficebackPath = f"{current_dir}/texture/office1.jpg"
OfficesidePath = f"{current_dir}/texture/office1.jpg"
OfficetopPath = f"{current_dir}/texture/office2.jpg"


def checkFile(path):
    return cmds.file(path, q=True, ex=True)

def isImageExsist(path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.tga', '.bmp', '.tiff', '.exr']
    file_extension = os.path.splitext(path)[-1].lower()
    return (file_extension in valid_extensions)

def saveText(name, side, path):
    data = {
        name+side: {
            'name': name,
            'side': side,
            'path': path
        }
    }
    with open(f'{current_dir}/save.json', 'r') as f:
        saveData = json.load(f)
    saveData['allText'].update({name: ''})
    newSave = saveData | data
    with open(f'{current_dir}/save.json', 'w') as f:
        json.dump(newSave, f, indent=4)

def readSave():
    with open(f'{current_dir}/save.json', 'r') as f:
        saveData = json.load(f)
    return saveData

for each in readSave():
    for key in readSave():
        if key != 'allText':
            var = readSave()[key]
            globals()[var['name']+var['side']+'Text'] = var['path']