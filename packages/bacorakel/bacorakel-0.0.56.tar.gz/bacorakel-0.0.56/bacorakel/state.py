from collections import deque
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Deque, List, Optional, Union

from serde import field, serde, toml
from serde.de import from_dict
from serde.se import to_dict

from bacorakel.logging import debug, warn


class UpdateAble:
    def update(self, new):
        for f in fields(new):
            if hasattr(self, f.name):
                setattr(self, f.name, getattr(new, f.name))


@serde
@dataclass
class ArduinoSettings(UpdateAble):
    device: str = "COM0"

    servo_pwm_pin: str = "d:10:p"
    servo_pwm: float = 0.0

    servo_min_pwm: float = 0.500
    servo_min_angle: float = 0.0

    servo_max_pwm: float = 1.200
    servo_max_angle: float = 180.0

    servo_pwm_thr: float = 0.005


@serde
@dataclass
class ScalesSettings(UpdateAble):
    device: str = "COM10"
    baud: int = 9600
    timeout: int = 5
    bytesize: int = 8
    stopbits: int = 1
    read_buf: int = 56


@serde
@dataclass
class Measurement(UpdateAble):
    weight: float = 0.0
    time: int = 0
    rate: float = 0.0


@serde
@dataclass
class MeasurementHistory(UpdateAble):
    data: Deque[Measurement] = field(
        default_factory=lambda: deque([], 100),
        serializer=lambda x: to_dict(list(x)),
        deserializer=lambda x: deque(from_dict(List[Measurement], x), 100),
    )
    rate_horizon: int = 60


@serde
@dataclass
class State(UpdateAble):
    host: str = "127.0.0.1"
    port: int = 8056
    debug: bool = False
    emulate: bool = False
    arduino: ArduinoSettings = field(default_factory=ArduinoSettings)
    scales: ScalesSettings = field(default_factory=ScalesSettings)
    keg_weight: float = 56.0
    keg_weight_empty: float = 10.5
    keg_capacity: float = 50.0
    state_file: Optional[str] = None
    history: MeasurementHistory = field(default_factory=MeasurementHistory)

    @property
    def keg_fraction(self) -> float:
        """Percentage that the keg is full."""
        return get_fraction(
            self.keg_weight,
            self.keg_weight_empty,
            self.keg_weight_empty + self.keg_capacity,
        )

    @property
    def servo_angle(self) -> float:
        """Servo angle corresponding to keg contents."""
        return apply_fraction(
            self.keg_fraction,
            self.arduino.servo_min_angle,
            self.arduino.servo_max_angle,
        )

    @property
    def servo_pwm(self) -> float:
        """Servo angle expressed as a servo PWM value."""
        return apply_fraction(
            self.keg_fraction, self.arduino.servo_min_pwm, self.arduino.servo_max_pwm
        )

    def load(self, path: Optional[Union[str, Path]] = None) -> "State":
        """Load state from file."""
        path = self.state_file if path is None else Path(path)
        if path is None:
            return self
        else:
            path = Path(path)
        try:
            debug(f"Loading state from {path}...")
            contents = path.read_text()
            obj = toml.from_toml(TomlState, contents)
            self.update(obj.bacorakel)
        except Exception as e:
            warn(f"Could not load state from {path.resolve()}. Returning default.")
            warn(str(e))
        return self

    def save(self, path: Optional[Union[str, Path]] = None) -> Optional[str]:
        """Save state to file."""
        path = self.state_file if path is None else Path(path)
        ser = None
        try:
            ser = toml.to_toml(TomlState(self))
            if path:
                path = Path(path)
                path.write_text(ser)
        except Exception as e:
            warn("Could not save state.")
            warn(str(e))
        return ser


state = State()


@serde
@dataclass
class TomlState(UpdateAble):
    bacorakel: State = field(default_factory=State)


def get_fraction(value: float, lower: float, upper: float) -> float:
    """Get a fraction [0.0-1.0] corresponding to a value within a range."""
    return max(0.0, value - lower) / (upper - lower)


def apply_fraction(fraction: float, lower: float, upper: float) -> float:
    """Apply a fraction [0.0-1.0] to a value range to obtain the corresponding value."""
    return lower + fraction * (upper - lower)


def calculate_rate(
    data: Deque["Measurement"],
    horizon: int,
    time: Optional[int] = None,
    cap: float = 0.05,
) -> float:
    """Calculate the flow rate from a measurement deque."""
    if len(data) < 2:
        return 0.0

    size = len(data)

    weight = data[-1].weight
    time = data[-1].time if time is None else time
    ref = Measurement(time=time - horizon)

    idx = -2
    while -idx < size:
        if ref.time > data[idx].time:
            debug("Interpolating around measurement horizon time.")
            m0 = data[idx]
            m1 = data[idx + 1]
            window = m1.time - m0.time
            if window <= 0:
                ref.weight = m1.weight
            else:
                ref.weight = (
                    (ref.time - m0.time) * m1.weight + (m1.time - ref.time) * m0.weight
                ) / (m1.time - m0.time)
            break
        # Progression cap exceeded for next entry. Interpolate regularly at idx.
        elif data[idx].weight - data[idx - 1].weight > cap:
            debug("Exceeded rate cap, limiting rate measurement horizon.")
            ref.time = data[idx].time
            ref.weight = data[idx].weight
            break

        idx -= 1

    # Horizon not exceeded, regular interpolation with first entry is fine.
    if -idx == size:
        debug("Regular rate interpolation, horizon not exceeded.")
        ref.time = data[0].time
        ref.weight = data[0].weight

    # Calculate slope.
    return (weight - ref.weight) / (time - ref.time)
