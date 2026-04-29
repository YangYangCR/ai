# main.py
# import calculator
from calculator import add

if __name__ == "__main__":
    print("--- 主程序开始 ---")
    #result = calculator.add(10, 20)
    result = add(10, 20)
    print(f"10 + 20 = {result}")