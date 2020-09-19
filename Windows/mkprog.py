import sys
from github import Github
import datetime 
from os import walk
import os, shutil, base64
from pygit2 import clone_repository
import time
import stat



now = datetime.datetime.now()

path = str(sys.argv[0]).replace(str(sys.argv[0]).split("\\")[-1],"")
print(path)

with open(f"{path}\\Config.txt",'r') as f:
    l_con = f.readlines()
USERNAME, PASSWORD, textEditorCMD = l_con[0].strip(),l_con[1].strip(), l_con[2].strip()

def listToString(s):  
    str1 = ""    
    for ele in s:  
        str1 += ele  + " "    
    return str1[0:(len(str1)-1)]

g = Github(USERNAME,PASSWORD)
user = g.get_user()

programPath = os.getcwd()

licence = "Copyright %s %s \nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\nTHE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE." % (now.year,USERNAME)
#print(listence)

def commitCreate(dirpath,i):
    fullProgramPath = programPath+"\\"+sys.argv[2]
    loc = dirpath.replace(fullProgramPath,"")+"\\"
    if(loc[0:6] != "\\.git\\"):
        if(os.path.getsize(f"{fullProgramPath}{loc}{i}") < 2000000):
            with open(f"{fullProgramPath}{loc}{i}",'r') as r:
                r_con = r.read()
        else:
            print(f"file {i} too large for automatic upload {os.path.getsize(f'{fullProgramPath}{loc}{i}')}")
        flLoc = str(loc+i).replace("\\","/")[1:]
        try:
            repo.create_file(flLoc,f"Edited {i} file",r_con)
            print(f"edited file {i}")
        except:
            print(f"error on {i} file" if i[-3:] != "exe" else f"File {i} too large maybe conpress?")
    

def createRepo(name,description):
    repo = user.create_repo(name.replace(" ","-"),description)
    repo.edit(private=True)
    os.mkdir(programPath+"\\"+name) #,int("0777") if getting errors
    with open(programPath+"\\"+name+"\\LICENSE","w+") as f:
        f.write(licence)
    repo.create_file("LICENSE","Made LICENCE file",licence)
    repo.get_issues(state='open')
    os.system(textEditorCMD.format(path = programPath+"\\"+name))

p = []

if(len(sys.argv) > 1 and sys.argv[1] == "-create"):
    createRepo(sys.argv[2],sys.argv[3])
    
            
elif(len(sys.argv) > 1 and sys.argv[1] == "-open"):
    repo = user.get_repo(sys.argv[2].replace(" ","-"))
    
    folder = f"{os.getcwd()}\\{sys.argv[2]}\\"

    for root, dirs, files in os.walk(folder):  
        for dir in dirs:
            os.chmod(f"{root}\\{dir}", stat.S_IRWXU)
        for file in files:
            os.chmod(f"{root}\\{file}", stat.S_IRWXU)

    try:
        shutil.rmtree(folder)
    except:
        os.mkdir(folder)
    

    
    prevPriv = repo.private
    repo.edit(private=False)
    time.sleep(0.5)
    clone_repository("git://github.com/%s/%s.git" %(USERNAME,sys.argv[2].replace(" ","-")),folder)
    repo.edit(private=prevPriv)
    os.system(textEditorCMD.format(path = programPath+"\\"+sys.argv[2]))
    

elif(len(sys.argv) > 1 and sys.argv[1] == "-publish"):
    repo = user.get_repo(sys.argv[2].replace(" ","-"))
    repo.edit(private=False)
    
elif(len(sys.argv) > 1 and sys.argv[1] == "-commit"):
    repo = user.get_repo(sys.argv[2].replace(" ","-"))

    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            repo.delete_file(file_content.path,"ressing vals",file_content.sha)

    for (dirpath, dirnames, filenames) in walk(programPath+"\\"+sys.argv[2]):
        if __name__ == "__main__":
            for i in(filenames):          
                commitCreate(dirpath,i)
   