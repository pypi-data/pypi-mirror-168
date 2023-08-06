from io import TextIOWrapper
from yaml import load as download_data # type: ignore
from yaml import Loader # type: ignore
from typing import List, Any, Union
from typing import cast

from ..translators.enums.rule_type import ListRuleType, RuleType
from ..translators.utils.rule_util import RuleFromValueUtil
from ..yaml_structures.yaml_dictionary import YamlDictionary
from ..yaml_structures.yaml_list import YamlList


class FromYamlTraslator:
    """ Translator from the format of yaml library, to the format accepeted from the YamlWrapper
    """
    def __init__(self , file_path: str) -> None:
        self._file_path: str = file_path
        
    def translate(self)-> list:
        """Returns a dict in the right format for YamlWrapper, with the content of yaml file

        Returns:
            list: Yaml file content in right format
        """
        data_from_file: dict =  self._read_from_file()
        if data_from_file is None:
            return []
        elif type(data_from_file) is list:
            data_to_return: list = []
            for item in data_from_file:
                if not isinstance(item, int) and (not isinstance(item, str)):
                    data_to_return.append(self._apply_rule_rec(list(item.keys()), item, []))
                else:
                    data_to_return.append(item)
            
            return [YamlList(data_to_return)]

        else:
            keys: list = []
            for key in data_from_file.keys():
                keys.append(key)
            rules_applied: list = self._apply_rule_rec(keys, data_from_file, [])
            
            return rules_applied
    
    def _read_from_file(self) -> dict:
        try:
            with open(self._file_path, "r") as file:
                data_from_file: dict = download_data(file, Loader)
        except OSError as error:
            raise error
        
        return data_from_file
    
    def _convert_dict_keys_to_dict(self, keys: Any) -> list:
        dict_keys_accumulator: list = []
        for key in keys:
            dict_keys_accumulator.append(key)
        
        return dict_keys_accumulator
            
    def _apply_rule_rec(self, keys: List[str], data: dict, returned_value: list ) -> list:
        if len(keys) == 0:
             return returned_value
        else:
            
            first_key: str = keys[0]
            
            rule_to_apply: RuleType = RuleFromValueUtil.define_rule_from_value(data[first_key])
            
            if rule_to_apply == RuleType.INT_RULE or rule_to_apply == RuleType.STR_RULE:
                returned_value.append(YamlDictionary(first_key, data[first_key]))
                
            elif rule_to_apply == RuleType.LIST_DICT_RULE:
                
                sub_keys: list = self._convert_dict_keys_to_dict(data[first_key].keys())
                returned_value.append(YamlDictionary(first_key, self._apply_rule_rec(sub_keys, data[first_key], [])))
            
            elif rule_to_apply == RuleType.LIST_RULE:
                data_copy = data[first_key]
                list_type: ListRuleType = RuleFromValueUtil.define_list_rule_type_from_value(data_copy)
        
                if list_type == ListRuleType.DICT_TYPE:
                    accumulator: List[Any] = []
                    
                    for item in  range(0, len(data[first_key])):
                        sub_keys_list : list = self._convert_dict_keys_to_dict(data[first_key][item].keys())
                       
                        accumulator.append(self._apply_rule_rec(sub_keys_list, data[first_key][item], []))
                    
                    returned_value.append(YamlDictionary(first_key, YamlList(accumulator)))

                else:
                       
                    returned_value.append(YamlDictionary(first_key, YamlList(data[first_key])))
     
                 
        return self._apply_rule_rec(keys[1:], data, returned_value) 
    