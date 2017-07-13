#!/usr/bin/env python
import os
import sys  #damn
import myfd		#my file directory manipulator module in ~/bin
import mysi		#my similar image module in ~/bin


argv = sys.argv
argc = len(argv)
cwd = os.getcwd() + '/'	#get current working directory


#print usage -----------------------------------------------------------------------
def usage():
	print "usage: $ python %s {--source} path/srcfile... {[-s, --search] path/srchfile...} {-f filter}" % argv[0]
	print "	finds similar image of file or directories"
	print "	--source : source files or directories"
	print "	-s, --search : search files or directories"
	print "	-f, --filter : similarity filter value"
	
#get arguments -------------------------------------------------------------------
def argumentCheck( argc, argv ):
	srcList = []		#source list
	srcImgFileList = [] #souce image file list
	srchList = []		#search list
	srchImgFileList = [] #search image list
	filterVal = .88	#filter value

	#check number of arguments
	if argc < 2:
		print "missing arguments"
		return ([], [], -1)	#return error value
	
	#check for help prompt
	if argv[1] in ["-h", "--help"]:
		return([], [], -1)
	
	i = 1
	while i < argc:
		if argv[i] in ["-f", "--filter"]:		#set filter value
			i += 1
			if argv[i].replace(".", "", 1).isdigit():
				filterVal = float(argv[i])
				print "filter value = " + str(filterVal)
		elif argv[i] in ["-s", "--search"]:		#set search list
			i += 1
			while i < argc and not argv[i].startswith('-'):
				print "search " + argv[i]
				srchList.append(argv[i])
				i += 1
			continue
		elif argv[i] == "--source":	#set source list
			i += 1
			while i < argc and not argv[i].startswith('-'):
				print "source " + argv[i]
				srcList.append(argv[i])
				i += 1
			continue
		elif not argv[i].startswith('-'):
			while i < argc and not argv[i].startswith('-'):
				print "source " + argv[i]
				srcList.append(argv[i])
				i += 1
			continue
		else:
			print "invalid argument"
			usage()
			quit()
		i += 1
	#end of while
	
	#define function that gets image file form srcList
	def imgInList( aList ):
		imgList = []	#image file only list
		for src in aList:
			if not cwd in src:
				src = cwd + src
			if os.path.isfile(src) and myfd.isImageFile(src):
				imgList.append(src)
			elif os.path.isdir(src):
				imgList.extend(myfd.getImgList(src))
		return imgList
	
	#get image files for each lists
	srcImgFileList = imgInList(srcList)
	srchImgFileList = imgInList(srchList)
	
	return (srcImgFileList, srchImgFileList, filterVal)

#main function for command line --------------------------------------------------
def main():
	srcImgFileList = []		#source image file list
	srchImgFileList = []	#search image file list
	simImgFileLists = []		#similar image list
	filterVal = 0				#filter value
	
	#check arguments
	srcImgFileList, srchImgFileList, filterVal = argumentCheck(argc, argv)
	if len(srcImgFileList) == 0:
		print "source images are messing"
		usage()
		quit()
	elif filterVal < 0.0 or filterVal > 1.0:
		print "invalid filter value"
		usage()
		quit()
		
	if len(srchImgFileList) == 0:
		srchImgFileList = srcImgFileList
	
	#search for similar images
	print "searching " + str(len(srchImgFileList)) + " images from " + str(len(srcImgFileList)) + " images"
	simImgFileLists = mysi.getSimImgLists(srcImgFileList, srchImgFileList, {}, filterVal)

	if len(simImgFileLists) == 0:
		print "no similar images found"
		quit()

	#make group directory
	count = 0
	for simImgFileList in simImgFileLists:
		groupDistList = []	#check created group dir path
		for imgFile in simImgFileList:
			imgPath = myfd.getPathAndPureName(imgFile)[0]
			#check if group dir has already been created
			if imgFile in srcImgFileList and not imgPath in groupDistList:
				groupDistList.append(imgPath)
				myfd.makeGroup(imgPath, simImgFileList, "simImg", False)
				print "created simImg" + str(count)
				count +=  1
				
				
#MAIN ====================================================
if __name__ == "__main__":
	main()
