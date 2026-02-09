
import vllm
from vllm import LLM, SamplingParams
import torch

if __name__ == "__main__":
    print(vllm.__version__)
    print(torch.cuda.is_available())
    print(torch.version.cuda)

    # 1. 模型路径（本地）
    MODEL_PATH = "C:\\Users\\87435\\PycharmProjects\\ai\\ai\\linear_model.pth"

    # 2. 创建 LLM 实例
    llm = LLM(
        model=MODEL_PATH,
        tokenizer=MODEL_PATH,  # 一般和模型在同一目录
        dtype="float16",  # 推荐：float16 / bfloat16
        gpu_memory_utilization=0.9,  # 显存利用率
        max_model_len=4096,  # 一定要限制
    )

    # 3. 采样参数
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=256,
    )

    # 4. 输入 prompt
    prompts = [
        "请用一句话解释什么是 vLLM。",
        "Explain what KV cache is in LLM inference."
    ]

    # 5. 执行推理
    outputs = llm.generate(prompts, sampling_params)

    # 6. 打印结果
    for i, output in enumerate(outputs):
        print(f"\n===== Prompt {i} =====")
        print(output.prompt)
        print("----- Output -----")
        print(output.outputs[0].text)