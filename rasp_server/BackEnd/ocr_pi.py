
import math

import cv2
import numpy as np
import pytesseract
import os
import time
from datetime import datetime
import sys



class OcrPy(object):
    def __init__(self, logger):
        self.logger = logger

    def get_new(self, old):
        new = np.ones(old.shape, np.uint8)
        cv2.bitwise_not(new, new)
        return new

    def get_correct_vert(self, point_array):
        """
        获取从左上角开始的顶点
        :param point_list:
        :return:
        """
        rows, cols = point_array.shape
        min_dis = 0
        min_ind = 0
        for i in range(rows):
            dis = self.distance(point_array[i], np.array([0, 0]))
            if i == 0:
                min_dis = dis
            else:
                if dis < min_dis:
                    min_dis = dis
                    min_ind = i

        if min_ind == 0:
            return point_array
        else:
            part_one = point_array[0:min_ind, :]
            part_two = point_array[min_ind:rows, :]

            result = np.append(part_two, part_one, axis=0)
            return result

    def distance(self, point1, point2):
        """
        距离公式
        :param point1:
        :param point2:
        :return:
        """
        point_x = point1[0] - point2[0]
        point_y = point1[1] - point2[1]
        return math.sqrt(math.pow(point_x, 2) + math.pow(point_y, 2))

    def get_height_and_width(self, point_array):
        """
        计算长宽
        :param point_array:
        :return:
        """
        a1 = self.distance(point_array[0], point_array[1])
        b1 = self.distance(point_array[1], point_array[2])
        a2 = self.distance(point_array[2], point_array[3])
        b2 = self.distance(point_array[3], point_array[0])
        max_b = b1 if b1 > b2 else b2
        max_a = a1 if a1 > a2 else a2
        if a1 + a2 > b1 + b2:
            return max_a, max_b
        else:
            return max_b, max_a

    def recognize(self, orig):
        # these constants are carefully picked
        MORPH = 9
        CANNY = 84
        HOUGH = 25

        img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        cv2.GaussianBlur(img, (3, 3), 0, img)

        # this is to recognize white on white
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
        dilated = cv2.dilate(img, kernel)

        edges = cv2.Canny(dilated, 0, CANNY, apertureSize=3)

        lines = cv2.HoughLinesP(edges, 1, 3.14 / 180, HOUGH)
        for line in lines[0]:
            cv2.line(edges, (line[0], line[1]), (line[2], line[3]),
                     (255, 0, 0), 2, 8)

        # finding contours
        # contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
        #                                cv2.CHAIN_APPROX_TC89_KCOS)
        image_temp, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)
        contours = filter(lambda cont: cv2.arcLength(cont, False) > 100, contours)
        contours = filter(lambda cont: cv2.contourArea(cont) > 1000, contours)

        # simplify contours down to polygons

        for cont in contours:
            rect = cv2.approxPolyDP(cont, 40, True).copy().reshape(-1, 2)
            r, c = rect.shape
            if r == 4:
                point_array = rect

                pt1 = self.get_correct_vert(point_array)
                new_cols, new_rows = self.get_height_and_width(point_array)
                new_cols = int(new_cols)
                new_rows = int(new_rows)

                cut_cols = new_cols // 10
                cut_rows = new_rows // 10

                pt1 = pt1.astype(np.float32)
                pt2 = np.float32([[0, 0], [0, new_rows], [new_cols, new_rows], [new_cols, 0]])

                matrix = cv2.getPerspectiveTransform(pt1, pt2)

                # 仿射变换
                result = cv2.warpPerspective(img, matrix, (new_cols, new_rows))

                # 腐蚀可疑区域
                result_erase = result[cut_rows: new_rows - cut_rows, cut_cols:new_cols - cut_cols]
                # cv2.imwrite(result_file, result_erase)

                (thresh, im_bw) = cv2.threshold(result_erase, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                cv2.imwrite("im_bw.png", im_bw)

                code = pytesseract.image_to_string(im_bw, lang='eng', config='-psm 7 digits')

                if code is None:
                    code = "None"
                else:
                    pass
                self.logger.info(code)

                return code, result_erase
        self.logger.info("Not Detected")
