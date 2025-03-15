import importlib.util
import shutil
import os
from pathlib import Path
import warnings
from pydeps.pydeps import pydeps
from pydeps import cli
import subprocess
import json
import sys

# os.system is potentially unsafe.
# Use some other library, maybe `subprocess`?


def get_package(package_name, package_url=None, clone=True):
    """
    Get the package source code.

    Parameters:
    - package_name (str): The name of the package to retrieve.
    - package_url (str): The URL of the package repository (required if cloning).
    - clone (bool): Whether to clone the package from the repository.
    """
    if clone:
        if package_url is None:
            raise ValueError("`package_url` kwarg not received in `clone` mode.")
        else:
            _clone_package(package_name, package_url)
    else:
        warnings.warn(
            """
            Not using `clone` mode builds the package source code by unzipping the wheels,
            hence the `C/C++` Extension files present in the source code will be lost due
            to the compiled nature of the wheel.
            """
        )
        _get_package_no_clone(package_name)


def _clone_package(package_name, package_url):
    """Clone the package from the given URL."""
    try:
        if package_name not in os.listdir("."):
            os.system(f"git clone {package_url}.git")
        return True
    except Exception as e:
        print(str(e))
        return False


def _get_package_no_clone(package_name):
    """Retrieve the package source code without cloning."""
    try:
        # Step 1: Locate the installed package
        if not sys.modules.get(package_name):
            spec = importlib.util.find_spec(package_name)
            if not spec or not spec.origin:
                print(f"Package {package_name} not found.")
                return False

            package_path = Path(spec.origin).parent
            print(f"Located package: {package_path}")

        else:
            package_path = sys.modules[package_name].__file__[: -1 * len("__init__.py")]
            print(f"Located package: {package_path}")

        # Step 2: Copy the source code to the current directory
        destination_dir = Path.cwd() / package_name
        if destination_dir.exists():
            shutil.rmtree(destination_dir)  # Remove if already exists

        try:
            shutil.copytree(package_path, destination_dir)
            print(f"Copied source files to: {destination_dir}")
        except Exception as e:
            print(f"Failed to copy source files: {e}")
            return False

        # Step 3: Remove unnecessary metadata folders
        for item in destination_dir.glob("*.dist-info"):
            shutil.rmtree(item, ignore_errors=True)
        for item in destination_dir.glob("*.egg-info"):
            shutil.rmtree(item, ignore_errors=True)
        for item in destination_dir.glob("__pycache__"):
            shutil.rmtree(item, ignore_errors=True)

        print(f"Cleaned up metadata for package: {package_name}")
        return True

    except Exception as e:
        print(f"Exception occurred: {e}")
        return False


def _cleanup_dir(folder):
    """Remove the specified directory if it exists."""
    if folder in os.listdir("."):
        shutil.rmtree(folder)


def _set_external(graph, folder=None, allow_clone=False):
    """Set external nodes in the graph based on external dependencies."""
    # Graph is a dependency Graph.
    # if folder is None:
    #     _get_package_no_clone(graph.graph.package_name)

    _args = [
        "pydeps",
        "-vv",
        f"--max-bacon={3}",
        "--external",
        f"{graph.graph.package_name}",
    ]

    result = subprocess.run(
        _args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"pydeps failed: {result.stderr}")

    try:
        result_list = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError("Failed to decode pydeps output")

    for _pkg in result_list:
        try:
            node = graph.graph.graph.nodes[_pkg]
            assert node is not None
            node["external"] = True
            print(f"Marked package {_pkg} as external.")
        except KeyError:
            pass
