from vectorObjects.DefinedVectors import Vector2D


def to_vector_2d(point):
    """Convert Point to Vector2D if it isn't already"""
    if isinstance(point, Vector2D):
        return point
    elif isinstance(point, (list, tuple)):
        x, y = point
        return Vector2D(x, y)
    else:
        raise TypeError(f"Expected Vector2D, Tuple, or List. Yet was given {type(point)}")
