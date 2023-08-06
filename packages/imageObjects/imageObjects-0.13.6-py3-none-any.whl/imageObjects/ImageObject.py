from imageObjects.Support import *

from matplotlib import pyplot as plt
from pathlib import Path
import numpy as np
import cv2
import sys


class ImageObject:
    """
    This creates an object from a cv2 compatible image which can then create new images from itself, or update itself by
    its inherent methods.
    """
    def __init__(self, image):
        self.image = image

    def __repr__(self):
        """
        Return for debug
        """
        return f"{self.image.shape}"

    def __str__(self):
        """
        Clearer message of what the current instance contains
        """
        if self.channels < 3:
            channels_type = "Mono"
        else:
            channels_type = "Colour"

        return f"Height: {self.height}\nWidth: {self.width}\nType: {channels_type}\nChannels: {self.channels}"

    def __copy__(self):
        """
        Allow duplication of instance
        """
        return ImageObject(self.image.copy())

    def __getitem__(self, item):
        """
        Allow for indexing of an image, which is just another way to extract a row

        :param item: Index
        :type item: int
        """
        if item < self.height:
            return self.extract_row(item)
        else:
            raise IndexError("Index out of range: Indexing an ImageObject returns that pixel row, so indexes cannot be"
                             "greater than height-1 as its base zero")

    def __iter__(self):
        """
        Iterate through the rows of an image
        """
        for row in self.image:
            yield row

    def __sub__(self, other):
        """
        Subtracts one image from another, always returns a new instance

        :param other: Another ImageObject
        :type other: ImageObject
        """
        return self._update_or_export(self.image - other.image, True)

    def __add__(self, other):
        """
        Adds one image to another, always returns a new instance

        :param other: Another ImageObject
        :type other: ImageObject
        """
        return self._update_or_export(self.image + other.image, True)

    @property
    def height(self):
        """
        The height of the image in pixels
        """
        return self.image.shape[0]

    @property
    def width(self):
        """
        The width of the image in pixels
        """
        return self.image.shape[1]

    @property
    def pixel_total(self):
        """
        Total number of pixels in the image
        """
        return self.width * self.height

    @property
    def channels(self):
        """
        The number of channels of colour data that exist in the image
        """
        if len(self.image.shape) < 3:
            return 1
        else:
            return self.image.shape[2]

    def count_colour_pixels(self, colour):
        """
        Count the number of pixels equal to a certain colour
        """
        return np.sum(self.image == colour)

    @property
    def empty(self):
        """
        Check to see if the image is empty
        """
        if cv2.countNonZero(self._create_temp_image(colour=False)) == 0:
            return True
        else:
            return False

    def assign_alpha_channel(self, alpha):
        """
        If an image has been converted to alpha, it will not have alpha data. You can assign alpha channel data via this
        method
        """

        if isinstance(alpha, ImageObject):
            self.image[:, :, 3] = alpha.image

        elif isinstance(alpha, np.ndarray):
            self.image[:, :, 3] = alpha

        else:
            raise TypeError(f"assign_alpha_channel expects an ImageObject or np.ndarray yet was passed {type(alpha)}")

    def extract_alpha_beta(self, clip_hist_percent=1):
        """
        Extract the alpha and beta of the image
        """
        return calculate_alpha_beta(self._create_temp_image(False), clip_hist_percent)

    def extract_contours(self, retrieval_mode, simple_method=True, hierarchy_return=False):
        """
        Extract the contours from the image
        """
        return find_contours(self._create_temp_image(False), retrieval_mode, simple_method, hierarchy_return)

    def extract_coloured_coordinates(self, colour):
        """Extract coloured coordinates as a Vector2D"""
        # As we are iterating through rows, its y-x rather than x-y that is returned
        y_list, x_list = np.where(self.image == [colour])
        return [Vector2D(x, y) for x, y in zip(x_list, y_list)]

    def extract_defining_contour(self):
        """
        Extract the largest contour from all contours in the image
        """
        return largest_contour(self._create_temp_image(False))

    def extract_column(self, column_index):
        """
        Extract the numpy array of an image column
        """
        return self.image[:, column_index]

    def extract_row(self, row_index):
        """
        Extract the numpy array of an image row
        """
        return self.image[row_index, :]

    def extract_skeletonized_points(self, skeletonize_method="lee"):
        """
        Extract the skeletonized points from the image
        """
        return skeletonize_points(self.normalise(True).image, skeletonize_method)

    def _create_temp_image(self, colour=True):
        """
        Sometimes we need to create a temporary image, when certain operations require a mono or three channel or more
        image and the current image is not of that type. This creates a colour image by default, but can also create
        mono image, of the current image. If the current image actually meets those specifications, then it is just
        duplicated.
        """
        if colour and self.channels < 3:
            image = self.change_to_colour(new_image=True).image
        elif not colour and self.channels > 2:
            image = self.change_to_mono(new_image=True).image
        else:
            image = self.image.copy()

        return image

    def _update_or_export(self, image, export):
        """
        Check if the user said to update or export our image
        """
        if export:
            return ImageObject(image)
        else:
            self.image = image

    def show(self, window_name="Image", delay=0):
        """
        Show the image and wait for a button to be pressed to continue. Mainly designed for debugging processes
        """
        cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
        cv2.imshow(window_name, self.image)
        cv2.waitKey(delay)

    def notebook_show(self, title="Image"):
        """
        For jupyter we don't want to create a new window, and instead want to show an image via matplotlib.
        """
        if self.channels > 1:
            plt.imshow(self.change_bgr_to_rgb(new_image=True).image)
        else:
            plt.imshow(self.image, cmap="gray", vmin=0, vmax=255)
        plt.title(title)
        plt.show()

    def write_to_file(self, directory, name, write_type="png", compression=0):
        """
        Write the image called 'name', to a 'directory', of type 'write_type'.

        Compression
        If using jpg or webp, then the quality is 0-100, with 100 being the best and 0 the worse
        If using png, then 0 is the best and 9 is the worst
        """
        if write_type == "png":
            comp = [cv2.IMWRITE_PNG_COMPRESSION, compression]
        elif write_type == "jpg":
            comp = [cv2.IMWRITE_JPEG_QUALITY, compression]
        elif write_type == "webp":
            comp = [cv2.IMWRITE_WEBP_QUALITY, compression]
        else:
            raise Exception(f"Unexpected file format of {write_type} found")
        cv2.imwrite(str(Path(directory, f"{name}.{write_type}").absolute()), self.image, comp)

    def change_bgr_to_rgb(self, new_image=False):
        """
        cv2 uses bgr rather than rgb, but this can be changed via this method
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB), new_image)

    def change_bgra_to_bgr(self, new_image=False):
        """
        Convert a four channel alpha image into a three channel image
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR), new_image)

    def change_bgr_to_bgra(self, new_image=False):
        """
        Convert a three channel alpha image to a four channel image
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA), new_image)

    def change_to_colour(self, new_image=False):
        """
        Convert image to colour
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR), new_image)

    def change_to_mono(self, new_image=False):
        """
        Convert to a mono channel gray image
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), new_image)

    def change_pixel_colour(self, pixel_column_index, pixel_row_index, colour):
        """
        Change a specific pixel to a certain colour via column and row indexes
        """
        self.image[pixel_column_index, pixel_row_index] = colour

    def change_row_colour(self, row_index, new_colour):
        """
        Change a whole row to a new colour
        """
        self.image[row_index, :] = new_colour

    def change_column_colour(self, column_index, new_colour):
        """
        Change a whole column to a new colour
        """
        self.image[:, column_index] = new_colour

    def change_a_colour(self, current_colour, new_colour, new_image=False):
        """
        Change all current pixels of one bgr colour to a different bgr colour
        """
        if new_image:
            image = self.image.copy()
            image[np.where((image == [current_colour]).all(axis=2))] = [new_colour]
            return ImageObject(image)
        else:
            self.image[np.where((self.image == [current_colour]).all(axis=2))] = [new_colour]

    def invert(self, new_image=False):
        """
        Invert the current image
        """
        return self._update_or_export(cv2.bitwise_not(self.image), new_image)

    def flip_vertical(self, new_image=False):
        """
        Flip Image vertically
        """
        return self._update_or_export(cv2.flip(self.image, 0), new_image)

    def flip_horizontal(self, new_image=False):
        """
        Flip Image Horizontally
        """
        return self._update_or_export(cv2.flip(self.image, 1), new_image)

    def normalise(self, new_image=False):
        """
        Use Cv2 normalize to set all images to be 0's or 1's.
        """
        return self._update_or_export(cv2.normalize(self._create_temp_image(colour=False), None, alpha=0, beta=1,
                                                    norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F), new_image)

    def morphology(self, morph_type, kernel_vertical, kernel_horizontal, kernel_type="rect", new_image=False):
        """
        This applies one of cv2's morph types to the image, or returns a new one if requested.

        morph_types
        ------------
        morph_types takes on of the following keywords: erode, dilate, open, close, gradient, tophat, blackhat

        kernel_types
        ------------
        kernel_type can take on the following keywords: rect, cross, ellipse. It defaults to rect
        """
        # Set kernel
        kernel_values = {"rect": cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_vertical, kernel_horizontal)),
                         "cross": cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_vertical, kernel_horizontal)),
                         "ellipse": cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_vertical, kernel_horizontal))}
        kernel = key_return("morphology", "kernel_type", kernel_values, kernel_type)

        # Set morphology type
        morph_values = {"erode": 0, "dilate": 1, "open": 2, "close": 3, "gradient": 4, "tophat": 5, "blackhat": 6}
        morph_type = key_return("morphology", "morph_type", morph_values, morph_type)

        if morph_type == 0:
            morphed = cv2.erode(self.image, kernel)
        elif morph_type == 1:
            morphed = cv2.dilate(self.image, kernel)
        elif 1 < morph_type < 7:
            morphed = cv2.morphologyEx(self.image, morph_type, kernel)
        else:
            sys.exit("CRITICAL ERROR: ImageObject.morphology\n"
                     "dict value return from morph_values fell outside of operating range")

        return self._update_or_export(morphed, new_image)

    def blank_like(self, new_image=False):
        """
        Create a blank image of the same dimensions as the image
        """
        return self._update_or_export(np.zeros_like(self.image), new_image)

    def draw_border(self, colour=(0, 0, 0), size=1, new_image=False):
        """
        This function is overlays a hollow square on the image to create an inset border
        """
        return self._update_or_export(cv2.rectangle(self.image.copy(), (0, 0), (self.width, self.height), colour, size),
                                      new_image)

    def draw_rounded_border(self, colour, thickness, radius, fill_percentage, new_image=False):
        """
        Draw a rounded border on the edge of the image
        """
        return self._update_or_export(draw_rounded_box(self._create_temp_image(), (0, 0), (self.width, self.height),
                                                       colour, thickness, radius, fill_percentage), new_image)

    def draw_line(self, point1, point2, colour, thickness, new_image=False):
        """
        Draw a line on the image between points 1-2 of colour and thickness provided
        """
        temp = self._create_temp_image()
        point1, point2 = to_vector_2d(point1), to_vector_2d(point2)
        return self._update_or_export(cv2.line(temp, (point1.x, point1.y), (point2.x, point2.y), colour, thickness),
                                      new_image)

    def draw_circle(self, point, colour, radius, thickness=-1, new_image=False):
        """
        Draw a circle on the image at 'point' of colour and radius provided, allow for changing thickness
        """
        temp = self._create_temp_image()
        point = to_vector_2d(point)
        return self._update_or_export(cv2.circle(temp, (point.x, point.y), radius, colour, thickness), new_image)

    def draw_rectangle(self, top_left_point, bottom_right_point, colour, thickness=-1, new_image=False):
        """
        Draw a rectangle on the image using its top left and bottom right points
        """
        temp = self._create_temp_image()
        top_left, bottom_right = to_vector_2d(top_left_point), to_vector_2d(bottom_right_point)
        return self._update_or_export(cv2.rectangle(temp, (top_left.x, top_left.y), (bottom_right.x, bottom_right.y),
                                                    colour, thickness), new_image)

    def draw_poly(self, points, colour, new_image=False):
        """
        Draw a polygon on the image using a list of clockwise points

        :param points: A list of lists, where sub lists are the x and y position of each point. The points need to be in
            a clockwise order
        :type points: list[list]

        :param colour: BGR colour
        :type colour: tuple

        :param new_image: If set will return a new image, defaults to false which will update this object.
        :type new_image: bool

        :return: If new image is set returns image object, else None
        :rtype: None | ImageObject
        """

        temp = self._create_temp_image()
        points = np.array(points, np.int32)
        points = points.reshape((-1, 1, 2))

        return self._update_or_export(cv2.fillPoly(temp, [points], colour), new_image)

    def draw_contour(self, contours, colour, thickness, new_image=False):
        """
        Draws a ContourObjects, or list/tuple of ContourObjects, onto the image
        """
        temp = self._create_temp_image()

        if isinstance(contours, ContourObject):
            cv2.drawContours(temp, [contours.contour], -1, colour, thickness)
            return self._update_or_export(temp, new_image)

        elif isinstance(contours, (list, tuple)) and all(isinstance(v, ContourObject) for v in contours):
            for c in contours:
                cv2.drawContours(self.image.copy(), [c.contour], -1, colour, thickness)
            return self._update_or_export(temp, new_image)

        else:
            raise TypeError(f"draw_contours takes a ContourObject or a list/tuple of ContourObject yet found "
                            f"{type(contours)}")

    def crop(self, height_min, height_max, width_min, width_max, relative=True, new_image=False):
        """
        Cropping can be relative or actual. If relative, each value represents a 0.0 - 1.0 range that acts as a
        percentage that the height and width will be cropped by. Otherwise, the actual pixel starting and ending values
        will be the input which should be in a range of 0-width/height max.
        """
        if relative:
            width = self.width
            height = self.height
        else:
            width = 1
            height = 1

        image = self.image.copy()
        crop = image[int(height * height_min):int(height * height_max), int(width * width_min):int(width * width_max)]

        # If we want to know where the crop points started, we can return these values
        return self._update_or_export(crop, new_image)

    def overlay_image(self, image_to_overlay, y_start, x_start, new_image=False):
        """
        This overlays a smaller image onto the current image, based on starting y and x position of the overlay.
        """
        original = self.image.copy()

        if isinstance(image_to_overlay, ImageObject):
            overlay = image_to_overlay
        else:
            overlay = ImageObject(image_to_overlay)

        original[y_start: y_start + overlay.height, x_start: x_start + overlay.width] = overlay.image

        return self._update_or_export(original, new_image)

    def overlay_additive(self, additive_image, new_image=False):
        """
        Overlays an image ontop of this image addatively, meaning any pixels in the new image will take precedence over
        the old one

        :param additive_image: ImageObject to add to this image
        :type additive_image: ImageObject

        :param new_image: If you want to return a new image or not
        :type new_image: bool
        """
        img_copy = self._create_temp_image()

        # Create an alpha mask of the overlay, then create an inverted copy
        alpha = additive_image.mask_alpha(True)
        inv = alpha.invert(True)

        # Isolate the area from the current copy that is not in the mask and vice versa
        front = cv2.bitwise_and(img_copy, img_copy, mask=inv.image)
        back = cv2.bitwise_and(additive_image.image, additive_image.image, mask=alpha.image)

        # Then add the areas together and mask them into the copy before updating the new image
        dst = cv2.add(front, back)
        img_copy[0:additive_image.height, 0:additive_image.width] = dst

        return self._update_or_export(img_copy, new_image)

    def extend_bounds(self, uniform=True, size=1, top=1, bottom=1, left=1, right=1, colour=(0, 0, 0), new_image=False):
        """
        This will extend the bounds of the image, if uniform is selected then you only need to adjust size and all
        borders will extend by that amount. Otherwise you can find tweak the size increase through the top, bottom,
        left, right parameters.
        """
        if uniform:
            output_border = cv2.copyMakeBorder(self.image, size, size, size, size, cv2.BORDER_CONSTANT, value=colour)
        else:
            output_border = cv2.copyMakeBorder(self.image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=colour)

        return self._update_or_export(output_border, new_image)

    def mask_on_colour_range(self, lower_thresh, upper_thresh, new_image=False):
        """
        Isolate shapes within a given bgr range.
        """
        return self._update_or_export(cv2.inRange(self._create_temp_image(), lower_thresh, upper_thresh), new_image)

    def mask_on_image(self, mask, new_image=False):
        """
        This will use another image as a mask for this image. Can be an ImageObject or any cv2 compatible image.
        """
        if isinstance(mask, ImageObject):
            masked = cv2.bitwise_and(self.image, self.image, mask=mask.image)
        else:
            masked = cv2.bitwise_and(self.image, self.image, mask=mask)

        return self._update_or_export(masked, new_image)

    def mask_alpha(self, new_image=False):
        """
        Takes a 4 channel image and returns the alpha channel as a mask
        """
        _, mask = cv2.threshold(self.image[:, :, 3], 0, 255, cv2.THRESH_BINARY)
        return self._update_or_export(mask, new_image)

    def threshold_binary(self, binary_threshold, binary_mode="binary", binary_max=255, new_image=False):
        """
        Create or push the image to a binary black on white image based on a threshold of mono pixel values.
        """
        binary_values = {"binary": 0, "binary_inv": 1, "trunc": 2, "to_zero": 3, "to_zero_inv": 4}
        binary_mode = key_return("binary_threshold", "binary_mode", binary_values, binary_mode)

        _, threshold_image = cv2.threshold(self.image, binary_threshold, binary_max, binary_mode)

        return self._update_or_export(threshold_image, new_image)

    def threshold_adaptive(self, assignment_value=255, gaussian_adaptive=True, binary_mode="binary",
                           neighborhood_size=51, subtract_constant=20, new_image=False):
        """
        This will apply by default a gaussian adaptive threshold using the binary method
        """
        # Set binary mode
        binary_values = {"binary": 0, "binary_inv": 1, "trunc": 2, "to_zero": 3, "to_zero_inv": 4}
        binary_mode = key_return("adaptive_threshold", "binary_mode", binary_values, binary_mode)

        # Set adaptive method
        if gaussian_adaptive:
            adaptive_mode = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        else:
            adaptive_mode = cv2.ADAPTIVE_THRESH_MEAN_C

        thresh = cv2.adaptiveThreshold(self._create_temp_image(colour=False), assignment_value, adaptive_mode,
                                       binary_mode, neighborhood_size, subtract_constant)

        return self._update_or_export(thresh, new_image)

    def perspective_transform(self, clockwise_points, new_image=False):
        """
        This will apply a perspective transformation on a image based on set of points given in order of:

        bottom_left, bottom_right, top_right, top_left
        """
        bottom_left, bottom_right, top_right, top_left = clockwise_points

        # 2) Set output dimensions
        diff_x = int(bottom_left[0] - bottom_right[0])
        diff_y = int(bottom_right[1] - top_right[1])

        # 3)Set output points
        out_top_left = (0, 0)
        out_top_right = (abs(diff_x), 0)
        out_bottom_left = (0, diff_y)
        out_bottom_right = (abs(diff_x), diff_y)

        # 4) Calculate transformation matrix
        pts1 = np.float32([[top_left], [top_right], [bottom_left], [bottom_right]])
        pts2 = np.float32([[out_top_left], [out_top_right], [out_bottom_left], [out_bottom_right]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        # 5) Apply the matrix transform on these points lists
        return self._update_or_export(cv2.warpPerspective(self.image, matrix, (abs(diff_x), diff_y)), new_image)

    def blur(self, blur_size, new_image=False):
        """
        Blur the image
        """

        return self._update_or_export(cv2.blur(self.image, (blur_size, blur_size)), new_image)

    def blur_gaussian(self, blur_size, sig_x=0, sig_y=0, new_image=False):
        """
        Blur using gaussian filter
        """
        # blur dimension should be odd
        if (blur_size % 2) == 0:
            blur_size += 1

        return self._update_or_export(cv2.GaussianBlur(self.image, (blur_size, blur_size), sig_x, sigmaY=sig_y),
                                      new_image)

    def resize(self, scale, scale_y=None, new_image=False):
        """
        Rescale an image by a float representation of a percentage

        :param scale: A float to scale an image by
        :type scale_y: float

        :param scale_y: An optional float for scaling on y to a different amount of x.
        :type scale_y: None | float

        :param new_image: If you want to return a new image or not
        :type new_image: bool
        """

        if scale_y:
            self._update_or_export(cv2.resize(self.image, (0, 0), fx=scale, fy=scale_y), new_image)
        else:
            self._update_or_export(cv2.resize(self.image, (0, 0), fx=scale, fy=scale), new_image)

    def match_on_image(self, match_image, match_type=5):
        """
        Match this image to another

        Notes
        -----
        See https://docs.opencv.org/master/df/dfb/group__imgproc__object.html#ga3a7850640f1fe1f58fe91a2d7583695d
        for options of match tpye and mathamaticas behind the matching algoethrim

        :param match_image: ImageObject to match against or an numpy array
        :type match_image: ImageObject | np.ndarray

        :param match_type: cv2 Template match method, defaults to TM_CCOEFF_NORMED
        :type match_type: int

        :return: Numpy array of row and column ids of match
        :rtype: np.ndarray
        """
        if isinstance(match_image, ImageObject):
            return cv2.matchTemplate(self.image, match_image.image, match_type)
        else:
            return cv2.matchTemplate(self.image, match_image, match_type)
