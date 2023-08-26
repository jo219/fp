#!/usr/bin/env python
# -*- coding: utf-8 -*-
#PyFingerprint
##Copyright (C) 2015 Bastian Raschke 
#All rights reserved.

import tempfile
from pyfingerprint.pyfingerprint import PyFingerprint
from compare2 import find_best_match
from compare3 import compare
import pygame

## Reads image and download it
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB1', 115200, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to read image and download it
while True:
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        print('Downloading image (this take a while)...')

        # # registering mode
        # n = input("dest: ")
        # imageDestination =  './samples/'+ n +'.bmp'

        # exec mode
        imageDestination =  './result.bmp'

        f.downloadImage(imageDestination)

        print('The image was saved to "' + imageDestination + '".')
        
        # # from compare3
        # compare()

        # from compare2
        best_match_file, best_score = find_best_match(imageDestination, "./samples")

        if best_match_file:
            print("Best Match: " + best_match_file)
            print("Score: {:.2f}%".format(best_score))
        else:
            print("No matches found.")

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

    