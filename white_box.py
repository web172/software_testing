def calculate(x, y):
    if x > 0 and y > 0:
        return x + y
    elif x < 0 or y < 0:
        return x - y
    else:
        return 0

def test_answer():
    assert calculate(2, 3) == 5
    assert calculate(-2, 5) == -7
    assert calculate(0, 0) == 0