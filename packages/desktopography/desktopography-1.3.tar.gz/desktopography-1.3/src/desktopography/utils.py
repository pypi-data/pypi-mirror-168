import subprocess
import typing


def gsettings(
    action: typing.Literal["set"] | typing.Literal["get"],
    schema: str,
    key: str,
    value: str | None = None,
) -> str:
    process = subprocess.run(
        args=[x for x in ("gsettings", action, schema, key, value) if x is not None],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return process.stdout.strip().strip("'")
