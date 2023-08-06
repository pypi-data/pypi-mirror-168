import cProfile
import enum
import pstats
import sys
import time
from logging import Logger
from typing import Iterable

from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from yet_another_fastapi_profiler.call_stat import CallStat

__VERSION__ = (1, 0, 0)


# noinspection PyArgumentList
class ProfilerMiddlewareSortOption(enum.Enum):
    # https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
    CALLS = enum.auto()
    CUMULATIVE = enum.auto()
    FILENAME = enum.auto()
    TIME = enum.auto()


class ProfilerMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            sort_by: ProfilerMiddlewareSortOption = ProfilerMiddlewareSortOption.CUMULATIVE,
            sort_reverse: bool = True,
            minimal_cumulative_time_to_print: int = 0,
            ignore_python_internals: bool = False,
            logger: Logger | None = None,
            endpoints_to_measure: Iterable[str] | None = None
    ):
        self.app = app
        self._profiler = cProfile.Profile(timer=time.perf_counter)
        self._sort_by = sort_by
        self._min_print_time = minimal_cumulative_time_to_print
        self._ignore_python_internals = ignore_python_internals
        self._logger = logger
        self._sort_reverse = sort_reverse
        self._base_name = sys.argv[0]
        self._endpoints_to_measure = endpoints_to_measure

        self._sort_keys_binds = {
            ProfilerMiddlewareSortOption.CUMULATIVE: 'cumulative_time',
            ProfilerMiddlewareSortOption.CALLS: 'number_of_calls',
            ProfilerMiddlewareSortOption.FILENAME: 'filename',
            ProfilerMiddlewareSortOption.TIME: 'total_time',
        }

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        method = request.method
        path = request.url.path

        profile = True
        if self._endpoints_to_measure is not None:
            if path not in self._endpoints_to_measure:
                profile = False

        status_code = 500

        async def wrapped_send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                nonlocal status_code
                status_code = message['status']
            await send(message)

        self._profiler.enable()
        begin = time.perf_counter()

        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            if profile:
                end = time.perf_counter()
                self._profiler.disable()
                stats = pstats.Stats(self._profiler)
                stats = self._parse_stats(stats)
                stats = self._filter_ps_stats(stats)
                stats = self._sort_stats(stats)
                self._log_stats(method, path, (end - begin), status_code, stats)

    def _filter_ps_stats(self, stats: list[CallStat]) -> list[CallStat]:
        if self._min_print_time != 0:
            stats = self._filter_min_time(stats)
        if self._ignore_python_internals:
            stats = self._filter_python_internals(stats)
        return stats

    def _filter_min_time(self, stats: list[CallStat]) -> list[CallStat]:
        stats = list(filter(lambda x: x.cumulative_time > self._min_print_time, stats))
        return stats

    def _filter_python_internals(self, stats: list[CallStat]) -> list[CallStat]:
        stats = list(filter(lambda x: not x.is_python_internal(self._base_name), stats))
        return stats

    def _sort_stats(self, stats: list[CallStat]) -> list[CallStat]:
        key = self._sort_keys_binds[self._sort_by]
        stats = sorted(stats, key=lambda x: x.__getattribute__(key), reverse=self._sort_reverse)
        return stats

    @staticmethod
    def _parse_stats(stats: pstats.Stats) -> list[CallStat]:
        result = []
        for k, v in stats.stats.items():
            file, line_no, name = k
            calls, _, total_time, cumulative_time, _ = v
            stat = CallStat(
                filename=file,
                line_number=line_no,
                function_name=name,
                number_of_calls=calls,
                total_time=total_time,
                cumulative_time=cumulative_time
            )
            result.append(stat)
        return result

    def _log(self, msg: str):
        if self._logger is None:
            print(msg)
        else:
            self._logger.info(msg)

    def _log_stats(self, method: str, path: str, time_elapsed: float, status_code: int, stats: list[CallStat]):
        log = f"{method} {path} {time_elapsed:.2f}, {status_code}"
        self._log(log)
        for stat in stats:
            self._log(str(stat))
