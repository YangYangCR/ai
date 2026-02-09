import torch
import torch.nn as nn
import torch.optim as optim


def train():
    # 1. 准备数据
    # y = 2x + 3，加一点随机噪声
    x = torch.linspace(-5, 5, steps=50).unsqueeze(1)  # 形状 (50, 1)
    y = 2 * x + 3 + 0.2 * torch.randn(x.size())

    # 2. 定义模型
    # 一个最简单的线性模型： y = wx + b
    model = nn.Linear(in_features=1, out_features=1)

    # 3. 定义损失函数 & 优化器
    criterion = nn.MSELoss()  # 均方误差
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 4. 训练过程
    for epoch in range(200):
        # 前向传播
        y_pred = model(x)

        # 计算损失
        loss = criterion(y_pred, y)

        # 反向传播 & 更新参数
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 40 == 0:
            print(f"Epoch [{epoch + 1}/200], Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "linear_model.pth")


def inference():
    model = nn.Linear(1, 1)  # 定义同样结构的模型
    model.load_state_dict(torch.load("linear_model.pth"))
    model.eval()
    test_x = torch.tensor([[4.0]])  # 输入一个 x=4
    pred_y = model(test_x)
    print(f"当 x=4 时，模型预测 y≈{pred_y.item():.2f}")


if __name__ == "__main__":
    # train()
    inference()
