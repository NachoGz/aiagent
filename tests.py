from functions.run_python import run_python

def test():
    result = run_python("calculator", "main.py")
    print("==================Test 1==================")
    print(result)
    print("==================Test 1==================")

    result = run_python("calculator", "main.py", ["3 + 5"])
    print("==================Test 2==================")
    print(result)
    print("==================Test 2==================")

    result = run_python("calculator", "tests.py")
    print("==================Test 3==================")
    print(result)
    print("==================Test 3==================")

    result = run_python("calculator", "../main.py")
    print("==================Test 4==================")
    print(result)
    print("==================Test 4==================")
    print()

    result = run_python("calculator", "nonexistent.py")
    print("==================Test 5==================")
    print(result)
    print("==================Test 5==================")
    print()


if __name__ == '__main__':
    test()
