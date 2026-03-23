# テスト用の関数
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("0で割ることはできません")
    return a / b


# テスト
def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0
    print("✅ test_add: OK")

def test_multiply():
    assert multiply(4, 3) == 12
    assert multiply(0, 100) == 0
    print("✅ test_multiply: OK")

def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    print("✅ test_divide: OK")


if __name__ == '__main__':
    test_add()
    test_multiply()
    test_divide()
    print("\n🎉 全テスト合格！")
