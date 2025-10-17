import requests, time, subprocess
def test_db_failure_recovery():
# 停掉数据库（假设用 docker-compose 起的 MySQL）
    subprocess.run(["docker","stop","mysql_db"])
    time.sleep(2)
    res = requests.post("http://127.0.0.1:5000/order", json={"item": "book","qty": 1})
    assert res.status_code in (500, 503) # 系统要能识别出错
    # 恢复数据库
    subprocess.run(["docker","start","mysql_db"])
    time.sleep(5)
    res2 = requests.post("http://127.0.0.1:5000/order", json={"item": "book","qty": 1})
    assert res2.status_code == 200