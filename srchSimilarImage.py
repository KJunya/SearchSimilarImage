import os
import shutil
import sys
import glob
from PIL import Image

argv = sys.argv
argc = len(argv)

#FUNCTIONS--------------------------
#print usage------------------------
def usage():
	print "usage: $ python %s {srcDir} {imgfile}" % argv[0]
	print " srcDir  - source directory of images"
	print " imgfile - image you want to search for"

#get hash value----------------------
def hashVal(img, crushS = 8):					#image, crush size
	cpImage = img.copy()			        	#copy image
	cpImage = cpImage.resize((crushS+1, crushS), Image.ANTIALIAS)	#resize image
	cpImage = cpImage.convert("L")			#convert to monochrome

	#calculata hash value
	hashVal = 0				#hash value
	loopC = 0				#loop count
	for x in range(crushS):
		for y in range(crushS):		#if pixel(x, y) is brighter than the next pixel
			if cpImage.getpixel((x, y)) > cpImage.getpixel((x+1, y)):	#set 1 to hashVal`s bit'
				hashVal += (1 << loopC)
			loopC += 1
	
	return hashVal
		
#MAIN --------------------------------
srchImgList = []	#empty searh image list

#check argc
if argc == 1:
	srcDir = "./"	#set source directory to current directory
if argc > 1:
	if argv[1] == "-h" or argv[1] == "--help":
		usage()
		quit()
	srcDir = argv[1] #set source directory
	if not srcDir.endswith('/'):
		srcDir += '/'
if argc == 3:
	srchImg = argv[2]	#set search image name
	srchImgList.append(srchImg)	#append srchImg to srchImgList

#image extention list
imgExts = [".jpg", ".png", ".jpeg", ".gif", ".tiff", ".bmp", ".ppm"]

#empty image list
imgList = []

#image file search loop---------------------
files = glob.glob(srcDir + "*.*")
for file in files:
	#check image file in srcDir
	fileName, ext = os.path.splitext(file)
	ext = ext.lower()
	if ext in imgExts:
		imgList.append(file)	#add image to list

print str(len(imgList)) + " images found in " + srcDir
if len(imgList) == 0:			#quit program if no image
	quit()

if argc < 3:				#if srchImg is not set
	srchImgList = imgList		#set srchImgList to images in imgList

checkImgCount = len(imgList) - 1		#exclude img
#search similar images in imgList-----------
for imgfile in srchImgList:
	simCount = 0					#count similar image
	imgCount = 0					#count checked image
	img = Image.open(imgfile)			#open img
	pureImgName = imgfile.replace(srcDir, "")	#imgfile name without directory path
	print "checking " + pureImgName + "-------------------------"
	imgHash = hashVal(img)				#get hash value of img

	for img2file in imgList:
		if img2file == imgfile:
			continue			#skip comparasion if same file
		img2 = Image.open(img2file)		#open img2
		pureImg2Name = img2file.replace(srcDir, "")	#img2file name without directory path
		img2Hash = hashVal(img2)		#get hash value of img2
		imgCount += 1
		
		#Show status
		status = 100 * imgCount/checkImgCount
		sys.stdout.write("\r%3d%% looking at %-50s" %(status, pureImg2Name))
		if status >= 100:
			sys.stdout.write("\r%3d%% search ended%-50s " %(status, ""))
		sys.stdout.flush()	

		#Check same bits
		difBits = imgHash ^ img2Hash 			#get difference of bit
		sameBitCount = 64 - bin(difBits).count("1")  	#count same bits

		#Check similarity
		if sameBitCount >= 64*0.8 :			#if sameBitCount were more than 80% of 64
			sameBitPercent = 100 * sameBitCount/64
			print pureImg2Name + " looks %3d%% similar" % sameBitPercent	#img2 is similar to img
			simCount += 1;
		#end of checking similarity of imgfile and img2file--------
		
	print "\n" + str(simCount) + " images similar to " + pureImgName
	#end of searching similar image of imgfile-----------

#end of searching similar images-----------------
