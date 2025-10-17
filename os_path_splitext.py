import os.path
import request
import pytest

def test_splitext_with_extension():
    # 测试正常带扩展名的情况（基础分支）
    assert os.path.splitext("document.txt") == ("document", ".txt")
    assert os.path.splitext("image.png") == ("image", ".png")
    # 带多个字符的扩展名
    assert os.path.splitext("data.tar.gz") == ("data.tar", ".gz")

def test_splitext_without_extension():
    # 测试无扩展名的情况（无点号分支）
    assert os.path.splitext("README") == ("README", "")
    assert os.path.splitext("notes123") == ("notes123", "")
    # 路径中包含目录分隔符但无扩展名
    assert os.path.splitext("/home/user/report") == ("/home/user/report", "")

def test_splitext_special_cases():
    # 测试特殊情况（点号相关分支）
    # 文件名以点号开头（隐藏文件，无扩展名）
    assert os.path.splitext(".bashrc") == (".bashrc", "")
    # 文件名仅有点号
    assert os.path.splitext(".") == (".", "")
    # 文件名包含多个点号
    assert os.path.splitext("file.v1.2.txt") == ("file.v1.2", ".txt")
    # 空字符串
    assert os.path.splitext("") == ("", "")
