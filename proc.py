import importlib.resources
import random
import maya.cmds as cmds
import importlib
from . import fileManage
from .fileManage import*

importlib.reload(fileManage)

def build(name,width,length,height):
    try:
        newName = 'Building' if name == '' else name
        width = check(width)
        length = check(length)
        height = check(height)
        create(newName,width,length,height)
    except ValueError:
        cmds.confirmDialog(
            title="Notification",
            message="Please enter int number!",
            button=["OK"],
            defaultButton="OK",
        )

def create(name,width,length,height):
    pre=['backWall','sideRightWallPre','sideLeftWallPre','frontWall','topWall']
    floor =[]
    roof=[]
    building=[]
    paddind = 3
    allObj = []

    cmds.currentUnit(linear='meter')
    cmds.grid(size=12, spacing=5, divisions=5)
    cmds.file(f"{current_dir}/model/plainModel.fbx",i=True, mergeNamespacesOnClash=False, pr=True, ra=True, ignoreVersion=True, defaultNamespace=True)
    importObj = cmds.ls(type='mesh')
    cmds.select(importObj)
    cmds.sets(importObj, edit=True, forceElement='initialShadingGroup')

    print(cmds.file(f"{current_dir}/model/plainModel.fbx", q=True, ex=True))
    for x in range(length):
        num = '%s%0{}d'.format(paddind)
        for z in range(width):
            if x==0:
                cmds.select('sideRightWallPre', r=True)
                obj = cmds.duplicate(rr = True)
                obj = cmds.rename(num%('sideRightWall',x+1))
                cmds.setAttr(f'{obj}.tz', -3*z)
                floor.append(obj)
            
            cmds.select('topWall', r=True)
            num = '%s%0{}d'.format(paddind)
            obj = cmds.duplicate(rr = True)
            obj = cmds.rename(num%('topWall',x+1))
            cmds.setAttr(f'{obj}.tz', -3*z)
            cmds.setAttr(f'{obj}.tx', 3*x)
            roof.append(obj)
            
        for side in ['frontWall', 'backWall']:
            cmds.select(side, r=True)
            num = '%s%0{}d'.format(paddind)
            obj = cmds.duplicate(rr = True)
            obj = cmds.rename(num%(side,x+1))
            cmds.setAttr(f'{obj}.tx', 3*x)
            if side =='backWall':
                cmds.setAttr(f'{obj}.tz', -3*(width-1))
            floor.append(obj)

        if x==length-1:
            for z in range(width):
                cmds.select('sideLeftWallPre', r=True)
                num = '%s%0{}d'.format(paddind)
                obj = cmds.duplicate(rr = True)
                obj = cmds.rename(num%('sideLeftWall',z+1))
                cmds.setAttr(f'{obj}.tz', -3*z)
                cmds.setAttr(f'{obj}.tx', 3*x)
                floor.append(obj)

    #allObj.append(obj for obj in floor)
    cmds.select(floor, r=True)
    group = cmds.group()
    group = cmds.rename('floor')
    building.append(group)
    cmds.move(0,-1.5,0, f'{group}.scalePivot',f'{group}.rotatePivot', r=True)
    
    for y in range(height-1):
        obj = cmds.duplicate(rr=True)
        obj = cmds.rename(num%('floor',y+2))
        cmds.setAttr(f'{obj}.ty', 3*(y+1))
        building.append(obj)
        
    #allObj.append(obj for obj in roof)
    cmds.select(roof, r=True)
    group = cmds.group()
    group = cmds.rename('roof')
    cmds.setAttr(f'{group}.ty', 3*(height-1))
    building.append(group)
    
    
    cmds.select(building, r=True)
    group = cmds.group()
    group = cmds.rename(name)
    cmds.delete(pre)

    
    cmds.select(group)
    print(group)
    sels = cmds.ls(sl=True, l=True)
    allObj = cmds.listRelatives(sels, allDescendents=True, fullPath=True)
    print(allObj)

    cmds.select(allObj)
    #cmds.select(group, r=True)



def check(x):
    if x == '':
        x = random.randint(1,20)
    x = int(x)
    return int(x)



def randomShadding():
    
    sels = cmds.ls(sl=True, l=True)
    allObj = cmds.listRelatives(sels, allDescendents=True, fullPath=True)

    for x in ['side','front','back','top']:
        if not cmds.ls(f'{x}Lambert'):
            ranR = random.uniform(0, 1)
            ranB = random.uniform(0, 1)
            ranG = random.uniform(0, 1)
            shader = cmds.shadingNode('lambert', asShader=True, name=f'{x}Lambert')
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{x}SG')
            cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader', force=True)
            shader = cmds.setAttr(f'{shader}.color',ranR ,ranG , ranB)

        for each in allObj:
            if x in each:
                cmds.sets(each, edit=True, forceElement=f'{x}SG')


def textureBySide(name, side, allObj, path):
        name = 'building' if name == '' else name
        if not cmds.ls(f'{name}_{side}Lambert') and isImageExsist(path):
            shader = cmds.shadingNode('lambert', asShader=True, name=f'{name}_{side}Lambert')
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}_{side}SG')
            cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader', force=True)
            
            picNode = cmds.shadingNode('file', asTexture=True, name= shader + '_file')
            cmds.setAttr(f'{picNode}.fileTextureName', path, type="string")
            cmds.connectAttr(picNode + ".outColor", shader + ".color", force=True)
        
        for each in allObj:
            if side in each:
                cmds.sets(each, edit=True, forceElement=f'{name}_{side}SG')

