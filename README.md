# SearchSimilarImage
A python script that searches similar image file in specified directory.
Python Imaging Library (PIL) is required.
Usage :
  1. srchSimilarImage.py (no arguments);
    search every similar images of image in current directory
  
  2. srchSimilarImage.py DIRECTORY_PATH;
    search every similar images of image in DIRECTORY_PATH
    
  3. srchSimilarImage.py DIRECTORY_PATH IMAGE_FILE_NAME;
    search similar images of IMAGE_FILE_NAME in DIRECTORY_PATH
    
The algorithm for searching image is done by comparing Difference Hash; produced by the image file.
Refered website -> http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
