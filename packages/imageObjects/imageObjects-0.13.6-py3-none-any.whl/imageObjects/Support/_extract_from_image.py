from imageObjects.ContourObject import ContourObject

from vectorObjects.DefinedVectors import Vector2D
import cv2


def key_return(method_name, dict_name, dict_of_values, key):
    """
    Many of our operations require a mode that is set via a dict, this will return the mode requested if it exists
    or raise a key error with information to the user of what they submitted vs what was expected.
    """
    try:
        return dict_of_values[key]
    except KeyError:
        raise KeyError(f"{method_name}s {dict_name} only takes {list(dict_of_values.keys())} but found {key}")


def draw_rounded_box(img, point1, point2, colour, thickness, radius, filled_percent):
    """
    Draw a rounded box on the image

    Adapted from: https://stackoverflow.com/questions/46036477/drawing-fancy-rectangle-around-face
    """

    # Set Points and the percentage between the corners to fill
    point1 = Vector2D(point1)
    point2 = Vector2D(point2)
    depth = int(((abs(point2.x - point1.x) / 2) - radius) * filled_percent)

    # If we are drawing on the ImageObject image set image to be self.image, else make a temp

    # Create Each of the four points
    # Top left
    cv2.line(img, (point1.x + radius, point1.y), (point1.x + radius + depth, point1.y), colour, thickness)
    cv2.line(img, (point1.x, point1.y + radius), (point1.x, point1.y + radius + depth), colour, thickness)
    cv2.ellipse(img, (point1.x + radius, point1.y + radius), (radius, radius), 180, 0, 90, colour, thickness)

    # Top right
    cv2.line(img, (point2.x - radius, point1.y), (point2.x - radius - depth, point1.y), colour, thickness)
    cv2.line(img, (point2.x, point1.y + radius), (point2.x, point1.y + radius + depth), colour, thickness)
    cv2.ellipse(img, (point2.x - radius, point1.y + radius), (radius, radius), 270, 0, 90, colour, thickness)

    # Bottom left
    cv2.line(img, (point1.x + radius, point2.y), (point1.x + radius + depth, point2.y), colour, thickness)
    cv2.line(img, (point1.x, point2.y - radius), (point1.x, point2.y - radius - depth), colour, thickness)
    cv2.ellipse(img, (point1.x + radius, point2.y - radius), (radius, radius), 90, 0, 90, colour, thickness)

    # Bottom right
    cv2.line(img, (point2.x - radius, point2.y), (point2.x - radius - depth, point2.y), colour, thickness)
    cv2.line(img, (point2.x, point2.y - radius), (point2.x, point2.y - radius - depth), colour, thickness)
    cv2.ellipse(img, (point2.x - radius, point2.y - radius), (radius, radius), 0, 0, 90, colour, thickness)
    return img


def calculate_alpha_beta(gray, clip_hist_percent):
    """
    This calculates the current alpha and beta values from an image

    From https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-
    of-a-sheet-of-paper
    """
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    previous = float(hist[0])
    accumulator = [previous]
    for index in range(1, hist_size):
        previous = previous + float(hist[index])
        accumulator.append(previous)

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum / 100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    return alpha, beta


def skeletonize_points(normalised_image, method):
    """
    Extract the points that make up the skeleton of the image via skimage
    """
    try:
        from skimage.morphology import skeletonize as ski_ske

        # Extract the binary points
        binary_points = ski_ske(normalised_image, method=method)

        # Return the list of points
        return [[ci, ri] for ri, row in enumerate(binary_points) for ci, column in enumerate(row) if column]

    except ImportError:
        raise ImportError("Skeletonise points requires sci-kit images")


def find_contours(gray, retrieval_mode, simple_method=True, hierarchy_return=False):
    """
    Find contours within the current image. Since find contours only works on mono channel images, if the current
    image is a colour image a new image is create that will not change the one in memory so it is not necessary to
    change the image to gray manually.
    retrieval_mode
    ---------------
    retrieval_mode can take on of the following values: external, list, ccomp, tree, floodfill
    simple_method
    --------------
    Simple methods will only use the extremes, so for a straight line it will store the first and last point. If you
    turn this off it will keep all the points on the line but this can lead to a very large over head so it is not
    recommend unless you have a specific need for all those points.
    hierarchy_return
    ----------------
    If you don't want to return the hierarchy you can leave this as default, otherwise set it to true
    """
    # Set retrieval mode
    retrieval_values = {"external": 0, "list": 1, "ccomp": 2, "tree": 3, "floodfill": 4}
    retrieval = key_return("find_contours", "retrieval_mode", retrieval_values, retrieval_mode)

    # Setup of extraction methods
    if simple_method:
        approx = cv2.CHAIN_APPROX_SIMPLE
    else:
        approx = cv2.CHAIN_APPROX_NONE

    # Look for contours base on the setup
    contours, hierarchy = cv2.findContours(gray, retrieval, approx)

    # If we find any contours, return the contours and the hierarchy if requested
    if len(contours) > 0:
        if hierarchy_return:
            return [ContourObject(cnt) for cnt in contours], hierarchy
        else:
            return [ContourObject(cnt) for cnt in contours]
    else:
        if hierarchy_return:
            return None, None
        else:
            return None


def largest_contour(gray):
    """Extract the largest element of the image as a contour"""
    contour_list = find_contours(gray, "external")
    if not contour_list or len(contour_list) == 0:
        print(f"Warning: No contours found!")
    elif len(contour_list) == 1:
        return contour_list[0]
    else:
        area = [c.area for c in contour_list]
        return contour_list[area.index(max(area))]


def find_overlap_center(image, masking_image):
    """Find the centroid of the overlap between two images via masking"""
    overlap = largest_contour(image.mask_on_image(masking_image, True).image)
    if not overlap:
        return None

    # todo Handle failing to find centeroid?
    else:
        return Vector2D((overlap.bottom.x + overlap.top.x) / 2, (overlap.bottom.y + overlap.top.y) / 2)
