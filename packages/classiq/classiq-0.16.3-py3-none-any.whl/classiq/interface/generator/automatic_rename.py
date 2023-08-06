from typing import Collection


def rename_existing_name(name: str) -> str:
    return name + "_"


def automatic_rename(name: str, names: Collection[str]) -> str:
    while name in names:
        name = rename_existing_name(name)
    return name
