import os
import glob
import shutil
import mylog	#my log file module

MYFDLOGFILE = "pathtoyourlog/file.txt"	#log filename
MYFDERROR = "!MYFDERROR!"			#error sign string


#return directory string ending with / -------------
def dirWithDash(srcDir):
	if srcDir.endswith('/'):
		return srcDir
	else:
		return srcDir + '/'

#get files in dir ----------------------------------
def getFiles(srcDir, ext=".*", name='*'):
	files = glob.glob(dirWithDash(srcDir) + name + ext)
	return files

#get directories in dir ----------------------------
def getDirs(srcDir, name='*'):
	dirList = []
	stuffs = glob.glob(dirWithDash(srcDir) + name)

	for stuff in stuffs:
		if os.path.isdir(stuff):
			dirList.append(stuff)

	return dirList

#get stuffs in dir ---------------------------------
def getStuffs(srcDir):
	stuffs = glob.glob(dirWithDash(srcDir) + '*')
	return stuffs

#get dir list and file list in srcDir --------------
def getDirAndFileList(srcDir):
	dirList = []
	fileList = []
	stuffs = getStuffs(srcDir)

	for stuff in stuffs:
		if os.path.isfile(stuff):
			fileList.append(stuff)
		elif os.path.isdir(stuff):
			dirList.append(stuff)

	return (dirList, fileList)

#check if file is image file -----------------------
def isImageFile(file):
	if os.path.splitext(file)[1].lower() in [".jpg", ".png", ".jpeg", ".gif", ".tiff", ".bmp", ".ppm"]:
		return True
	else:
		return False

#get dir list from srcDir --------------------------
def getDirList(srcDir):
	dirList = []
	files = []

	if not srcDir.endswith('/'):
		files = glob.glob(srcDir + '/' + '*')
	else:
		files = glob.glob(srcDir + '*')

	for file in files:
		if os.path.isdir(file):
			dirList.append(file)

	return dirList

#get image file list from srcDir -------------------
def getImgList(srcDir):
	imgList = []
	files = []
	files = getFiles(dirWithDash(srcDir))

	print "hi"
	for file in files:
		if isImageFile(file):
			imgList.append(file)

	return imgList

#get name without path -----------------------------
def getPathAndPureName(file):
	path, pureN = file.rsplit('/', 1)
	return (path, pureN)

#check whether a directory has a same file/directory name -------
def doesDirHas(srcDir, name):
	path, pureName = getPathAndPureName(name)
	check = name.replace(path, srcDir)
	if os.path.isfile(check):
		return True
	elif os.path.isdir(check):
		return True
	else:
		return False

#make group directory to dstDir --------------------
def makeGroup(dstDir, group, groupName = "group", move = False):
	groupDir = dstDir

	if not groupDir.endswith('/'):
		groupDir += '/'

	groupDir += groupName

	#check for same group directory name
	groupNo = 0
	while doesDirHas(dstDir, groupDir + str(groupNo)):
		groupNo += 1

	#make group directory
	groupDir += str(groupNo) + '/'
	os.mkdir(groupDir)
	mylog.writeLog(MYFDLOGFILE, "(makeGroup) made directory: " + groupDir)

	#copy or move groupDir
	for file in group:
		cpFileName = groupDir + getPathAndPureName(file)[1]

		#check for same filename in groupDir
		if doesDirHas(groupDir, cpFileName):
			cpNo = 1
			fn, ext = os.path.splitext(cpFileName)
			while doesDirHas(groupDir, fn + "_cp" + str(cpNo) + ext):
				cpNo += 1
			cpFileName += "_cp" + str(cpNo) + ext

		mylog.writeLog(MYFDLOGFILE, "(makeGroup) cpFileName: " + cpFileName)

		if move == True:
			if os.path.isfile(file):	#check existence of file before moving
				shutil.move(file, cpFileName)	#if move flag is on, move file
				mylog.writeLog(MYFDLOGFILE, "(makeGroup) " + MYFDERROR + file + " to " + groupDir)
			else:
				mylog.writeLog(MYFDLOGFILE, "(makeGroup) " + MYFDERROR + " cannot find " + cpFileName)
		else:
			shutil.copyfile(file, cpFileName)	#anything else, copy file
			mylog.writeLog(MYFDLOGFILE, "(makeGroup) copied " + file + " to " + groupDir)

	return groupDir
