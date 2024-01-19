import re
import shutil
from tqdm import tqdm
from pathlib import Path

datasetFolder = Path("./GTOS")
splitFolder = datasetFolder / Path("color_imgs")
metadataFolder = datasetFolder / Path("labels")

# 获取metadatafolder下test*.txt和train*.txt的文件
# testFiles = [i for i in metadataFolder.glob("test*.txt")]
# trainFiles = [i for i in metadataFolder.glob("train*.txt")]

# 只使用train1和test1，这样不会重复
trainFiles = [metadataFolder / Path("train1.txt")]
testFiles = [metadataFolder / Path("test1.txt")]

Path.mkdir(datasetFolder / Path("train"), exist_ok=True)
Path.mkdir(datasetFolder / Path("test"), exist_ok=True)
with open(metadataFolder / Path("classInd.txt")) as f:
    json = {}
    classInd = f.readlines()
    for row in classInd:
        split = re.split(r'\s+|\n', row)
        json[split[0]] = split[1]
# print(json)
for value in json.values():
    # print(value)
    Path.mkdir(datasetFolder / Path("train") / Path(value), exist_ok=True)
    Path.mkdir(datasetFolder / Path("test") / Path(value), exist_ok=True)

use = []
for txt in trainFiles:
    with open(txt, 'r') as f:
        content = f.readlines()
        for row in tqdm(content, desc=txt.name):
            split = re.split(r'\s+|/|\n', row)
            # print(split)
            shutil.copytree(splitFolder / Path(split[1]), datasetFolder / Path("train") / Path(split[0]), dirs_exist_ok=True)
            use.append(split[1])

for txt in testFiles:
    with open(txt, 'r') as f:
        content = f.readlines()
        for row in tqdm(content, desc=txt.name):
            split = re.split(r'\s+|/|\n', row)
            # print(split)
            # 
            if split[1] not in use:
                shutil.copytree(splitFolder / Path(split[1]), datasetFolder / Path("test") / Path(split[0]), dirs_exist_ok=True)
            else:
                print(f"{split[1]}已经使用！")
                
# 计算有多少张正确使用的
i = 0
for files in (datasetFolder / Path("train")).rglob("*.*"):
    i+=1
print(i)

i = 0
for files in (datasetFolder / Path("test")).rglob("*.*"):
    i+=1
print(i)