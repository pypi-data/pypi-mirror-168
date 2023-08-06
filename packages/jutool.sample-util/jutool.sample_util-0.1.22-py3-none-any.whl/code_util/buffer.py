from functools import wraps
import os, pickle
from code_util.env import buffer_folder
from code_util.str_adv import hash_obj_strbase, hash_str
from code_util.log import log_error

_buffer_items = {}


def _get_hash_key_(fun_name, *args, **kwargs):
    key_buffer_ = [hash_str(fun_name)]
    if len(args) > 0:
        key_buffer_.append([hash_obj_strbase(arg) for arg in args])
    if len(kwargs) > 0:
        key_buffer_.append([hash_obj_strbase(kwarg) for kwarg in kwargs])
    return fun_name + "_" + hash_obj_strbase(key_buffer_)


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


def _delete_buffer_file(key):
    path = os.path.join(os.getcwd(), buffer_folder, key)
    if os.path.exists(path):
        os.remove(path)


def _has_buffer_file(key):
    path = os.path.join(os.getcwd(), buffer_folder, key)
    return os.path.exists(path)


def buffer_item(key: str, value):
    nkey = _get_hash_key_(key)
    _buffer_items[nkey] = value
    _save_buffer_file(nkey)


def get_buffer_item(key: str):
    nkey = _get_hash_key_(key)

    if nkey in _buffer_items:
        return _buffer_items[nkey]

    if _has_buffer_file(nkey):
        _load_buffer_file(nkey)
        return _buffer_items[nkey]

    log_error("没有此buffer item")


def has_item_key(key: str):
    nkey = _get_hash_key_(key)

    if nkey in _buffer_items:
        return True

    if _has_buffer_file(nkey):
        return True

    return False


def remove_item(key: str):
    nkey = _get_hash_key_(key)

    if nkey in _buffer_items:
        del _buffer_items[nkey]
    if _has_buffer_file(nkey):
        _delete_buffer_file(nkey)


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
            nkey = _get_hash_key_(func.__name__, args, kwargs)
            if has_item_key(nkey):
                return get_buffer_item(nkey)

            func_result = func(*args, **kwargs)
            buffer_item(nkey, func_result)

            return func_result

        return wrapper

    return dector
