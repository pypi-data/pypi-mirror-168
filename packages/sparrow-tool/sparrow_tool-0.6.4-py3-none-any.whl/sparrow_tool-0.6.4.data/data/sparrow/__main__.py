import fire
from .widgets import timer
from .multiprocess import start_server
from .docker import save_all_images as save_docker_images
from .docker import load_dir_images as load_docker_images

func_list = [
    timer,
    start_server,
    save_docker_images,
    load_docker_images,
]
func_dict = {}
for func in func_list:
    func_dict[func.__name__] = func


def main():
    fire.Fire(func_dict)
