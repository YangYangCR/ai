import pyarrow as pa
from pyarrow._flight import RecordBatchStream
import time

if __name__ == '__main__':
    schema = pa.schema([
        pa.field("state", pa.string()),
        pa.field("fail_reason", pa.string())
    ])
    start_state: dict[str, list] =  {}
    start_state["state"] = ["success"]
    start_state["fail_reason"] = [None]
    pipeline_server_result_table = pa.Table.from_pydict(start_state, schema=schema)
    RecordBatchStream(pipeline_server_result_table)
    print(time.time())

    if schema:
        print("=====")