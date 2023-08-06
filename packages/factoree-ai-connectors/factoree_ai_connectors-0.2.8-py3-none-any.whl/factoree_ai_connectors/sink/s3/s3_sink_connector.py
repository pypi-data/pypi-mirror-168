import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import TypeVar
from factoree_ai_connectors.sink.s3_client import S3Client
from factoree_ai_connectors.files.file_types import S3File

T = TypeVar('T', bound=S3File)


def grid_to_csv(data: list[list]):
    comma_separated_rows = []
    for row_idx in range(len(data)):
        new_row = []
        for value in data[row_idx]:
            new_row.append(str(value))
        comma_separated_rows.append(",".join(new_row))
    return "\n".join(comma_separated_rows)


class S3SinkConnector:
    def __init__(
            self,
            s3_client: S3Client
    ):
        super().__init__()
        self.s3_client = s3_client

    def write_csv_file(self, bucket_name: str, filename: str, data: list[list]) -> bool:
        return self.s3_client.put(bucket_name, filename, grid_to_csv(data))

    def write_json_file(self, bucket_name: str, filename: str, json_data: dict) -> bool:
        print(f'{datetime.now().strftime("%H:%M:%S")} - write_json_file({filename})')
        return self.s3_client.put(bucket_name, filename, json.dumps(json_data))

    def write_json_files(self, bucket_name: str, filenames: list[str],
                         json_data: list[dict]) -> int:
        max_workers = max(30, len(filenames))
        written_json_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(write_json_file, self, bucket_name, filenames[i], json_data[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                written_json_files += 1 if future.result() else 0

        return written_json_files

    def delete(self, bucket_name: str, filename: str) -> bool:
        return self.s3_client.delete(bucket_name, filename)

    def delete_files(self, bucket_name: str, filenames: list[str]) -> int:
        max_workers = max(30, len(filenames))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, bucket_name, filenames[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def delete_S3Files(self, files: list[T]) -> int:
        max_workers = max(30, len(files))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, files[i].bucket_name, files[i].filename) for i in
                       range(len(files))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def copy(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        copy_source = {'Bucket': src_bucket, 'Key': src_filename}
        return self.s3_client.copy(copy_source, dst_bucket, dst_filename)

    def exist(self, bucket_name: str, filename: str) -> bool:
        return self.s3_client.exist(bucket_name, filename)

    def move(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        return self.copy(src_bucket, src_filename, dst_bucket, dst_filename) and self.delete(src_bucket, src_filename)


def write_json_file(connector: S3SinkConnector, bucket_name: str, filename: str, json_data: dict) -> bool:
    return connector.write_json_file(bucket_name, filename, json_data)


def delete(connector: S3SinkConnector, bucket_name: str, filename: str) -> bool:
    return connector.delete(bucket_name, filename)
