from typing import Union
from ..synchronisers.exceptions.not_synchronisable_object_exception import NotSynchronisableObjectException
from ..translators.to_yaml_translator import ToYamlTranslator
from ..yaml_structures.yaml_dictionary import YamlDictionary
from ..yaml_structures.yaml_list import YamlList


class Synchroniser:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._to_yaml_translator: ToYamlTranslator = ToYamlTranslator(file_path)
    
    def synchronise(self, content_to_synchronise: list) -> Union[dict, list, None]:
        self._check_object_content(content_to_synchronise)
        
        return self._to_yaml_translator.translate(content_to_synchronise)
    
    def _check_object_content(self, content_to_synchronise: list) -> None:
        for item in content_to_synchronise:
            if (not isinstance(item, YamlList)) and (not isinstance(item, YamlDictionary)):
                raise NotSynchronisableObjectException