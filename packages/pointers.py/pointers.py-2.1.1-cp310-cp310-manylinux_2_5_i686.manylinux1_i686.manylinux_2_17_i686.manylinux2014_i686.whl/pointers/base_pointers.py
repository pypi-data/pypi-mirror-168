import ctypes
import faulthandler
import sys
from abc import ABC, abstractmethod
from contextlib import suppress
from io import UnsupportedOperation
from typing import (
    Any, Generic, Iterator, Optional, Tuple, Type, TypeVar, Union
)

from _pointers import add_ref, remove_ref

from ._utils import deref, force_set_attr, move_to_mem
from .exceptions import DereferenceError, FreedMemoryError, NullPointerError

__all__ = (
    "BasePointer",
    "BaseObjectPointer",
    "NULL",
    "Nullable",
    "BasicPointer",
    "BaseCPointer",
    "BaseAllocatedPointer",
    "Dereferencable",
    "IterDereferencable",
)

T = TypeVar("T")
A = TypeVar("A", bound="BasicPointer")

with suppress(
    UnsupportedOperation
):  # in case its running in idle or something like that
    faulthandler.enable()


class NULL:
    """Unique object representing a NULL address."""


Nullable = Union[T, Type[NULL]]


class BasicPointer(ABC):
    """Base class representing a pointer with no operations."""

    @property
    @abstractmethod
    def address(self) -> Optional[int]:
        """Address that the pointer is looking at."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __rich__(self):
        ...

    def __str__(self) -> str:
        return hex(self.address or 0)

    @abstractmethod
    def __del__(self) -> None:
        ...

    def __eq__(self, data: object) -> bool:
        if not isinstance(data, BasePointer):
            return False

        return data.address == self.address

    def ensure(self) -> int:
        """Ensure that the pointer is not null.

        Raises:
            NullPointerError: Address of pointer is `None`

        Returns:
            Address of the pointer.

        Example:
            ```py
            ptr = to_ptr(NULL)
            address = ptr.ensure()  # NullPointerError
            ptr >>= 1
            address = ptr.ensure()  # works just fine
            ```"""

        if not self.address:
            raise NullPointerError("pointer is NULL")
        return self.address


class Movable(ABC, Generic[T, A]):
    @abstractmethod
    def move(
        self,
        data: Union[A, T],
        *,
        unsafe: bool = False,
    ) -> None:
        """Move data to the target address.

        Args:
            data: Pointer or object to move into the current data.
            unsafe: Should buffer overflows be allowed.
        """
        ...

    def __ilshift__(self, data: Union[A, T]):
        self.move(data)
        return self

    def __ixor__(self, data: Union[A, T]):
        self.move(data, unsafe=True)
        return self


class Dereferencable(ABC, Generic[T]):
    """Abstract class for an object that may be dereferenced."""

    @abstractmethod
    def dereference(self) -> T:
        """Dereference the pointer.

        Returns:
            Value at the pointers address."""
        ...

    def __invert__(self) -> T:
        """Dereference the pointer."""
        return self.dereference()


class IterDereferencable(Dereferencable[T], Generic[T]):
    """
    Abstract class for an object that may be dereferenced via * (`__iter__`)
    """

    def __iter__(self) -> Iterator[T]:
        """Dereference the pointer."""
        return iter({self.dereference()})


class BasePointer(
    Dereferencable[T],
    Movable[T, "BasePointer[T]"],
    BasicPointer,
    ABC,
    Generic[T],
):
    """Base class representing a pointer."""

    @property
    @abstractmethod
    def address(self) -> Optional[int]:
        """Address that the pointer is looking at."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __rich__(self):
        ...

    def __str__(self) -> str:
        return hex(self.address or 0)

    @abstractmethod
    def __del__(self) -> None:
        ...

    def __eq__(self, data: object) -> bool:
        if not isinstance(data, BasePointer):
            return False

        return data.address == self.address


class Typed(ABC, Generic[T]):
    """Base class for a pointer that has a type attribute."""

    @property
    @abstractmethod
    def type(self) -> T:
        """Type of the value at the address."""
        ...


class Sized(ABC):
    """Base class for a pointer that has a size attribute."""

    @abstractmethod
    def ensure(self) -> int:
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        """Size of the target value."""
        ...

    def make_ct_pointer(self) -> "ctypes._PointerLike":
        """Convert the address to a ctypes pointer.

        Returns:
            The created ctypes pointer.
        """
        return ctypes.cast(
            self.ensure(),
            ctypes.POINTER(ctypes.c_char * self.size),
        )

    @abstractmethod
    def _make_stream_and_ptr(
        self,
        size: int,
        address: int,
    ) -> Tuple["ctypes._PointerLike", bytes]:
        ...


class BaseObjectPointer(
    IterDereferencable[T],
    Typed[T],
    BasePointer[T],
    ABC,
):
    """Abstract class for a pointer to a Python object."""

    def __init__(
        self,
        address: Optional[int],
        typ: Type[T],
        increment_ref: bool = False,
    ) -> None:
        """
        Args:
            address: Address of the underlying value.
            typ: Type of the pointer.
            increment_ref: Should the reference count on the target object get incremented.
        """  # noqa
        self._address: Optional[int] = address
        self._type: Type[T] = typ

        if increment_ref and address:
            add_ref(~self)

        self._origin_size = sys.getsizeof(~self if address else None)

    @property
    def type(self):
        """Type of the value at the target address."""
        return self._type

    def set_attr(self, key: str, value: Any) -> None:
        v: Any = ~self  # mypy gets angry if this isnt any
        if not isinstance(~self, type):
            v = type(v)

        force_set_attr(v, key, value)

    def assign(
        self,
        target: Nullable[Union["BaseObjectPointer[T]", T]],
    ) -> None:
        """Point to a new address.

        Args:
            target: New pointer or value to look at.
        """
        if target is NULL:
            self._address = None
            return

        new: BasePointer[T] = self._get_ptr(target)  # type: ignore

        if not isinstance(new, BaseObjectPointer):
            raise ValueError(
                "can only point to object pointer",
            )

        if (new.type is not self.type) and self.address:
            raise TypeError(
                f"object at new address must be the same type (pointer looks at {self.type.__name__}, target is {new.type.__name__})",  # noqa
            )

        if not self.address:
            self._type = new.type

        with suppress(NullPointerError):
            remove_ref(~self)

        self._address = new.address
        add_ref(~self)

    @property
    def address(self) -> Optional[int]:
        return self._address

    def dereference(self) -> T:
        return deref(self.ensure())

    def __irshift__(
        self,
        value: Nullable[Union["BaseObjectPointer[T]", T]],
    ):
        self.assign(value)
        return self

    @classmethod
    @abstractmethod
    def make_from(cls, obj: T) -> "BaseObjectPointer[T]":
        """Create a new instance of the pointer.

        Args:
            obj: Object to create pointer to.

        Returns:
            Created pointer.

        Example:
            ```py
            ptr = Pointer.make_from(1)
            ```"""
        ...

    @classmethod
    def _get_ptr(cls, obj: Union[T, "BasePointer[T]"]) -> "BasePointer[T]":
        return (
            obj
            if isinstance(
                obj,
                BasePointer,
            )
            else cls.make_from(obj)
        )

    def __del__(self):
        if self.address:
            remove_ref(~self)


class BaseCPointer(
    IterDereferencable[T],
    Movable[T, "BaseCPointer[T]"],
    BasicPointer,
    Sized,
    ABC,
):
    def __init__(self, address: int, size: int):
        self._address = address
        self._size = size

    @property
    def address(self) -> Optional[int]:
        return self._address

    def _make_stream_and_ptr(
        self,
        size: int,
        address: int,
    ) -> Tuple["ctypes._PointerLike", bytes]:
        bytes_a = (ctypes.c_ubyte * size).from_address(address)
        return self.make_ct_pointer(), bytes(bytes_a)

    def move(
        self,
        data: Union["BaseCPointer[T]", T],
        *,
        unsafe: bool = False,
    ) -> None:
        """Move data to the target address."""
        if not isinstance(data, BaseCPointer):
            raise ValueError(
                f'"{type(data).__name__}" object is not a valid C pointer',
            )

        ptr, byte_stream = self._make_stream_and_ptr(
            data.size,
            data.ensure(),
        )
        move_to_mem(ptr, byte_stream, unsafe=unsafe, target="C data")

    def __ilshift__(self, data: Union["BaseCPointer[T]", T]):
        self.move(data)
        return self

    def __ixor__(self, data: Union["BaseCPointer[T]", T]):
        self.move(data, unsafe=True)
        return self

    def make_ct_pointer(self):
        return ctypes.cast(
            self.ensure(),
            ctypes.POINTER(ctypes.c_char * self.size),
        )

    def _as_parameter_(self) -> "ctypes._CData":
        """Convert the pointer to a ctypes pointer."""
        ...


class BaseAllocatedPointer(BasePointer[T], Sized, ABC):
    @property
    @abstractmethod
    def address(self) -> Optional[int]:
        ...

    @address.setter
    def address(self, value: int) -> None:
        ...

    @property
    def freed(self) -> bool:
        """Whether the allocated memory has been freed."""
        return self._freed

    @freed.setter
    def freed(self, value: bool) -> None:
        self._freed = value

    @property
    def assigned(self) -> bool:
        """Whether the allocated memory has been assigned a value."""
        return self._assigned

    @assigned.setter
    def assigned(self, value: bool) -> None:
        self._assigned = value

    def move(
        self,
        data: Union[BasePointer[T], T],
        unsafe: bool = False,
    ) -> None:
        add_ref(data)
        self.ensure_valid()
        from .object_pointer import to_ptr

        data_ptr = data if isinstance(data, BasePointer) else to_ptr(data)

        ptr, byte_stream = self._make_stream_and_ptr(
            sys.getsizeof(~data_ptr),
            data_ptr.ensure(),
        )

        move_to_mem(ptr, byte_stream, unsafe=unsafe)
        self.assigned = True
        remove_ref(data)

    def dereference(self) -> T:
        if self.freed:
            raise FreedMemoryError(
                "cannot dereference memory that has been freed",
            )

        if not self.assigned:
            raise DereferenceError(
                "cannot dereference allocated memory that has no value",
            )

        return deref(self.ensure())

    @abstractmethod
    def __add__(self, amount: int) -> "BaseAllocatedPointer[Any]":
        ...

    @abstractmethod
    def __sub__(self, amount: int) -> "BaseAllocatedPointer[Any]":
        ...

    def __del__(self):
        pass

    def _make_stream_and_ptr(
        self,
        size: int,
        address: int,
    ) -> Tuple["ctypes._PointerLike", bytes]:
        if self.freed:
            raise FreedMemoryError("memory has been freed")

        bytes_a = (ctypes.c_ubyte * size).from_address(address)  # fmt: off
        return self.make_ct_pointer(), bytes(bytes_a)

    @abstractmethod
    def free(self) -> None:
        """Free the memory."""
        ...

    def ensure_valid(self) -> None:
        """Ensure the memory has not been freed."""
        if self.freed:
            raise FreedMemoryError(
                f"{self} has been freed",
            )

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        self._size = value
