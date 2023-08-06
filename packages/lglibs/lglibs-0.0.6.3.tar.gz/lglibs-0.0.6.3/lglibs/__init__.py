import sys as _system
import inspect as _inspect
import time as _time
import os as _os
import base64 as _base64
from . import color as _color

def encode(content: str, save: bool = False, save_path:str=None):
    if not save and save_path is not None:
        raise ValueError("save is off, but still have save path")
    elif save and save_path is None:
        raise ValueError("save is on, but save path is None")
    elif save and save_path is not None:
        file = open(save_path, "wb")
        file.write(_base64.b64encode(content.encode("ascii")))
        file.close()
    else:
        return _base64.b64encode(content.encode("ascii"))
def decode(_bytes: bytes = None, read: bool = False, read_path: str = None):
    if _bytes is not None and read:
        raise ValueError("Bytes have been passed in but read mode is still on")
    elif not read and read_path is not None:
        raise ValueError("read is off, but still have read path")
    elif read and read_path is None:
        raise ValueError("read is on, but read path is None")
    elif read and read_path is not None:
        file = open(read_path, "rb")
        content = _base64.b64decode(file.read()).decode("utf-8")
        file.close()
        return content
    else:
        return _base64.b64decode(_bytes).decode("utf-8")
def decimal(obj: float):
    _obj = str(obj)
    returned = []
    for index in range(1, len(_obj)):
        if _obj[-index] == ".": break
        else: returned.append(_obj[-index])
    returned.reverse()
    rstring = ""
    for char in returned: rstring += char
    return rstring
def _merge_string_list(obj: list):
    new_string = ""
    for text in obj: new_string += text
    return new_string
def Round(obj: float, _to: int = 0):
    if not _to: return round(obj)
    if len(str(decimal(obj))) < _to:
        return round(obj, _to)
    decimals = list(str(decimal(obj)))
    count = 1
    AddOne = False
    if len(decimals) == 1: return obj
    if int(decimals[_to]) >= 5:
        decimals[_to - 1] = str(int(decimals[_to - 1]) + 1)
    del decimals[_to: len(decimals)]
    while int(decimals[_to - count]) == 10:
        if _to - count <= 0: decimals[_to - count] = "0"; AddOne = True; break
        decimals[_to - count] = "0"
        decimals[_to - count - 1] = str(int(decimals[_to - count - 1]) + 1)
        count += 1
    decimals = _merge_string_list(decimals)
    Object = str(int(obj))
    res = Object + "." + decimals
    if AddOne: return float(res) + 1
    else: return float(res)
def Range(range_x: int or float, range_y: int or float = None, step: int or float = None):
    if range_y is None: range_y = range_x; range_x = 0
    if step is None: step = 1
    if range_x < range_y:
        while range_x < range_y:
            yield range_x
            range_x += step
    if range_x > range_y:
        while range_x >= range_y:
            yield range_x
            range_x -= step

# Convert variable name to string
def nameof(var):
    callers_local_vars = _inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]

def createof(Type, *args, **kwargs):
    __object__ = Type(*args, **kwargs)
    for keys, vals in Type.__dict__.items():
        if type(vals) is list: __object__[keys] = Type.__dict__[keys].copy()
        if type(vals) is dict: __object__[keys] = Type.__dict__[keys].copy()
    return __object__
def Convert(obj, Type):
    if type(obj) is list:
        return_list = [].copy()
        for index in range(len(obj)):
            return_list[index] = Type(obj[index])
        return return_list
    elif type(obj) is dict:
        return_dict = {}.copy()
        for key in obj:
            return_dict[key] = Type(obj[key])
        return return_dict
    else: return Type(obj)
def breakdown(obj):
    return_list = [].copy()
    for index in range(len(obj)):
        try:
            for _index in range(len(obj[index])):
                return_list.append(obj[index][_index])
        except TypeError:
            continue
    return return_list
                

class cursor:
    def __init__(self):
        self.ci = None
        if _os.name == "nt":
            self._msvcrt = __import__("msvcrt")
            self._ctypes = __import__("ctypes")
            class _CursorInfo(self._ctypes.Structure):
                _fields_ = [("size", self._ctypes.c_int), ("visible", self._ctypes.c_byte)]
            self.ci = _CursorInfo()
    def hide(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self.ci.visible = False
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _system.stdout.write("\033[?25l")
            _system.stdout.flush()
    def show(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self.ci.visible = True
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _system.stdout.write("\033[?25h")
            _system.stdout.flush()


class console:
    @staticmethod
    def write(*content, timer: int = 0.02, skip=breakdown(_color._allcolor),sep=" " ,end="\n"):
        for text in content:
            text = str(text)
            for index in range(len(text)):
                _system.stdout.write(text[index])
                _system.stdout.flush()
                if type(skip) is str and text[index] != skip: _time.sleep(timer)
                if type(skip) is list and text[index] not in skip: _time.sleep(timer)
                if type(skip) is not str and type(skip) is not list: raise Exception("Error, arg skip should be \'str\' or \'list\', not " + type(skip).__name__)
            _system.stdout.write(sep)
            _system.stdout.flush()
        print(end=end, flush=True)
    @staticmethod
    def read(putout: str = "", rtype=str, **args):
        console.write(putout, end="", **args)
        return rtype(input(""))
    @staticmethod
    def clsline(clear_char=50): _system.stdout.write("\r" + " " * clear_char + "\r"); _system.stdout.flush()
    @staticmethod
    def reline(): print(end="\033[F", flush=True)
# Any variable can be stored in the template, and can be Assgin later with the Add function
class Template:
    def __init__(self, **args):
        self.args = args
        self.assginSelf()

    def __str__(self):
        return str(self.args)

    def assginSelf(self):
        for key, value in self.args.items():
            self.__dict__[key] = value

    def Assgin(self, **arg):
        for key, value in arg.items():
            self.args[key] = value
        self.assginSelf()

    def AssginDict(self, *arg):
        for rdict in arg:
            for key, value in rdict.items():
                self.args[key] = value
            self.assginSelf()

    def delete(self, *arg_names):
        for name in arg_names:
            for vals_name, vals in self.__dict__.items():
                if vals_name == name:
                    del self.__dict__[vals_name]
                    del self.args[vals_name]

    def __add__(self, otherT):
        ReTemplate = Template()
        ReTemplate.AssginDict(self.args, otherT.args)
        return ReTemplate

    def __sub__(self, other):
        ReTemplate = Template()



