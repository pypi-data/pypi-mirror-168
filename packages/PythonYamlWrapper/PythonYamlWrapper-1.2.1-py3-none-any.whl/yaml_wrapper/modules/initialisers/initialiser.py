from ..translators.from_yaml_traslator import FromYamlTraslator
from ...utils.file.file_utils import FileUtil


class Initialiser:
    def __init__(self, file_path: str, create_not_exitent_file: bool = False) -> None:
        self._file_path: str = file_path
        self._from_yaml_traslator: FromYamlTraslator = FromYamlTraslator(file_path)
        self._create_not_exitent_file: bool = create_not_exitent_file
    
    def initialise(self) -> list:
        try:
            return self._from_yaml_traslator.translate()
        except OSError:
            if self._create_not_exitent_file:
                FileUtil.create_file_from_path(self._file_path)
                return self._from_yaml_traslator.translate()
            else:
                raise FileNotFoundError("File \"" + self._file_path + "\" not found!")