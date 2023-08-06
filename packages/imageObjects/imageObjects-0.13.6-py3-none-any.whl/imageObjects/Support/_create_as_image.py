from imageObjects.ImageObject import ImageObject

from pathlib import Path
import numpy as np
import textwrap
import cv2


def load_image(path_to_image, channels_to_load=3):
    """
    Loads an image into a cv2 numpy array to be used within an image object

    :param path_to_image: Path to the image you want to load
    :type path_to_image: str | Path

    :param channels_to_load: Number of channels to load, can take the values of 3 for colour or 4 for png's with alpha.
    :type channels_to_load: int

    :return: cv2 loaded image of numpy arrays
    """

    assert Path(path_to_image).exists(), f"Path to image is invalid: {path_to_image}"

    # CV2 doesn't like pathlib
    if isinstance(path_to_image, Path):
        path_to_image = str(path_to_image.absolute())

    if channels_to_load == 1:
        return cv2.imread(path_to_image, 0)

    elif channels_to_load == 3:
        return cv2.imread(path_to_image)

    elif channels_to_load == 4:
        return cv2.imread(path_to_image, cv2.IMREAD_UNCHANGED)

    else:
        raise IndexError(f"Load image can load images colour (3), or colour with alpha (4), yet was "
                         f"provided {channels_to_load}")


def create_blank(width, height):
    """
    If the user has not defined anything, they can create a new image of zeros of size width-height
    :rtype: ImageObject
    """
    return ImageObject(np.zeros((width, height), dtype=np.uint8))


def _construct_text_box_image(wrapped_text, font, font_size, font_thickness):
    """
    This method creates the box by extracting the width and height of each line of text, as well as the height of
    the text objects themselves to use as a gap, and creates an ImageObject in which to put the text on.
    """
    width_bounds = []
    height_total = 0
    width_gap = 0
    for index, line in enumerate(wrapped_text):

        # Get the widths and the gap, which we will use to determine the width of the box
        (width, height), line_gap = cv2.getTextSize(line, font, font_size, font_thickness)
        width_bounds.append(width)
        width_gap = line_gap

        # The first and last lines we want to have a gap above and below, otherwise just below
        if index == 0:
            height_total += (height + (line_gap * 2))
        elif 0 < index < len(wrapped_text) - 1:
            height_total += (height + line_gap)
        else:
            height_total += (height + (line_gap * 2))

    width = max(width_bounds) + width_gap
    return create_blank(width, height_total)


def create_text_box(text, font, wrap_length, font_size=5, font_thickness=5, text_colour=(0, 0, 0),
                    background_colour=(255, 255, 255)):
    """
    Create a text box, containing the text that the user specified.

    Adapted this stack exchange post : shorturl.at/jrsy7

    """

    # Create the text at a given level of wrapping
    wrapped_text = textwrap.wrap(text, width=wrap_length)

    # Create the text box and colour it to the background_colour
    text_box = _construct_text_box_image(wrapped_text, font, font_size, font_thickness)
    text_box.change_to_colour()
    text_box.change_a_colour((0, 0, 0), background_colour)

    for i, line in enumerate(wrapped_text):
        (width, height), line_gap = cv2.getTextSize(line, font, font_size, font_thickness)

        line_space = height + line_gap
        y = int(line_gap + height) + i * line_space
        x = int((text_box.width - width) / 2)

        cv2.putText(text_box.image, line, (x, y), font, font_size, text_colour, font_thickness,
                    lineType=cv2.LINE_AA)
    return text_box
