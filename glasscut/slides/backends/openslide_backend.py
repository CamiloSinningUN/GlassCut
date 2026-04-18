"""OpenSlide backend for slide reading (CPU-based)."""

from pathlib import Path
from typing import Dict, Tuple, Union

import PIL.Image
import openslide

from glasscut.exceptions import SlidePropertyError
from .base import SlideBackend


class OpenSlideBackend(SlideBackend):
    """OpenSlide-based backend for reading whole slide images.

    This is the CPU-based fallback backend. It uses the OpenSlide library
    to read various slide formats (SVS, TIFF, etc.).
    """

    def __init__(self) -> None:
        self._slide = None
        self._path = None

    def open(self, path: Union[str, Path]) -> None:
        """Open a slide file using OpenSlide.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the slide file

        Raises
        ------
        FileNotFoundError
            If the slide file does not exist
        BackendError
            If OpenSlide cannot open the file
        """
        self._path = str(path) if isinstance(path, Path) else path

        try:
            self._slide = openslide.open_slide(self._path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Slide file not found: {self._path}")
        except Exception as e:
            raise RuntimeError(f"Failed to open slide with OpenSlide: {e}")

    def close(self) -> None:
        """Close the slide."""
        if self._slide is not None:
            self._slide.close()
            self._slide = None

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Get slide dimensions at level 0.

        Returns
        -------
        Tuple[int, int]
            (width, height) at highest magnification
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")
        return self._slide.dimensions

    @property
    def properties(self) -> Dict[str, str]:
        """Get slide metadata properties.

        Returns
        -------
        Dict[str, str]
            Dictionary of slide properties
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")
        return dict(self._slide.properties)

    @property
    def num_levels(self) -> int:
        """Get number of pyramid levels.

        Returns
        -------
        int
            Number of pyramid levels
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")
        return len(self._slide.level_dimensions)

    def read_region(
        self, location: Tuple[int, int], level: int, size: Tuple[int, int]
    ) -> PIL.Image.Image:
        """Read a region/tile from the slide.

        Parameters
        ----------
        location : Tuple[int, int]
            (x, y) coordinates at level 0
        level : int
            Pyramid level to read from
        size : Tuple[int, int]
            (width, height) of the tile in pixels

        Returns
        -------
        PIL.Image.Image
            The tile image in RGB format
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")

        image = self._slide.read_region(location, level, size)
        return image.convert("RGB")

    def get_thumbnail(self, size: Tuple[int, int]) -> PIL.Image.Image:
        """Get thumbnail of the slide.

        Parameters
        ----------
        size : Tuple[int, int]
            Maximum size of the thumbnail (width, height)

        Returns
        -------
        PIL.Image.Image
            Thumbnail image in RGB format
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")

        thumbnail = self._slide.get_thumbnail(size)
        return thumbnail.convert("RGB")

    @property
    def mpp(self) -> float:
        """Get microns per pixel at base magnification.

        Returns
        -------
        float
            Microns per pixel (MPP)

        Raises
        ------
        SlidePropertyError
            If MPP cannot be determined from metadata
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")

        props = self.properties

        # Try common MPP property names
        if "openslide.mpp-x" in props:
            return float(props["openslide.mpp-x"])

        if "aperio.MPP" in props:
            return float(props["aperio.MPP"])

        if (
            "tiff.XResolution" in props
            and props.get("tiff.ResolutionUnit") == "centimeter"
        ):
            return 1e4 / float(props["tiff.XResolution"])

        raise SlidePropertyError(
            f"Could not determine MPP from slide properties. "
            f"Available properties: {list(props.keys())}"
        )

    @property
    def base_magnification(self) -> int | float:
        """Get the base magnification (objective power) of the slide.

        Returns
        -------
        int | float
            Base magnification value

        Raises
        ------
        SlidePropertyError
            If base magnification cannot be determined from metadata
        """
        if self._slide is None:
            raise RuntimeError("Slide not opened")

        props = self.properties

        # Try common objective power property names (OpenSlide)
        if "openslide.objective-power" in props:
            try:
                return float(props["openslide.objective-power"])
            except ValueError:
                pass

        # Try Aperio format
        if "aperio.AppMag" in props:
            try:
                return float(props["aperio.AppMag"])
            except ValueError:
                pass

        # Try generic magnification properties
        if "magnification" in props:
            try:
                return float(props["magnification"])
            except ValueError:
                pass

        # If all else fails, raise an error
        raise SlidePropertyError(
            f"Could not determine base magnification from slide properties. "
            f"Available properties: {list(props.keys())}"
        )
