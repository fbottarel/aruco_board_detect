#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import argparse
import cv2
import sys
import os


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", required=True,
                        help="path to output image containing ArUCo tag")
    parser.add_argument("-i", "--id", type=int, required=True,
                        help="ID of ArUCo tag to generate")
    parser.add_argument("-t", "--type", type=str,
                        default="DICT_ARUCO_ORIGINAL",
                        help="type of ArUCo tag to generate")
    parser.add_argument("-s", "--size", required=True, type=int,
                        help="size (in pixel)")
    parser.add_argument("-b", "--bborder", type=int,
                        default=50,
                        help="black border around marker (in pixel)")
    parser.add_argument("-w", "--wborder", type=int,
                        default=50,
                        help="white border around marker (in pixel)")

    args = vars(parser.parse_args())

    print(args)

    # Verify the dictionary tag is valid
    # Names of each possible ArUco tag OpenCV supports

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    }

    if args['type'] not in ARUCO_DICT.keys():
        print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
        sys.exit(0)

    # Load the ArUCo dictionary

    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[args['type']])

    # Generate marker

    print("[INFO] Generating marker ID {} from dictionary {}".format(args['id'], args['type']))

    marker = np.zeros((args['size'], args['size'], 1), dtype=np.uint8)
    cv2.aruco.drawMarker(aruco_dict, args['id'], args['size'], marker, 1)

    if args['wborder'] > 0 or args['bborder'] > 0:
        size = args['size']
        bborder = args['bborder']
        wborder = args['wborder']
        border = wborder + bborder

        bordered_image = np.zeros((size+2*border, size+2*border, 1), dtype=np.uint8)

        bordered_image[bborder:bborder+size+2*wborder, bborder:bborder+size+2*wborder, :] = 255

        bordered_image[border:border+size, border:border+size, :] = marker

        marker = bordered_image

    cv2.imshow('Marker {}'.format(args['id']), marker)

    if cv2.imwrite(args['output'], marker):
        print("[INFO] Saved as {}".format(args['output']))
        sys.exit(0)
    else:
        print("[ERROR] Could not save as {}".format(args['output']))
        sys.exit(1)
