# Compare the differences between two png images
## Base idea of the image comparison.
https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
## requirement
* required scikit-image and imutils.
* scikit-image and imutils shoudl be up-to-date.
* note1
    * if you use Anaconda, add the "conda-forge" channel and install imutils.
* note2
    * if you encountered the "rocedure endpoint OPENSSL_sk_nre_reserve could not found" error when installing imutils, check the following page to fix the error.
    * https://github.com/conda/conda/issues/9003#issuecomment-516499958
        * i.e. you have to copy the libssl-1_1-x64.dll in Anaconda/DLLS and replaced that in Anaconda/Library/bin
* other requirement
    * put the base image file(s) into the "img/1.first" folder.
    * put the comparison file(s) into the "img/2.second" folder.
    * The image files to be compared in the "1.first" and "2.second" folders must have the same file name.
    * Do not include UNICODE (double-byte characters or spaces) in file names, including PATH, because cv2.imread() and cv2.imwrite() do not support PATH containing UNICODE.
## How it works
* Finds and compares files with the same name in the "2.second" folder against files in the "1.first" folder.
* If the file exists in the "1.first" folder but not in the "2.second" folder, an error message will be output.
* Files that do not exist in the "1.first" folder but exist in the "2.second" folder are not detected.
* The assumption is that image files of the same dimension are being compared; attempting to compare images of different dimensions will be judged as "there are differences".
* By default, this program runs in a multi-process manner, launching as many processes as the number of CPU cores on the PC on which it runs.
* If you want to specify the number of processes to run, specify by changing "num_processors" in the source.
