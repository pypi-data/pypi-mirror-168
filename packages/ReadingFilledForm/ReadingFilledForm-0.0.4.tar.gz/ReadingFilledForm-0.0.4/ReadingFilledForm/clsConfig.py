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

class clsConfig(object):
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
        'SUBTRACT_PARAM': (123.68, 116.78, 103.94)
    }
