"""camera calibration"""
from __future__ import annotations
import phase.pyphase.calib
import typing
import numpy
import phase.pyphase.types
_Shape = typing.Tuple[int, ...]

__all__ = [
    "CHECKERBOARD",
    "CalibrationBoardType",
    "CalibrationFileType",
    "CalibrationSelection",
    "CameraCalibration",
    "INVALID_BOARD",
    "INVALID_YAML",
    "LEFT",
    "OPENCV_YAML",
    "RIGHT",
    "ROS_YAML",
    "StereoCameraCalibration"
]


class CalibrationBoardType():
    """
                Enum to indicate calibration board type.
                

    Members:

      CHECKERBOARD : 
                Checkerboard calibration board type

                

      INVALID_BOARD : 
                Invalid calibration board type

                
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
    CHECKERBOARD: phase.pyphase.calib.CalibrationBoardType # value = <CalibrationBoardType.CHECKERBOARD: 0>
    INVALID_BOARD: phase.pyphase.calib.CalibrationBoardType # value = <CalibrationBoardType.INVALID_BOARD: 1>
    __members__: dict # value = {'CHECKERBOARD': <CalibrationBoardType.CHECKERBOARD: 0>, 'INVALID_BOARD': <CalibrationBoardType.INVALID_BOARD: 1>}
    pass
class CalibrationFileType():
    """
                Enum to indicate calibration file type. OpenCV uses different YAML standard from ROS.
                

    Members:

      ROS_YAML : 
                ROS YAML calibration file type (YAML v1.2 used by ROS)

                

      OPENCV_YAML : 
                OpenCV YAML calibration file type (YAML v1.0 used by OpenCV)
                
                

      INVALID_YAML : 
                Invalid calibration file type
                
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
    INVALID_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.INVALID_YAML: 2>
    OPENCV_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.OPENCV_YAML: 1>
    ROS_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.ROS_YAML: 0>
    __members__: dict # value = {'ROS_YAML': <CalibrationFileType.ROS_YAML: 0>, 'OPENCV_YAML': <CalibrationFileType.OPENCV_YAML: 1>, 'INVALID_YAML': <CalibrationFileType.INVALID_YAML: 2>}
    pass
class CalibrationSelection():
    """
            Enum to indicate calibration from left or right camera/image

            

    Members:

      LEFT

      RIGHT
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
    LEFT: phase.pyphase.calib.CalibrationSelection # value = <CalibrationSelection.LEFT: 0>
    RIGHT: phase.pyphase.calib.CalibrationSelection # value = <CalibrationSelection.RIGHT: 1>
    __members__: dict # value = {'LEFT': <CalibrationSelection.LEFT: 0>, 'RIGHT': <CalibrationSelection.RIGHT: 1>}
    pass
class CameraCalibration():
    """
    Store and manipulate mono camera calibration data.
    """
    @typing.overload
    def __init__(self, calibration_filepath: str) -> None: 
        """
        Initalise camera calibration from calibration file.

        Parameters
        ----------
        calibration_filepath : str
            Stereo calibration file path location



        Initalise camera calibration using the values provided.

        Parameters
        ----------
        width : int
            Image width of camera
        height : int
            Image height of camera
        camera_matrix : numpy.ndarray
            Camera matrix of camera
        distortion_coefficients : numpy.ndarray
            Distortion coefficients of camera
        rectification_matrix : numpy.ndarray
            Rectification matrix of camera
        projection_matrix : numpy.ndarray
            Projection matrix of camera
        """
    @typing.overload
    def __init__(self, width: int, height: int, camera_matrix: numpy.ndarray, distortion_coefficients: numpy.ndarray, rectification_matrix: numpy.ndarray, projection_matrix: numpy.ndarray) -> None: ...
    @staticmethod
    def calibrationFromIdeal(width: int, height: int, pixel_pitch: float, focal_length: float, translation_x: float, translation_y: float) -> CameraCalibration: 
        """
        Create ideal calibration from camera information

        Parameters
        ----------
        width : int
            Image width of camera
        height : int
            Image height of camera
        pixel_pitch : float
            Pixel pitch of camera
        focal_length : float
            Focal length of camera
        translation_x : float
            Translation of principle point in X
        translation_y : float
            Translation of principle point in Y
        """
    def getCameraCX(self) -> float: 
        """
        Get camera principle point in X in calibration (in pixels)

        Returns
        -------
        cameraCX : float
            Principle point in X
        """
    def getCameraCY(self) -> float: 
        """
        Get camera principle point in Y in calibration (in pixels)

        Returns
        -------
        cameraCY : float
            Principle point in Y
        """
    def getCameraFX(self) -> float: 
        """
        Get camera focal length in X in calibration (in pixels)

        Returns
        -------
        cameraFX : float
            Focal length in X
        """
    def getCameraFY(self) -> float: 
        """
        Get camera focal length in Y in calibration (in pixels)

        Returns
        -------
        cameraFY : float
            Focal length in Y
        """
    def getCameraMatrix(self) -> numpy.ndarray: 
        """
        Get the camera matrix of calibration file

        Returns
        -------
        camera_matrix : numpy.ndarray                
            Camera matrix of calibration
        """
    def getDistortionCoefficients(self) -> numpy.ndarray: 
        """
        Get the distortion coefficients of calibration

        Returns
        -------
        distortion_coefficients : numpy.ndarray  
            Distortion coefficients of calibration
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get the downsample factor

        Returns
        -------
        value : float
            Value of downsample factor
        """
    def getImageHeight(self) -> int: 
        """
        Get the image height from calibration

        Returns
        -------
        height : int
            Value of image height from calibration
        """
    def getImageWidth(self) -> int: 
        """
        Get the image width from calibration

        Returns
        -------
        width : int
            Value of image width from calibration
        """
    def getProjectionCX(self) -> float: 
        """
        Get camera principle point in X in calibration projection (in pixels)

        Returns
        -------
        projectionCX : float
            Principle point in X
        """
    def getProjectionCY(self) -> float: 
        """
        Get camera principle point in Y in calibration projection (in pixels)

        Returns
        -------
        projectionCY : float
            Principle point in Y
        """
    def getProjectionFX(self) -> float: 
        """
        Get camera focal length in X in calibration projection (in pixels)

        Returns
        -------
        projectionFX : float
            Focal length in X
        """
    def getProjectionFY(self) -> float: 
        """
        Get camera focal length in Y in calibration projection (in pixels)

        Returns
        -------
        projectionFY : float
            Focal length in Y
        """
    def getProjectionMatrix(self) -> numpy.ndarray: 
        """
        Get the projection matrix of calibration

        Returns
        -------
        projection_matrix : numpy.ndarray  
            Projection matrix of calibration
        """
    def getProjectionTX(self) -> float: 
        """
        Get camera baseline in calibration projection (in pixels)

        Returns
        -------
        projectionTX : float
            Baseline
        """
    def getRectificationMatrix(self) -> numpy.ndarray: 
        """
        Get the rectification matrix of calibration file

        Returns
        -------
        rectification_matrix : numpy.ndarray  
            Rectification matrix of calibration
        """
    def isValid(self) -> bool: 
        """
        Check if loaded calibration is valid 

        Returns
        -------
        bool
            True if calibration is valid
        """
    def rectify(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> None: 
        """
        Rectify image based on calibration

        Parameters
        ----------
        left_image : numpy.ndarray
            Image to rectify
        right_image : numpy.ndarray
            Image to store rectified image
        """
    def setDownsampleFactor(self, value: float) -> None: 
        """
        Set the downsample factor

        Parameters
        ----------
        value : float
        """
    pass
class StereoCameraCalibration():
    """
    Store and manipulate stereo camera calibration data.
    """
    def __init__(self, left_calibration: CameraCalibration, right_calibration: CameraCalibration) -> None: 
        """
        Initalise stereo camera calibration using left and right calibration.

        Parameters
        ----------
        left_calibration : phase.pyphase.calib.CameraCalibration
            Left calibration file
        right_calibration : phase.pyphase.calib.CameraCalibration
            Right calibration file
        """
    @staticmethod
    def calibrationFromIdeal(width: int, height: int, pixel_pitch: float, focal_length: float, baseline: float) -> StereoCameraCalibration: 
        """
        Create ideal stereo calibration from camera information

        Parameters
        ----------
        width : int
            Image width of cameras
        height : int
            Image height of cameras
        pixel_pitch : float
            Pixel pitch of cameras
        focal_length : float
            Focal length of cameras
        baseline : float
            Baseline of stereo camera
        """
    @staticmethod
    def calibrationFromImages(left_cal_folder: str, right_cal_folder: str, left_img_wildcard: str, right_img_wildcard: str, board_type: CalibrationBoardType, pattern_size_x: int, pattern_size_y: int, square_size: float) -> StereoCameraCalibration: 
        """
        Create ideal stereo calibration from camera information

        Parameters
        ----------
        left_cal_folder : str
            Path to folder with left calibration images
        right_cal_folder : str
            Path to folder with right calibration images
        left_img_wildcard : str
            Wildcard to use for identifying left images
        right_img_wildcard : str
            Wildcard to use for identifying right images
        board_type : phase.pyphase.calib.CalibrationBoardType
            Calibration board type used in calibration images
        pattern_size_x : int
            Number of rows in calibration board pattern
        pattern_size_y : int
            Number of columns in calibration board pattern
        square_size : float
            Width of single square in calibration board pattern (in meters)

        Returns
            Stereo camera calibration
        """
    @staticmethod
    def calibrationFromYAML(left_calibration: str, right_calibration: str) -> StereoCameraCalibration: 
        """
        Load calibration from yaml files

        Parameters
        ----------
        left_calibration_filepath : str
            Left side calibration file path directory
        right_calibration_filepath : str
            Right side calibration file path directory
        """
    def getBaseline(self) -> float: 
        """
        Get the baseline from calibration

        Returns
        -------
        value : float
            Baseline value of calibration file
        """
    def getDownsampleFactor(self) -> float: 
        """
        Get downsample factor

        Returns
        -------
        value : float
            Downsample value of calibration files
        """
    def getHFOV(self) -> float: 
        """
        Get horitonzal Field Of View of camera from calibration

        Returns
        -------
        fov_x : float
            Horitonzal Field Of View of camera
        """
    def getQ(self) -> numpy.ndarray: 
        """
        Get the Q matrix

        Returns
        -------
        Q : numpy.ndarray
            Q matrix
        """
    def isValid(self) -> bool: 
        """
        Check if loaded calibration is valid

        Returns
        -------
        bool
            True if calibration file is valid
        """
    def isValidSize(self, width: int, height: int) -> bool: 
        """
        Check if loaded calibration image width and height match specified values

        Parameters
        ----------
        width : int
            Image width to check against
        height : int
            Image height to check against


        Returns
        -------
        bool
            True if calibration file is valid in size
        """
    def rectify(self, left_image: numpy.ndarray, right_image: numpy.ndarray) -> phase.pyphase.types.StereoImagePair: 
        """
        Rectify stereo images based on calibration

        Parameters
        ----------
        left_image : numpy.ndarray
            Left image to rectify
        right_image : numpy.ndarray
            Right image to rectify

        Returns
        -------
        rect_pair : phase.pyphase.types.StereoImagePair
            Rectified stereo image pair
        """
    def saveToYAML(self, left_calibration_filepath: str, right_calibration_filepath: str, cal_file_type: CalibrationFileType) -> bool: 
        """
        Save stereo camera calibration to YAML files

        Parameters
        ----------
        left_calibration_filepath : str
            Desired path directory to save calibration file
        right_calibration_filepath : str
            Desired path directory to save calibration file
        cal_file_type : phase.pyphase.calib.CalibrationFileType
            Type of calibration file, e.g. ROS_YAML/OPENCV_YAML

        Returns
        -------
        bool
            True if calibration yaml files are saved
        """
    def setDownsampleFactor(self, value: float) -> None: 
        """
        Set downsample factor

        Parameters
        ----------
        value : float
            Desired value of downsample factor
        """
    @property
    def left_calibration(self) -> CameraCalibration:
        """
                    Stores left camera calibration

                    

        :type: CameraCalibration
        """
    @left_calibration.setter
    def left_calibration(self, arg0: CameraCalibration) -> None:
        """
        Stores left camera calibration
        """
    @property
    def right_calibration(self) -> CameraCalibration:
        """
                    Stores right camera calibration

                    

        :type: CameraCalibration
        """
    @right_calibration.setter
    def right_calibration(self, arg0: CameraCalibration) -> None:
        """
        Stores right camera calibration
        """
    pass
CHECKERBOARD: phase.pyphase.calib.CalibrationBoardType # value = <CalibrationBoardType.CHECKERBOARD: 0>
INVALID_BOARD: phase.pyphase.calib.CalibrationBoardType # value = <CalibrationBoardType.INVALID_BOARD: 1>
INVALID_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.INVALID_YAML: 2>
LEFT: phase.pyphase.calib.CalibrationSelection # value = <CalibrationSelection.LEFT: 0>
OPENCV_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.OPENCV_YAML: 1>
RIGHT: phase.pyphase.calib.CalibrationSelection # value = <CalibrationSelection.RIGHT: 1>
ROS_YAML: phase.pyphase.calib.CalibrationFileType # value = <CalibrationFileType.ROS_YAML: 0>
