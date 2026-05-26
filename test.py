from typing import Annotated, get_type_hints, get_args, get_origin

def double(x: Annotated[int, (0, 100)]) -> int:

    type_hints = get_type_hints(double, include_extras=True)
    hint = type_hints['x']

    if get_origin(hint) is Annotated:
        hint_type, *hint_args = get_args(hint)
        low, high = hint_args[0]
        if x < low or x > high:
            raise ValueError(f"Value {x} is out of range [{low}, {high}]")

    return x * 2

result = double(101)
print(result)
