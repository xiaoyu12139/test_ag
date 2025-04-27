import builtins
import inspect
import os

import base

class BuiltinInjector:
    def __init__(self):
        self.injected_names = []

    def inject_from_module(self, module, only_functions=True):
        """从模块注入函数/对象到builtins"""
        for name, obj in inspect.getmembers(module):
            if only_functions and not inspect.isfunction(obj):
                continue
            if name.startswith("__"):
                continue
            setattr(builtins, name, obj)
            self.injected_names.append(name)

    def cleanup(self):
        """从builtins移除注入过的名字"""
        for name in self.injected_names:
            if hasattr(builtins, name):
                delattr(builtins, name)
        self.injected_names.clear()

    @staticmethod
    def get_module(module, only_functions=True):
        res_list = []
        for name, obj in inspect.getmembers(module):
            if only_functions and not inspect.isfunction(obj):
                continue
            if name.startswith("__"):
                continue
            res_list.append(name)
        return res_list

    @staticmethod
    def check_module(module, only_functions=True):
        module_list = BuiltinInjector.get_module(module, only_functions)
        res_list = []
        for name in dir(builtins):
            if name in module_list:
                res_list.append(name)
        if res_list:
            print("========疑似污染=======")
            print(res_list)
        else:
            print("========安全=======")

if __name__ == '__main__':
    # 检测环境是否被污染
    BuiltinInjector.check_module(base)
    # os.system('pause')
    input('任意键继续...')