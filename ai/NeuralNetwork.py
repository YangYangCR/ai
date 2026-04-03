import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


class NeuralNetwork:
    """2层神经网络：输入层 -> 隐藏层(64个神经元) -> 输出层(10个神经元)"""

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        # 初始化参数（使用小随机数打破对称性）
        self.W1 = np.random.randn(hidden_size, input_size) * 0.01
        self.b1 = np.zeros((hidden_size, 1))
        self.W2 = np.random.randn(output_size, hidden_size) * 0.01
        self.b2 = np.zeros((output_size, 1))
        self.lr = learning_rate

    def relu(self, Z):
        """ReLU激活函数：负数归零，正数保留"""
        return np.maximum(0, Z)

    def relu_derivative(self, Z):
        """ReLU的导数：正数为1，负数为0"""
        return (Z > 0).astype(float)

    def softmax(self, Z):
        """Softmax：将输出转换为概率分布"""
        exp_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))  # 数值稳定版本
        return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)

    def forward(self, X):
        """前向传播：计算每一层的输出"""
        # X形状: (input_size, m)，m是样本数
        self.Z1 = np.dot(self.W1, X) + self.b1  # 隐藏层线性变换
        self.A1 = self.relu(self.Z1)  # 隐藏层激活
        self.Z2 = np.dot(self.W2, self.A1) + self.b2  # 输出层线性变换
        self.A2 = self.softmax(self.Z2)  # 输出层概率
        return self.A2

    def compute_loss(self, y_true, y_pred):
        """交叉熵损失函数"""
        m = y_true.shape[1]
        # 防止log(0)导致NaN
        epsilon = 1e-12
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.sum(y_true * np.log(y_pred)) / m
        return loss

    def backward(self, X, y_true, y_pred):
        """反向传播：计算梯度"""
        m = X.shape[1]

        # 输出层梯度
        dZ2 = y_pred - y_true  # Softmax + 交叉熵的简化形式
        dW2 = np.dot(dZ2, self.A1.T) / m
        db2 = np.sum(dZ2, axis=1, keepdims=True) / m

        # 隐藏层梯度
        dA1 = np.dot(self.W2.T, dZ2)
        dZ1 = dA1 * self.relu_derivative(self.Z1)
        dW1 = np.dot(dZ1, X.T) / m
        db1 = np.sum(dZ1, axis=1, keepdims=True) / m

        # 保存梯度用于更新
        self.grads = {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}

    def update_params(self):
        """梯度下降更新参数"""
        self.W1 -= self.lr * self.grads['dW1']
        self.b1 -= self.lr * self.grads['db1']
        self.W2 -= self.lr * self.grads['dW2']
        self.b2 -= self.lr * self.grads['db2']

    def train(self, X, y, epochs=1000, verbose=True):
        """完整训练循环"""
        losses = []
        for epoch in range(epochs):
            # 前向传播
            y_pred = self.forward(X)

            # 计算损失
            loss = self.compute_loss(y, y_pred)
            losses.append(loss)

            # 反向传播
            self.backward(X, y, y_pred)

            # 更新参数
            self.update_params()

            # 打印进度
            if verbose and epoch % 100 == 0:
                accuracy = self.compute_accuracy(X, y)
                print(f"Epoch {epoch:4d}, Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

        return losses

    def predict(self, X):
        """预测类别（返回最大概率的索引）"""
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=0)

    def compute_accuracy(self, X, y_true):
        """计算准确率"""
        y_pred_idx = self.predict(X)
        y_true_idx = np.argmax(y_true, axis=0)
        return np.mean(y_pred_idx == y_true_idx)


if __name__ == "__main__":
    # ========== 加载数据：手写数字识别 ==========
    print("加载手写数字数据集...")
    digits = load_digits()
    X = digits.data / 16.0  # 归一化到[0,1]
    y = digits.target

    # 转换为神经网络需要的格式
    # X: (样本数, 特征数) -> (特征数, 样本数)
    X = X.T  # 形状: (64, 1797)
    # y: one-hot编码
    encoder = OneHotEncoder(sparse_output=False)
    y_onehot = encoder.fit_transform(y.reshape(-1, 1)).T  # 形状: (10, 1797)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X.T, y_onehot.T, test_size=0.2, random_state=42
    )
    # 转回 (特征数, 样本数) 格式
    X_train = X_train.T
    X_test = X_test.T
    y_train = y_train.T
    y_test = y_test.T

    print(f"训练集大小: {X_train.shape[1]} 样本")
    print(f"测试集大小: {X_test.shape[1]} 样本")
    print(f"输入特征数: {X_train.shape[0]}, 输出类别数: {y_train.shape[0]}")

    # ========== 创建并训练神经网络 ==========
    nn = NeuralNetwork(
        input_size=64,  # 8x8图片 = 64像素
        hidden_size=64,  # 隐藏层64个神经元
        output_size=10,  # 数字0-9共10类
        learning_rate=0.1
    )

    print("\n开始训练...")
    losses = nn.train(X_train, y_train, epochs=500, verbose=True)

    # ========== 测试模型 ==========
    test_accuracy = nn.compute_accuracy(X_test, y_test)
    print(f"\n测试集准确率: {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")

    # ========== 可视化训练过程 ==========
    plt.figure(figsize=(12, 4))

    # 损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(losses)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('训练损失曲线')
    plt.grid(True)

    # 展示一些预测结果
    plt.subplot(1, 2, 2)
    # 随机选5个测试样本
    sample_indices = np.random.choice(X_test.shape[1], 5, replace=False)
    for i, idx in enumerate(sample_indices):
        image = X_test[:, idx].reshape(8, 8)
        true_label = np.argmax(y_test[:, idx])
        pred_label = nn.predict(X_test[:, idx:idx + 1])[0]

        plt.subplot(2, 5, i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(f'真:{true_label}\n预:{pred_label}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()

    # ========== 查看学习到的权重 ==========
    # 可视化第一层权重（每个隐藏层神经元对应一个8x8的权重图）
    plt.figure(figsize=(10, 8))
    for i in range(min(64, nn.W1.shape[0])):
        plt.subplot(8, 8, i + 1)
        weight_image = nn.W1[i, :].reshape(8, 8)
        plt.imshow(weight_image, cmap='RdBu', vmin=-np.abs(weight_image).max(),
                   vmax=np.abs(weight_image).max())
        plt.axis('off')
    plt.suptitle('第一层权重可视化（红色=正权重，蓝色=负权重）')
    plt.tight_layout()
    plt.show()