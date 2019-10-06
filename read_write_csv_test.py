import os
for (root, dirs, files) in os.walk("E:/SHZQ"):
    for x in range(len(files)):
        print(files[x] in 'SH')