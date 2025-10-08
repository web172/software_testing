def password(lst):
    if len(lst) == 0: return False
    if len(lst) <=6&len(lst)>=15: return True
    return lst.isalnum()

def test_answer():
    assert password("Abc123")==True
    assert password("A1b2")==True
    assert password("A1b2C3d4E5f6G7H8")==True
    assert password("Abc12!")==False
    assert password("")==False