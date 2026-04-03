from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from PIL import Image
from mineru_vl_utils import MinerUClient

# https://huggingface.co/opendatalab/MinerU2.5-2509-1.2B
if __name__ == "__main__":
    # for transformers>=4.56.0
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "opendatalab/MinerU2.5-2509-1.2B",
        dtype="auto",  # use `torch_dtype` instead of `dtype` for transformers<4.56.0
        device_map="auto"
    )

    processor = AutoProcessor.from_pretrained(
        "opendatalab/MinerU2.5-2509-1.2B",
        use_fast=True
    )

    client = MinerUClient(
        backend="transformers",
        model=model,
        processor=processor
    )

    print("===================================")
    image = Image.open("C:\\Users\\87435\\Downloads\\1.png")
    extracted_blocks = client.two_step_extract(image)
    print("===================================")
    print(extracted_blocks)
