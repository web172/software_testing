# 自定义异常类（明确区分不同异常场景）
class UserNotFoundError(Exception):
    """用户不存在时抛出的异常"""
    pass

class BookNotFoundError(Exception):
    """图书不存在时抛出的异常"""
    pass

class BookOutOfStockError(Exception):
    """图书库存为0时抛出的异常"""
    pass

# 模拟数据（实际项目中替换为数据库）
# 1. 用户数据：key=用户名，value=用户详情（示例含姓名、ID）
USERS = {
    "user1": {"user_id": 1, "name": "张三"},
    "user2": {"user_id": 2, "name": "李四"},
    "user3": {"user_id": 3, "name": "王五"}
}

# 2. 图书数据：key=图书ID/ISBN，value=图书详情（含库存）
BOOKS = {
    "b001": {"title": "Python编程", "author": "张三", "stock": 5},  # 库存充足
    "b002": {"title": "算法导论", "author": "李四", "stock": 0},   # 库存为0
    "b003": {"title": "数据结构", "author": "王五", "stock": 2}    # 库存充足
}

def borrow_book(user: str, book_id: str) -> str:
    """
    实现借书功能
    :param user: 用户名（需在 USERS 中存在）
    :param book_id: 图书ID（需在 BOOKS 中存在）
    :return: 借书成功提示信息
    :raises: UserNotFoundError/BookNotFoundError/BookOutOfStockError
    """
    # 1. 检查用户是否存在
    if user not in USERS:
        raise UserNotFoundError(f"用户「{user}」不存在，无法借书")
    
    # 2. 检查图书是否存在
    if book_id not in BOOKS:
        raise BookNotFoundError(f"图书ID「{book_id}」不存在，无法借书")
    
    # 3. 检查图书是否可借（库存 > 0）
    book = BOOKS[book_id]
    if book["stock"] <= 0:
        raise BookOutOfStockError(f"图书「{book['title']}」（ID：{book_id}）库存为0，无法借书")
    
    # 4. 借书成功：库存减少1
    book["stock"] -= 1
    
    # 返回成功信息（包含用户、图书、剩余库存）
    return (f"用户「{USERS[user]['name']}」（用户名：{user}）成功借出图书「{book['title']}」\n"
            f"图书剩余库存：{book['stock']}")
import pytest

# ---------------------- 测试前重置数据（避免用例间相互影响）----------------------
@pytest.fixture(autouse=True)  # autouse=True：每个测试用例执行前自动调用
def reset_data():
    # 重置图书库存为初始状态
    BOOKS["b001"]["stock"] = 5
    BOOKS["b002"]["stock"] = 0
    BOOKS["b003"]["stock"] = 2
    yield  # 测试用例执行后，自动继续（此处无后续操作，仅重置前置数据）

# ---------------------- 测试用例 ----------------------
def test_borrow_book_normal():
    """测试1：正常借书（用户存在、图书存在、库存充足）"""
    result = borrow_book(user="user1", book_id="b001")
    # 断言1：返回信息包含成功关键词
    assert "成功借出" in result
    # 断言2：库存减少1（初始5 → 4）
    assert BOOKS["b001"]["stock"] == 4

def test_borrow_book_user_not_found():
    """测试2：用户不存在（异常场景）"""
    with pytest.raises(UserNotFoundError) as excinfo:
        borrow_book(user="user_not_exist", book_id="b001")
    # 断言：异常信息符合预期
    assert "用户「user_not_exist」不存在" in str(excinfo.value)

def test_borrow_book_book_not_found():
    """测试3：图书不存在（异常场景）"""
    with pytest.raises(BookNotFoundError) as excinfo:
        borrow_book(user="user1", book_id="b999")
    # 断言：异常信息符合预期
    assert "图书ID「b999」不存在" in str(excinfo.value)

def test_borrow_book_out_of_stock():
    """测试4：图书库存为0（异常场景）"""
    with pytest.raises(BookOutOfStockError) as excinfo:
        borrow_book(user="user1", book_id="b002")  # b002 初始库存0
    # 断言：异常信息包含库存为0
    assert "库存为0，无法借书" in str(excinfo.value)

def test_borrow_book_stock_to_zero():
    """测试5：连续借书至库存0（边界场景）"""
    # 第一次借书（库存2→1）
    borrow_book(user="user2", book_id="b003")
    # 第二次借书（库存1→0）
    borrow_book(user="user2", book_id="b003")
    # 第三次借书（库存0，应抛异常）
    with pytest.raises(BookOutOfStockError):
        borrow_book(user="user2", book_id="b003")
    # 断言：库存最终为0
    assert BOOKS["b003"]["stock"] == 0

def test_borrow_book_invalid_input_type():
    """测试6：异常输入类型（如用户名为数字、图书ID为列表，边界场景）"""
    # 测试用户名不是字符串（如int）
    with pytest.raises(UserNotFoundError):
        borrow_book(user=123, book_id="b001")  # user=123 不在 USERS（key是字符串）
    # 测试图书ID不是字符串（如list）
    with pytest.raises(BookNotFoundError):
        borrow_book(user="user1", book_id=["b001"])  # book_id是列表，不在 BOOKS