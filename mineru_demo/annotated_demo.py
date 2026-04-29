from typing import Annotated, get_type_hints


def show(x: Annotated[int, "this is meta", "this is test" ]):
    print(f"x: {x}")
    pass


if __name__ == "__main__":
    hints = get_type_hints(show)
    print(hints)
