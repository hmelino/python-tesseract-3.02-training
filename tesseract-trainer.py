# Tesseract 3.02 Font Trainer
# V0.01 - 3/04/2013

'''
Edited by Matus Hmelar 17/04/2020
- support for Windows file system
- added working directory, your original files will not be affected 
- Input and Output folder for better organisation of files 
'''
# Complete the documentation 

import os
fontname = 'your_new_font'
language = 'eng'
cwd=os.getcwd()
cwdInput=cwd+'\\Input\\'
workingDir=cwd+'\\workDir\\'
os.system(f'cd {cwd}')
os.system(f'mkdir workDir')

print('Tesseract Font Builder - assumes training TIFFs and boxfiles already created')
print('Note: Only up to 32 .tiff files are supported for training purposes')
tifCount = 0
boxCount = 0
#Copy all files into working directory
for file in os.listdir(cwdInput):
    copy =f'copy {cwdInput}{file} workDir\\{file}'
    print(copy)
    os.system(copy)
    if file.endswith('.tif'):
        rename =f'rename workDir\\{file} {language}.{fontname}.exp{tifCount}.tif'
        print(rename)
        os.system(rename)
    if file.endswith('.box'):
        rename =f'rename workDir\\{file} {language}.{fontname}.exp{boxCount}.box'
        print(rename)
        os.system(rename)
    
        

#Train tif with box data
for files in os.listdir(workingDir):
    if files.endswith(".tif"):
        fData=files.split('.')
        command=f'tesseract {workingDir}{files} {files[:-4]} nobatch box.train.stderr'
        print(command) 
        os.system(command)

#Copy created data into working directory
for file in os.listdir(cwd):
    if file.endswith('.tr'):
        move =f'move {cwd}\\{file} {workingDir}\\{file}'
        print(move)
        os.system(move)

trfilelist = ''
boxfilelist = ''
font_properties = ''

for files in os.listdir(workingDir):
    if files.endswith(".tr"):
        trfilelist = f'{trfilelist} {workingDir}{files}'
        font_properties = fontname+' 0 0 0 0 0'    
    if files.endswith(".box"):
        boxfilelist =f'{boxfilelist} {workingDir}{files}'

#Build the Unicharset File
command2 = f'unicharset_extractor {boxfilelist} '
print(command2)
os.system(command2)

#Move unicharset into working Directory
os.system(f'move {cwd}\\unicharset {workingDir}')

#Build the font properties file  
fontpropertiesfile = open(f'{workingDir}\\font_properties', 'a+') # saving into a file        
fontpropertiesfile.write(font_properties)
print('Wrote font_properties file')
fontpropertiesfile.close()

#Clustering
command3 = f'shapeclustering -F {workingDir}\\font_properties -U {workingDir}\\unicharset ' + trfilelist

#command3 = 'shapeclustering '
print(command3)
os.system(command3)

#move shapetable
os.system(f'move {cwd}\\shapetable {workingDir}')
mftraining = f'mftraining -F {workingDir}\\font_properties -U {workingDir}\\unicharset -O {workingDir}\\'+fontname+'.charset '+trfilelist
print (mftraining)
os.system(mftraining)

#move inttemp pffmtable shapetable
os.system(f'move {cwd}\\inttemp {workingDir}')
os.system(f'move {cwd}\\pffmtable {workingDir}')
os.system(f'move {cwd}\\shapetable {workingDir}')

#CNTraining
command4 = 'cntraining ' + trfilelist
print(command4)
os.system(command4)

#Move normproto
os.system(f'move {cwd}\\normproto {workingDir}')

#Rename necessary files
os.system(f'rename {workingDir}\\unicharset '+fontname+'.unicharset')
os.system(f'rename {workingDir}\\shapetable '+fontname+'.shapetable')
os.system(f'rename {workingDir}\\normproto '+fontname+'.normproto')
os.system(f'rename {workingDir}\\pffmtable '+fontname+'.pffmtable')
os.system(f'rename {workingDir}\\inttemp '+fontname+'.inttemp')

##Put it all together
command5 = f'combine_tessdata {workingDir}\\'+fontname+'.'
os.system(command5)

#Move tessData into output
os.system(f'mkdir Output')
os.system(f'move {workingDir}//{fontname}.traineddata {cwd}//Output')
print(f'Your {fontname}.traineddata have been saved into {cwd}\Output')