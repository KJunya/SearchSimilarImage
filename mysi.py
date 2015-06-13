import os
import sys
from PIL import Image
import myfd		#my file directory manipulator module in ~/bin
import mylog	#my log file module


MYSILOGFILE = "pathtolog/file.txt"
MYSIERROR = "!MYSIERROR!"


#FUNCTIONS ==============================================
#get hash value -------------------------------------------------------------------
def getHashVal( imgFile ):
	crushS	= 8
	try:
		img 	= Image.open(imgFile)
	except:
		mylog.writeLog(MYSILOGFILE, "(getHashVal) " + MYSIERROR +" failed to open image: " + imgFile)
	cpImage = img.copy()				#copy image
	cpImage = cpImage.resize((crushS+1, crushS), Image.ANTIALIAS)	#resize image
	cpImage = cpImage.convert("L")		#convert to monochrome

	#calculata hash value
	hashVal = 0	#hash value
	loopC = 0	#loop count
	for x in range(crushS):
		for y in range(crushS):		#if pixel(x, y) is brighter than the next pixel
			if cpImage.getpixel((x, y)) > cpImage.getpixel((x+1, y)):	#set 1 to hashVal`s bit'
				hashVal += (1 << loopC)
			loopC += 1
	
	mylog.writeLog(MYSILOGFILE, "(getHashVal) " + imgFile +" hashVal=0x" + str(hex(hashVal)))
	return hashVal

#get hash value dict -------------------------------------------------------------
def getHashValDict( imgFiles ):
	hashValDict = {}
	imgCount = 0
	listLen = len(imgFiles)
	
	for imgFile in imgFiles:
		hashValDict[imgFile] = getHashVal(imgFile)
	
	return hashValDict

#get number of same bits of hash value -------------------------------------
def getSameHashBitCount( srcImgFile, srchImgFile, hashValDict = {}):
	srcHash = 0
	srchHash = 0
	
	if len(hashValDict) == 0:
		srcHash = getHashVal(srcImgFile)
		srchHash = getHashVal(srchImgFile)
	else:
		srcHash = hashValDict[srcImgFile]
		srchHash = hashValDict[srchImgFile]
		
	diffBits = srcHash ^ srchHash	#same bits to 0, different bits to 1
	return 64 - bin(diffBits).count("1")

#get similar images in srcImgFiles -----------------------------------------------
def getSimImgList( srcImgFiles, srchImgFile, hashValDict = {}, filterVal = .88 ):
	simImgList = []	#similar image list
	
	#if hashValDict is not defined, set new hashValDict
	if len(hashValDict) == 0:
		hashValDict = getHashValDict(srcImgFiles)
		hashValDict[srchImgFile] = getHashVal(srchImgFile)
	
	#get similar image list
	for srcImgFile in srcImgFiles:
		if srcImgFile == srchImgFile:
			continue
		sameBits = getSameHashBitCount(srcImgFile, srchImgFile, hashValDict)
		if sameBits >= 64 * filterVal:
			simImgList.append(srcImgFile)
	
	simImgList.append(srchImgFile)
	return simImgList
	
#get similar images lists list in srcImgFiles --------------------------------------
def getSimImgLists( srcImgFiles, srchImgFiles, hashValDict = {}, filterVal = .88 ):
	simImgLists = []	#similar image list list
	tmpList = []		#temp list

	#if hashValDict is not defined, set new hashValDict	
	if len(hashValDict) == 0:
		hashValDict = getHashValDict(srcImgFiles)
		hashValDict.update(getHashValDict(srchImgFiles))
	
	#make similar image list list
	for srchImgFile in srchImgFiles:
		aList = getSimImgList(srcImgFiles, srchImgFile, hashValDict, filterVal)
		if len(aList) > 1:
			tmpList.append(aList)

	#delete same list in similar image list
	for simImgList in tmpList:
		simImgList.sort()
		if not simImgList in simImgLists:
			simImgLists.append(simImgList)
			
	return simImgLists
