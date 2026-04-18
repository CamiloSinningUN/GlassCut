from abc import ABC, abstractmethod

import numpy as np
from PIL import Image


class TissueDetector(ABC):
    """Base class for tissue detection strategies.

    Implement this class to support custom tissue detection methods
    (e.g., CNN-based, paper-specific approaches).
    """

    @abstractmethod
    def detect(self, image: Image.Image) -> np.ndarray:
        """Detect tissue in an image and return a binary mask.

        Parameters
        ----------
        image : Image.Image
            Input image in RGB format

        Returns
        -------
        np.ndarray
            Binary tissue mask (0 = background, 1 = tissue)
        """
        pass