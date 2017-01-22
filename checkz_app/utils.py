# -*- coding: utf-8 -*-
import os


def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')

if __name__ == "__main__":

    print(get_app_base_path())
    print(get_instance_folder_path())