##############################################
#### Written By: SATYAKI DE               ####
#### Written On: 20-Dec-2019              ####
#### Modified On 20-Dec-2019              ####
####                                      ####
#### Objective: Main scripts for logging  ####
##############################################

from setuptools import setup, find_packages

setup(
name="ReadingFilledForm",
version="0.0.3",
author="Satyaki De",
author_email='satyakide.us@gmail.com',
description="This is the main calling python script that will invoke the class to initiate the reading capability & display text from a formatted forms.",
packages=find_packages(exclude=['Scans','Template']),
python_requires='>=3.7',
url='https://github.com/SatyakiDe2019/ScannedCopyDataExtraction',
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
license_files='license.txt',
readme="README.md"
)
