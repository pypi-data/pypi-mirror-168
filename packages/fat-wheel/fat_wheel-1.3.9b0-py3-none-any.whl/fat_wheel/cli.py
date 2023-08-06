import argparse
from fat_wheel.fat import process
from fat_wheel.utils import path_exits


def build_options(args):
    options = []
    if args.wheel:
        options.append("bdist_wheel")
    if args.egg:
        options.append("bdist_egg")
    if args.build:
        options.append("build")
        options.append("sdist")
    if len(options) == 0:
        options.append("bdist_wheel")
    return options


def main():
    parser = argparse.ArgumentParser(description="Fat wheel options")
    parser.add_argument("project_dir",
                        help="project dir to build(example|project_dir=<path>|<path>|",
                        nargs=1)
    parser.add_argument("-b", "--build",
                        help="create project local copy with dependencies and build source dist",
                        action="store_true")
    parser.add_argument("-w", "--wheel",
                        help="build wheel file with all dependencies",
                        action="store_true")
    parser.add_argument("-e", "--egg",
                        help="build egg file with all dependencies",
                        action="store_true")
    args = parser.parse_args()
    options = build_options(args)
    project_dir = str(args.project_dir[0]).split("=")[-1]
    if path_exits(project_dir):
        process(project_dir, options)
    else:
        print(f"path: {project_dir} does not exits")


if __name__ == '__main__':
    main()
