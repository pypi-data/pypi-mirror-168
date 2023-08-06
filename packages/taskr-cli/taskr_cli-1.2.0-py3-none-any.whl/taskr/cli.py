import argparse
import os
import subprocess
import sys
from typing import Any, List

from .__version__ import version as VERSION
from .taskr import _Taskr


def _handle_docker(
    engine: str, image_name: str, task: str, custom_args: List[Any]
) -> None:
    """
    If we want to run a task in an image instead,
    get the image name and run a generic `docker run`
    on the image

    This assume taskr is in the container - it runs the task with it...

    Could possibly
    - Use docker/podman plugin, but that a dependency
    - Simple implementation here
    - Allow a custom command too?
    - Remove all together in favor of a 'runner.docker' helper

    """
    expanded = " ".join(custom_args)
    task_to_run = f"taskr {task} {expanded}"
    command = f"{engine} run --rm -a stdin -a stdout -t {image_name} {task_to_run}"

    print(f"▸ Running {command}")

    subprocess.Popen(
        command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT
    ).wait()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="taskr", description="A cli utility to run generic tasks"
    )
    parser.add_argument(
        "-d",
        "--docker",
        action="store_true",
        help="run a task in an image with docker. Requires IMAGE_NAME set in tasks.py",
    )
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        default=False,
        help="generate a template task file",
    )
    parser.add_argument("-l", "--list", action="store_true", help="show defined tasks")
    parser.add_argument(
        "-p",
        "--podman",
        action="store_true",
        help="run a task in an image with podman. Requires IMAGE_NAME set in tasks.py",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show the version number"
    )
    # parser.add_argument('task', nargs='?', default=None)

    args, custom_args = parser.parse_known_args()

    # No Taskr needed yet
    if args.init:
        _Taskr.init()
        return

    if args.version:
        print(f"Running {VERSION}")
        return

    # Below actions needs an instance of taskr

    try:
        # Attempt to import the tasks file from any sub directory, if we
        # are in a virtual environment with pyenv
        root = ""
        if "PYENV_DIR" in os.environ:
            root = os.environ["PYENV_DIR"]
        elif "TASKR_DIR" in os.environ:
            root = os.environ["TASKR_DIR"]

        sys.path.append(root)
        import tasks

    except ImportError:
        print("No valid tasks.py file found in current directory. Run 'taskr --init'")
        parser.print_help()
        sys.exit(1)

    Taskr = _Taskr(tasks)

    # Custom arguments take precedence
    if custom_args:
        # Custom task was passed, take it in
        task = custom_args.pop(0)

        # Ignore anything that looks like a normal arg, it shouldn't be here
        if task.startswith("-"):
            parser.print_help()
            return

        # We have a task, process it with docker or taskr
        if args.docker and args.podman:
            print("Cannot choose docker and podman")

        engine = None

        if args.docker:
            engine = "docker"
        if args.podman:
            engine = "podman"

        if not engine:
            Taskr.process(task, custom_args)
            return

        if engine and Taskr.image_name:
            _handle_docker(engine, Taskr.image_name, task, custom_args)
        else:
            print("'IMAGE_NAME' not defined in tasks.py. Cannot run in a a container")
            return

    # Non tasks command below
    elif args.list:
        Taskr.list()

    # No tasks passed, check if we have a default task
    elif Taskr.hasDefault():
        Taskr.default()

    # Finally print help
    else:
        parser.print_help()
