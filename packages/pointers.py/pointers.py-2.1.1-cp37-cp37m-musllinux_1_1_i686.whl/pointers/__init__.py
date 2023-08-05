if __import__("sys").implementation.name != "cpython":
    # using __import__ to make sure sys isnt exported
    raise Exception(
        "pointers.py is only supported on cpython",
    )

from ._utils import force_set_attr
from .base_pointers import (
    NULL, BaseAllocatedPointer, BaseCPointer, BaseObjectPointer, BasePointer,
    BasicPointer, Dereferencable, IterDereferencable, Nullable, Sized, Typed
)
from .bindings import *
from .c_pointer import (
    StructPointer, TypedCPointer, VoidPointer, array, cast, to_c_ptr,
    to_struct_ptr
)
from .calloc import AllocatedArrayPointer, calloc
from .custom_binding import binding, binds
from .decay import decay, decay_annotated, decay_wrapped
from .exceptions import (
    AllocationError, DereferenceError, FreedMemoryError,
    InvalidBindingParameter, InvalidSizeError
)
from .magic import _
from .malloc import AllocatedPointer, free, malloc, realloc
from .object_pointer import Pointer, to_ptr
from .std_structs import DivT, Lconv, LDivT, Tm
from .structure import Struct

__version__ = "2.1.1"
