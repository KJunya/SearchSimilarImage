SearchSimilarImage
===

## Description
srchSimilarImage.py - A python script that searches similar image file in specified directory.
					  It will copy each similar image groups and creates group directories in source directory.  
myfd.py - A Directory/File manipulater module.  
mylog.py - A simple log file handler module. **It's very primitive!**  
mysi.py - A similar image searcher module.  

## Requirement
Python Imaging Library (PIL or Pillow).  
Please change global variable "MY__LOGFILE" to your log file path/name in each "my"module; mylog.py, myfd.py.  

## Usage
```
usage: $ python srchSimilarImage.py {--source} srcpath/file1 {srcpath/file2 ...} {[-s, --search] srchpath/file1 {srchpath.file2 ...}} {[-f, --filter] filtervalue}
	--source : source files or directories
	-s, --search : search files or directories
	-f, --filter : similarity filter value
```

## Examples
	$ python srchSimilarImage.py SourceDir
			# This searches similar images in SourceDir.
			
	$ python srchSimilarImage.py SourceDir -f 0.75
			# This searches similar images that has similarity of 75% in SourceDir.
			
	$ python srchSimilarImage.py SourceDir -s SearchDir
			# This searches similar images from SourceDir in SearchDir.
			
	$ python srchSimilarImage.py SourceDir1 SourceDir2 -s SearchDir1 SearchDir2
			# This searches similar images from SourceDir1 and SourceDir2 in SearchDir1 SearchDir2.
			
	$ python srchSimilarImage.py SourceDir -f 0.75
			# This searches similar images that has similarity of 75% in SourceDir.

## Reference
The algorithm for searching image is done by comparing Difference Hash; produced by the image file.  
Refered website -> http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

## Author
KJunya