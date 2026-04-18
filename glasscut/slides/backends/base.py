"""Abstract backend interface for slide reading."""

from abc import ABC, abstractmethod
from pathlib import Path
from types import TracebackType

import PIL.Image


class SlideBackend(ABC):
    """Abstract base class for slide reading backends.

    This defines the interface that all slide backends must implement.
    Backends handle the actual reading of slide files and tile extraction.
    """

    @abstractmethod
    def open(self, path: str | Path) -> None:
        """Open a slide file.

        Parameters
        ----------
        path : str | Path
            Path to the slide file
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the slide and free resources."""
        pass

    @property
    @abstractmethod
    def dimensions(self) -> tuple[int, int]:
        """Get slide dimensions at level 0 (width, height).

        Returns
        -------
        tuple[int, int]
            Width and height in pixels at highest magnification
        """
        pass

    @property
    @abstractmethod
    def properties(self) -> dict[str, str]:
        """Get slide metadata/properties.

        Returns
        -------
        dict[str, str]
            Dictionary of slide properties
        """
        pass

    @property
    @abstractmethod
    def num_levels(self) -> int:
        """Get number of pyramid levels.

        Returns
        -------
        int
            Number of pyramid levels
        """
        pass

    @abstractmethod
    def read_region(
        self, location: tuple[int, int], level: int, size: tuple[int, int]
    ) -> PIL.Image.Image:
        """Read a region/tile from the slide.

        Parameters
        ----------
        location : tuple[int, int]
            (x, y) coordinates at level 0
        level : int
            Pyramid level to read from
        size : tuple[int, int]
            (width, height) of the tile to read in pixels

        Returns
        -------
        PIL.Image.Image
            The tile image in RGB format
        """
        pass

    @abstractmethod
    def get_thumbnail(self, size: tuple[int, int]) -> PIL.Image.Image:
        """Get thumbnail of the slide.

        Parameters
        ----------
        size : tuple[int, int]
            Maximum size of the thumbnail (width, height)

        Returns
        -------
        PIL.Image.Image
            Thumbnail image
        """
        pass

    @property
    @abstractmethod
    def mpp(self) -> float:
        """Get microns per pixel at base magnification.

        Returns
        -------
        float
            Microns per pixel

        Raises
        ------
        SlidePropertyError
            If MPP cannot be determined from slide metadata
        """
        pass

    @property
    @abstractmethod
    def base_magnification(self) -> int | float:
        """Get the base magnification (objective power) of the slide.

        This is the magnification at level 0 (highest resolution).
        For example, 40x, 20x, 10x, etc.

        Returns
        -------
        int | float
            Base magnification value

        Raises
        ------
        SlidePropertyError
            If base magnification cannot be determined from slide metadata
        """
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit."""
        self.close()
