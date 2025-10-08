def loop(lst,target):
    for x in range(len(lst)):
        if lst[x] == target:
            return x
    return -1
def test_answer():
    assert loop([5],5)==0
    assert loop([5],10)==-1
    assert loop([1,2],2)==1
    assert loop([1,2,3,4],4)==3
    assert loop([1,2,3,4,5],5)==4
    assert loop([1,2,3,4,5,6],10)==-1