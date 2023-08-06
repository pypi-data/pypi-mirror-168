"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import pathlib
import os
import asyncio
import threading
import typing

from colorama import Fore

from ru.annotations import Path


def logger(
        name: typing.Optional[str] = None,
        fmt: typing.Optional[str] = None,
        filename: typing.Optional[Path] = None
) -> logging.Logger:
    lg: Logger = Logger(name, fmt, filename)
    return lg()


class Logger:
    __loggers: typing.Dict[str, logging.Logger] = {}

    def __init__(
            self,
            name: typing.Optional[str] = None,
            fmt: typing.Optional[str] = None,
            filename: typing.Optional[Path] = None
    ) -> None:
        self._name = name if name else __name__
        self._fmt = fmt if fmt else '%(asctime)s:%(levelname)s:%(message)s'
        self._filename = filename
        self._root_path: Path = pathlib.Path('.').absolute()

    def _get_log_file(self) -> Path:
        fn: Path = self._filename if self._filename else 'log'
        log_path: Path = os.path.join(self._root_path, 'logs')
        log_file: Path = os.path.join(log_path, f'{fn}.log')
        if not os.path.exists(log_path):
            os.mkdir(os.path.join(log_path))
        return log_file

    def _create_logger(self) -> logging.Logger:
        _logger: logging.Logger = logging.getLogger(self._name)
        _logger.setLevel(level=logging.DEBUG)

        formatter: logging.Formatter = logging.Formatter(self._fmt)
        file_handler: logging.FileHandler = logging.FileHandler(self._get_log_file(), encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        _logger.addHandler(file_handler)
        _logger.addHandler(stream_handler)

        return _logger

    def __call__(self) -> logging.Logger:
        if self._name in self.__loggers:
            return self.__loggers[self._name]
        else:
            _logger: logging.Logger = self._create_logger()
            self.__loggers[self._name] = _logger
            return _logger


class BaseColorPrint:
    mutex: typing.Optional[typing.Union[asyncio.Lock, threading.Lock, threading.RLock]] = None

    def _print(self, text: str, color: str) -> None:
        with self.mutex:
            print(color + text)

    def info(self, text: str, color: str = Fore.MAGENTA) -> None:
        self._print(text, color)

    def warning(self, text: str, color: str = Fore.YELLOW) -> None:
        self._print(text, color)

    def success(self, text: str, color: str = Fore.GREEN) -> None:
        self._print(text, color)

    def error(self, text: str, color: str = Fore.RED) -> None:
        self._print(text, color)


class ColorPrint(BaseColorPrint):
    mutex: threading.Lock = threading.Lock()


class AsyncColorPrint(BaseColorPrint):
    mutex: asyncio.Lock = asyncio.Lock()

    async def _print(self, text: str, color: str) -> None:
        async with self.mutex:
            print(color + text)

    async def info(self, text: str, color: str = Fore.MAGENTA) -> None:
        await self._print(text, color)

    async def warning(self, text: str, color: str = Fore.YELLOW) -> None:
        await self._print(text, color)

    async def success(self, text: str, color: str = Fore.GREEN) -> None:
        await self._print(text, color)

    async def error(self, text: str, color: str = Fore.RED) -> None:
        await self._print(text, color)
