import os
import zipfile
from pathlib import Path

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.fs_path = 'vfs'
        self.extract_zip(zip_path)
        self.current_path = self.fs_path

    def extract_zip(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(path=self.fs_path)

    def list_files(self):
        try:
            return [f for f in os.listdir(self.current_path) if f != '.DS_Store']
        except FileNotFoundError:
            print(f"Error: {self.current_path} does not exist.")
            return []

    def change_directory(self, path):
        if path == '/':
            self.current_path = self.fs_path
        else:
            new_path = os.path.normpath(os.path.join(self.current_path, path))
            if os.path.commonpath([os.path.abspath(self.fs_path), os.path.abspath(new_path)]) == os.path.abspath(self.fs_path):
                if os.path.isdir(new_path):
                    self.current_path = new_path
                else:
                    print(f"cd: no such file or directory: {path}")
            else:
                print("cd: Access denied. You cannot leave the VFS.")

    def read_file(self, file_path):
        file_abs_path = os.path.join(self.current_path, file_path)
        if os.path.isfile(file_abs_path):
            with open(file_abs_path, 'r') as f:
                return f.read()
        else:
            print(f"read_file: {file_path} does not exist or is not a file.")

    def remove_file(self, file_name):
        file_path = os.path.join(self.current_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"rm: {file_name} deleted")
        else:
            print(f"rm: cannot remove '{file_name}': No such file")
