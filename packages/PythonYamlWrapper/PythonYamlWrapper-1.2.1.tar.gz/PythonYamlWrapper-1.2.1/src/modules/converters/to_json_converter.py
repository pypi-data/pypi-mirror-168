from json import dumps as convert_to_json
from typing import Any, List
from typing import Union
from typing import cast
from ..yaml_structures.yaml_dictionary import YamlDictionary
from ..yaml_structures.yaml_list import YamlList

class ToJsonConverter:
    """ **ToJsonConverter** converts a list of YamlDictionary or YamlList objects to a JSON string.
    """
    @staticmethod
    def convert(data_to_convert: list) -> str:
        """
        Converts a list of YamlDictionary or YamlList to a JSON string.

        ***Args:***
            - `data_to_convert (list)`: List to convert.

        ***Returns:***
            - `str`: JSON string.
        """
        content_to_convert: Union[dict, list] = ToJsonConverter._convert_recursion(data_to_convert, {})
        return convert_to_json(content_to_convert)
    
    
    @staticmethod
    def _convert_recursion(objects: Union[List[YamlDictionary], List[YamlList], Any], returned_value: Union[dict, list]) -> Union[dict, list]:
        if len(objects) == 0: 
            return returned_value
        else:
            first_object: Union[YamlDictionary, YamlList] = objects[0]
            value_to_return: dict = cast(dict,returned_value)
            
            if isinstance(first_object, YamlDictionary):
                if isinstance(first_object.value, str) or isinstance(first_object.value, int):
                    
                    value_to_return[first_object.key] = first_object.value 
                    
                elif isinstance(first_object.value, list) and isinstance(first_object.value[0], YamlDictionary):
                   
                    value_to_return[first_object.key] = ToJsonConverter._convert_recursion(first_object.value, {})
                    
                else:
                    value_to_return[first_object.key] = ToJsonConverter._convert_recursion([first_object.value], [])

                return  ToJsonConverter._convert_recursion(objects[1:], value_to_return)
            else:
                if isinstance(first_object, YamlList):
                    if isinstance(first_object.values[0], int) or isinstance(first_object.values[0], str):
                        return first_object.values
                    else: 
                        partial_return: list = []
                        for item in  first_object.values:
                            partial_return.append(ToJsonConverter._convert_recursion(item, {}))
                        return partial_return