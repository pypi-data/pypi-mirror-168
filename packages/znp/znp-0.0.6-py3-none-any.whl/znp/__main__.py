#!/usr/bin/env python3
import sys
from loadconf import Config
from pathlib import Path
from .options import get_opts
from .prompts import zathura_prompt
from .utils import (
    get_next_or_prev_file,
    NoFileOrDirectory,
)
from .zathura import Zathura
from .zsocket import send_to_socket

# from .config import UserSettings


__license__ = "GPL-v3.0"
__program__ = "znp"
# Create zathura object
z = Zathura()


def open_next_or_prev(
    file_path,
    next_file=False,
    prev_file=False,
    prompt_cmd=None,
):
    """
    Open file in zathura optionally open the next file in
    the directory of the given file
    """
    # Try to get the next or prev file in the cwd
    try:
        next_or_prev_file = get_next_or_prev_file(
            current_file_path=file_path,
            next_file=next_file,
            prev_file=prev_file,
        )
        # If next_or_prev_file is None then file_path
        # is the only valid file in the cwd. Exit gracefully
        if not next_or_prev_file:
            return 0
    except NoFileOrDirectory as err:
        print(err, sys.stderr)
        return 1
    # If user has ewmh try and use it to get the pid
    if z.has_ewmh:
        try:
            z.ewmh_get_pid()
            z.open(file_path=next_or_prev_file, pid=z.epid)
            return 0
        # Failed so we contiue and get the pid the hard way
        except TypeError:
            pass
    # Try searching for the given file manually
    # If found open it and exit
    if z.zathura_search(z.pids, search_file=file_path):
        z.open(file_path=next_or_prev_file, pid=z.search_pid)
        # z.remove_tmp_files()
        return 0
    # No prompt_cmd given, exit
    if not prompt_cmd:
        # z.remove_tmp_files()
        return 1
    # Prompt user for their desired instance
    choice = zathura_prompt(pid_dict=z.pid_dict, prompt_cmd=prompt_cmd)
    # No selection made, exit
    if not choice:
        # z.remove_tmp_files()
        return 1
    # Try opening the next file and exit
    z.open(file_path=next_or_prev_file, pid=choice)
    # z.remove_tmp_files()
    return 0


def open_given_file(
    file_path,
    prompt_cmd,
    prompt_args=None,
    pid=None,
):
    """
    Open the given file in zathura. Function may run in several ways:
        1. znp file.pdf
        2. znp -P 123456 file.pdf
        3. znp -P 123456 /path/to/file.pdf
        4. znp /path/to/file.pdf
    """
    # Resolve file_path if needed
    file_path = str(Path(file_path).resolve())
    # If given a pid then check if it exists an open the
    # file in the given instance
    if pid is not None and pid in z.pids:
        z.open(file_path=file_path, pid=pid)
        return 0
    # No pids open zathura ourself
    elif z.pid_count == 0:
        z.open(file_path=file_path)
        return 0
    # If only one pid then open file there
    elif z.pid_count == 1:
        z.open(file_path=file_path, pid=z.pids[0])
        return 0
    # Multiple zathura instances
    # Search and prompt user
    if z.zathura_search(z.pids):
        # TODO decide if znp should check for no choice
        # currently the znp will open the file in a new instance
        # if none is selected. Kind of nice but maybe not a good
        # idea.
        choice = zathura_prompt(
            z.pid_dict,
            prompt_cmd=prompt_cmd,
            prompt_args=prompt_args,
        )
        z.open(file_path=file_path, pid=choice)
        return 0
    # Search failed for some reason
    return 1


def main():
    """
    Main function for znp
    """
    args = get_opts()
    user = Config(__program__)
    user_files = {
        "conf_file": f"{__program__}.conf",
    }
    read_files = ["conf_file"]
    user.define_files(user_files=user_files)
    user.create_files(create_files=read_files)
    default_settings = {
        "prompt_cmd": "fzf",
        "prompt_args": "",
    }
    user.define_settings(settings=default_settings)
    user_settings = ["prompt_cmd", "prompt_args"]
    user.read_conf(
        user_settings=user_settings,
        read_files=read_files,
    )
    # Connect client to server_address to send args.file and args.pid
    # to the calling znp server
    if args.client is not None:
        return send_to_socket(
            pid=args.pid,
            parent_pid=args.source,
            file_path=args.file,
            server_address=args.client,
        )
    # User is opening next or prev file
    if args.next or args.prev:
        return open_next_or_prev(
            file_path=args.file,
            next_file=args.next,
            prev_file=args.prev,
            prompt_cmd=user.settings["prompt_cmd"],
        )
    # User just wants a the pid of a specific instance
    if args.query:
        return z.query(search_file=args.file)
    # User wants to open the given file in an optionally given zathura instance
    return open_given_file(
        file_path=args.file,
        prompt_cmd=user.settings["prompt_cmd"],
        prompt_args=user.settings["prompt_args"],
        pid=args.pid,
    )


if __name__ == "__main__":
    # Store main exit status
    sys.exit(main())
