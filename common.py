from dataclasses import dataclass

@dataclass
class Vec2:
    x: int
    y: int

# Vec2 = namedtuple('Vec2', 'x y')