import os
import os.path
import time
#记录开始时间
start =time.perf_counter()

now=int(time.time())
timeStruct=time.localtime(now)
strTime1=time.strftime("%Y-%m-%d",timeStruct)
strTime2=time.strftime("%Y-%m-%d",timeStruct)+" 00:00:00"


#把某一目录下的所有文件复制到指定目录中
def copyFiles(sourceDir,  targetDir):
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)

#删除一级目录下的所有文件:
def removeFileInFirstDir(targetDir):
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)

sourceDir="E:/Stock/Data_Day_original/"+ strTime1 +"/"
targetDir="E:/Stock/Data_Day/"

removeFileInFirstDir(targetDir)
copyFiles(sourceDir,  targetDir)




