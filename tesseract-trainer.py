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
import subprocess
fontname = 'hsbc'
language = 'eng'
cwd=os.getcwd()
cwdInput=cwd+'\\Input\\'
workingDir=cwd+'\\workDir\\'
os.system(f'cd {cwd}')
os.system(f'mkdir workDir')

print('Tesseract Font Builder - assumes training TIFFs and boxfiles already created')
#print('Note: Only up to 32 .tiff files are supported for training purposes')

#Delete output file
os.system(f'del {cwd}\\Output\\{fontname}.traineddata')

dFcount=0
#Empty WorkDir
for file in os.listdir('WorkDir\\'):
    delete=f'del {cwd}\\WorkDir\\{file}'
    #print(delete)
    os.system(delete)
    dFcount+=1
print(f'Deleted {dFcount} files in {cwd}\WorkDir')

tifCount = 0
boxCount = 0
#Copy all files into working directory
for file in os.listdir('Input\\'):
    copy =f'copy {cwd}\\Input\\{file} workDir\\{file} >NUL'
    #print(copy)
    os.system(copy)
    if file.endswith('.tiff'):
        #rename = 'mv '+files+' '+language+'.'+fontname+'.exp'+str(count)+'.tif'
        rename =f'rename {cwd}\\workDir\\{file} {language}.{fontname}.exp{tifCount}.tif'
        #print(rename)
        os.system(rename)
        tifCount+=1
    if file.endswith('.box'):
        #command='tesseract eng.'+fontname+'.exp'+str(count)+'.tif eng.'+fontname+'.exp'+str(count)+' nobatch box.train.stderr'
        rename =f'rename {cwd}\\workDir\\{file} {language}.{fontname}.exp{boxCount}.box'
        #print(rename)
        os.system(rename)
        boxCount+=1
    
        

#Train tif with box data
for files in os.listdir(workingDir):
    if files.endswith(".tif"):
        fData=files.split('.')
        #comand = subprocess.Popen(f'tesseract {cwd}\\workDir\\{files} {files[:-4]} nobatch box.train.stderr',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        #comand= subprocess.run(f'tesseract {cwd}\\workDir\\{files} {files[:-4]} nobatch box.train.stderr',stdout=subprocess.PIPE)
        #o=comand.stdout
        command=f'tesseract {cwd}\\workDir\\{files} {files[:-4]} nobatch box.train.stderr'
        #print(command) 
        os.system(command)

#Copy created data into working directory
for file in os.listdir(cwd):
    if file.endswith('.tr'):
        move =f'move {cwd}\\{file} {cwd}\\WorkDir\\{file}'
        #print(move)
        os.system(move)

trfilelist = ''
boxfilelist = ''
font_properties = ''


for files in os.listdir(workingDir):
    if files.endswith(".tr"):
        trfilelist = f'{trfilelist} {cwd}\\WorkDir\\{files}'
        font_properties = fontname+' 0 0 0 0 0'    
    if files.endswith(".box"):
        boxfilelist =f'{boxfilelist} {cwd}\\WorkDir\\{files}'

#Build the Unicharset File
command2 = f'unicharset_extractor {boxfilelist} '
print(command2)

subprocess.run(command2)
#os.system(command2)

#Move unicharset into working Directory
os.system(f'move {cwd}\\unicharset {cwd}\\WorkDir')

#Build the font properties file  
fontpropertiesfile = open(f'{cwd}\\WorkDir\\font_properties', 'a+') # saving into a file        
fontpropertiesfile.write(font_properties)
print('Wrote font_properties file')
fontpropertiesfile.close()

#Clustering
command3 = f'shapeclustering -F {cwd}\\WorkDir\\font_properties -U {cwd}\\WorkDir\\unicharset ' + trfilelist

#command3 = 'shapeclustering '
print(command3)
#os.system(command3)
subprocess.run(command3)

#move shapetable
os.system(f'move {cwd}\\shapetable {cwd}\\WorkDir')
mftraining = f'mftraining -F {cwd}\\WorkDir\\font_properties -U {cwd}\\WorkDir\\unicharset -O {cwd}\\WorkDir\\'+fontname+'.charset '+trfilelist
print (mftraining)
subprocess.run(mftraining)
#os.system(mftraining)

#move inttemp pffmtable shapetable
os.system(f'move {cwd}\\inttemp {cwd}\\WorkDir')
os.system(f'move {cwd}\\pffmtable {cwd}\\WorkDir')
os.system(f'move {cwd}\\shapetable {cwd}\\WorkDir')

#CNTraining
command4 = 'cntraining ' + trfilelist
print(command4)
subprocess.run(command4)
#os.system(command4)

#Move normproto
os.system(f'move {cwd}\\normproto {cwd}\\WorkDir\\')

#Rename necessary files
os.system(f'rename {cwd}\\WorkDir\\unicharset '+fontname+'.unicharset')
os.system(f'rename {cwd}\\WorkDir\\shapetable '+fontname+'.shapetable')
os.system(f'rename {cwd}\\WorkDir\\normproto '+fontname+'.normproto')
os.system(f'rename {cwd}\\WorkDir\\pffmtable '+fontname+'.pffmtable')
os.system(f'rename {cwd}\\WorkDir\\inttemp '+fontname+'.inttemp')

##Put it all together
command5 = f'combine_tessdata {cwd}\\WorkDir\\'+fontname+'.'
os.system(command5)

#Move tessData into output
os.system(f'mkdir Output')
os.system(f'move {cwd}\\WorkDir\\{fontname}.traineddata {cwd}\\Output')
print(f'Your {fontname}.traineddata have been saved into {cwd}\Output')

os.system(f'del D:\\Program Files\\Tesseract-OCR\\tessdata\\hsbc.traineddata')
os.system(f'copy {cwd}\\Output\\hsbc.traineddata D:\\Program Files\\Tesseract-OCR\\tessdata\\')

input()