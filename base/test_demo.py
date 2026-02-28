import pytest
import sys


# pytest test_demo.py::test_big_computation

# 给测试函数打上 “slow” 标签
# pytest -m slow
@pytest.mark.slow
def test_big_computation():
    assert 1 + 1 == 2


# 强制跳过测试
@pytest.mark.skip(reason="功能未实现")
def test_not_ready():
    assert False

# 条件跳过
@pytest.mark.skipif(sys.platform == "win32", reason="Windows 不支持这个功能")
def test_linux_only():
    assert True