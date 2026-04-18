from glasscut.exceptions import MagnificationError


def build_magnification_mapping(
    base_magnification: int | float, num_levels: int
) -> list[int | float]:
    """Build a list of available magnifications from pyramid levels.

    Parameters
    ----------
    base_magnification : int | float
        The magnification at level 0 (e.g., 40, 20)
    num_levels : int
        Number of pyramid levels in the slide

    Returns
    -------
    list[int | float]
        List of magnifications in descending order (e.g., [40.0, 20.0, 10.0, 5.0])
    """
    magnifications: list[int | float] = []
    for i in range(num_levels):
        downsample = 2**i
        mag = base_magnification / downsample
        magnifications.append(mag)
    return sorted(magnifications, reverse=True)


def magnification_to_level(
    magnification: int | float, available_magnifications: list[int | float]
) -> int:
    """Convert magnification to the pyramid level.

    This function performs EXACT matching - the requested magnification must
    be available in the slide, otherwise an error is raised.

    Parameters
    ----------
    magnification : int | float
        Target magnification (e.g., 40, 20, 10, 5)
    available_magnifications : list[int | float]
        List of available magnifications for the slide (in descending order)

    Returns
    -------
    int
        The level index corresponding to the magnification

    Raises
    ------
    MagnificationError
        If the requested magnification is not available on this slide
    """
    if not available_magnifications:
        raise MagnificationError("No available magnifications in slide")

    # Check for exact match (with tolerance for floating point)
    tolerance = 0.01
    for level, available_mag in enumerate(available_magnifications):
        if abs(available_mag - magnification) < tolerance:
            return level

    # No match found
    raise MagnificationError(
        f"Magnification {magnification}x is not available on this slide. "
        f"Available magnifications: {available_magnifications}"
    )
