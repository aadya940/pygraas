import os


def _clone_package(package_name, package_url):
    try:
        if package_name not in os.listdir("."):
            os.system(f"git clone {package_url}.git")
        return True
    except Exception as e:
        print(str(e))
        return False


def _cleanup_dir(folder):
    if folder in os.listdir("."):
        shutil.rmtree(folder)
