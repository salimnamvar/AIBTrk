""" Camera

This python file contains the camera class object for handling reading frames from a camera.

Classes:
    - `Camera`: Represents a camera object for reading frames from a camera.

Functions:
    None

Variables:
    None
"""

# region Imported Dependencies
import logging
import time
import uuid
import warnings
from typing import NoReturn, Tuple, Union
import cv2
import numpy as np
from brain.util import Video2D, Frame2DList, Frame2D

# endregion Imported Dependencies


class Camera(Video2D):
    """Camera

    This python file contains the camera class object for handling reading frames from a camera.

    Attributes:
        reinit_duration (int):
            The reinitialization duration in seconds that indicates how long the camera can try to reinitialize its
            connection during connection failures.
        reinit_interval (int):
            The reinitialization interval in seconds that indicates how long the reinitialization trials should be
            postponed during trial failures.
        source: Union[int, str]
            A value indicating the camera source, which can be an integer (camera index) or a string (resource file).
        cache_size: int
            An integer representing the cache size for storing frames from the camera.
        id: uuid.UUID
            A universally unique identifier (:class:`UUID`) specifying the ID of the Camera object.
        backend: int
            An integer specifying the backend for video capture, using OpenCV constants.
        name: str
            A string specifying the name of the Camera object.
        logger: logging.Logger
            A :class:`logging.Logger` instance for logging camera-related messages.
        frames: Frame2DList
            A :class:`Frame2DList` for storing :class:`Frame2D` objects with a specified cache size.
    """

    def __init__(
        self,
        a_source: Union[int, str],
        a_cache_size: int,
        a_reinit_duration: int,
        a_reinit_interval: int,
        a_id: uuid.UUID = None,
        a_backend=cv2.CAP_FFMPEG,
        a_name: str = "CAM",
    ):
        """Constructor

        Initializes a Camera object.

        Args:
            a_source (Union[int, str]):
                The source of the camera, which can be an integer (camera index) or a string (resource file).
            a_cache_size (int):
                The cache size for storing frames from the camera.
            a_reinit_duration (int):
                The reinitialization duration in seconds that indicates how long the camera can try to reinitialize its
                connection during connection failures.
            a_reinit_interval (int):
                The reinitialization interval in seconds that indicates how long the reinitialization trials should be
                postponed during trial failures.
            a_id (uuid.UUID, optional):
                The ID of the Camera object as a :class:`uuid.UUID`. Defaults to None.
            a_backend (int, optional):
                The backend for video capture, using OpenCV constants. Defaults to cv2.CAP_FFMPEG.
            a_name (str, optional):
                The name of the Camera object. Defaults to 'CAM'.

        Raises:
            TypeError: If the `a_cache_size` argument is not an integer or is less than 1.

        """
        # region Input Checking
        if not isinstance(a_cache_size, int):
            raise TypeError(f"`a_cache_size` argument must be a `int` but it's type is {type(a_cache_size)}")
        if a_cache_size < 1:
            raise TypeError(f"`a_cache_size` argument must be at least +1 but it is {a_cache_size}")
        # endregion Input Checking

        super().__init__(a_source=a_source, a_id=a_id, a_backend=a_backend, a_name=a_name)
        self.logger = logging.getLogger(self.name)
        self.reinit_duration: int = a_reinit_duration
        self.reinit_interval: int = a_reinit_interval
        self.frames: Frame2DList = Frame2DList(a_max_size=a_cache_size)

    def __reduce__(self):
        """Serialization Method

        Used for pickling and serialization to recreate a new instance of the Camera class.

        Returns:
            tuple:
                A tuple containing the class itself and a tuple of arguments (source, id, backend, name) needed
                to recreate the object.

        """
        return self.__class__, (self.source, self.id, self.backend, self.name)

    def stream(self) -> NoReturn:
        """Stream Camera Frames

        Continuously reads frames from the camera and appends them to the frames list while the camera is opened.

        Raises:
            RuntimeError: If an error occurs during frame reading, a RuntimeError is raised with an error message.

        """
        try:
            while self.is_opened:
                ret, frame = self.read()
                self.frames.append(frame)
        except Exception as e:
            msg = f"{self.name} frame reading got an error of `{e}`."
            self.logger.fatal(msg)
            raise RuntimeError(msg)

    @property
    def frame(self) -> Frame2D:
        """Get the Latest Cached Frame

        Retrieves the latest frame in the cache from the frames list.

        Returns:
            Frame2D:
                The latest frame in the cache as a :class:`Frame2D` object.

        Raises:
            RuntimeError: If the frames list is empty, a RuntimeError is raised indicating the error.

        """
        try:
            frame = self.frames[-1]
        except RuntimeError as e:
            raise RuntimeError(f"The camera's frames list is empty; The error is `{e}`")
        return frame

    def read(self) -> Tuple[bool, Frame2D]:
        """Read the Next Frame from the Camera

        Attempts to read the next frame from the camera using OpenCV's video capture.

        Returns:
            Tuple[bool, Frame2D]:
                A tuple containing two values - a boolean indicating the success of frame retrieval,
                and the :class:`Frame2D` object representing the captured frame.

        Raises:
            RuntimeError: If there is an error during the frame retrieval process, a RuntimeError is raised.
        """
        try:
            error = False
            ret, frame = self.video_capture.read()
            if frame is None:
                error = True
                msg = f"{self.name}'s `read` method got an error of `The current frame is None.`."
                self.logger.warning(msg)
                warnings.warn(msg)
            if not ret:
                error = True
                msg = (
                    f"{self.name}'s `read` method got an error of `The retrival flag of the camera frame reading "
                    f"is False.`."
                )
                self.logger.warning(msg)
                warnings.warn(msg)
        except cv2.error as e:
            msg = f"An Unexpected OpenCV error occurred during reading video's frame. The error is `{e}`"
            self.logger.warning(msg)
            warnings.warn(msg)
            error = True
        except Exception as e:
            msg = f"An Unexpected OpenCV error occurred during reading video's frame. The error is `{e}`"
            self.logger.warning(msg)
            warnings.warn(msg)
            error = True

        if error:
            ret, frame = self.reinitialize_camera()

        if not ret or frame is None:
            msg = (
                f"{self.name}'s `read` method got an error of `Camera Frame reading is stoped due to unexpected "
                f"error`."
            )
            self.logger.fatal(msg)
            raise RuntimeError(msg)
        else:
            self._current_frame_id += 1
            frame = Frame2D(a_data=frame, a_sequence_id=self._current_frame_id, a_video_id=self._id)
        return ret, frame

    def reinitialize_camera(self) -> Tuple[bool, np.ndarray]:
        """Reinitialize the Camera

        Attempts to reinitialize the camera after encountering errors during frame retrieval.

        Returns:
            Tuple[bool, np.ndarray]:
                A tuple containing two values - a boolean indicating the success of camera reinitialization
                and the first frame captured after reinitialization.

        Raises:
            RuntimeError:
                If the camera is not able to be opened even after reinitialization trials, a RuntimeError is raised.

        """
        self.video_capture.release()
        start_time = time.time()
        end_time = start_time + self.reinit_duration
        current_time = start_time
        i = 0
        ret = False
        frame = None
        while current_time < end_time:
            i += 1
            self.logger.info(f"{self.name} is trying to re-initialize itself; the trial number is {i}.")
            self.initialize_video()
            if self.is_opened:
                ret, frame = self.video_capture.read()
                self.logger.info(f"{self.name} is correctly re-initialized; the trial number is {i}.")
                break
            else:
                msg = f"{self.name} failed in re-initialization of trial {i}."
                self.logger.warning(msg)
                warnings.warn(msg)

                self.video_capture.release()
                current_time = time.time()
                if current_time < end_time:
                    time_to_sleep = min(end_time - current_time, self.reinit_interval)
                    time.sleep(time_to_sleep)

        if not self.is_opened or not ret or frame is None:
            msg = (
                f"{self.name}'s `read` method got an error of `Camera is not able to be opened even after "
                f"re-initialization trials."
            )
            self.logger.critical(msg)
            raise RuntimeError(msg)
        return ret, frame
