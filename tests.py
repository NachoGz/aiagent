from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print("==================Test 1==================")
    print(result)
    print("==================Test 1==================")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("==================Test 2==================")
    print(result)
    print("==================Test 2==================")

    result = run_python_file("calculator", "tests.py")
    print("==================Test 3==================")
    print(result)
    print("==================Test 3==================")

    result = run_python_file("calculator", "../main.py")
    print("==================Test 4==================")
    print(result)
    print("==================Test 4==================")
    print()

    result = run_python_file("calculator", "nonexistent.py")
    print("==================Test 5==================")
    print(result)
    print("==================Test 5==================")
    print()


if __name__ == '__main__':
    test()
