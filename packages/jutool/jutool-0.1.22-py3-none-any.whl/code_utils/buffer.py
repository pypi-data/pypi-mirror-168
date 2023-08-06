from functools import wraps
import os, pickle
from code_utils.env import buffer_folder
from code_utils.str_adv import hash_obj_strbase, hash_str

_buffer_items = {}


def _get_hash_key_(fun_name, *args, **kwargs):
    key_buffer_ = [hash_str(fun_name)]
    if len(args) > 0:
        key_buffer_.append([hash_obj_strbase(arg) for arg in args])
    if len(kwargs) > 0:
        key_buffer_.append([hash_obj_strbase(kwarg) for kwarg in kwargs])
    return hash_obj_strbase(key_buffer_)


def _load_buffer_file(key):
    path = os.path.join(os.getcwd(), buffer_folder, key)
    with open(path, 'rb') as f:
        saved_item = pickle.load(f)
    _buffer_items[key] = saved_item


def _save_buffer_file(key):
    path = os.path.join(os.getcwd(), buffer_folder, key)
    folder = os.path.join(os.getcwd(), buffer_folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    with open(path, 'wb') as f:
        pickle.dump(_buffer_items[key], f)


def _has_buffer_file(key):
    path = os.path.join(os.getcwd(), buffer_folder, key)
    return os.path.exists(path)


def buffer(permanent=False):
    '''
    缓存方法的值
    :param permanent: 是否永久化存储
    :return:
    '''

    def dector(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _buffer_items
            key = _get_hash_key_(func.__name__, args, kwargs)
            if key in _buffer_items:
                return _buffer_items[key]

            if permanent and _has_buffer_file(key):
                _load_buffer_file(key)
                return _buffer_items[key]

            func_result = func(*args, **kwargs)
            _buffer_items[key] = func_result

            if permanent:
                _save_buffer_file(key)

            return func_result

        return wrapper

    return dector
