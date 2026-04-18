"""Slide reading backends."""

from .base import SlideBackend
from .cucim_backend import CuCimBackend
from .openslide_backend import OpenSlideBackend

__all__ = ["SlideBackend", "OpenSlideBackend", "CuCimBackend"]
