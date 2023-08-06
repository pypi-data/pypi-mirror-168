import hashlib
import os
from tqdm import tqdm
from google.cloud import storage
import click


class googleStorage:
    service_account_file = "config-model-ver/model-version-storage-key.json"
    download_dir = "download-model-ver"

    def __init__(self, bucket_name):
        self.storage_client = storage.Client.from_service_account_json(self.service_account_file)
        self.bucket = self.storage_client.get_bucket(bucket_name)
        self.bucket_name = bucket_name

    def delete_entire_directory(self, directory_name):
        blobs = self.bucket.list_blobs(prefix=directory_name)
        for blob in blobs:
            blob.delete()
        click.echo("ver deleted successfully")

    def delete_file(self, directory_name, file_name):
        hash_file = (file_name.split('.'))[0] + '.hash'
        blob = self.bucket.blob(directory_name + file_name)
        blob.delete()
        blob = self.bucket.blob(directory_name + hash_file)
        blob.delete()
        click.echo("file deleted successfully")

    def download_file_from_storage(self, source_blob_name, destination_file_name):
        destination_full_file_name = os.getcwd() + '/' + self.download_dir + '/' + destination_file_name
        if self.file_exists(source_blob_name):
            dirname = os.path.dirname(destination_full_file_name)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            blob = self.bucket.get_blob(source_blob_name)
            storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
            blob._chunk_size = 5 * 1024 * 1024
            with open(destination_full_file_name, "wb") as in_file:
                total_bytes = blob.size
                with tqdm.wrapattr(in_file, "write", total=total_bytes, miniters=1,
                                   desc="download to %s" % destination_full_file_name, colour="green") as file_obj:
                    self.storage_client.download_blob_to_file(blob, file_obj)
        else:
            click.echo(
                "object {} from bucket {} not found".format(
                    source_blob_name, self.bucket_name
                )
            )

    def download_ver_from_storage(self, project, ver):
        blob_list = self.list_dir(project + "/" + ver, True, False)
        for blob in blob_list:
            blobItemsArray = blob.split('/')
            i = 0
            destFileName = ""
            for blobItem in blobItemsArray:
                if (i > 1):
                    destFileName = destFileName + blobItem + '/'
                i = i + 1
            destFileName = destFileName[:-1]
            self.download_file_from_storage(blob, ver + '/' + destFileName)

    def download_all_ver_from_storage(self, project):
        ver_list = self.list_dir(project + "/", False, False)
        for ver in ver_list:
            ver = ver[:-1]
            self.download_ver_from_storage(project, ver)

    def list_dir(self, full_folder, get_version_files, display_console=True):
        if get_version_files:
            blobs = self.storage_client.list_blobs(self.bucket_name, prefix=full_folder)
            blob_list = []
            for blob in blobs:
                if not blob.name.endswith('.hash'):
                    blob_list.append(blob.name)
                    blob_no_prefix = blob.name.replace(full_folder, "")
                    if display_console:
                        click.echo(blob_no_prefix)
            return blob_list
        else:
            blobs = self.storage_client.list_blobs(
                bucket_or_name=self.bucket_name,
                prefix=full_folder,
                delimiter="/",
                max_results=1
            )
            next(blobs, ...)
            blob_list = []
            for folder in list(blobs.prefixes):
                dir_no_suffix = folder.replace(full_folder, "")
                blob_list.append(dir_no_suffix)
                if display_console:
                    click.echo(dir_no_suffix)
            return blob_list

    def upload_to_bucket(self, full_file_path, path_to_file, bucket_hash_key=None):
        if not self.file_exists(full_file_path):
            self.upload_file_and_hash_to_bucket(full_file_path, path_to_file)
        else:
            bucket_hash_file = self.rename_file_to_hash_suffix(full_file_path)
            if self.file_exists(bucket_hash_file):
                bucket_hash_key = self.get_file(bucket_hash_file).decode('utf-8')
            calculated_hash = self.calculate_hash(path_to_file)
            if calculated_hash != bucket_hash_key:
                overwrite_question = input(
                    "a different file with the same name already exists do you want to overwrite it (yes, no)\n")
                if overwrite_question.lower() == ("yes"):
                    self.upload_file_and_hash_to_bucket(full_file_path, path_to_file)

    def upload_file_and_hash_to_bucket(self, full_file_path, path_to_file, content_type=None):
        blob = self.bucket.blob(full_file_path)
        storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
        blob._chunk_size = 5 * 1024 * 1024
        with open(path_to_file, "rb") as in_file:
            total_bytes = os.fstat(in_file.fileno()).st_size
            with tqdm.wrapattr(in_file, "read", total=total_bytes, miniters=1,
                               desc="upload to %s" % full_file_path, colour="green") as file_obj:
                blob.upload_from_file(
                    file_obj,
                    content_type=content_type,
                    size=total_bytes,
                )
                self.create_hash_and_upload(full_file_path, path_to_file)

    def create_hash_and_upload(self, full_file_path, path_to_file):
        hash_file = self.rename_file_to_hash_suffix(full_file_path)
        calculated_hash = self.calculate_hash(path_to_file)
        blob = self.bucket.blob(hash_file)
        blob.upload_from_string(calculated_hash)

    def rename_file_to_hash_suffix(self, file_name):
        return os.path.splitext(file_name)[0] + '.hash'

    def get_file(self, full_file_path):
        blob = self.bucket.blob(full_file_path)
        data = blob.download_as_string()
        return data;

    # def get_files(self, full_folder):
    #     blobs = self.bucket.list_blobs(prefix=full_folder)
    #     for blob in blobs:
    #         print(blob.name)

    def calculate_hash(self, file_path):
        BUF_SIZE = 65536
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    def file_exists(self, full_file_path):
        return storage.Blob(bucket=self.bucket, name=full_file_path).exists(self.storage_client)
