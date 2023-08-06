from typing import List, Any
from typing import Union
from typing import cast
from ....modification_handlers.exceptions.not_valid_filter_exception import NotValidFilterException
from ....yaml_structures.exceptions.list_not_respect_integrity import ListNotRespectIntegriry

from ....yaml_structures.yaml_dictionary import YamlDictionary
from ....yaml_structures.yaml_list import YamlList

class ValueByPathReferenceSearcher:
    @staticmethod
    def search(filters: List[str], search_in_objects: list) -> Union[YamlDictionary, YamlList, None]:
        return ValueByPathReferenceSearcher._search_recursion(filters, search_in_objects, cast(Union[YamlDictionary, YamlList], {}))
    
    @staticmethod
    def _search_recursion(filters: List[str], search_in_objects: list, returned_value: Union[YamlDictionary, YamlList, None]) -> Union[YamlDictionary, YamlList, None]:
        if len(filters) == 0:
            return returned_value
        else:
            
            for item in search_in_objects:
                first_filter: str = filters[0]

                if first_filter != "[]":
                    if isinstance(item, YamlDictionary) and cast(YamlDictionary, item).key == first_filter:
                        return  ValueByPathReferenceSearcher._search_recursion(filters[1:],
                                                                            [cast(YamlDictionary, item).value], 
                                                                            item)
                    elif isinstance(item, list):
                        if not ValueByPathReferenceSearcher._check_list_integrity(item, YamlDictionary):
                            raise ListNotRespectIntegriry("Items in list not respect integrity: they not have the same type.")
                        
                        for sub_item in item:
                            value_to_return = ValueByPathReferenceSearcher._search_recursion(filters, item, None)
                            if value_to_return is not None:
                                return ValueByPathReferenceSearcher._search_recursion([], [], value_to_return)
                else:
                    if first_filter == "[]":
                        if not isinstance(item, YamlList):
                            raise NotValidFilterException("The filter is not applicable to the structure of the object.")
                    if ValueByPathReferenceSearcher._check_list_integrity(item.values[0], YamlDictionary):
                        returned_value  = None
                        
                        for sub_item in item.values:
                            result = ValueByPathReferenceSearcher._search_recursion(filters[1:], sub_item, item)
                            
                            if result is not None:
                                returned_value = result
                        return ValueByPathReferenceSearcher._search_recursion([],[], returned_value)
                    else: 
                        return ValueByPathReferenceSearcher._search_recursion([], [], item.values)
            return ValueByPathReferenceSearcher._search_recursion([], [], cast(Union[YamlDictionary, YamlList], {}))   
            
    
    @staticmethod
    def _check_list_integrity(list_to_check: List[Any], type_of_list: type) -> bool:
        for item in list_to_check:
            if not isinstance(item, type_of_list):
                return False
        return True
                