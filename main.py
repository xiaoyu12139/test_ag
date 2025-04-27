import logging

import pytest
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def find_newtest():
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 列出当前文件夹所有文件
    files = os.listdir(current_dir)
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
        cmd_str.append(new_file + "::Solution")
    cmd_str.extend(['-p','no:warnings']) # 配置忽略警告
    log.info(f'cmd_str: {cmd_str}')
    pytest.main(cmd_str)