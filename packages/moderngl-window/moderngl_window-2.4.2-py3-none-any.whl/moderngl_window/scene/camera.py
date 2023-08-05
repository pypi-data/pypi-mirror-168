import time
from math import cos, radians, sin

import numpy
from pyrr import Vector3, Matrix44, vector, vector3

from moderngl_window.opengl.projection import Projection3D
from moderngl_window.context.base import BaseKeys

# Direction Definitions
RIGHT = 1
LEFT = 2
FORWARD = 3
BACKWARD = 4
UP = 5
DOWN = 6

# Movement Definitions
STILL = 0
POSITIVE = 1
NEGATIVE = 2


class Camera:
    """Simple camera class containing projection.

    .. code:: python

        # create a camera
        camera = Camera(fov=60.0, aspect_ratio=1.0, near=1.0, far=100.0)

        # Get the current camera matrix as numpy array
        print(camera.matrix)

        # Get projection matrix as numpy array
        print(camera.projection.matrix)
    """

    def __init__(self, fov=60.0, aspect_ratio=1.0, near=1.0, far=100.0):
        """Initialize camera using a specific projection

        Keyword Args:
            fov (float): Field of view
            aspect_ratio (float): Aspect ratio
            near (float): Near plane
            far (float): Far plane
        """
        self.position = Vector3([0.0, 0.0, 0.0])
        # Default camera placement
        self.up = Vector3([0.0, 1.0, 0.0])
        self.right = Vector3([1.0, 0.0, 0.0])
        self.dir = Vector3([0.0, 0.0, -1.0])
        # Yaw and Pitch
        self._yaw = -90.0
        self._pitch = 0.0

        # World up vector
        self._up = Vector3([0.0, 1.0, 0.0])

        # Projection
        self._projection = Projection3D(aspect_ratio, fov, near, far)

    @property
    def projection(self):
        """:py:class:`~moderngl_window.opengl.projection.Projection3D`: The 3D projection"""
        return self._projection

    def set_position(self, x, y, z) -> None:
        """Set the 3D position of the camera.

        Args:
            x (float): x position
            y (float): y position
            z (float): z position
        """
        self.position = Vector3([float(x), float(y), float(z)])

    def set_rotation(self, yaw, pitch) -> None:
        """Set the rotation of the camera.

        Args:
            yaw (float): yaw rotation
            pitch (float): pitch rotation
        """
        self._pitch = float(pitch)
        self._yaw = float(yaw)
        self._update_yaw_and_pitch()

    @property
    def yaw(self) -> float:
        """float: The current yaw angle."""
        return self._yaw

    @yaw.setter
    def yaw(self, value) -> None:
        self._yaw = float(value)
        self._update_yaw_and_pitch()

    @property
    def pitch(self) -> float:
        """float: The current pitch angle."""
        return self._pitch

    @pitch.setter
    def pitch(self, value) -> None:
        self._pitch = float(value)
        self._update_yaw_and_pitch()

    @property
    def matrix(self) -> numpy.ndarray:
        """numpy.ndarray: The current view matrix for the camera"""
        self._update_yaw_and_pitch()
        return self._gl_look_at(self.position, self.position + self.dir, self._up)

    def _update_yaw_and_pitch(self) -> None:
        """Updates the camera vectors based on the current yaw and pitch"""
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.dir = vector.normalise(front)
        self.right = vector.normalise(vector3.cross(self.dir, self._up))
        self.up = vector.normalise(vector3.cross(self.right, self.dir))

    def look_at(self, vec=None, pos=None) -> numpy.ndarray:
        """Look at a specific point

        Either ``vec`` or ``pos`` needs to be supplied.

        Keyword Args:
            vec (pyrr.Vector3): position
            pos (tuple/list): list of tuple ``[x, y, x]`` / ``(x, y, x)``
        Returns:
            numpy.ndarray: Camera matrix
        """
        if pos is not None:
            vec = Vector3(pos)

        if vec is None:
            raise ValueError("vector or pos must be set")

        return self._gl_look_at(self.position, vec, self._up)

    def _gl_look_at(self, pos, target, up) -> numpy.ndarray:
        """The standard lookAt method.

        Args:
            pos: current position
            target: target position to look at
            up: direction up
        Returns:
            numpy.ndarray: The matrix
        """
        z = vector.normalise(pos - target)
        x = vector.normalise(vector3.cross(vector.normalise(up), z))
        y = vector3.cross(z, x)

        translate = Matrix44.identity(dtype="f4")
        translate[3][0] = -pos.x
        translate[3][1] = -pos.y
        translate[3][2] = -pos.z

        rotate = Matrix44.identity(dtype="f4")
        rotate[0][0] = x[0]  # -- X
        rotate[1][0] = x[1]
        rotate[2][0] = x[2]
        rotate[0][1] = y[0]  # -- Y
        rotate[1][1] = y[1]
        rotate[2][1] = y[2]
        rotate[0][2] = z[0]  # -- Z
        rotate[1][2] = z[1]
        rotate[2][2] = z[2]

        return rotate * translate


class KeyboardCamera(Camera):
    """Camera controlled by mouse and keyboard.
    The class interacts with the key constants in the
    built in window types.

    Creating a keyboard camera:

    .. code:: python

        camera = KeyboardCamera(
            self.wnd.keys,
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )

    We can also interact with the belonging
    :py:class:`~moderngl_window.opengl.projection.Projection3D` instance.

    .. code:: python

        # Update aspect ratio
        camera.projection.update(aspect_ratio=1.0)

        # Get projection matrix in bytes (f4)
        camera.projection.tobytes()
    """

    def __init__(self, keys: BaseKeys, fov=60.0, aspect_ratio=1.0, near=1.0, far=100.0):
        """Initialize the camera

        Args:
            keys (BaseKeys): The key constants for the current window type
        Keyword Args:
            fov (float): Field of view
            aspect_ratio (float): Aspect ratio
            near (float): near plane
            far (float): far plane
        """
        # Position movement states
        self.keys = keys
        self._xdir = STILL
        self._zdir = STILL
        self._ydir = STILL
        self._last_time = 0
        self._last_rot_time = 0

        # Velocity in axis units per second
        self._velocity = 10.0
        self._mouse_sensitivity = 0.5

        super().__init__(fov=fov, aspect_ratio=aspect_ratio, near=near, far=far)

    @property
    def mouse_sensitivity(self) -> float:
        """float: Mouse sensitivity (rotation speed).

        This property can also be set::

            camera.mouse_sensitivity = 2.5
        """
        return self._mouse_sensitivity

    @mouse_sensitivity.setter
    def mouse_sensitivity(self, value: float):
        self._mouse_sensitivity = value

    @property
    def velocity(self):
        """float: The speed this camera move based on key inputs

        The property can also be modified::

            camera.velocity = 5.0
        """
        return self._velocity

    @velocity.setter
    def velocity(self, value: float):
        self._velocity = value

    def key_input(self, key, action, modifiers) -> None:
        """Process key inputs and move camera

        Args:
            key: The key
            action: key action release/press
            modifiers: key modifier states such as ctrl or shit
        """
        # Right
        if key == self.keys.D:
            if action == self.keys.ACTION_PRESS:
                self.move_right(True)
            elif action == self.keys.ACTION_RELEASE:
                self.move_right(False)
        # Left
        elif key == self.keys.A:
            if action == self.keys.ACTION_PRESS:
                self.move_left(True)
            elif action == self.keys.ACTION_RELEASE:
                self.move_left(False)
        # Forward
        elif key == self.keys.W:
            if action == self.keys.ACTION_PRESS:
                self.move_forward(True)
            if action == self.keys.ACTION_RELEASE:
                self.move_forward(False)
        # Backwards
        elif key == self.keys.S:
            if action == self.keys.ACTION_PRESS:
                self.move_backward(True)
            if action == self.keys.ACTION_RELEASE:
                self.move_backward(False)

        # UP
        elif key == self.keys.Q:
            if action == self.keys.ACTION_PRESS:
                self.move_down(True)
            if action == self.keys.ACTION_RELEASE:
                self.move_down(False)

        # Down
        elif key == self.keys.E:
            if action == self.keys.ACTION_PRESS:
                self.move_up(True)
            if action == self.keys.ACTION_RELEASE:
                self.move_up(False)

    def move_left(self, activate) -> None:
        """The camera should be continiously moving to the left.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(LEFT, activate)

    def move_right(self, activate) -> None:
        """The camera should be continiously moving to the right.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(RIGHT, activate)

    def move_forward(self, activate) -> None:
        """The camera should be continiously moving forward.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(FORWARD, activate)

    def move_backward(self, activate) -> None:
        """The camera should be continiously moving backwards.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(BACKWARD, activate)

    def move_up(self, activate) -> None:
        """The camera should be continiously moving up.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(UP, activate)

    def move_down(self, activate):
        """The camera should be continiously moving down.

        Args:
            activate (bool): Activate or deactivate this state
        """
        self.move_state(DOWN, activate)

    def move_state(self, direction, activate) -> None:
        """Set the camera position move state.

        Args:
            direction: What direction to update
            activate: Start or stop moving in the direction
        """
        if direction == RIGHT:
            self._xdir = POSITIVE if activate else STILL
        elif direction == LEFT:
            self._xdir = NEGATIVE if activate else STILL
        elif direction == FORWARD:
            self._zdir = NEGATIVE if activate else STILL
        elif direction == BACKWARD:
            self._zdir = POSITIVE if activate else STILL
        elif direction == UP:
            self._ydir = POSITIVE if activate else STILL
        elif direction == DOWN:
            self._ydir = NEGATIVE if activate else STILL

    def rot_state(self, dx: int, dy: int) -> None:
        """Update the rotation of the camera.

        This is done by passing in the relative
        mouse movement change on x and y (delta x, delta y).

        In the past this method took the viewport position
        of the mouse. This does not work well when
        mouse exclusivity mode is enabled.

        Args:
            dx: Relative mouse position change on x
            dy: Relative mouse position change on y
        """
        now = time.time()
        delta = now - self._last_rot_time
        self._last_rot_time = now

        # Greatly decrease the chance of camera popping.
        # This can happen when the mouse enters and leaves the window
        # or when getting focus again.
        if delta > 0.1 and max(abs(dx), abs(dy)) > 2:
            return

        dx *= self._mouse_sensitivity
        dy *= self._mouse_sensitivity

        self._yaw -= dx
        self._pitch += dy

        if self.pitch > 85.0:
            self.pitch = 85.0
        if self.pitch < -85.0:
            self.pitch = -85.0

        self._update_yaw_and_pitch()

    @property
    def matrix(self) -> numpy.ndarray:
        """numpy.ndarray: The current view matrix for the camera"""
        # Use separate time in camera so we can move it when the demo is paused
        now = time.time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(now - self._last_time, 0)
        self._last_time = now

        # X Movement
        if self._xdir == POSITIVE:
            self.position += self.right * self._velocity * t
        elif self._xdir == NEGATIVE:
            self.position -= self.right * self._velocity * t

        # Z Movement
        if self._zdir == NEGATIVE:
            self.position += self.dir * self._velocity * t
        elif self._zdir == POSITIVE:
            self.position -= self.dir * self._velocity * t

        # Y Movement
        if self._ydir == POSITIVE:
            self.position += self.up * self._velocity * t
        elif self._ydir == NEGATIVE:
            self.position -= self.up * self._velocity * t

        return self._gl_look_at(self.position, self.position + self.dir, self._up)


class OrbitCamera(Camera):
    """Camera controlled by the mouse to pan around the target.

    The functions :py:function:`~camera.OrbitCamera.rot_state` and :py:function:`~camera.OrbitCamera.rot_state`
    are used to update the rotation and zoom.

    Creating a orbit camera:

    .. code:: python

        camera = OrbitCamera(
            target=(0., 0., 0.),
            radius=2.0
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )

    We can also interact with the belonging
    :py:class:`~moderngl_window.opengl.projection.Projection3D` instance.

    .. code:: python

        # Update aspect ratio
        camera.projection.update(aspect_ratio=1.0)

        # Get projection matrix in bytes (f4)
        camera.projection.tobytes()
    """

    def __init__(
        self, target=(0.0, 0.0, 0.0), radius=2.0, angles=(45.0, -45.0), **kwargs
    ):
        """Initialize the camera

        Keyword Args:
            target (float, float, float): Target point
            radius (float): Radius
            angles (float, float): angle_x and angle_y in degrees
            fov (float): Field of view
            aspect_ratio (float): Aspect ratio
            near (float): near plane
            far (float): far plane
        """
        # values for orbit camera
        self.radius = radius  # radius in base units
        self.angle_x, self.angle_y = angles  # angles in degrees
        self.target = target  # camera target in base units
        self.up = (0.0, 1.0, 0.0)  # camera up vector

        self._mouse_sensitivity = 1.0
        self._zoom_sensitivity = 1.0

        super().__init__(**kwargs)

    @property
    def matrix(self) -> numpy.ndarray:
        """numpy.ndarray: The current view matrix for the camera"""
        # Compute camera (eye) position, calculated from angles and radius.
        position = (
            cos(radians(self.angle_x)) * sin(radians(self.angle_y)) * self.radius + self.target[0],
            cos(radians(self.angle_y)) * self.radius + self.target[1],
            sin(radians(self.angle_x)) * sin(radians(self.angle_y)) * self.radius + self.target[2],
        )
        self.set_position(*position)
        return Matrix44.look_at(
            position,
            self.target,  # what to look at
            self.up,  # camera up direction (change for rolling the camera)
            dtype="f4",
        )

    @property
    def angle_x(self) -> float:
        """float: camera angle x in degrees.

        This property can also be set::
            camera.angle_x = 45.
        """
        return self._angle_x

    @angle_x.setter
    def angle_x(self, value: float):
        """Set camera rotation_x in degrees."""
        self._angle_x = value

    @property
    def angle_y(self) -> float:
        """float: camera angle y in degrees.

        This property can also be set::
            camera.angle_y = 45.
        """
        return self._angle_y

    @angle_y.setter
    def angle_y(self, value: float):
        """Set camera rotation_y in degrees."""
        self._angle_y = value

    @property
    def mouse_sensitivity(self) -> float:
        """float: Mouse sensitivity (rotation speed).

        This property can also be set::
            camera.mouse_sensitivity = 2.5
        """
        return self._mouse_sensitivity

    @mouse_sensitivity.setter
    def mouse_sensitivity(self, value: float):
        self._mouse_sensitivity = value

    @property
    def zoom_sensitivity(self) -> float:
        """float: Mousewheel zooming sensitivity (zoom speed).

        This property can also be set::
            camera.zoom_sensitivity = 2.5
        """
        return self._zoom_sensitivity

    @zoom_sensitivity.setter
    def zoom_sensitivity(self, value: float):
        self._zoom_sensitivity = value

    def rot_state(self, dx: float, dy: float) -> None:
        """Update the rotation of the camera around the target point.

        This is done by passing relative mouse change in the x and y axis (delta x, delta y)

        Args:
            dx: Relative mouse position change on x axis
            dy: Relative mouse position change on y axis
        """
        self.angle_x += dx * self.mouse_sensitivity / 10.0
        self.angle_y += dy * self.mouse_sensitivity / 10.0

        # clamp the y angle to avoid weird rotations
        self.angle_y = max(min(self.angle_y, -5.0), -175.0)

    def zoom_state(self, y_offset: float) -> None:
        # allow zooming in/out
        self.radius -= y_offset * self._zoom_sensitivity
        self.radius = max(1.0, self.radius)
