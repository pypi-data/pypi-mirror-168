# pylint: skip-file
import os
import io


class Project:

    def __init__(self, name, version, root_dir, deps, wheel_type, test, config_file, is_root, pkg_name, fat_config_yml):
        self.name = name
        self.version = version
        self.root_dir = root_dir
        self.deps = deps
        self.wheel_type = wheel_type
        self.test = test
        self.config_file = config_file
        self.is_root = is_root
        self.pkg_name = pkg_name
        self.fat_config_yml = fat_config_yml

    def set_version(self, version):
        self.version = version


class ProjectBuilder:

    def __init__(self):
        self._name = None
        self._version = None
        self._root_dir = None
        self._deps = None
        self._wheel_type = None
        self._test = None
        self._config_file = None
        self._is_root = None
        self._pkg_name = None
        self._fat_config_yml = None

    @classmethod
    def builder(cls):
        return cls()
    
    def build_by_path(self, project_dir):
        REQUIREMENTS_TXT = "requirements.txt"
        FAT_WHEEL_YAML = "fat-wheel.yaml"
        PY_PROJECT_YAML = "pyproject.toml"
        fat_wheel_config = [REQUIREMENTS_TXT, FAT_WHEEL_YAML, PY_PROJECT_YAML]
        self._is_root = False

        if project_dir.strip().__eq__(""):
            project_dir = os.getcwd()
        project_dir = os.path.abspath(project_dir)
        _fat_wheel_config = list(map(lambda x: os.path.join(project_dir, x), fat_wheel_config))
        self._name = os.path.basename(project_dir)
        for wheel_config_path in _fat_wheel_config:
            if os.path.exists(wheel_config_path):
                self._is_root = True
                if REQUIREMENTS_TXT in wheel_config_path:
                    self._config_file = wheel_config_path
                if FAT_WHEEL_YAML in wheel_config_path:
                    self._fat_config_yml = wheel_config_path

        if not self._is_root:
            return self
        self._root_dir = project_dir
        self._deps = extract_deps(self._config_file)

        for i in os.scandir(project_dir):
            if os.path.isdir(i.path):
                if os.path.exists(os.path.join(i.path, "__init__.py")):
                    self._pkg_name = i.name

        return self

    def name(self, name):
        self._name = name
        return self
    
    def version(self, version):
        self._version = version
        return self
    
    def root_dir(self, root_dir):
        self._root_dir = root_dir
        return self
    
    def deps(self, deps):
        self._deps = deps
        return self
    
    def wheel_type(self, wheel_type):
        self._wheel_type = wheel_type
        return self
    
    def test(self, test):
        self._test = test
        return self
    
    def config_file(self, config_file):
        self._config_file = config_file
        return self
    
    def is_root(self, is_root):
        self._is_root = is_root
        return self
    
    def build(self):
        return Project(self._name, self._version, self._root_dir, self._deps, self._wheel_type,
                       self._test, self._config_file, self._is_root, self._pkg_name, self._fat_config_yml)


def extract_deps(config):
    """read deps from reqirements.txt"""
    with io.open(config, 'r', encoding='utf-16-le') as c:
        deps = c.read()[1:].splitlines()
    return list(map(lambda x: x.split("=")[0].lower(), filter(lambda x: len(x) != 1, deps)))
