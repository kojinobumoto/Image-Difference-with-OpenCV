from skimage.metrics import structural_similarity
import imutils
import cv2

import traceback
import sys

from pathlib import Path
from . import settings

settings.init()

def compimgdiff_init(str_start_datetime):
    compare_image_diff.DATA_OUT_DIRNAME = settings.DATA_OUT_DIRNAME_BASE + '-' + str_start_datetime
    Path(compare_image_diff.DATA_OUT_DIRNAME).mkdir(exist_ok=True, parents=True)


def compare_image_diff(orig_image_with_path):

    ssim_score = 0.0

    try:

        arr_msg = []
        bool_dimension_diff = False

        # load the two input images
        #
        # cv2.imread() and cv2.imwrite() do not support PATH containing UNICODE.
        image_file_name = Path(orig_image_with_path).name
        imageA = cv2.imread(str(orig_image_with_path), 1)

        # [TODO]
        # Error handring in case there's no SECOND_IMAGE_DIRNAME + '/' + image_file_name.
        imageB_file_path = settings.SECOND_IMAGE_DIRNAME + '/' + image_file_name
        obj_imageB = Path(imageB_file_path)

        if not obj_imageB.is_file():
            arr_msg.append(f'Comparison file ({imageB_file_path}) was not found corresponding to theoriginal file ({orig_image_with_path}).')
        else:
            imageB = cv2.imread(settings.SECOND_IMAGE_DIRNAME + '/' + image_file_name, 1)
            imageA = imageA.astype('uint8')
            imageB = imageB.astype('uint8')
            # convert the images to grayscale
            grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
            grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

            # compute the Structural Similarity Index (SSIM) between the two
            # images, ensuring that the difference image is returned
            #(ssim_score, diff) = compare_ssim(grayA, grayB, full=True)

            # initialize
            ssim_score = 0.0
            diff = -1

            try :
                (ssim_score, diff) = structural_similarity(grayA, grayB, full=True)
            except ValueError:
                # the idea came from https://stackoverflow.com/questions/48945249/images-dimensions-error-in-python
                (H, W) = imageA.shape[:-1] # see https://stackoverflow.com/questions/38122948/w-h-template-shape-1-results-in-value-error-too-many-values-to-unpack
                imageB = cv2.resize(imageB, (W, H))
                grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                (ssim_score, diff) = structural_similarity(grayA, grayB, full=True)
                bool_dimension_diff = True
            except Exception as e:
                raise

            diff = (diff * 255).astype("uint8")

            # if there's no difference between two images, then SIM to be 1.0.
            if ssim_score == 1.0:
                arr_msg.append('No difference between two "{image_file_name}".')
            else:
                if bool_dimension_diff == True:
                    arr_msg.append(f'[Image sizes are different - forced comparison] There are differences in the files "{image_file_name}" (SSIM={ssim_score}).')
                    bool_dimension_diff == False
                else:
                    arr_msg.append('There are differences in the files "{image_file_name}" (SSIM={ssim_score})')

                # threshold the difference image, followed by finding contours to
                # obtain the regions of the two input images that differ
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)

                # loop over the contours
                for c in cnts:
                    # compute the bounding box of the contour and then draw the
                    # bounding box on both input images to represent where the two
                    # images differ
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 5)
                    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 5)

                    # show the output images


                file_name_body = image_file_name.split('.')[0]
                save_file_orig_path    = compare_image_diff.DATA_OUT_DIRNAME + '/' + file_name_body + '-1.orig.png'
                save_file_new_path     = compare_image_diff.DATA_OUT_DIRNAME + '/' + file_name_body + '-2.new.png'
                save_file_diff_path    = compare_image_diff.DATA_OUT_DIRNAME + '/' + file_name_body + '-3.diff.png'
                save_file_thresh_path  = compare_image_diff.DATA_OUT_DIRNAME + '/' + file_name_body + '-4.thresh.png'

                retOriginalS = cv2.imwrite(save_file_orig_path, imageA)

                module_name = 'cv2.imwrite'
                if retOriginalS == False:
                    arr_msg.append('[Error ({module_name})] Failed to save image file (original). {save_file_orig_path}')

                retModifiedS = cv2.imwrite(save_file_new_path, imageB)
                if retModifiedS == False:
                    arr_msg.append('[Error ({module_name})] Failed to save image file (comarison). {save_file_new_path}')

                retDiffS = cv2.imwrite(save_file_diff_path, diff)
                if retDiffS == False:
                    arr_msg.append('[Error ({module_name})] Failed to save image file (diff). {save_file_diff_path}')

                retTreshS = cv2.imwrite(save_file_thresh_path, thresh)
                if retDiffS == False:
                    arr_msg.append('[Error ({module_name})] Failed to save image file (thresh). {save_file_thresh_path}}')

    except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            sam =  traceback.format_exception(exc_type, exc_value, exc_traceback)
            arr_msg.append('[ERROR] {0} in {1} : {2} : {3}'.format(type(ex).__name__
                                                             , sys._getframe().f_code.co_name
                                                             , ex, sam[-4].replace('"', '\\"').strip("\n").replace("\r\n", "")))
    finally:
            return [ssim_score, image_file_name, "\n".join(arr_msg)]