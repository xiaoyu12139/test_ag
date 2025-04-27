import logging
from dataclasses import dataclass
from functools import wraps

import pytest
import inspect

logging.basicConfig(level=logging.DEBUG)
log_debug = logging.getLogger("debug")

def ag_test(cases, expected):
    def decorator(func):
        # 判断装饰的是类，还是类中的方法，还是函数
        if inspect.isclass(func):
            pass
        elif inspect.isfunction(func):
            qualname = func.__qualname__  # 形如 "MyClass.my_method" 或 "plain_func"
            if "." in qualname:  # 方法的 qualname 含点号
                log_debug.debug("method_in_class")
                # arg_names = func.__code__.co_varnames[:len(cases[0]) + 1]
                arg_names = func.__code__.co_varnames[1:]
                log_debug.debug(f'arg_names: {arg_names}')

                @pytest.mark.parametrize(",".join(arg_names), cases)
                @wraps(func)
                def wrapper(*args, **kwargs):
                    real_args = tuple(kwargs[name] for name in arg_names)
                    try:
                        index = next(i for i, case in enumerate(cases) if tuple(case) == tuple(real_args))
                    except StopIteration:
                        raise ValueError(f"传入参数 {real_args} 不在cases列表中！")
                    expected_value = expected[index]
                    result = func(*args, **kwargs)
                    assert result == expected_value, f"断言失败，返回值={result}, 预期值={expected_value}，参数={real_args}"
                    return result

                return wrapper
            else:
                log_debug.debug("module_function")
                arg_names = func.__code__.co_varnames[:len(cases[0])]
                logging.info(f'arg_names: {arg_names}')

                @pytest.mark.parametrize(",".join(arg_names), cases)
                @wraps(func)
                def wrapper(*args, **kwargs):
                    real_args = args[1:] if isinstance(args[0], object) else args
                    index = next(i for i, case in enumerate(cases) if case == real_args)
                    expected_value = expected[index]
                    result = func(*args, **kwargs)
                    assert result == expected_value, f"断言失败，返回值={result}, 预期值={expected_value}，参数={args}"
                    return result

                return wrapper
        else:
            pass
    return decorator


def ag_parametrize_assert(cases, expected, assert_func):
    """
    @ag_parametrize_assert(
        cases=[...],
        expected=[...],
        assert_func=lambda result, expected: result == expected
    )
    """

    def decorator(func):
        if len(cases) != len(expected):
            raise ValueError("cases和expected长度必须一致")

        arg_names = func.__code__.co_varnames[:len(cases[0])]

        @pytest.mark.parametrize(",".join(arg_names), cases)
        @wraps(func)
        def wrapper(*args, **kwargs):
            # pytest参数化时，没法直接拿 expected，所以需要动态映射
            index = cases.index(args)
            expected_value = expected[index]

            result = func(*args, **kwargs)

            assert assert_func(result, expected_value), \
                f"断言失败，返回值={result}, 预期={expected_value}, 参数={args}"
            return result

        return wrapper

    return decorator

@dataclass
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

@dataclass
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(arr):
    head = ListNode()
    cur = head
    for item in arr:
        cur.next = TreeNode(item)
        cur = cur.next
    return head.next

def build_tree(lst):
    """
    [1,2,2,2,None,2]层序遍历构建树，最后一个叶子节点为空不需要写None
    :param lst:
    :return:
    """
    if not lst:
        return None

    # 创建根节点
    root = TreeNode(lst[0])

    # 使用队列进行层序遍历，构建树
    queue = [root]
    i = 1
    while i < len(lst):
        node = queue.pop(0)

        # 左子节点
        if lst[i] is None:
            node.left = None
        elif i < len(lst):
            node.left = TreeNode(lst[i])
            queue.append(node.left)
        i += 1
        if not i < len(lst):
            break
        # 右子节点
        if lst[i] is None:
            node.right = None
        elif i < len(lst):
            node.right = TreeNode(lst[i])
            queue.append(node.right)
        i += 1

    return root