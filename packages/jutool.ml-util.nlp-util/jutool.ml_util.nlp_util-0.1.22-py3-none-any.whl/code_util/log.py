import math
from enum import Enum
import time, sys


class log_level_enum(Enum):
    Error = 1
    Warning = 2
    normal = 3
    pigeonhole = 4


def log(str, log_level: log_level_enum = log_level_enum.normal):
    print(f"{log_level}:{str}")


def log_error(error_message: str):
    log(error_message, log_level_enum.Error)
    raise Exception(error_message)


class process_status_bar:
    def __init__(self, processbar_length=20):
        self._iter_stack = []
        self._process_bar_len = processbar_length
        self._print_str = ""

    def _flush_(self):
        stack_str = ""
        for iter_i in range(len(self._iter_stack) - 1):
            p_value = self._iter_stack[iter_i]['value'] / float(self._iter_stack[iter_i]['max'])
            p_value = "%.2f" % (p_value * 100)
            stack_str += f"[{self._iter_stack[iter_i]['key']} {p_value}%] >>"
            pass

        current_item = self._iter_stack[-1]
        p_value = current_item["value"] / float(current_item["max"])
        p_value_str = "%.2f" % (p_value * 100)

        bar_size = math.floor(p_value * self._process_bar_len)

        bar_str = ""
        for i in range(self._process_bar_len):
            if i + 1 <= bar_size:
                bar_str += "*"
            else:
                bar_str += " "

        sys.stdout.write(
            f'\r{stack_str} {current_item["key"]} {current_item["value"]}/{current_item["max"]}  [{bar_str}]{p_value_str}% - {self._print_str} ')
        sys.stdout.flush()

    def iter_bar(self, iter_item, key=None, max=None):
        if max is None:
            if iter_item is list:
                max = len(iter_item)
            elif iter_item is {}:
                max = len(iter_item.keys())
            else:
                log_error("需要制定max值")

        if key is None:
            key = f"Iter {len(self._iter_stack)}"
        self._iter_stack.append({
            'key': key,
            'value': 0,
            'max': max
        })

        for _iter in iter_item:
            self._flush_()
            yield _iter
            self._iter_stack[-1]['value'] += 1

        self._flush_()
        self._iter_stack.pop(-1)

    def process_print(self, str):
        self._print_str = str


def process_bar_iter(iter_item, key=None, max=None):
    pb = process_status_bar()
    for item in pb.iter_bar(iter_item, key=key, max=max):
        yield item

# psb = process_status_bar()
# for s1 in psb.iter_bar([1, 2, 3], "key1", max=3):
#     for s2 in psb.iter_bar([1, 2, 3], "key2", max=3):
#         for s2 in psb.iter_bar([1, 2, 3], "key3", max=3):
#             time.sleep(0.3)
