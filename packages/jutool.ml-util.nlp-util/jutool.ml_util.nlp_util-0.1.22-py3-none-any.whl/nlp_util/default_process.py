import time
from enum import Enum
from code_util.log import log_error
import os, re, importlib


class process_enum(Enum):
    SentenceCut = 1
    WordCut = 2
    Embedding = 3


class process_setting:
    def __init__(self):
        self.process_dic = {}

    def __getitem__(self, item: process_enum):
        if item not in self.process_dic:
            nlp_util = importlib.import_module("nlp_util.components." + item.name)
            default_type = None
            for type in dir(nlp_util):
                if type.startswith("default_"):
                    default_type = type
                    break
            if default_type is None:
                log_error("找不到默认的component")
            default_type = getattr(nlp_util, default_type)
            default_type_call = getattr(default_type(), "call")
            self.process_dic[item] = default_type_call
        return self.process_dic[item]

    def replace_process(self, process_key, process_func):
        self.process_dic[process_key] = process_func


default_process_setting = process_setting()
