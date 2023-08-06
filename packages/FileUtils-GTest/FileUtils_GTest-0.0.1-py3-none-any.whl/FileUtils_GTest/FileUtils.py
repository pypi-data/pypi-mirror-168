#!/usr/bin/python
# -*-coding: utf-8-*-

import urllib
import re
import os
import json
import re
import io
import platform
import pandas as pd
import struct
import shutil

def move(src, dest):
	checkCreateFolder(dest)
	shutil.move(src, dest)

def copyFile(srcFile, targetFile):
	targetFileFolder = getFileFolder(targetFile)
	if not os.path.exists(targetFileFolder):
		os.makedirs(targetFileFolder)
	shutil.copyfile(srcFile, targetFile)

def readInt(datFile, offset):
	allBytes = readBytes(datFile)
	dateBytes = allBytes[offset:offset+4]
	ret = struct.unpack("i", dateBytes)[0]
	return ret

def readBytes(datFile):
	file = open(datFile, "rb")
	allBytes = file.read()
	file.close()
	return allBytes

def writeBytes(datFile, allBytes):
	checkCreateFolder(getFileFolder(datFile))
	if(type(allBytes) == list):
		allBytes = bytearray(allBytes)
	file = open(datFile, "wb")
	file.write(allBytes)
	file.close()

def readConfigExcel(configExcel, parsedKeys = []):
	# print("==> readConfigExcel:", configExcel)
	df1 = pd.read_excel(configExcel, index_col = 0).ffill()
	jsonStr = df1.to_json(orient="records", force_ascii=False)
	tmpConfigs = json.loads(jsonStr)
	for item in tmpConfigs:
		for key in item:
			if(key in parsedKeys):
				item[key] = json.loads(item[key])


	return tmpConfigs

def writeConfigExcel(configExcel, jsonArray):
	dataFrame = pd.DataFrame(jsonArray)
	dataFrame.to_excel(configExcel, encoding='utf-8', index=True, header=True)

def getFileName(file, hasExt = False):
	fsList = get_filePath_fileName_fileExt(file)
	if (hasExt):
		return "{}{}".format(fsList[1], fsList[2])
	else:
		return fsList[1]

def getFileFolder(file):
	fsList = get_filePath_fileName_fileExt(file)
	return fsList[0]

def get_filePath_fileName_fileExt(filename):
		(filepath,tempfilename) = os.path.split(filename);
		(shotname,extension) = os.path.splitext(tempfilename);
		return filepath,shotname,extension;
		
def checkCreateFolder(folder):
	if(not os.path.exists(folder)):
		os.makedirs(folder);

def writeFile(fileName, info):
	checkCreateFolder(getFileFolder(fileName))
	with io.open(fileName, "w", encoding="utf-8") as my_file:
		my_file.write(info)

def readFile(fileName):
	data = "null"
	with io.open(fileName, "r", encoding="utf-8") as myFile:
		data = myFile.read()

	return data;

def getFiles(folder, ext = "", onlyTop = False):
	fileList = []
	for root,folders, files in os.walk(folder):
		isCurrentFolder = os.path.normcase(folder) == os.path.normcase(root)
		fullPathFiles = [os.path.join(root,item) for item in files]
		extFiles = [item for item in fullPathFiles if (ext == "" or item.endswith(ext))]
		if (onlyTop):
			if (isCurrentFolder):
				fileList.extend(extFiles)
		else:
			fileList.extend(extFiles)

	return fileList







