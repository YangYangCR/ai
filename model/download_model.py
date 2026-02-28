from huggingface_hub import snapshot_download
import os

if __name__ == '__main__':
    # snapshot_download(
    #     repo_id="facebook/opt-125m",
    #     local_dir="opt-125m",
    #     local_dir_use_symlinks=False
    # )

    # snapshot_download(
    #     repo_id="intfloat/e5-small",
    #     local_dir="e5-small",
    #     local_dir_use_symlinks=False
    # )
    # snapshot_download(
    #     repo_id="BAAI/bge-reranker-v2-m3",
    #     local_dir="bge-reranker-v2-m3",
    #     local_dir_use_symlinks=False
    # )

    # os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    # os.environ['HF_ENDPOINT'] = 'https: // mirrors.tuna.tsinghua.edu.cn'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['ALL_PROXY'] = 'http://127.0.0.1:7890'


    snapshot_download(
        repo_id="Qwen/Qwen-Image-2512",
        local_dir="qwen-image",
        local_dir_use_symlinks=False
    )

