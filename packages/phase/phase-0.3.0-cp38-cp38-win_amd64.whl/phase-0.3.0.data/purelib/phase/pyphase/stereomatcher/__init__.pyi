"""stereo matcher"""
from __future__ import annotations
import phase.pyphase.stereomatcher
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "AbstractStereoMatcher",
    "STEREO_MATCHER_BM",
    "STEREO_MATCHER_I3DRSGM",
    "STEREO_MATCHER_SGBM",
    "StereoBM",
    "StereoI3DRSGM",
    "StereoMatcherComputeResult",
    "StereoMatcherType",
    "StereoParams",
    "StereoSGBM",
    "createStereoMatcher"
]


class AbstractStereoMatcher():
    """
    Abstract base class for building stereo matcher
    classes. Includes functions/structures common across
    all stereo matchers. A stereo matcher takes a two images
    (left and right) and calculates to pixel disparity of features.
    The produces a disparity value for each pixel which can be
    used to generate depth.
    """
    def compute(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> StereoMatcherComputeResult: 
        """
        Compute stereo matching
        Generates disparity from left and right images

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> StereoMatcherComputeResult: 
        """
        Get results from threaded compute process
        Should be used with startComputeThread()

        Returns
        -------
        StereoMatcherComputeResult
            Result from compute
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    @staticmethod
    def setComputeThreadCallback(*args, **kwargs) -> typing.Any: 
        """
        Set callback function to run when compute thread completes
        Should be used with startComputeThread()
        Useful as an external trigger that compute is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def startComputeThread(self, left_image: numpy.ndarray, left_image: numpy.ndarray) -> None: 
        """
        Start compute thread
        Generates disparity from left and right images
        Use getComputeThreadResult() to get results of compute

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoBM():
    """
    OpenCV's block matcher for generting disparity from stereo images.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Initalise Stereo matcher and set default matching parameters



        Initalise Stereo matcher and use provided StereoParams to set matching parameters
        """
    @typing.overload
    def __init__(self, stereo_params: StereoParams) -> None: ...
    def compute(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> StereoMatcherComputeResult: 
        """
        Compute stereo matching
        Generates disparity from left and right images

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> StereoMatcherComputeResult: 
        """
        Get results from threaded compute process
        Should be used with startComputeThread()

        Returns
        -------
        StereoMatcherComputeResult
            Result from compute
        """
    def getMinDisparity(self) -> int: 
        """
        Get minimum disparity value

        Returns
        -------
        value : int
            Value of minimum disparity
        """
    def getNumDisparities(self) -> int: 
        """
        Get number of disparities

        Returns
        -------
        value : int
            Value of number of disparities
        """
    def getWindowSize(self) -> int: 
        """
        Get window size value

        Returns
        -------
        value : int
            Value of window size
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    @staticmethod
    def setComputeThreadCallback(*args, **kwargs) -> typing.Any: 
        """
        Set callback function to run when compute thread completes
        Should be used with startComputeThread()
        Useful as an external trigger that compute is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setMinDisparity(self, value: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, value: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setWindowSize(self, value: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> None: 
        """
        Start compute thread
        Generates disparity from left and right images
        Use getComputeThreadResult() to get results of compute

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoI3DRSGM():
    """
    I3DRS's stereo semi-global matcher for generting disparity from stereo images.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Initalise Stereo matcher and set default matching parameters



        Initalise Stereo matcher and use provided StereoParams to set matching parameters
        """
    @typing.overload
    def __init__(self, stereo_params: StereoParams) -> None: ...
    def compute(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> StereoMatcherComputeResult: 
        """
        Compute stereo matching
        Generates disparity from left and right images

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def enableInterpolation(self, enable: bool) -> None: 
        """
        To enable interpolation

        Parameters
        ----------
        enable : bool
            Set True to enable interpolation
        """
    def enableOcclusionDetection(self, enable: bool) -> None: 
        """
        To enable occlusion detection

        Parameters
        ----------
        enable : bool
            Set True to enable occlusion detection
        """
    def enableOcclusionInterpolation(self, enable: bool) -> None: 
        """
        To enable occlusion interpolation

        Parameters
        ----------
        enable : bool
            Set True to enable occlusion interpolation
        """
    def enableSubpixel(self, enable: bool) -> None: 
        """
        To enable subpixel

        Parameters
        ----------
        enable : bool
            Set True to enable subpixel
        """
    def getComputeThreadResult(self) -> StereoMatcherComputeResult: 
        """
        Get results from threaded compute process
        Should be used with startComputeThread()

        Returns
        -------
        StereoMatcherComputeResult
            Result from compute
        """
    def getMinDisparity(self) -> int: 
        """
        Get minimum disparity value

        Returns
        -------
        value : int
            Value of minimum disparity
        """
    def getNumDisparities(self) -> int: 
        """
        Get number of disparities

        Returns
        -------
        value : int
            Value of number of disparities
        """
    def getSpeckleMaxDiff(self) -> float: 
        """
        Get speckle maximum difference

        Returns
        -------
        value : int
            Value of speckle maximum difference
        """
    def getSpeckleMaxSize(self) -> int: 
        """
        Get speckle maximum size

        Returns
        -------
        value : int
            Value of speckle maximum size
        """
    def getWindowSize(self) -> int: 
        """
        Get window size value

        Returns
        -------
        value : int
            Value of window size
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    def isInterpolationEnabled(self) -> bool: 
        """
        Get enable/disable status of interpolation

        Returns
        -------
        bool
            true if enabled
        """
    @staticmethod
    def isLicenseValid() -> bool: 
        """
        Check if the I3DRSGM license is valid

        Returns
        -------
        bool
            True if license is valid
        """
    def isOcclusionDetectionEnabled(self) -> bool: 
        """
        Get enable/disable status of occlusion detection

        Returns
        -------
        bool
            true if enabled
        """
    def isOcclusionInterpolationEnabled(self) -> bool: 
        """
        Get enable/disable status of occlusion interpolation

        Returns
        -------
        bool
            true if enabled
        """
    def isSubpixelEnabled(self) -> bool: 
        """
        Get enable/disable status of subpixel refinement

        Returns
        -------
        bool
            true if enabled
        """
    @staticmethod
    def setComputeThreadCallback(*args, **kwargs) -> typing.Any: 
        """
        Set callback function to run when compute thread completes
        Should be used with startComputeThread()
        Useful as an external trigger that compute is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setMinDisparity(self, value: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, value: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setSpeckleMaxDiff(self, value: float) -> None: 
        """
        Set speckle maximum difference

        Parameters
        ----------
        value : float
            Value of speckle maximum difference
        """
    def setSpeckleMaxSize(self, value: int) -> None: 
        """
        Set speckle maximum size

        Parameters
        ----------
        value : int
            Value of speckle maximum size
        """
    def setWindowSize(self, value: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> None: 
        """
        Start compute thread
        Generates disparity from left and right images
        Use getComputeThreadResult() to get results of compute

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
class StereoMatcherComputeResult():
    """
    Struture to store the result from a stereo match. Used in the stereo matcher classes.
    """
    def __init__(self, valid: bool, disparity: numpy.ndarray) -> None: 
        """
        StereoMatcherComputeResult constructor
        """
    @property
    def disparity(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @disparity.setter
    def disparity(self, arg0: numpy.ndarray) -> None:
        pass
    @property
    def valid(self) -> bool:
        """
        :type: bool
        """
    @valid.setter
    def valid(self, arg0: bool) -> None:
        pass
    pass
class StereoMatcherType():
    """
            Enum to indicate stereo matcher type. Used in stereo matcher class to select which matcher to use.

            

    Members:

      STEREO_MATCHER_BM

      STEREO_MATCHER_SGBM

      STEREO_MATCHER_I3DRSGM
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    STEREO_MATCHER_BM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_BM: 0>
    STEREO_MATCHER_I3DRSGM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>
    STEREO_MATCHER_SGBM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_SGBM: 1>
    __members__: dict # value = {'STEREO_MATCHER_BM': <StereoMatcherType.STEREO_MATCHER_BM: 0>, 'STEREO_MATCHER_SGBM': <StereoMatcherType.STEREO_MATCHER_SGBM: 1>, 'STEREO_MATCHER_I3DRSGM': <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>}
    pass
class StereoParams():
    """
    Struture to store stereo parameters
    """
    def __init__(self, matcherType: StereoMatcherType, windowSize: int, minDisparity: int, numDisparities: int, interpolation: bool) -> None: 
        """
        Stereo parameters contain matcherType, windowSize, minDisparity, numDisparities, interpolation
        """
    @property
    def interpolation(self) -> bool:
        """
        :type: bool
        """
    @interpolation.setter
    def interpolation(self, arg0: bool) -> None:
        pass
    @property
    def matcherType(self) -> StereoMatcherType:
        """
        :type: StereoMatcherType
        """
    @matcherType.setter
    def matcherType(self, arg0: StereoMatcherType) -> None:
        pass
    @property
    def minDisparity(self) -> int:
        """
        :type: int
        """
    @minDisparity.setter
    def minDisparity(self, arg0: int) -> None:
        pass
    @property
    def numDisparities(self) -> int:
        """
        :type: int
        """
    @numDisparities.setter
    def numDisparities(self, arg0: int) -> None:
        pass
    @property
    def windowSize(self) -> int:
        """
        :type: int
        """
    @windowSize.setter
    def windowSize(self, arg0: int) -> None:
        pass
    pass
class StereoSGBM():
    """
    OpenCV's semi-global block matcher for generting disparity from stereo images
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Initalise Stereo matcher and set default matching parameters



        Initalise Stereo matcher and use provided StereoParams to set matching parameters
        """
    @typing.overload
    def __init__(self, stereo_params: StereoParams) -> None: ...
    def compute(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> StereoMatcherComputeResult: 
        """
        Compute stereo matching
        Generates disparity from left and right images

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    def getComputeThreadResult(self) -> StereoMatcherComputeResult: 
        """
        Get results from threaded compute process
        Should be used with startComputeThread()

        Returns
        -------
        StereoMatcherComputeResult
            Result from compute
        """
    def getMinDisparity(self) -> int: 
        """
        Get minimum disparity value

        Returns
        -------
        value : int
            Value of minimum disparity
        """
    def getNumDisparities(self) -> int: 
        """
        Get number of disparities

        Returns
        -------
        value : int
            Value of number of disparities
        """
    def getWindowSize(self) -> int: 
        """
        Get window size value

        Returns
        -------
        value : int
            Value of window size
        """
    def isComputeThreadRunning(self) -> bool: 
        """
        Check if compute thread is running

        Returns
        -------
        bool
            True is compute thread is running
        """
    @staticmethod
    def setComputeThreadCallback(*args, **kwargs) -> typing.Any: 
        """
        Set callback function to run when compute thread completes
        Should be used with startComputeThread()
        Useful as an external trigger that compute is complete
        and results can be retrieved.

        Parameters
        ----------
        f : callback
        """
    def setMinDisparity(self, value: int) -> None: 
        """
        Set minimum disparity value

        Parameters
        ----------
        value : int
            Desired value of minimum disparity value
        """
    def setNumDisparities(self, value: int) -> None: 
        """
        Set number of disparities

        Parameters
        ----------
        value : int
            Desired value of number of disparities
        """
    def setWindowSize(self, value: int) -> None: 
        """
        Set window size value

        Parameters
        ----------
        value : int
            Desired value of window size value
        """
    def startComputeThread(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> None: 
        """
        Start compute thread
        Generates disparity from left and right images
        Use getComputeThreadResult() to get results of compute

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image of stereo pair
        right_image : numpy.ndarray
            Right image of stereo pair
        """
    pass
@typing.overload
def createStereoMatcher(matcher_type: StereoMatcherType) -> AbstractStereoMatcher:
    """
    Create stereo matching from stereo matcher type




    Create stereo matching from stereo matcher parameters
    """
@typing.overload
def createStereoMatcher(stereo_params: StereoParams) -> AbstractStereoMatcher:
    pass
STEREO_MATCHER_BM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_BM: 0>
STEREO_MATCHER_I3DRSGM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_I3DRSGM: 2>
STEREO_MATCHER_SGBM: phase.pyphase.stereomatcher.StereoMatcherType # value = <StereoMatcherType.STEREO_MATCHER_SGBM: 1>
