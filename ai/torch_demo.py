import torch

if __name__ == "__main__":
    # 设置数据类型和设备
    dtype = torch.double  # 张量数据类型为浮点型
    device = torch.device("cpu")  # 本次计算在 CPU 上进行

    # 创建并打印两个随机张量 a 和 b
    a = torch.randn(2, 3, device=device, dtype=dtype)  # 创建一个 2x3 的随机张量
    b = torch.randn(2, 3, device=device, dtype=dtype)  # 创建另一个 2x3 的随机张量

    print("张量 a:")
    print(a)

    print("张量 b:")
    print(b)

    # 逐元素相乘并输出结果
    print("a 和 b 的逐元素乘积:")
    print(a * b)

    # 输出张量 a 所有元素的总和
    print("张量 a 所有元素的总和:")
    print(a.sum())

    # 输出张量 a 中第 2 行第 3 列的元素（注意索引从 0 开始）
    print("张量 a 第 2 行第 3 列的元素:")
    print(a[1, 2])

    # 输出张量 a 中的最大值
    print("张量 a 中的最大值:")
    print(a.max())

    print("===================")
    print(torch.randn(2, device=device, dtype=dtype))
    print(torch.randn(2, 3, device=device, dtype=dtype))
    print(torch.randn(2, 3, 4, device=device, dtype=dtype))
    print(torch.randn(2, 3, 2, 2, device=device, dtype=dtype))



    device = "cpu"
    seed = 42

    generator = torch.Generator(device=device).manual_seed(seed)

    # 使用生成器创建随机张量
    random_tensor1 = torch.randn(3, 3, generator=generator)
    random_tensor2 = torch.randn(3, 3, generator=generator)

    print("第一次生成的随机数:")
    print(random_tensor1)
    print("\n第二次生成的随机数:")
    print(random_tensor2)

    # 重置生成器状态（使用相同种子）
    generator = torch.Generator(device=device).manual_seed(seed)
    random_tensor3 = torch.randn(3, 3, generator=generator)

    print("\n重置后生成的随机数（应该与第一次相同）:")
    print(random_tensor3)
    print(f"\n两次生成是否相同: {torch.allclose(random_tensor1, random_tensor3)}")
    print(torch.randn(3, 3, generator=generator))