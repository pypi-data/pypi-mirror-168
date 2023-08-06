# PythonYamlWrapper
![GitHub](https://img.shields.io/github/license/alexandruparaschivdumitru/yaml_wrapper?style=for-the-badge)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/alexandruparaschivdumitru/yaml_wrapper?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/alexandruparaschivdumitru/yaml_wrapper?style=for-the-badge)

<p align="center">
<img src="https://user-images.githubusercontent.com/49406681/183289867-ce12c95d-8363-46c6-bfdd-21f0b8fd7eeb.png" width="80%">
</p>

## Description
***YamlWrapper*** is an abstraction over PyYAML library. Its purpuse is to made easier to interact with `.yaml` files. This is made possible by create/update/remove operations with two main abstract data types: `YamlDictionary` and `YamlList`.
## Documentation
You can find the official documentation at this [link](https://alexandruparaschivdumitru.github.io/yaml_wrapper/src/API/yaml_wrapper.html)  
## Installation
```zsh
   pip install PythonYamlWrapper
```
## Importing
```python
   from yaml_wrapper import YamlWrapper
   
   yaml_wrapper: YamlWrapper = YamlWrapper("tmp/file_path.yaml")
```
## Abstract data types and examples
The core functionalities provided by `YamlWrapper` work with `YamlDictionary` and `YamlList`. 
- **Dictionary**
```yaml
    key_1: "value"
    key_2:
       sub_key_1: "sub_value"
       sub_key_2: 1
```
Is rappresented by:
```python
  data = [
            YamlDictionary("key", "value"),
            YamlDictionary("sub_key", [
                                          YamlDictionary("sub_key_1", "sub_value"),
                                          YamlDictionary("sub_key_2", 1)
                                       ])
  
         ]
```
- **Lists**
```yaml
- "first_value"
- "second_value"
- "third_value"
```

Is rappresented by:
```python
  data = [
            YamlList(["first_value", "second_value", "third_value"])
         ]
```
- **Dictionary with list**
```yaml
   key: 
      - "first_value"
      - "second_value"
      - "third_value"
```
Is rappresented by:
```python
  data = [  
            YamlDictionary("key", YamlList(["first_value", "second_value", "third_value"]))
         ]
```
## Special thanks
[PyYaml](https://pypi.org/project/PyYAML/)

## Author
- [Alexandru Paraschiv Dumitru](aaaalexdumitru@gmail.com)
