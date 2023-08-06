from typing import Any, List, Union, Tuple
from ...translators.enums.object_type import ObjectType
from ...translators.enums.rule_type import ListRuleType, RuleType
from ...translators.exceptions.rule_not_found_exception import RuleNotFoundException
from ...yaml_structures.yaml_dictionary import YamlDictionary
from ...yaml_structures.yaml_list import YamlList


class RuleFromValueUtil:
  
    @staticmethod
    def define_rule_from_value(value: Any) -> RuleType:
        if isinstance(value, int):
            return RuleType.INT_RULE
        elif isinstance(value, str):
            return RuleType.STR_RULE
        elif isinstance(value, dict):
            return RuleType.LIST_DICT_RULE
        elif isinstance(value, list):
            return RuleType.LIST_RULE
        else:
            raise RuleNotFoundException("Not able to find a valid rule.")
        
    @staticmethod
    def define_list_rule_type_from_value(value: List[Union[dict, Any]]) -> ListRuleType:
            first_element: Union[dict, Any ] = value[0]
            if isinstance(first_element, dict):
                return ListRuleType.DICT_TYPE
            
            return ListRuleType.OTHER_TYPE
        

class RuleFromObjectUtil:
    
    @staticmethod
    def define_rule_from_object(object: Union[YamlDictionary, YamlList]) -> ObjectType:
        if isinstance(object, YamlDictionary):
            return ObjectType.DICT
        elif isinstance(object, YamlList):
            return ObjectType.LIST
        else:
            raise RuleNotFoundException("Not able to find a valid rule.")

