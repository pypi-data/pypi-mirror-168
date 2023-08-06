from abc import ABC, abstractmethod


class Vector(ABC):
    def __str__(self):
        return self.__class__.__name__ + str(self.__dict__)

    def __iter__(self) -> float:
        for component in self.__dict__.values():
            yield component

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, scalar):
        pass

    @abstractmethod
    def __pow__(self, scalar, modulo=None):
        pass

    @abstractmethod
    def __truediv__(self, scalar):
        pass

    @abstractmethod
    def __floordiv__(self, scalar):
        pass

    @abstractmethod
    def __mod__(self, scalar):
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def __abs__(self) -> float:
        pass

    @abstractmethod
    def magnitude(self) -> float:
        pass

    @abstractmethod
    def magnitude_squared(self) -> float:
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def dot(self, other) -> float:
        pass

    @abstractmethod
    def cross(self, other):
        pass

    @abstractmethod
    def set_magnitude(self, magnitude):
        pass

    @abstractmethod
    def reflect(self, normal_vector):
        pass

    @abstractmethod
    def distance_to(self, other) -> float:
        pass

    @abstractmethod
    def distance_to_squared(self, other) -> float:
        pass

    @abstractmethod
    def lerp(self, other, alpha):
        pass

    @abstractmethod
    def apply(self, func):
        pass

    @abstractmethod
    def angle_to(self, other) -> float:
        pass


if __name__ == '__main__':
    pass
