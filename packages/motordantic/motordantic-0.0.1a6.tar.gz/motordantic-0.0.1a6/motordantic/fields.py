from typing import Optional, Any, Callable, cast

from pydantic.fields import (
    Field as PydanticField,
    FieldInfo as PydanticFieldInfo,
    Undefined,
)

__all__ = ('Field', 'FieldInfo')


class FieldInfo:
    __slots__ = ("pydantic_field_info", "db_field_name", "default")

    def __init__(
        self,
        *,
        pydantic_field_info: PydanticFieldInfo,
        db_field_name: Optional[str],
    ):
        self.pydantic_field_info = pydantic_field_info
        self.db_field_name = db_field_name


def Field(
    default: Any = Undefined,
    *,
    db_field_name: Optional[str] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    **extra: Any,
) -> Any:
    pydantic_field = PydanticField(
        default,
        default_factory=default_factory,
        # alias=db_field_name,
        title=cast(str, title),
        description=cast(str, description),
        const=cast(bool, const),
        gt=cast(float, gt),
        ge=cast(float, ge),
        lt=cast(float, lt),
        le=cast(float, le),
        multiple_of=cast(float, multiple_of),
        min_items=cast(int, min_items),
        max_items=cast(int, max_items),
        min_length=cast(int, min_length),
        max_length=cast(int, max_length),
        regex=cast(str, regex),
        **extra,
    )
    return FieldInfo(pydantic_field_info=pydantic_field, db_field_name=db_field_name)
