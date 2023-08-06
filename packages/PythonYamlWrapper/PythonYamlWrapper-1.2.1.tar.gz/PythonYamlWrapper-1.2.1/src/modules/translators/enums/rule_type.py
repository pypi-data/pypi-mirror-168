from enum import Enum

class RuleType(Enum):
    INT_RULE = 'int_rule'
    STR_RULE = "str_rule"
    LIST_DICT_RULE = "list_dict_rule"
    LIST_RULE = "list_rule"
    
class ListRuleType(Enum):
    DICT_TYPE = "dict_type"
    OTHER_TYPE = "other_type"