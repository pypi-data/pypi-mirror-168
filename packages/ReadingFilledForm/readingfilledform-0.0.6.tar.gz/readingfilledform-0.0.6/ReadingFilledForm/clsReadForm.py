#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 22-Jul-2022                     ####
#### Modified On 30-Aug-2022                     ####
####                                             ####
#### Objective: This is the main python class,   ####
#### which scans from the source & tries match   ####
#### with the supplied template & then extract   ####
#### the text from the aligned template from a   ####
#### specific regions.                           ####
#####################################################

# import the necessary packages
from . import clsAlignTemplates as at
from .clsConfig import clsConfig as cf

from collections import namedtuple
import pytesseract
import imutils
import cv2
import re
import pandas as p

###############################################################################
################            Start Of Global Section       #####################
###############################################################################

# create a named tuple which we can use to create locations of the
# input document which we wish to OCR
ExtractTextLocation = namedtuple("ExtractTextLocation", ["id", "bbox", "filter_keywords"])

# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = []
parsingResults = []

x1 = at.clsAlignTemplates()

###############################################################################
################              End Of Global Section       #####################
###############################################################################

class clsReadForm:
        def __init__(self, scannedImagePath, templatePath):
                self.img_path = scannedImagePath
                self.templ_path = templatePath

        def filterText(self, text):
                try:
                        # strip out non-ASCII text so we can draw the text on the image
                        # using OpenCV
                        return "".join([c if ord(c) < 128 else "" for c in text]).strip()
                except Exception as e:
                        x = str(e)
                        print('Error: ', x)

                        return ""

        def extractFields(self, rowDF):
                try:
                        inDf = rowDF
                        str_id = str(inDf['id'])
                        str_bbox = str(inDf['bbox'])
                        str_filter_keywords = str(inDf['filter_keywords'])

                        return (str_id, str_bbox, str_filter_keywords)
                except Exception as e:
                        x = str(e)
                        print('Error: ', x)

                        str_id = null
                        str_bbox = null
                        str_filter_keywords = null

                        return (str_id, str_bbox, str_filter_keywords)

        def getOCRLocations(self, my_dict):
                try:
                        df = p.DataFrame.from_dict(my_dict)
                        df.reset_index(inplace=True)
                        df = df.rename(columns={'index': 'attribute_id'})

                        # Pivoting from rows to columns
                        pivotedDF = df.T

                        # grab the first row for the header
                        new_header = pivotedDF.iloc[0]

                        # take the data less the header row
                        finDF = pivotedDF[1:]

                        # set the header row as the df header
                        finDF.columns = new_header

                        finDF.reset_index(drop=True, inplace=True)
                        resDF = finDF.iloc[:, 0:]

                        print('Total number of rows::')
                        cnt = resDF.shape[0]
                        print(cnt)

                        # Iterating individual entries
                        for i in range(cnt):
                                try:
                                        print('*'*60)
                                        print(resDF.iloc[i])
                                        id_temp, bbox_temp, filter_keywords_temp = self.extractFields(resDF.iloc[i])

                                        id = id_temp
                                        bbox_int = re.sub("[()]", '', bbox_temp).split(',')
                                        bbox = [eval(i) for i in bbox_int]
                                        filter_keywords = re.sub("[()']", '', filter_keywords_temp).split(',')

                                        OCR_LOCATIONS.append(ExtractTextLocation(id, tuple(bbox), filter_keywords))
                                except Exception as e:
                                        x = str(e)
                                        print('Named Tuple Error: ', x)

                        print('OCR_LOCATIONS :: ')
                        print(OCR_LOCATIONS)

                        return OCR_LOCATIONS
                except Exception as e:
                        x = str(e)
                        print('Error: ', x)

                        return OCR_LOCATIONS

        def startProcess(self, debugInd, var, focussedArea):
                try:
                        img_path = self.img_path
                        templ_path = self.templ_path

                        # Capturing the highlighted area
                        my_dict = focussedArea
                        print('Dictoionary::')
                        print(my_dict)

                        # Populating dynamically from the configuration lists
                        OCR_LOCATIONS = self.getOCRLocations(my_dict)

                        # load the input image and template from disk
                        print("[INFO] Loading Sources...")

                        image = cv2.imread(img_path)
                        template = cv2.imread(templ_path)

                        # align the images
                        print("[INFO] Aligning with Templates...")
                        aligned = x1.startAligning(image, template)

                        # initialize a results list to store the document OCR parsing results
                        print("[INFO] Extracting Text from the Document...")

                        # loop over the locations of the document we are going to OCR
                        for loc in OCR_LOCATIONS:
                                # extract the OCR ROI from the aligned image
                                (x, y, w, h) = loc.bbox
                                roi = aligned[y:y + h, x:x + w]

                                # OCR the ROI using Tesseract
                                rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                                text = pytesseract.image_to_string(rgb)

                                # break the text into lines and loop over them
                                for line in text.split("\n"):
                                        # if the line is empty, ignore it
                                        if len(line) == 0:
                                                continue

                                        # convert the line to lowercase and then check to see if the
                                        # line contains any of the filter keywords (these keywords
                                        # are part of the *form itself* and should be ignored)
                                        lower = line.lower()
                                        count = sum([lower.count(x) for x in loc.filter_keywords])

                                        # if the count is zero than we know we are *not* examining a
                                        # text field that is part of the document itself (ex., info,
                                        # on the field, an example, help text, etc.)
                                        if count == 0:
                                                # update our parsing results dictionary with the OCR'd
                                                # text if the line is *not* empty
                                                parsingResults.append((loc, line))

                        # initialize a dictionary to store our final OCR results
                        results = {}

                        # loop over the results of parsing the document
                        for (loc, line) in parsingResults:
                                # grab any existing OCR result for the current ID of the document
                                r = results.get(loc.id, None)

                                # if the result is None, initialize it using the text and location
                                # namedtuple (converting it to a dictionary as namedtuples are not
                                # hashable)
                                if r is None:
                                        results[loc.id] = (line, loc._asdict())

                                # otherwise, there exists a OCR result for the current area of the
                                # document, so we should append our existing line
                                else:
                                        # unpack the existing OCR result and append the line to the
                                        # existing text
                                        (existingText, loc) = r
                                        text = "{}\n{}".format(existingText, line)

                                        # update our results dictionary
                                        results[loc["id"]] = (text, loc)

                        # loop over the results
                        for (locID, result) in results.items():
                                # unpack the result tuple
                                (text, loc) = result

                                # display the OCR result to our terminal
                                print(loc["id"])
                                print("=" * len(loc["id"]))
                                print("{}\n\n".format(text))

                                # extract the bounding box coordinates of the OCR location and
                                # then strip out non-ASCII text so we can draw the text on the
                                # output image using OpenCV
                                (x, y, w, h) = loc["bbox"]
                                clean = self.filterText(text)

                                # draw a bounding box around the text
                                cv2.rectangle(aligned, (x, y), (x + w, y + h), (0, 255, 0), 2)

                                # loop over all lines in the text
                                for (i, line) in enumerate(text.split("\n")):
                                        # draw the line on the output image
                                        startY = y + (i * 70) + 40
                                        cv2.putText(aligned, line, (x, startY),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

                        # show the input and output images, resizing it such that they fit
                        # on our screen
                        cv2.imshow("Input", imutils.resize(image, width=700))
                        cv2.imshow("Output", imutils.resize(aligned, width=700))
                        cv2.waitKey(0)

                        return 0

                except Exception as e:
                        x = str(e)
                        print('Error: ', x)

                        return 1
