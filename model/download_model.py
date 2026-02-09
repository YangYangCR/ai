from huggingface_hub import snapshot_download

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
    snapshot_download(
        repo_id="BAAI/bge-reranker-v2-m3",
        local_dir="bge-reranker-v2-m3",
        local_dir_use_symlinks=False
    )
