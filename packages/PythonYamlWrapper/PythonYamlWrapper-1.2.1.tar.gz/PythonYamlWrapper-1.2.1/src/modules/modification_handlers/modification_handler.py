from copy import copy
from typing import Any, List, Union, cast

from ..modification_handlers.exceptions.key_already_used_exception import KeyAlreadyUsedException
from ..initialisers.initialiser import Initialiser
from ..modification_handlers.exceptions.filter_not_found_exception import FilterNotFoundException
from ..modification_handlers.exceptions.not_safe_load_exception import NotSafeLoadException
from ..modification_handlers.exceptions.not_valid_filter_exception import NotValidFilterException
from ..modification_handlers.exceptions.not_valid_remove_exception import NotValidRemoveException
from ..modification_handlers.exceptions.not_valid_update_exception import NotValidUpdateException
from ..modification_handlers.utils.searchers.object_by_path_reference_searcer import ObjectByPathReference
from ..modification_handlers.utils.searchers.value_by_path_boolean_searcher import ValueByPathBooleanSearcher
from ..modification_handlers.utils.searchers.value_by_path_reference_searcher import ValueByPathReferenceSearcher

from ..synchronisers.synchroniser import Synchroniser
from ..validators.yaml_object_path_format_validator import YamlObjectPathFormatValidator
from ..validators.yaml_object_path_remove_validator import YamlObjectPathRemoveValidator
from ..yaml_structures.yaml_dictionary import YamlDictionary
from ..yaml_structures.yaml_list import YamlList

class ModificationHandler:
    """`ModificationHandler` class handles all the possible modification that are allowed using the `YamlDictionary` and `YamlList` classes.
        IMPORTANT NOTES:
        - When an instance of this class is created the content of file is not automatically loaded. This is done only when the `load` method is called.
        - It's IMPORTANT to remember that this class has an internal state, so all the modifications automaticaly update the internal state of the object,
        and the file content.
        
        
    """
    def __init__(self, file_path: str, safe_load: bool = True, safe_initialization: bool = True) -> None:
        self._file_path = file_path
        self._object: list = []
        self._safe_load: bool = safe_load
        self._safe_initialization: bool = safe_initialization
        self._loaded: bool = False
        self._synchroniser: Synchroniser = Synchroniser(file_path)
        self._initialiser: Initialiser = Initialiser(file_path, self._safe_initialization)
        self._path_format_validator: YamlObjectPathFormatValidator = YamlObjectPathFormatValidator()
        self._path_remove_validator: YamlObjectPathRemoveValidator = YamlObjectPathRemoveValidator()
        
    
    def load(self) -> list:
        """Reads the file and creates the object with the readed information, then returns a copy of the created object.

        Returns:
            list: Copy of created object with the content of file.
        """
        self._loaded = True
        self._object = self._initialiser.initialise()
        return self._object.copy()

    def get(self) -> list:
        """Returns a copy of the contents of the file.

        Returns:
            list: Copy of object with content of file.
        """
        self._check_safe_load()
        
        return self._object.copy() 
    
    def find_by_filter(self, filter: str) -> Union[YamlDictionary, YamlList]:
        """Search an item using a filter. If the item is found returns it, otherwise raises an exception.

        Args:
            filter (str): Filter used to search the item.
        
        Raise:
            FilterNotFoundException: If the item is not found.

        Returns:
            Union[YamlDictionary, YamlList]: Item found.
        """
        self._check_safe_load()
        filter_splitted: list = filter.split(".")
        try:
            object_to_modify: Union[YamlDictionary, YamlList, None] = ValueByPathReferenceSearcher.search(filter_splitted, self._object)
            if object_to_modify == {}:
                raise FilterNotFoundException("The filter not produced any result.")
        except (FilterNotFoundException, NotValidRemoveException) as error:
            raise error
       
       
        searched_object: Union[YamlDictionary, YamlList, None] = ValueByPathReferenceSearcher.search(filter_splitted, self._object)
        if searched_object is None:
            raise FilterNotFoundException("The filter not produced any result.")
        
        return copy(searched_object)
        
    
    
    def check(self, filter: str, value: Union[str, int]) -> bool:
        """Checks if a value exist, using a filter to determine the position of the value.

        Args:
            filter (str): Filter used to determine the position of the value.
            value (Union[str, int]): Value to be checked.

        Returns:
            bool: True if the value exist, False otherwise.
        """
        self._check_safe_load()
        if not self._path_format_validator.validate(filter):
            raise NotValidFilterException("The filter is not valid.")
        
        search_in_object: list = self._object.copy()
        filter_splitted: list = filter.split(".")
        return ValueByPathBooleanSearcher.search(filter_splitted, value, search_in_object)
        
    def add(self, key: str, data_to_add: Union[int, str, YamlDictionary, YamlList, List[YamlDictionary], List[List[YamlDictionary]]]) -> list:
        """Adds and item under the specified key.

        Args:
            key (str): Key to add.
            data_to_add (Union[int, str, YamlDictionary, YamlList, List[YamlDictionary], List[List[YamlDictionary]]]): Object to add.

        Raises:
            KeyAlreadyUsedException: If the key already exists.

        Returns:
            list: Copy of the object with the item added.
            
        Note: This method doesn't check the data_to_add parameter, it this is not in right format, the file .yaml can be corrupted.
        """
        self._check_safe_load()
        
        if self._check_if_key_already_exists(key):
            raise KeyAlreadyUsedException("Key "+ key +" already exists.")
        
        self._object.append(YamlDictionary(key, data_to_add))
        
        self._synchroniser.synchronise(self._object.copy())
        
        return self._object.copy()
    
    def update(self, 
               filter: str, 
               update_data: Union[int, str, YamlDictionary, YamlList, List[YamlDictionary], List[List[YamlDictionary]],  List[YamlList]]) -> Any:
        """Updates a value in the file, using a filter to determine the position of the value.

        Args:
            filter (str): Filter used to determine the position of the value.
            update_data (Union[int, str, YamlDictionary, YamlList, List[YamlDictionary], List[List[YamlDictionary]],  List[YamlList]]): Data to be updated.

        Raises:
            FilterNotFoundException: If the filter not proce any result.
            NotValidFilterException: If the filter format is not valid.
        Returns:
            list: Copy of object with updated value.
        """
        self._check_safe_load()
        if not self._path_format_validator.validate(filter):
            raise NotValidFilterException("The filter is not valid. Probably its structure is not correct.")
        
        filter_splitted: list = filter.split(".")
        try:
            object_to_modify: Union[YamlDictionary, YamlList, None] = ValueByPathReferenceSearcher.search(filter_splitted, self._object)
            if object_to_modify is None:
                raise FilterNotFoundException("The filter not produced any result.")
        except (FilterNotFoundException, NotValidRemoveException) as error:
            raise error
        
        self._check_if_update_is_valid(object_to_modify, update_data)

        if isinstance(object_to_modify, YamlDictionary):
            cast(YamlDictionary, object_to_modify).value = cast(Union[int, str, YamlDictionary, YamlList, List[YamlDictionary]], update_data)
        else: 
            cast(YamlList, object_to_modify).values = cast(Union[List[YamlDictionary], List[Any]],update_data)
        
        self._synchroniser.synchronise(self._object.copy())
        
        return self._object.copy()
    
    def remove(self, filter: str) -> list:
        """ Removes a value from the file, using a filter to determine the position of the value.

        Args:
            filter (str): Filter used to determine the position of the value.

        Returns:
            list: Copy of object with the item removed.
        """
        self._check_safe_load()
        
        if not self._path_format_validator.validate(filter):
            raise NotValidFilterException("The filter is not valid. Probably its structure is not correct.")
        
        
        if not self._path_remove_validator.validate(filter):
            raise NotValidRemoveException("The filter is not valid, for removing.")
        
        filter_splitted: list = filter.split(".")
        
        object_to_remove: Union[YamlDictionary, YamlList, None] = ObjectByPathReference.search(filter_splitted, self._object)
        if object_to_remove is None:
            raise FilterNotFoundException("The filter not produced any result.")
        
        
        self._synchroniser.synchronise(self._object.copy())
        
        return self._object.copy()
    
    def clean_file(self, return_file_content: bool = False) -> Union[list, None]:
        """Cleans the file.

        Args:
            return_file_content (bool, optional): If True the file content is returned. Defaults to False.

        Returns:
            Union[list, None]: If the parameter return_file_content is True, returns the content of the file. Otherwise, returns None.
        """
        copy_of_object: list = self._object.copy()
        self._object = []
        self._synchroniser.synchronise(self._object.copy())
        
        self._synchroniser.synchronise(self._object.copy())
        
        if  return_file_content:
            return copy_of_object

        return None
    
    def _check_safe_load(self) -> None:
        if not self._loaded and self._safe_load:
            raise NotSafeLoadException("The file is not loaded, and the safe load is enabled.")
        
    def _check_if_update_is_valid(self, 
                                value_to_update: Union[YamlDictionary, YamlList], 
                                update: Union[int, 
                                              str, 
                                              YamlDictionary, 
                                              YamlList, 
                                              List[YamlDictionary], 
                                              List[YamlList], 
                                              List[Any]]) -> None:
        
        if isinstance(value_to_update, YamlDictionary):
            if not (isinstance(update, int) or
                    isinstance(update, str) or
                    isinstance(update, YamlDictionary) or
                    isinstance(update, YamlList) or
                    all(isinstance(item, YamlDictionary) for item in update)):
                raise NotValidUpdateException("The update is not valid.")
        else:
            if not (isinstance(update, List)):
                raise NotValidUpdateException("The update is not valid.")
            
    def _check_if_key_already_exists(self, key: str) -> bool:
        key_already_exists: bool = False
        for item in self._object:
            if isinstance(item, YamlDictionary) and item.key == key:
                key_already_exists = True
                
        return key_already_exists