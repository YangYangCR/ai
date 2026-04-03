from vllm import LLM
from PIL import Image
from mineru_vl_utils import MinerUClient
from mineru_vl_utils import MinerULogitsProcessor  # if vllm>=0.10.1

if __name__ == "__main__":
    llm = LLM(
        model="opendatalab/MinerU2.5-2509-1.2B",
        logits_processors=[MinerULogitsProcessor]  # if vllm>=0.10.1
    )

    client = MinerUClient(
        backend="vllm-engine",
        vllm_llm=llm
    )

    image = Image.open("/path/to/the/test/image.png")
    extracted_blocks = client.two_step_extract(image)
    print(extracted_blocks)
