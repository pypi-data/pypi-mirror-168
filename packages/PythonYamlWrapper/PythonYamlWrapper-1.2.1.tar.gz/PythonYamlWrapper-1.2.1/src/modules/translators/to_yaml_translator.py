from yaml import dump as upload_data # type: ignore
from yaml import Dumper
from yaml import YAMLError
from typing import Any, List, Union, cast
from ..translators.exceptions.rule_not_found_exception import RuleNotFoundException
from ..translators.exceptions.writing_yaml_exception import WritingYamlException
from ..yaml_structures.yaml_dictionary import YamlDictionary
from ..yaml_structures.yaml_list import YamlList
from ...utils.file.file_utils import FileUtil


class ToYamlTranslator:
    """Translator from the format of Yaml wrapper, to the format of yaml library.
    """
    def __init__(self , file_path: str) -> None:
        self._file_path: str = file_path
        
    def translate(self, content_to_translate: list) -> Union[dict, list, None]:
        """Translates the content of the YamlWrapper to the format of yaml library.

        Returns:
            Union[dict, list, None]: Content translated in the format accepted by yaml library.
            
        Note:
            Temporary the support for lists is only for list with integers and strings, and lists of lists of YamlDictionary.
        """
        if len(content_to_translate) == 0:
            FileUtil.delete_file(self._file_path)
            FileUtil.create_file_from_path(self._file_path)
            return None
        else:    
            content_to_write: Union[dict, list] = self._apply_rule_rec(content_to_translate, {})
            self._write_to_file(content_to_write)
            return content_to_write
    
    def _write_to_file(self, content_to_write: Union[dict, list]) -> None:
        try:
            with open(self._file_path, "w") as file:
                upload_data(content_to_write, file, Dumper)
        except YAMLError:
            raise WritingYamlException("Error writing the content to the yaml file.")
        
    def _apply_rule_rec(self, objects: Union[List[YamlDictionary], List[YamlList], Any], returned_value: Union[dict, list]) -> Union[dict, list]:
        if len(objects) == 0: 
            return returned_value
        else:
            first_object: Union[YamlDictionary, YamlList] = objects[0]
            value_to_return: dict = cast(dict,returned_value)
            
            if isinstance(first_object, YamlDictionary):
                if isinstance(first_object.value, str) or isinstance(first_object.value, int):
                    
                    value_to_return[first_object.key] = first_object.value 
                    
                elif isinstance(first_object.value, list) and isinstance(first_object.value[0], YamlDictionary):
                   
                    value_to_return[first_object.key] = self._apply_rule_rec(first_object.value, {})
                    
                else:
                    value_to_return[first_object.key] = self._apply_rule_rec([first_object.value], [])

                return  self._apply_rule_rec(objects[1:], value_to_return)
            else:
                if isinstance(first_object, YamlList):
                    if isinstance(first_object.values[0], int) or isinstance(first_object.values[0], str):
                        return first_object.values
                    else: 
                        partial_return: list = []
                        for item in  first_object.values:
                            partial_return.append(self._apply_rule_rec(item, {}))
                        return partial_return
        