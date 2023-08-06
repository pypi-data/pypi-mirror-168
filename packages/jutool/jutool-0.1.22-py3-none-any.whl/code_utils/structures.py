from functools import wraps
from code_utils.env import __isDebug
from code_utils.log import log, log_level_enum
import time


def iter_idx(iter_item):
    """
    返回 item，idx的可枚举
    :param iter_item:
    :return:
    """
    return zip(iter_item, range(len(iter_item)))


def _type_error(func_name, param_name, except_type, actual_type):
    raise Exception(
        f'{func_name}中的参数{param_name}类型错误，期望类型：{str(except_type)}, 实际类型：{str(actual_type)}')


def _type_blank(func_name, param_name):
    log(f'Warning:{func_name}中的参数{param_name}未指定类型。', log_level=log_level_enum.Warning)


def func_check(func):
    """
    对方法的参数注释的检测
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def check_type(obj, type_limited, default=None):
            p = obj if obj is not None else default
            return isinstance(p, type_limited)

        if not __isDebug:
            return func(*args, **kwargs)

        types_limited = func.__annotations__
        par_names = func.__code__.co_varnames
        defaults_values = func.__defaults__

        arg_dic = []
        for name, idx in iter_idx(par_names):
            c_dic = {'key': name, 'limit': None, 'arg': None, 'default': None}
            if name in types_limited:
                c_dic['limit'] = types_limited[name]
            if idx < len(args):
                c_dic['arg'] = args[idx]
            if name in kwargs:
                c_dic['arg'] = kwargs[name]

            arg_dic.append(c_dic)
        # default value
        if defaults_values is not None:
            for _, idx in iter_idx(defaults_values):
                arg_idex = len(par_names) - len(defaults_values) + idx
                arg_dic[arg_idex]['default'] = defaults_values[idx]

        for dic_item in arg_dic:
            if dic_item['limit'] is None:
                _type_blank(func.__name__, dic_item['key'])
            else:
                if not check_type(dic_item['arg'], dic_item['limit'], dic_item['default']):
                    key = dic_item['key']
                    _type_error(func.__name__, key, dic_item['limit'], None)

        result_item = func(*args, **kwargs)

        if 'return' in types_limited:
            if not check_type(result_item, types_limited['return'], None):
                _type_error(func.__name__, "return", types_limited['return'], None)
        else:
            _type_blank(func.__name__, "return")

        return result_item

    return wrapper


_time_cost_dic = {}


def time_cost(key='#'):
    def dector(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _time_cost_dic
            start = time.time()
            ret = func(*args, **kwargs)
            log(f'{func.__name__} cost {time.time() - start}', log_level_enum.normal)
            last_cost = time.time() - start
            _time_cost_dic[key] = last_cost
            _time_cost_dic['#'] = last_cost
            return ret

        return wrapper

    return dector


def get_last_time_cost():
    return _time_cost_dic['#']
