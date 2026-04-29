import asyncio
import os
from mineru.cli.fast_api import StoredUpload, ParseRequestOptions, run_parse_job

if __name__ == "__main__":
    print("start run_parse_job ......")
    # [StoredUpload(original_name='demo1.pdf', stem='demo1',
    #               path='/tmp/mineru-api-client-q4qixb6m/output/8adfdb0d-49b4-4b3e-b7db-bfc5175ea69b/uploads/demo1.pdf')]
    store_upload = StoredUpload(
        original_name="demo1.pdf",
        stem="demo1",
        path="/mnt/c/Users/87435/Downloads/demo1.pdf",
    )
    # config = getattr(self.app.state, "config", {})
    request_options = ParseRequestOptions(
        files=[store_upload],
        lang_list=[],
        # backend="vlm-auto-engine",
        backend="pipeline",
        parse_method="auto",
        formula_enable=True,
        table_enable=True,
        server_url=None,
        return_md=True,
        return_middle_json=True,
        return_model_output=True,
        return_content_list=True,
        return_images=True,
        response_format_zip=True,
        return_original_file=True,
        start_page_id=0,
        end_page_id=99999
    )

    result = asyncio.run(run_parse_job(
        output_dir="/root/mineru_res",
        uploads=[store_upload],
        request_options=request_options,
        config={},
    ))
    print(f"result: {result}")