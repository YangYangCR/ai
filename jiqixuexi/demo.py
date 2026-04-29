

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

if __name__ == "__main__":

    # 1. 构造数据（面积 -> 房价）
    X = np.array([[50], [60], [80], [100], [120]])  # 面积
    y = np.array([150, 180, 240, 300, 360])        # 房价

    # 2. 创建模型
    model = LinearRegression()

    # 3. 训练模型
    model.fit(X, y)

    # 4. 预测
    predicted_price = model.predict([[90]])
    print("预测90平米房价:", predicted_price)

    path = ""
    if not path:
        print("=====")

    # 5. 可视化
    # plt.scatter(X, y, label="真实数据")
    # plt.plot(X, model.predict(X), color='red', label="拟合直线")
    # plt.xlabel("面积")
    # plt.ylabel("价格")
    # plt.legend()
    # plt.show()