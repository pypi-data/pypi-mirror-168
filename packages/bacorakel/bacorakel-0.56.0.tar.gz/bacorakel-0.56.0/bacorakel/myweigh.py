import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Transmission:
    weight: Optional[float] = None
    kg: Optional[bool] = None
    overload: Optional[bool] = None
    sign: Optional[bool] = None
    timestamp: datetime = field(default_factory=datetime.now)


def encode(t: Transmission) -> bytes:
    """Encode a Transmission as a MyWeight serial message."""
    weight = 0.0 if t.weight is None else t.weight
    kg = True if t.kg is None else t.kg
    overload = False if t.overload is None else t.overload
    sign = True if t.sign is None else t.sign

    weight = round(weight, 1)  # Round to 1 digit.
    head = "M" if overload else "W"
    sign_enc = "" if sign else "-"
    data = str(weight)
    padding = (10 - len(data)) * " "
    unit = "kg" if kg else "lb"
    cr = "\r\n"

    return f"{head}{sign_enc}{padding}{data}{unit}{cr}".encode()


def encode_weight(weight: float) -> bytes:
    """Encode a weight value as a MyWeight serial message."""
    return encode(Transmission(weight=weight))


# PAT = re.compile(r"([MW]):([+-])[ ]*([0-9\.]+)(kg|lb)")
PAT = re.compile(r"([MW])(-?)\s*([0-9\.]+)(kg)")


def decode(msg: bytes) -> List[Transmission]:
    """Decode a MyWeight serial message."""
    matches = PAT.findall(msg.decode())
    transmissions = [
        Transmission(
            overload=match[0] == "M",
            sign=match[1] != "-",
            weight=float(match[2]),
            kg=match[3] == "kg",
        )
        for match in matches
    ]

    return transmissions
