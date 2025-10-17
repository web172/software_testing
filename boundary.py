def age(lst):
    if type(lst)!=type(1): return False
    if (lst <18)|(lst>60): return False
    return True

def test_answer():
    assert age(18)==True
    assert age(60)==True
    assert age(18.2)==False
    assert age(-19)==False
    assert age("-")==False
