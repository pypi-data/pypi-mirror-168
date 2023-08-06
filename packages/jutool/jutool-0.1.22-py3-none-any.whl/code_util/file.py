import os


def create_folder_if_not_exsited(*args):
    path = os.path.join(args)
    if not os.path.exists(path):
        os.mkdir(path)
    return path
