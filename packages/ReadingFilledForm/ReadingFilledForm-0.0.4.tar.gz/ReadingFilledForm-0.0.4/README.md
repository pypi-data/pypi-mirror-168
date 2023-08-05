# Reading texts from the pre-filled scanned forms or live-scanner individual frames.

## About this package

This computer-vision package will invoke the python script that will instantiate the class to initiate the reading capability & display text from a pre-filled scanned forms or live scanner-based individual frames. This application developed using Open-CV. This project is for the advanced Python developer & Data Science Newbi's.


## How to use this package

(The following instructions apply to Posix/bash. Windows users should check
[here](https://docs.python.org/3/library/venv.html).)

First, clone this repository and open a terminal inside the root folder.

Create and activate a new virtual environment (recommended) by running
the following:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Run the Augmented Reality-App:

```bash
python readingFormLib.py
```

Make sure that you are properly connected with a functional WebCam or scanned images (Preferably a separate external WebCAM).

## How to use this Package

We need to understand that the current class has some basic limitations. We need to define the areas in terms of pixel position, which we need to extract.

We need to fill-up the zone in the following way -

```
'MY_DICT': {
          "atrib_1": {"id": "FileNo", "bbox": (425, 60, 92, 34), "filter_keywords": tuple(["FILE", "DEPT"])},
          "atrib_2": {"id": "DeptNo", "bbox": (545, 60, 87, 40), "filter_keywords": tuple(["DEPT", "CLOCK"])},
          "atrib_3": {"id": "ClockNo", "bbox": (673, 60, 75, 36), "filter_keywords": tuple(["CLOCK","VCHR.","NO."])},
          "atrib_4": {"id": "VCHRNo", "bbox": (785, 60, 136, 40), "filter_keywords": tuple(["VCHR.","NO."])},
          "atrib_5": {"id": "DigitNo", "bbox": (949, 60, 50, 38), "filter_keywords": tuple(["VCHR.","NO.", "056"])},
          "atrib_6": {"id": "CompanyName", "bbox": (326, 140, 621, 187), "filter_keywords": tuple(["COMPANY","FILE"])},
          "atrib_7": {"id": "StartDate", "bbox": (1264, 143, 539, 44), "filter_keywords": tuple(["Period", "Beginning:"])},
          "atrib_8": {"id": "EndDate", "bbox": (1264, 193, 539, 44), "filter_keywords": tuple(["Period", "Ending:"])},
          "atrib_9": {"id": "PayDate", "bbox": (1264, 233, 539, 44), "filter_keywords": tuple(["Pay", "Date:"])},
    }
```

From the above, as you can see that you need pass the area that you want to extract by the following method ->

"atrib_<Number>": {"id": <Your FieldName that you want to capture inside the Python>, "bbox": (x-Coordinates, y-Coordinates, Width, Height), "filter_keywords": tuple(["Mention the overlapping printed text that you don't want to capture. Make sure you are following the exact Case to proper detection."])}

You can easily get the individual intended text position by using any Photo editor.

Let's see the complete code of this config file (clsConfigClient.py) ->

```
################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 25-Jul-2022               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### Augmented Reality via WebCAM streaming.####
####                                        ####
################################################

import os
import platform as pl

my_dict = {}

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'REPORT_PATH': Curr_Path + sep + 'report',
        'SRC_PATH': Curr_Path + sep + 'data' + sep,
        'FINAL_PATH': Curr_Path + sep + 'Target' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Scans' + sep,
        'TEMPLATE_PATH': Curr_Path + sep + 'Template' + sep,
        'APP_DESC_1': 'Text Extraction from Video!',
        'DEBUG_IND': 'N',
        'INIT_PATH': Curr_Path,
        'SUBDIR': 'data',
        'WIDTH': 320,
        'HEIGHT': 320,
        'PADDING': 0.1,
        'SEP': sep,
        'MIN_CONFIDENCE':0.5,
        'GPU':-1,
        'FILE_NAME':'FilledUp.jpeg',
        'TEMPLATE_FILE_NAME':'Template.jpeg',
        'TITLE': "Text Reading!",
        'ORIG_TITLE': "Camera Source!",
        'LANG':"en",
        'OEM_VAL': 1,
        'PSM_VAL': 7,
        'DRAW_TAG': (0, 0, 255),
        'LAYER_DET':[
        	"feature_fusion/Conv_7/Sigmoid",
        	"feature_fusion/concat_3"],
        "CACHE_LIM": 1,
        'ASCII_RANGE': 128,
        'SUBTRACT_PARAM': (123.68, 116.78, 103.94),
        'MY_DICT': {
                    "atrib_1": {"id": "FileNo", "bbox": (425, 60, 92, 34), "filter_keywords": tuple(["FILE", "DEPT"])},
        			"atrib_2": {"id": "DeptNo", "bbox": (545, 60, 87, 40), "filter_keywords": tuple(["DEPT", "CLOCK"])},
        			"atrib_3": {"id": "ClockNo", "bbox": (673, 60, 75, 36), "filter_keywords": tuple(["CLOCK","VCHR.","NO."])},
        			"atrib_4": {"id": "VCHRNo", "bbox": (785, 60, 136, 40), "filter_keywords": tuple(["VCHR.","NO."])},
        			"atrib_5": {"id": "DigitNo", "bbox": (949, 60, 50, 38), "filter_keywords": tuple(["VCHR.","NO.", "056"])},
        			"atrib_6": {"id": "CompanyName", "bbox": (326, 140, 621, 187), "filter_keywords": tuple(["COMPANY","FILE"])},
        			"atrib_7": {"id": "StartDate", "bbox": (1264, 143, 539, 44), "filter_keywords": tuple(["Period", "Beginning:"])},
        			"atrib_8": {"id": "EndDate", "bbox": (1264, 193, 539, 44), "filter_keywords": tuple(["Period", "Ending:"])},
                    "atrib_9": {"id": "PayDate", "bbox": (1264, 233, 539, 44), "filter_keywords": tuple(["Pay", "Date:"])},
        		  }
    }

```

Following is the sample demo snippet to invoke the main python package (readingFormLib.py) -

```
#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 22-Jul-2022                     ####
#### Modified On 15-Sep-2022                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### ReadingFilledForm package to initiate       ####
#### the reading capability in real-time         ####
#### & display text from a formatted forms.      ####
#####################################################

# We keep the setup code in a different class as shown below.
from ReadingFilledForm import clsReadForm as rf

from clsConfigClient import clsConfigClient as cf

import datetime
import logging

###############################################
###           Global Section                ###
###############################################
# Instantiating all the main class
scannedImagePath = str(cf.conf['IMAGE_PATH']) + str(cf.conf['FILE_NAME'])
templatePath = str(cf.conf['TEMPLATE_PATH']) + str(cf.conf['TEMPLATE_FILE_NAME'])

x1 = rf.clsReadForm(scannedImagePath, templatePath)

###############################################
###    End of Global Section                ###
###############################################

def main():
    try:
        # Other useful variables
        debugInd = 'Y'
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        var1 = datetime.datetime.now()

        print('Start Time: ', str(var))
        # End of useful variables

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        logging.basicConfig(filename=general_log_path + 'readingForm.log', level=logging.INFO)

        print('Started extracting text from formatted forms!')

        # Getting the dictionary
        my_dict = cf.conf['MY_DICT']

        # Execute all the pass
        r1 = x1.startProcess(debugInd, var, my_dict)

        if (r1 == 0):
            print('Successfully extracted text from the formatted forms!')
        else:
            print('Failed to extract the text from the formatted forms!')

        var2 = datetime.datetime.now()

        c = var2 - var1
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', str(minutes))

        print('End Time: ', str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()

```

Note that the debug indicator is set to "Y". This will generate logs. If you change this to 'N'. No logs will be generated. However, the process will be faster.

## Resources

- To learn more about Open-CV, check out our [documentation](https://opencv.org/opencv-free-course/).
- To learn more about my website, check out the blog [documentation](https://satyakide.com).
