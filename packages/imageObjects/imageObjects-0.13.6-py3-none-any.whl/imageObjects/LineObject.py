from imageObjects import ImageObject

from miscSupports import group_adjacent, flatten
import numpy as np
import cv2
import sys


class LineObject:
    def __init__(self, image, target_colour, min_length, mark_colour=180, block_out=None, warnings=True):
        if isinstance(image, ImageObject):
            self.img = image.mask_on_colour_range(target_colour, target_colour, new_image=True)

            self._mark = mark_colour
            self._mark_bgr = (mark_colour, mark_colour, mark_colour)
            self._block_out = block_out
            self._len_min = min_length

            self._WHITE = 255
            self._WHITE_BGR = (255, 255, 255)
            self._BLACK = 0
            self._BLACK_BGR = (0, 0, 0)

            if warnings and (cv2.countNonZero(self.img.image) / self.img.pixel_total > 0.5):
                print("Warning: The number of pixels you are running is more than 50% of the image and may cause "
                      "significant slowdown.\nYou can turn this warning off with warnings=False")

        else:
            sys.exit("LineObject expects an ImageObject")

    def find_vertical_lines(self, adjacent_pixels=None, fill_gaps_max_length=None):
        """
        This will look for vertical lines that meet the minimum width requirement

        :param adjacent_pixels: If specified, this number of adjacent pixels will also be selected from each line found
        :type adjacent_pixels: int | None

        :param fill_gaps_max_length:  If specified, this will try to find and fill gaps between lines that might occur
            on damaged or old images. The integer passed is the maximum gap you will permit, the min is taken from
            min_length passed to the class object.
        :type fill_gaps_max_length int | None
        """

        # For each column of the image, find how many of the current column are not zero, grouping them by adjacency. If
        # the adjacent groups meet the minimum length requirement, draw them. Once all column are complete, isolate
        # the lines
        for i in range(self.img.width):
            [self._draw_vertical_lines(i, y_indexes) for y_indexes in group_adjacent(self._isolate_column(i))]
        self.img.mask_on_colour_range(self._mark_bgr, self._mark_bgr)

        # If we want to enlarge the lines a bit, we can do so via drawing them larger via draw_contours.
        if adjacent_pixels:
            [c.draw_contour(self.img, self._WHITE_BGR, adjacent_pixels) for c in self.img.extract_contours("external")]

        # If we want to try to bridge gaps between lines, this method will do so as long as the distance is less than
        # the maximum length provided by the user via fill_gaps_max_length
        if fill_gaps_max_length:
            self._fill_vertical_gaps(fill_gaps_max_length)

    def find_horizontal_lines(self, adjacent_pixels=None, fill_gaps_max_length=None):
        """
        This will look for horizontal lines that meet the minimum width requirement

        :param adjacent_pixels: If specified, this number of adjacent pixels will also be selected from each line found
        :type adjacent_pixels: int | None

        :param fill_gaps_max_length:  If specified, this will try to find and fill gaps between lines that might occur
            on damaged or old images. The integer passed is the maximum gap you will permit, the min is taken from
            min_length passed to the class object.
        :type fill_gaps_max_length int | None
        """
        # For each row of the image, find how many of the current row are not zero, grouping them by adjacency. If the
        # adjacent groups meet the minimum length requirement, draw them. Once all rows are complete, isolate the lines
        for i in range(self.img.height):
            [self._draw_horizontal_lines(i, x_indexes) for x_indexes in group_adjacent(self._isolate_row(i))]
        self.img.mask_on_colour_range(self._mark_bgr, self._mark_bgr)

        # If we want to enlarge the lines a bit, we can do so via drawing them larger via draw_contours.
        if adjacent_pixels:
            [c.draw_contour(self.img, self._WHITE_BGR, adjacent_pixels) for c in self.img.extract_contours("external")]

        # If we want to try to bridge gaps between lines, this method will do so as long as the distance is less than
        # the maximum length provided by the user via fill_gaps_max_length
        if fill_gaps_max_length:
            self._fill_horizontal_gaps(fill_gaps_max_length)

    @staticmethod
    def _isolate_gaps(row):
        """
        Isolate gaps by the absence of pixels between two sets of found lines. Return the maximum gap.
        """
        gap_list = [[min(g), max(g)] for g in group_adjacent(row)]
        if len(gap_list) > 1:
            return max([gap_list[i][0] - gap_list[i - 1][1] for i, gap in enumerate(gap_list) if i > 0])
        else:
            return 0

    def _isolate_row(self, index):
        """
        Isolate the non zero indexes from the current row as a list
        """
        return flatten(np.asarray((self.img.image[index, :]).nonzero()))

    def _isolate_column(self, index):
        """
        Isolate the non zero indexes from the current column as a list
        """
        return flatten(np.asarray((self.img.image[:, index]).nonzero()))

    def _draw_vertical_lines(self, i, y_indexes):
        """
        Draws a vertical line on an image, as long as it meets the minimum length requirement, via pixel indexes

        For the vertical lines our index i is our column index with ii being our row index
        """
        return [self.img.change_pixel_colour(ii, i, self._mark) for ii in y_indexes if len(y_indexes) > self._len_min]

    def _draw_horizontal_lines(self, i, x_indexes):
        """
        Draws a horizontal line on an image, as long as it meets the minimum length requirement, via pixel indexes.

        For the horizontal draw lines our index i is our row index and our in line ii is the column index.
        """
        return [self.img.change_pixel_colour(i, ii, self._mark) for ii in x_indexes if len(x_indexes) > self._len_min]

    def _fill_horizontal_gaps(self, gap_max):
        """
        If a row has any pixels that are a line, we isolate this rows pixel values and break the row into lines. If
        there is more than 1 segment, and the gap length between them is less than gap_max, then it is filled. If
        block_out is set as a preference for failures, then if these lines where to small individual then they will be
        removed.
        """
        row_pixel_values = np.sum(self.img.image == self._WHITE, axis=1)
        for row_i, row_sum in enumerate(row_pixel_values):
            if row_sum > 0:
                row = self._isolate_row(row_i)

                # If there are pixels in this row, isolate the gaps and if the gaps meet the criteria fill them
                if (0 < self._isolate_gaps(row) < gap_max) and (row_sum > self._len_min):
                    r_min = min(row)
                    [self.img.change_pixel_colour(row_i, r_min + i, self._WHITE) for i in range(0, max(row) - r_min)]

                # If we want to remove anything that fails the size check we can block it out
                elif self._block_out and (row_sum < self._len_min):
                    [self.img.change_pixel_colour(row_i, i, self._BLACK) for i in row]

    def _fill_vertical_gaps(self, gap_max):
        """
        If a column has any pixels that are a line, we isolate this columns pixel values and break the column into
        lines. If there is more than 1 segment, and the gap length between them is less than gap_max, then it is filled.
        If block_out is set as a preference for failures, then if these lines where to small individual then they will
        be removed.
        """
        column_pixel_values = np.sum(self.img.image == self._WHITE, axis=0)
        for column_i, column_sum in enumerate(column_pixel_values):
            if column_sum > 0:
                column = self._isolate_column(column_i)

                # If there are pixels in this column, isolate the gaps and if the gaps meet the criteria fill them
                if (0 < self._isolate_gaps(column) < gap_max) and (column_sum > self._len_min):
                    c_min = min(column)
                    [self.img.change_pixel_colour(c_min + i, column_i, self._WHITE)
                     for i in range(0, max(column) - c_min)]

                # If we want to remove anything that fails the size check we can block it out
                elif self._block_out and (column_sum < self._len_min):
                    [self.img.change_pixel_colour(i, column_i, self._BLACK) for i in column]
