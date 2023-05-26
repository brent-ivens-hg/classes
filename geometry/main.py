"""
2D Geometry
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.patheffects as pfx

from collections.abc import Callable
from dataclasses import dataclass, asdict, fields, make_dataclass
from functools import total_ordering
from itertools import repeat
from math import dist, hypot
from statistics import mean
from string import ascii_uppercase

__all__ = ['EPSILON', 'gradient', 'midpoint', 'unpack', 'Visualizer']


def gradient(p, q) -> float:
    """
    :returns: the slope of (p, q)
    """
    (px, py), (qx, qy) = p, q
    return (py - qy) / (px - qx)


def midpoint(*p) -> tuple[float, ...]:
    """
    :returns: the middle-point of (p, q)
    """
    return tuple(map(mean, zip(*p)))


def unpack(__dataclass) -> tuple:  # non-recursive dataclass.astuple
    """
    :returns: unpacked dataclass
    """
    return tuple(getattr(__dataclass, field.name) for field in fields(__dataclass))


plt.style.use('dark_background')


@dataclass
class Visualizer:
    xmin: float = None
    xmax: float = None
    ymin: float = None
    ymax: float = None
    zoom: float = 1
    dpi: float = 150
    figzize: tuple = (6, 6)

    def visualize(self, *args, **kwargs) -> None:
        plt.rcParams['figure.dpi'] = self.dpi
        plt.rcParams['figure.figsize'] = self.figzize
        colors = plt.rcParams['axes.prop_cycle']()
        plt.grid(color='gray')

        for obj in args:
            if isinstance(obj, Line):
                plt.ylabel('Y-Axis')
                plt.xlabel('X-Axis')
                plt.axhline(color='white')
                plt.axvline(color='white')

                a = obj.x()
                b = obj.y()
                if a is None:  # horizontal line
                    plt.axhline(y=b.y, **next(colors))
                elif b is None:  # vertical line
                    plt.axvline(x=a.x, **next(colors))
                else:
                    plt.axline((b.x, b.y), slope=obj.slope(), **next(colors))
                continue

            points = asdict(obj)
            values = [p.values() for p in points.values()]

            for label, coords in points.items():
                x, y = coords.values()
                txt = plt.text(x + 0.5, y + 0.5, f'{label} ({x}, {y})')
                txt.set_path_effects([pfx.withStroke(linewidth=2.5, foreground='black')])

            plt.plot(*zip(*values + values[:1]), marker='o', **next(colors))

        for label, obj in kwargs.items():
            if isinstance(obj, Point):
                txt = plt.text(obj.x + 0.5, obj.y + 0.5, f'{label} ({obj.x}, {obj.y})')
                txt.set_path_effects([pfx.withStroke(linewidth=2.5, foreground='black')])
                plt.plot(obj.x, obj.y, marker='o', **next(colors))
                continue

        ax = plt.gca()
        xlim_min, xlim_max = ax.get_xlim()
        ylim_min, ylim_max = ax.get_ylim()
        ax.set_xlim([(self.xmin if self.xmin is not None else xlim_min) * self.zoom,
                     (self.xmax if self.xmax is not None else xlim_max) * self.zoom])
        ax.set_ylim([(self.ymin if self.ymin is not None else ylim_min) * self.zoom,
                     (self.ymax if self.ymax is not None else ylim_max) * self.zoom])
        plt.tight_layout()
        plt.show()


@total_ordering
@dataclass
class Epsilon:
    value: float

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other


EPSILON = Epsilon(1e-6)  # Global Precision


class GeometryException(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Point:
    """
    Point: (x, y)
    """
    x: float
    y: float

    def __getitem__(self, item: int) -> float:
        return unpack(self)[item]

    def dist(self, other: Point | Line) -> float:
        if isinstance(other, Point):
            return dist(self, other)
        if isinstance(other, Line):
            return abs(other.a * self.x + other.b * self.y + other.c) / hypot(other.a, other.b)
        raise NotImplementedError


# noinspection SpellCheckingInspection
@dataclass(frozen=True, slots=True)
class Line:
    """
    Line: Ax + By + C = 0                 (general equation form)

    y = mx + q        => A=m, B=-1, C=q   (slope-intercept form)

    A = 0: y = -c/b   => A=0, B=b, C=c    (horizontal line)
    B = 0: x = -c/a   => A=a, B=0, C=c    (vertical line)
    C = 0: y = -ax/b  => A=a, B=b, C=0    (line through origin)

    """
    a: float
    b: float
    c: float

    def __getitem__(self, item: int) -> float:
        return unpack(self)[item]

    def __and__(self, other: Line) -> Point | Line | None:
        return self.intersect(other)

    def __xor__(self, other: Line) -> Line:
        return self.bisect(other)

    def __contains__(self, point: Point) -> bool:
        return abs(self.a * point.x + self.b * point.y + self.c) <= EPSILON.value

    def x(self) -> Point | None:
        """
        :returns: the x intercept
        """
        if self.a == 0:
            return None
        return Point(-self.c / self.a, 0)

    def y(self) -> Point | None:
        """
        :returns: the y intercept
        """
        if self.b == 0:
            return None
        return Point(0, -self.c / self.b)

    def slope(self) -> float:
        try:
            return -self.a / self.b
        except ZeroDivisionError:
            return float('inf')

    def intercept(self) -> float:
        """
        :returns: the y intercept
        """
        try:
            return -self.c / self.b
        except ZeroDivisionError:
            return float('inf')

    def dist(self, other: Point | Line) -> float:
        if isinstance(other, Point):
            return abs(self.a * other.x + self.b * other.y + self.c) / hypot(self.a, self.b)
        if isinstance(other, Line):
            m = self.slope()
            if m != other.slope():  # intersecting
                return 0.0
            return abs(self.intercept() - other.intercept()) / hypot(m, 1)  # parallel or identical
        raise NotImplementedError

    def intersect(self, other: Line) -> Point | Line | None:
        denom = self.b * other.a - self.a * other.b
        if denom == 0:  # equal slopes
            if self.intercept() != other.intercept():
                return None  # identical or parallel
            return Line(self.a, self.b, self.c)
        x = (self.c * other.b - self.b * other.c) / denom
        y = self(x) if self.y() is not None else other(x)
        return Point(x, y)

    def bisect(self, other: Line):  # -> tuple[Line, Line]:
        # TODO: http://www.math-principles.com/2012/11/angle-bisector-two-intersecting-lines.html
        # FIXME: this shit trash
        m1, q1 = self.slope_intercept_form()
        m2, q2 = other.slope_intercept_form()
        m = mean([m1, m2])
        if m1 == m2:
            return Line.from_slope_intercept_form(m, mean([q1, q2]))
        return Line.from_point_slope_form(self & other, m)

    def __eq__(self, other) -> bool:
        return isinstance(other, Line) and self.slope() == other.slope() and self.intercept() == other.intercept()

    def __call__(self, x: float | None = None, y: float | None = None) -> float:
        """
        :returns: x-value if y-value or y-value if given x-value
        """
        if x is not None and y is None:
            if self.b == 0:
                return -self.a * x - self.c
            return (-self.a * x - self.c) / self.b
        if y is not None and x is None:
            if self.a == 0:
                return -self.b * y - self.c
            return (-self.b * y - self.c) / self.a
        raise GeometryException(f'invalid argument: use x=... or y=...')

    def perpendicular(self, p: Point):
        """
        :returns: perpendicular line through point a
        """
        m = -1 / self.slope()
        q = p.y - m * p.x
        return Line.from_slope_intercept_form(m, q)

    def slope_intercept_form(self) -> tuple[float, float]:
        return self.slope(), self.intercept()

    @classmethod
    def vline(cls, x: float) -> Line:
        return Line(1, 0, -x)

    @classmethod
    def hline(cls, y: float) -> Line:
        return Line(0, 0, y)

    @classmethod
    def from_slope_intercept_form(cls, slope: float, intercept: float) -> Line:
        """
        :returns: y = mx + q => A=m, B=-1 and C=q
        """
        return Line(slope, -1, intercept)

    @classmethod
    def from_point_slope_form(cls, point: Point, slope: float) -> Line:
        """
        :returns: y - y1 = m(x - x1) => A=m, B=-1 and C=-mx1-y1
        """
        return Line(slope, -1, point.y - slope * point.x)

    @classmethod
    def from_points(cls, a: Point, b: Point) -> Line:
        """
        :returns: line going through point a and b
        """
        if a.x == b.x:
            return Line.vline(a.x)  # x = b
        return Line.from_point_slope_form(a, gradient(a, b))


# a = Line.from_slope_intercept_form(1, 0)
# b = Line.from_slope_intercept_form(3, 0)
# c = a ^ b
#
# visualize(a, b, c)


@dataclass(frozen=True, slots=True)
class Segment:
    """
    Line Segment: (a, b)
    """
    A: Point
    B: Point

    def __getitem__(self, item: int) -> Point:
        return unpack(self)[item]

    def __abs__(self) -> float:
        return self.length()

    def length(self) -> float:
        return dist(*self)

    def line(self) -> Line:
        return Line.from_points(*self)

    def midpoint(self) -> Point:
        return Point(*midpoint(*self))

    def perpendicular_bisector(self) -> Line:
        """
        :returns: the perpendicular bisector of this line segment
        """
        return self.perpendicular(self.midpoint())

    def median(self, other: Point) -> Segment:
        """
        :returns: the median from a given point to this line segment
        """
        return Segment(other, self.midpoint())

    def perpendicular(self, other: Point) -> Line:
        """
        :returns: a perpendicular line through the given point
        """
        denom = self.A.y - self.B.y
        if denom == 0:
            return Line.vline(other.x)
        return Line.from_point_slope_form(other, -1 / gradient(*self))


@dataclass(frozen=True, slots=True)
class Polygon(dict):
    """
    Polygon Class
    """

    def __iter__(self) -> iter:
        return iter(unpack(self))

    def __getitem__(self, item: int) -> Point:
        return unpack(self)[item]

    def perimeter(self) -> float:
        points = unpack(self)
        return sum(map(dist, points, points[1:] + points))

    def area(self) -> float:
        points = unpack(self)
        return abs(sum(px * qy - py * qx for (px, py), (qx, qy) in zip(points, points[1:] + points))) / 2

    def segments(self) -> list[Segment]:
        points = unpack(self)
        return list(map(Segment, points, points[1:] + points))

    def perpendicular_bisectors(self) -> list[Line]:
        return [segment.perpendicular_bisector() for segment in self.segments()]

    def medians(self) -> list[Segment]:
        segments = self.segments()
        return [s.median(p) for p, s in zip(unpack(self), segments[1:] + segments)]

    def perpendicular_heights(self) -> list[Line]:
        segments = self.segments()
        return [s.perpendicular(p) for p, s in zip(unpack(self), segments[1:] + segments)]

    def centroid(self) -> Point:
        return Point(*midpoint(*self))

    def circumcenter(self) -> Point:
        assert len(unpack(self)) == 3
        a, b = self.perpendicular_bisectors()[:2]
        return a & b

    def orthocenter(self) -> Point:
        assert len(unpack(self)) == 3
        a, b = self.perpendicular_heights()[:2]
        return a & b

    def euler(self) -> Line:
        """
        :returns: the euler line of a triangle
        """
        assert len(unpack(self)) == 3
        return Line.from_points(self.circumcenter(), self.centroid())


def poly(n: int) -> Callable[..., Polygon]:
    return make_dataclass(
        cls_name=Polygon.__name__,
        fields=zip(ascii_uppercase, repeat(float, times=n)),
        bases=(Polygon,),
        frozen=True,
        slots=True
    )


Triangle = poly(3)


def doctests() -> None:
    """
    >>> A = Point(2, 12)
    >>> O = Point(0, 0)
    >>> B = Point(10, 0)

    >>> midpoint((2, 12), (0, 0))
    (1, 6)
    >>> midpoint(A, O)
    (1, 6)

    >>> dist(O, A)
    12.165525060596439
    >>> O.dist(B)
    10.0

    >>> a = Line.from_slope_intercept_form(3, 2)
    >>> b = Line.from_slope_intercept_form(-2, 12)
    >>> c = Line.from_slope_intercept_form(3, 1)
    >>> Point(0, 0) in a
    False
    >>> Point(-2, -4) in a
    True

    >>> a & b  # one point (intersection)
    Point(x=2.0, y=8.0)
    >>> a & a  # all points (identical lines)
    Line(a=3, b=-1, c=2)
    >>> a & c  # no points (parallel lines)

    >>> v = Line.from_points(Point(1, 2), Point(1, 3))  # vertical line
    >>> v
    Line(a=1, b=0, c=-1)
    >>> v.slope()
    inf
    >>> v.y()
    >>> v.x()
    Point(x=1.0, y=0)

    >>> h = Line.from_slope_intercept_form(0, 2)
    >>> h.x()
    >>> Point(4, 4).dist(h)
    2.0
    >>> h.dist(Point(4, 4))
    2.0

    >>> v.dist(h)  # intersecting lines
    0.0
    >>> Line.from_slope_intercept_form(0, 3).dist(h)  # parallel lines
    1.0
    >>> h.dist(h)  # identical lines
    0.0

    >>> Line.from_slope_intercept_form(2, 3).slope_intercept_form()
    (2.0, 3.0)

    >>> AB = Segment(A, B)
    >>> AB
    Segment(A=Point(x=2, y=12), B=Point(x=10, y=0))
    >>> abs(AB)  # AB.length()
    14.422205101855956
    >>> AB.midpoint()
    Point(x=6, y=6)
    >>> AB.line()
    Line(a=-1.5, b=-1, c=15.0)
    >>> AB.perpendicular_bisector()
    Line(a=0.6666666666666666, b=-1, c=2.0)

    >>> t = Triangle(A, O, B)
    >>> t
    Polygon(A=Point(x=2, y=12), B=Point(x=0, y=0), C=Point(x=10, y=0))
    >>> t.perimeter()
    36.587730162452395
    >>> t.area()
    60.0
    >>> t.circumcenter()
    Point(x=5.0, y=5.333333333333334)
    >>> t.orthocenter()
    Point(x=2.0, y=1.3333333333333333)
    >>> t.centroid()
    Point(x=4, y=4)
    >>> t.euler()
    Line(a=1.333333333333334, b=-1, c=-1.3333333333333357)
    >>> abs(2 * dist(t.centroid(), t.circumcenter()) - dist(t.centroid(), t.orthocenter())) <= EPSILON
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # segment = Segment(Point(1, 4), Point(5, 6))
    # Visualizer(ymax=10, xmax=10).visualize(
    #     # segment.line(),
    #     segment.perpendicular_bisector(),
    #     segment,
    # )
    # T1 = Triangle(Point(2, 12), Point(0, 0), Point(10, 0))
    # Visualizer().visualize(
    #     T1,
    #     *T1.medians(),
    #     *T1.perpendicular_bisectors(),
    #     *T1.perpendicular_heights(),
    #     D=D,
    #     H=H,
    #     G=G,
    # )
    # Visualizer().visualize(
    #     T1,
    #     T1.euler(),
    # )
