"""
        pyPhase is a python wrapper package over I3DR's Phase library.
    """
from __future__ import annotations
import phase.pyphase
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "bgr2bgra",
    "bgr2rgba",
    "bgra2rgba",
    "calib",
    "cvMatIsEqual",
    "depth2xyz",
    "disparity2depth",
    "disparity2xyz",
    "flip",
    "getAPIVersionMajor",
    "getAPIVersionMinor",
    "getAPIVersionPatch",
    "getAPIVersionString",
    "normaliseDisparity",
    "readImage",
    "savePLY",
    "scaleImage",
    "showImage",
    "stereocamera",
    "stereomatcher",
    "toMono",
    "types",
    "xyz2depth"
]


def bgr2bgra(bgr: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to BGRA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        BGRA image
    """
def bgr2rgba(bgr: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to RGBA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def bgra2rgba(bgra: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGRA image to RGBA.

    Parameters
    ----------
    bgra : numpy.ndarray
        BGRA image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def cvMatIsEqual(mat1: numpy.ndarray, mat2: numpy.ndarray) -> bool:
    """
    Check if two numpy.ndarray objects are equal.

    Parameters
    ----------
    mat1 : numpy.ndarray
        First numpy.ndarray object
    mat2 : numpy.ndarray
        Second numpy.ndarray object

    Returns
    -------
    bool
        True if equal
    """
def depth2xyz(xyz: numpy.ndarray, hfov: float) -> numpy.ndarray:
    """
    Calculate Point cloud (xyz) from depth image.

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)
    hfov : float
        Horizontal field of view (degrees)

    Returns
    -------
    numpy.ndarray
        Point cloud (xyz)
    """
def disparity2depth(disparity: numpy.ndarray, Q: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Depth image
    """
def disparity2xyz(disparity: numpy.ndarray, Q: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate point cloud (xyz) from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Point clouds (xyz)
    """
def flip(image: numpy.ndarray, flip_code: int) -> numpy.ndarray:
    """
    Flip image horizontally or vertically based on flip code.

    Parameters
    ----------
    image : numpy.ndarray
        Image to flip
    flip_code : int
        Flip code (0 = horizontal, 1 = vertical)

    Returns
    -------
    numpy.ndarray
        Flipped image
    """
def getAPIVersionMajor() -> int:
    """
    Get major of Phase

    Returns
    -------
    value : int
    """
def getAPIVersionMinor() -> int:
    """
    Get minor of Phase

    Returns
    -------
    value : int
    """
def getAPIVersionPatch() -> int:
    """
    Get version patch of Phase

    Returns
    -------
    value : int
    """
def getAPIVersionString() -> str:
    """
    Get version of Phase

    Returns
    -------
    string : str
    """
def normaliseDisparity(disparity: numpy.ndarray) -> numpy.ndarray:
    """
    Normalise disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Dispairty image to normalise

    Returns
    -------
    numpy.ndarray
        Normalised disparity image
    """
def readImage(image_filepath: str) -> numpy.ndarray:
    """
    Read image from file.

    Parameters
    ----------
    image_filepath : str
        Filepath of image

    Returns
    -------
    numpy.ndarray
        Image
    """
def savePLY(ply_filepath: str, xyz: numpy.ndarray, rgb: numpy.ndarray) -> bool:
    """
    Save point cloud to PLY file.

    Parameters
    ----------
    ply_filepath : str
        Filepath of PLY file
    xyz : numpy.ndarray
        Point cloud (xyz)
    rgb : numpy.ndarray
        RGB image for point cloud colours

    Returns
    -------
    bool
        True if successful
    """
def scaleImage(image: numpy.ndarray, scale_factor: float) -> numpy.ndarray:
    """
    Scale image to a new size.

    Parameters
    ----------
    image : numpy.ndarray
        Image to scale
    scale_factor : float
        Scale factor to apply to image

    Returns
    -------
    numpy.ndarray
        Scaled image
    """
def showImage(window_name: str, image: numpy.ndarray) -> int:
    """
    Display image in GUI window.

    Parameters
    ----------
    window_name : str
        Name of window
    image : numpy.ndarray
        Point cloud (xyz)
    """
def toMono(image_in: numpy.ndarray, image_out: numpy.ndarray) -> bool:
    """
    Convert image to monochrome

    Parameters
    ----------
    image_in : numpy.ndarray
        Input image
    image_out : numpy.ndarray
        Mono output image
    """
def xyz2depth(xyz: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from point cloud (xyz).

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)

    Returns
    -------
    numpy.ndarray
        Depth image
    """
__version__ = '0.3.0'
