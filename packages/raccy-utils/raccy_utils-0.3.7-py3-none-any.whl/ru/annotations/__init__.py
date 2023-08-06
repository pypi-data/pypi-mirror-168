import os
import typing

Cast = typing.Callable[[typing.Any], typing.Any]
Path = typing.Union[str, bytes, os.PathLike]
Config = typing.Dict[str, str]
