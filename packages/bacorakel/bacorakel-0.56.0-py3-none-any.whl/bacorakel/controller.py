from typing import List, Optional

import pyfirmata
import serial
from pyfirmata.mockup import MockupBoard
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from bacorakel import myweigh
from bacorakel.logging import debug, warn
from bacorakel.mockup import MockupScales
from bacorakel.state import Measurement, calculate_rate, state


class Controller:
    """BACorakel controller. Reads scales and actuates servo in each cycle."""

    def __init__(self):
        debug("Creating controller...")
        self.arduino_status: Optional[Exception] = Exception("Disconnected.")
        self.arduino_board: pyfirmata.Board
        self.arduino_iterator: pyfirmata.util.Iterator
        self.arduino_pin: pyfirmata.Pin
        self.set_arduino()
        self.scales_mockup: Optional[MockupScales] = None
        self.scales_status: Optional[Exception] = Exception("Disconnected.")
        debug("Created controller!")

    def set_arduino(self):
        """Set Arduino settings."""
        debug("Setting Arduino settings...")
        settings = state.arduino
        try:
            if getattr(self, "arduino_board", None) is not None:
                self.arduino_board.exit()
            if settings.device == "emulate":
                self.arduino_board = MockupBoard(
                    state.arduino.device, pyfirmata.BOARDS.get("arduino")
                )
            else:
                self.arduino_board = pyfirmata.Arduino(settings.device)
                self.arduino_board.name = settings.device
            self.it = pyfirmata.util.Iterator(self.arduino_board)
            self.it.start()
            self.arduino_pin = self.arduino_board.get_pin(settings.servo_pwm_pin)
            self.arduino_pin.write(state.servo_pwm)
            self.arduino_status = None
            debug("Set Arduino settings!")
        except Exception as e:
            self.arduino_status = e
            warn(str(e))

    def read_scales(self):
        """Read the scales and process the results into a weight and rate value."""
        try:
            debug("Reading scales...")
            contents = self._read_scales_buf()
            if not len(contents):
                raise Exception("Did not receive any scales message.")
            debug(f"Scales message: {contents}")
            ts = myweigh.decode(contents)
            debug(f"Transmissions: {ts}")
            weight = None
            for t in ts[::-1]:
                # Only positive non-overload weights allowed.
                if t.weight >= 0.0 and t.sign and not t.overload:
                    weight = t.weight
                    state.history.data.append(
                        Measurement(weight=weight, time=int(t.timestamp.timestamp()))
                    )
                    state.history.data[-1].rate = calculate_rate(
                        state.history.data, state.history.rate_horizon
                    )
                    debug(f"{state.history.data[-1]}")
                    break
            if weight is None:
                raise Exception("Could not find a suitable weight value.")
            else:
                state.keg_weight = weight
                self.scales_status = None
        except Exception as e:
            self.scales_status = e
            warn(str(e))

    def _read_scales_buf(self, size: Optional[int] = None) -> bytes:
        """Read bytes from the scales port."""
        scales = state.scales
        size = state.scales.read_buf if size is None else size
        if scales.device == "emulate":
            if self.scales_mockup is None:
                self.scales_mockup = MockupScales(
                    scales.device,
                    scales.baud,
                    scales.timeout,
                    state.keg_weight_empty,
                    state.keg_capacity + state.keg_weight_empty,
                )
            return self.scales_mockup.read(size)
        else:
            with serial.Serial(
                port=scales.device,
                baudrate=scales.baud,
                bytesize=scales.bytesize,
                stopbits=scales.stopbits,
                timeout=scales.timeout,
            ) as ser:
                return ser.read(size)

    def write_servo(self):
        """Actuate the servo."""
        try:
            # Try to fix any status errors.
            if self.arduino_status or state.arduino.device != self.arduino_board.name:
                self.set_arduino()

            # Only run when we're OK.
            if not self.arduino_status:
                pwm = state.servo_pwm
                if abs(pwm - state.arduino.servo_pwm) > state.arduino.servo_pwm_thr:
                    debug(f"Writing new servo pwm: {pwm}...")
                    self.arduino_pin.write(pwm)
                    state.arduino.servo_pwm = pwm
                else:
                    debug("PWM too close to previous value, don't bother updating.")
        except Exception as e:
            self.arduino_status = e
            warn(str(e))

    def cycle(self):
        debug("Cycle starting...")
        state.load()
        self.read_scales()
        self.write_servo()
        state.save()
        debug("Cycle finished.")


def list_all_ports() -> List[ListPortInfo]:
    """List all available serial ports."""
    return sorted(list_ports.grep(".*"))
