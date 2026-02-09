import os

TARGET_DIR = "docs"
SOURCE_DIR = "static"


def copy_static_files():
    remove_target_dir_contents()
    copy_file_or_directory(SOURCE_DIR, TARGET_DIR)


def remove_target_dir_contents():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    for root, dirs, files in os.walk(TARGET_DIR, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def copy_file_or_directory(src_path: str, dest_path: str) -> None:
    # recutsevely copy files and directories from src_path to dest_path
    if os.path.isdir(src_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for item in os.listdir(src_path):
            copy_file_or_directory(
                os.path.join(src_path, item), os.path.join(dest_path, item)
            )
    else:
        with open(src_path, "rb") as src_file:
            with open(dest_path, "wb") as dest_file:
                dest_file.write(src_file.read())
