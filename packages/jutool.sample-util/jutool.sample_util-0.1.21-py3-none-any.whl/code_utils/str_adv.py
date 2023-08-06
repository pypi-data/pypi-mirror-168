import hashlib
from code_utils.structures import func_check
from collections import Iterable


@func_check
def hash_str(target_str: str) -> str:
    """
    使用MD5对str进行hash编码
    :param target_str: 需要编码的str
    :return:
    """
    return hashlib.md5(target_str.encode("utf8")).hexdigest()


def hash_obj_strbase(obj) -> str:
    """
    对对象进行迭代编码
    :param obj:
    :return:
    """
    if isinstance(obj, str):
        return hash_str(obj)
    if isinstance(obj, Iterable) or isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict):
        items_hashed_list = [hash_obj_strbase(x) for x in obj]
        return hash_str("".join(items_hashed_list))
    else:
        return hash_str(obj.__str__())


