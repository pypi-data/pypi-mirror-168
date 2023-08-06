import os
import jinja2
import pkginfo
from fat_wheel.parse.py_file import get_py_file_meta_data, SetupPyArg


class SetupPyData:

    def __init__(self):
        self.version = None
        self.before_setup = None
        self.after_setup = None
        self.setup_options = None

    @staticmethod
    def build_setup_py_meta_data(root_dir, pkg_name):
        setup_py_data = SetupPyData()
        meta_data = get_py_file_meta_data(os.path.join(root_dir, "setup.py"))
        default_package_data = True
        default_entry_points = True
        version = None
        for meta in meta_data:
            if meta.arg == "version":
                version = meta.value
            elif meta.arg == "package_data":
                default_package_data = False
                package_data_dict = meta.value
                pkg_data = ["deps/*"]
                if pkg_name in package_data_dict:
                    pkg_data.extend(package_data_dict.get(pkg_name))
                package_data_dict[pkg_name] = pkg_data
            elif meta.arg == "entry_points":
                default_entry_points = False
                entry_points_list = meta.value.get("console_scripts")
                entry_points = [f"{pkg_name} = {pkg_name}.runner:install"]
                entry_points_list.extend(entry_points)

        if default_entry_points:
            entry_points_dict = {"console_scripts": [f"{pkg_name} = {pkg_name}.runner:install"]}
            pkg = SetupPyArg("entry_points", entry_points_dict, "dict", 0, 0)
            meta_data.insert(-1, pkg)

        if default_package_data:
            package_data_dict = {pkg_name: ["deps/*"]}
            pkg = SetupPyArg("package_data", package_data_dict, "dict", 0, 0)
            meta_data.insert(-1, pkg)

        for m in meta_data:
            if m.arg == "before_setup" or m.arg == "after_setup":
                tmp = []
                for g in m.value:
                    if g != "\n":
                        tmp.append(g[:-1])
                m.value = tmp

        setup_py_data.version = version
        setup_py_data.before_setup = meta_data.pop(0)
        setup_py_data.after_setup = meta_data.pop(-1)
        setup_py_data.setup_options = meta_data
        return setup_py_data

    def get_version(self):
        return self.version

    def get_before_setup(self):
        return self.before_setup

    def get_after_setup(self):
        return self.after_setup

    def get_setup_options(self):
        return self.setup_options


# below code will be removed soon
TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "template")
TEMPLATE_FILE = "setup.txt"


def copy_installer(dest):
    """ moved to template_writer remove after 1.5"""
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("runner.py")
        dest_list = []
        for i in os.scandir(os.path.join(dest, "deps")):
            dest_list.append(pkginfo.get_metadata(i.path).name)
        output_text = template.render(dep_list=str(dest_list))
        with open(os.path.join(dest, "runner.py"), mode="w") as s:
            s.write(output_text)
    except Exception as e:
        raise e


def generator(options, build_path=""):
    """ moved to template_writer remove after 1.5"""
    try:
        before_setups = options.pop(0)
        after_setups = options.pop(-1)
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(TEMPLATE_FILE)
        output_text = template.render(before_setups=before_setups,
                                      options=options,
                                      after_setups=after_setups)
        with open(os.path.join(build_path, "setup.py"), mode="w") as s:
            s.write(output_text)
    except Exception as e:
        raise e


def generate_setup_py_v2(fat_wheel_build_path, setup_meta_data):
    generator(setup_meta_data, build_path=fat_wheel_build_path)


def build_setup_py_meta_data(root_dir, pkg_name):
    meta_data = get_py_file_meta_data(os.path.join(root_dir, "setup.py"))
    default_package_data = True
    default_entry_points = True
    for meta in meta_data:
        if meta.arg == "package_data":
            default_package_data = False
            package_data_dict = meta.value
            pkg_data = ["deps/*"]
            if pkg_name in package_data_dict:
                pkg_data.extend(package_data_dict.get(pkg_name))
            package_data_dict[pkg_name] = pkg_data
        if meta.arg == "entry_points":
            default_entry_points = False
            entry_points_list = meta.value.get("console_scripts")
            entry_points = [f"{pkg_name} = {pkg_name}.runner:install"]
            entry_points_list.extend(entry_points)

    if default_entry_points:
        entry_points_dict = {"console_scripts": [f"{pkg_name} = {pkg_name}.runner:install"]}
        pkg = SetupPyArg("entry_points", entry_points_dict, "dict", 0, 0)
        meta_data.insert(-1, pkg)

    if default_package_data:
        package_data_dict = {pkg_name: ["deps/*"]}
        pkg = SetupPyArg("package_data", package_data_dict, "dict", 0, 0)
        meta_data.insert(-1, pkg)

    for m in meta_data:
        if m.arg == "before_setup" or m.arg == "after_setup":
            tmp = []
            for g in m.value:
                if g != "\n":
                    tmp.append(g[:-1])
            m.value = tmp
    return meta_data


def get_version(setup_meta_data):
    for key in setup_meta_data:
        if "version" in key.arg:
            return key.value


def generate_setup_py(fat_wheel_build_path, root_dir, pkg_name):
    """ not used any where remove it soon """
    meta_data = get_py_file_meta_data(os.path.join(root_dir, "setup.py"))
    default_package_data = True
    default_entry_points = True
    for meta in meta_data:
        if meta.arg == "package_data":
            default_package_data = False
            package_data_dict = meta.value
            pkg_data = ["deps/*"]
            if pkg_name in package_data_dict:
                pkg_data.extend(package_data_dict.get(pkg_name))
            package_data_dict[pkg_name] = pkg_data
        if meta.arg == "entry_points":
            default_entry_points = False
            entry_points_list = meta.value.get("console_scripts")
            entry_points = [f"{pkg_name} = {pkg_name}.runner:install"]
            entry_points_list.extend(entry_points)

    if default_entry_points:
        entry_points_dict = {"console_scripts": [f"{pkg_name} = {pkg_name}.runner:install"]}
        pkg = SetupPyArg("entry_points", entry_points_dict, "dict", 0, 0)
        meta_data.insert(-1, pkg)

    if default_package_data:
        package_data_dict = {pkg_name: ["deps/*"]}
        pkg = SetupPyArg("package_data", package_data_dict, "dict", 0, 0)
        meta_data.insert(-1, pkg)

    for meta in meta_data:
        if meta.arg == "before_setup" or meta.arg == "after_setup":
            tmp = []
            for g in meta.value:
                if g != "\n":
                    tmp.append(g[:-1])
            meta.value = tmp
    # extra_options = [[[pkg_name, '"deps/*"']], [f"{pkg_name} = {pkg_name}.runner:install"]]
    generator(meta_data, build_path=fat_wheel_build_path)
