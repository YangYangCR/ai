from tqdm import tqdm
import time
from queue import Queue

if __name__ == "__main__":

    for i in tqdm(range(100), desc="处理中"):
        # 你的代码
        time.sleep(0.1)

    # 动态更新描述
    pbar = tqdm(range(100), desc="初始状态")
    for i in pbar:
        time.sleep(0.1)
        pbar.set_description(f"处理第 {i} 项")