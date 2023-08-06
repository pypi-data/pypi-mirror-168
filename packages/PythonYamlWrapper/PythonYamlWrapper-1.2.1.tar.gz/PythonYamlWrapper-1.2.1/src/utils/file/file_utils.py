import os
import os.path as path
import yaml # type: ignore
from typing import Any, Union

from .enums.file_type import FileType
from .exceptions.not_supported_file_extension import NotSupportedFileExtensionException
from .exceptions.not_valid_file_content import NotValidFileContent



class FileUtil:
    @staticmethod
    def create_file(file_path: str, file_name: str, file_type: FileType, file_content: Union[dict, str]) -> str:
        if file_type == FileType.YAML:
            if not isinstance(file_content, dict) and (not isinstance(file_content, list)):
                raise NotValidFileContent("The content for the file is not in the right format.")
            with open(file_path + file_name + file_type.value, "w") as file:
                documents = yaml.dump(file_content, file)
                file.close()
    
        else:
            if not isinstance(file_content, str):
                raise NotValidFileContent("The content for the file is not in the right format.")
            with open(file_path + file_name + file_type.value, "w") as file:
                file.write(file_content)
                file.close()
                
        return file_path + file_name + file_type.value 
    
    @staticmethod
    def create_file_from_path(file_path: str):
        open(file_path, 'w').close()
        return file_path 
    
    @staticmethod
    def create_empty_file(file_path: str, file_name: str, file_type: FileType,) -> str:
        if (file_type != FileType.YAML) and (file_type != FileType.TXT):
            raise NotSupportedFileExtensionException("The file type is not valid.")
        open(file_path + file_name + file_type.value, 'w').close()
             
        return file_path + file_name + file_type.value 
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        if path.isfile(file_path):
            os.remove(file_path)
            return True
        raise FileNotFoundError("File " + file_path + " not exist.")