from typing import  List, Union

from ..modules.modification_handlers.exceptions.filter_not_found_exception import FilterNotFoundException
from ..modules.modification_handlers.modification_handler import ModificationHandler
from ..modules.yaml_structures.yaml_dictionary import YamlDictionary
from ..modules.yaml_structures.yaml_list import YamlList


class YamlWrapper:
    """**YamlWrapper** creates an abstraction over the `.yaml` file.    
    
    **Main data types:**
    - `YamlDictionary`: Dictionary with the format accepted by the Yaml Wrap library.
    - `YamlList`: List with the format accepted by the Yaml Wrap library.
    
    **IMPORTANT NOTES:**
    The main purpose of this class is to create an abstraction layer over the PyYaml library. It's important to remember that the format of file contenten used in PyYaml library is
    not compatible.
    *Example:*
    For example if in PyYaml library a dictionary is rappresented ad `{"key", "value"}`, in YamlWrapper is rappresented by YamlDictionary("key", "value").
    
    """
    def __init__(self, file_path: str, safe_initialization: bool = True) -> None:
        """Constructor of the class.

        ***Args:***
        - `file_path (str)`: File path in the format `path/format/accepted_by_the_library.yaml`.
        - `safe_initialization (bool, optional)`: If `true` and the file at the specified path not exist, this will be created, otherwise it will be
        raised the exception `FileNotDFoundError`. Defaults to True.
        """
        self._file_name: str = file_path
        self._safe_initialization: bool = safe_initialization
        self._modification_handler: ModificationHandler = ModificationHandler(file_path, safe_initialization)
        
        self._modification_handler.load()
    
    def get_file_name(self) -> str:
        """Returns the name of the file.

        ***Returns:*** File name.
        """
        return self._file_name
    
    def get_file_content(self) -> list:
        """Returns the content of the file in a list that contains it in the format accepted by the Yaml Wrap library.

        ***Returns:***
            `list`: Content of the file.
        """
        return self._modification_handler.get()
    
    def find_by_filter(self, filter: str) -> Union[YamlDictionary, YamlList, None]:
        """Search an item using a filter. If the item is found returns it.
        ***Args:***
        - filter (str)`: Filter used to determine the position of the value.

        ***Returns:***
        - `Union[YamlDictionary, YamlList, None]`: : Item found, or None if is not found.
        """
        value_to_return: Union[YamlDictionary, YamlList, None]
        try:
            value_to_return = self._modification_handler.find_by_filter(filter)
        except FilterNotFoundException:
            value_to_return = None
           
        return value_to_return 
    
    def update(self, filter: str, value: Union[int, str, List[YamlDictionary], YamlList]) -> list:
        """Updates the value of the file, using a filter to determine the position of the value. After the update the file is synchronised automatically.

        ***Args:***
        - `filter (str)`: Filter used to determine the position of the value.
        - `value (Union[int, str, List[YamlDictionary], YamlList])`: Value to be updated.

        ***Returns:***
            `list`: Content of the file updates.
        
        *Filter format:*
        - File content: `[YamlDictionary("key",[YamlDictionary("sub_key", "value")])` -> filter: `"key.sub_key"`
        - File content: `[YamlDictionary("key",YamlList([1, 2, 3]))` -> `filter: "key.[]"`
        - File content: `[YamlDictionary("key",YamlList([[YamlDictionary("sub_key_1", "value_1"), YamlDictionary("sub_key_2", "value_2")]])]` -> filter: `"key.[].sub_key_1"`
        
        *Note:*  <br /> 
        The filter it must be in the following format:  <br /> 
        Supposte che file content is a dictionary with another dictionary as value, so the situation is
        
        ```python
        [ YamlDictionary("key", 
                            [YamlDictionary("sub_key", "value")
                            ]
                        )
        ]
        ``` 
        in order to change the value the filter must be in the following format: `"key.sub_key"`.
        
        """
        return self._modification_handler.update(filter, value)
    
    def add(self, key: str, data_to_add: Union[int, str, List[YamlDictionary], YamlList]) -> list:
        """Adds an item under the specified `key`.

        ***Args:***
        - `key (str)`: Key to add.
        - `data_to_add (Union[int, str, List[YamlDictionary], YamlList])`: Data to add.
        
        ***Raises:***
        -  `KeyAlreadyUsedException`: If the key already exists.
        
        ***Returns:***
            `list`: Content of the file updated, after the add.
       
        
        ***Note***: This method doesn't check the `data_to_add parameter`, it this is not in right format, the file `.yaml` can be corrupted.
        """
        return self._modification_handler.add(key, data_to_add)
    
    def remove(self, filter: str) -> list:
        """Remove a value from the file, using a filter to determine the position. After the remove the file is synchronised automatically.

        ***Args:***
        - `filter (str)`: Filter used to determine the position of the value.

        ***Returns:***
            `list`: Content of the file updated, after the remove.
        
        ***Filter format:***
        - File content: `[YamlDictionary("key",YamlDictionary("sub_key", "value"))` -> filter: `"key.sub_key"`
        For the remotion the filter must not contain `[]`. This because the list is completely removed, using the value of its key.
    
        *Example:* 
        - List remotion:
            - File content: `[YamlDictionary("key",YamlList([1, 2, 3]))`
                - Filter: `"key"`
                - After remove: `[]`
            - File content: `[YamlDictionary("key",[YamlDictionary("sub_key_1", "value_1"), YamlDictionary("sub_key_2", "value_2") ]]`
                - Filter: `"key.sub_key_1"`
                - After remove: `[YamlDictionary("key",[YamlDictionary("sub_key_2", "value_2")])]`
        """
        return self._modification_handler.remove(filter)   
    
    def clean_file(self, return_old_file_content: bool = False) -> Union[list, None]:
        """Clean the file, removing all the content. After the clean the file is synchronised automatically.
        
        ***Args:***
        - `return_old_file_content (bool)`: If True the file content is returned. Defaults to False.
        
        ***Returns:***
        - `Union[list, None]`: If `return_old_file_content` is True the file content is returned, otherwise None.
        
        """
        return self._modification_handler.clean_file(return_old_file_content)