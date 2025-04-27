import manage_builtin
import logging

import pytest
import os
import sys
import base

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

test_dir = 'test'

def find_newtest():
    # 获取当前工作目录
    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, test_dir)
    # 列出当前文件夹所有文件
    files = os.listdir(target_dir)
    # 筛选出以 test_ 开头的文件
    test_files = [f for f in files if f.startswith("test")]
    if not test_files:
        return None  # 没有找到
    test_files_sorted = sorted(test_files)
    latest_file = test_files_sorted[-1]
    return latest_file

if __name__ == '__main__':
    new_file = find_newtest()
    cmd_str = []
    # cmd_str.append('-q')  # 简化输出
    # cmd_str.append('--tb=short')  # 简化输出
    cmd_str.append('--tb=line')  # 简化输出
    if new_file:
        log.info(f"New file found: {new_file}")
        file_path = os.path.join(test_dir, new_file)
        # cmd_str.append(file_path + "::Solution")
        cmd_str.append(file_path)
    # cmd_str.extend(['-p','no:warnings']) # 配置忽略警告
    cmd_str.append('--disable-warnings') # 配置忽略警告
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        cmd_str.append('--log-cli-level=DEBUG')
    log.info(f'cmd_str: {cmd_str}')
    injector = manage_builtin.BuiltinInjector()
    try:
        injector.inject_from_module(base)  # 启动时注入
        pytest.main(cmd_str)
    finally:
        injector.cleanup()  # 程序结束时清理
