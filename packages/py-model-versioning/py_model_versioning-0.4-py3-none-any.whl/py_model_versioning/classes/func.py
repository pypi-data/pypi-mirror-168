import json
import os
import click
from os import walk

from .google_storage import googleStorage


class App:
    __conf = {
        "cloud_provider": "google",
        "bucket_name": ""
    }
    __setters = ["cloud_provider", "bucket_name"]

    @staticmethod
    def config(name):
        return App.__conf[name]

    @staticmethod
    def set(name, value):
        if name in App.__setters:
            App.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")


class func:
    config_dir = "config-model-ver"

    def __init__(self, init=True):
        if init:
            self.config_files_exists = func.check_config_files_exists(self)
            self.get_bucket_name()
            self.func_storage = googleStorage(self.bucket_name)

    def delete_entire_directory(self, directory_name):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.delete_entire_directory(directory_name)

    def delete_file(self, directory_name, file_name):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.delete_file(directory_name, file_name)

    def download_file_from_storage(self, source_blob_name, destination_file_name):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.download_file_from_storage(source_blob_name, destination_file_name)

    def download_ver_from_storage(self, project, ver):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.download_ver_from_storage(project, ver)

    def download_all_ver_from_storage(self, project):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.download_all_ver_from_storage(project)

    def list_dir(self, full_folder, get_version_files, display_console=True):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        self.func_storage.list_dir(full_folder, get_version_files, display_console)

    def add_directory(self, directory, project, ver):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        full_directory = os.getcwd() + '/' + directory
        filenames = next(walk(full_directory), (None, None, []))[2]
        for file in filenames:
            self.upload_file(project, ver, full_directory + '/' + file, directory)

    def upload_file(self, project, ver_name, file_name, dir_name):
        storage_file_name = os.path.basename(file_name)
        if os.path.exists(file_name):
            if dir_name == '':
                self.func_storage.upload_to_bucket(project + '/' + ver_name + '/' + storage_file_name, file_name)
            else:
                self.func_storage.upload_to_bucket(project + '/' + ver_name + '/' + dir_name + '/' + storage_file_name,
                                                   file_name)
        else:
            click.echo("file " + file_name + " does not exists")

    def add_file(self, project, ver_name, file_name):
        if self.bucket_name == "" or not self.config_files_exists:
            return
        if not file_name.endswith("/."):
            self.upload_file(project, ver_name, file_name, '')
        else:
            prefix_dir = file_name.replace("/.", "")
            if len(prefix_dir) > 0:
                prefix_dir = prefix_dir + "/"
            full_dir_name = os.getcwd() + '/' + prefix_dir
            filenames = next(walk(full_dir_name), (None, None, []))[2]
            for file in filenames:
                self.upload_file(project, ver_name, prefix_dir + file, '')

    def get_bucket_name(self):
        self.bucket_name = App.config("bucket_name")
        if self.bucket_name == "":
            click.echo("no bucket defined, please configure bucket name")

    def save_config_file(self, cloud_provider, bucket_name):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        config_json = {"Cloud_Provider": cloud_provider, "Bucket_Name": bucket_name}
        with open(self.config_dir + '/config.json', 'w') as config_file:
            json.dump(config_json, config_file)
            click.echo("configuration file saved successfully")

    def display_config_file(self):
        if not self.read_config_file(True):
            click.echo("no configuration file was found, please use configure flag to create one")

    def check_config_files_exists(self):
        if not self.read_config_file():
            return False
        else:
            cloud_provider = App.config("cloud_provider")
            if not self.check_that_storage_permission_exists(cloud_provider):
                return False
            else:
                return True

    def read_config_file(self, print_json=False):
        if os.path.exists(self.config_dir + '/config.json'):
            with open('config-model-ver/config.json', 'r') as config_file:
                json_config = json.load(config_file)
                if "Cloud_Provider" in json_config:
                    App.set("cloud_provider", json_config["Cloud_Provider"])
                if "Bucket_Name" in json_config:
                    App.set("bucket_name", json_config["Bucket_Name"])
                if print_json:
                    pretty_json = json.dumps(json_config, indent=4)
                    click.echo(pretty_json)
            return True;
        else:
            print("Configuration file not found in config-model-ver directory\n")
            return False

    def check_that_storage_permission_exists(self, cloud_provider):
        if cloud_provider == 'google':
            if not os.path.exists(self.config_dir + '/model-version-storage-key.json'):
                click.echo(
                    "model-version-storage-key.json file does not exists, please make sure it is in config-model-ver directory \n")
                return False
            else:
                return True
