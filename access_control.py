def grant_access(is_employee, has_high_clearance, is_within_visit_window,is_escorted):
    grant = False
    if is_employee and (has_high_clearance or (is_within_visit_window and is_escorted)):
        grant = True
    return grant


def test_answer():
    assert grant_access(True, True, True, True) == True
    assert grant_access(True, True, True, False) == True
    assert grant_access(True, True, False, False) == True
    assert grant_access(True, False, True, True) == True
    assert grant_access(True, False, True, False) == False
    assert grant_access(False, True, True, True) == False
    assert grant_access(False, True, True, False) == False
