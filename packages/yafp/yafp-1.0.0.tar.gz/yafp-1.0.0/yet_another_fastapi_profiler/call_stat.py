from dataclasses import dataclass


@dataclass
class CallStat:
    filename: str
    line_number: int
    function_name: str
    number_of_calls: int
    total_time: float
    cumulative_time: float

    def is_python_internal(self, base_name: str) -> bool:
        return not self.filename.startswith(base_name)

    def __str__(self):
        return f'{self.filename}:{self.line_number} ({self.function_name}) {self.number_of_calls} ' \
               f'{self.total_time:.2f} {self.cumulative_time:.2f}'
