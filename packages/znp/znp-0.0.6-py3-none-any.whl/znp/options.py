#!/usr/bin/env python3
import argparse


def get_opts(prog_name="znp"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""
        Add a file to a given instance of zathura
        """,
        allow_abbrev=False,
    )
    parser.add_argument(
        "-c",
        "--client",
        metavar="SERVER_ADDRESS",
        action="store",
        # default=None,
        help="""
        Send a message to the socket at SERVER_ADDRESS. Message has a seven byte header
        which defaults to 0000000 if PID is not given. FILE is the message that will be
        sent and need not be an actual message. Used internally when searching for active
        instances and their open files and is executed like so:
        `znp -P 1234567 -c "/tmp/znp/znp_socket" "/path/to/current.pdf"` from the instance
        that belongs to pid 1234567.
        """,
    )
    parser.add_argument(
        "-n",
        "--next",
        action="store_true",
        help="""
        Go to the next file in the directory of the given file
        """,
    )
    parser.add_argument(
        "-p",
        "--prev",
        action="store_true",
        help="""
        Go to the prev file in the directory of the given file
        """,
    )
    parser.add_argument(
        "-P",
        "--pid",
        metavar="PID",
        action="store",
        # default=None,
        help="""
        PID of the zathura instance to use. Default is the
        active window detected via ewmh
        """,
    )
    parser.add_argument(
        "-q",
        "--query",
        action="store_true",
        help="""
        Query zathura instances for the instance with FILE open.
        If found prints the pid, else prints nothing and exits with status 1.
        """,
    )
    parser.add_argument(
        "-s",
        "--source",
        metavar="PID",
        action="store",
        # default=None,
        help="""
        PID of the zathura instance to use. Default is the
        active window detected via ewmh
        """,
    )
    parser.add_argument(
        "file",
        metavar="FILE",
        help="""
        The file to open, or the file that is currently open.
        """,
    )
    args = parser.parse_args()
    return args
