#!/usr/bin/env python3
import os
import psutil
import dbus
import subprocess
import pathlib
import time
import tempfile
from importlib.util import find_spec
from .zsocket import SocketListener


if find_spec("ewmh"):
    from ewmh import EWMH

    has_ewmh = True
else:
    has_ewmh = False


class Zathura:
    """
    Class to interact with zathura
    methods:
        self._mk_pid_file()     # Used internally to create files
                                # where znp -w $TMP_FILE $FILE
                                # will wite the value of $FILE

        self.ewmh_get_pid()     # Used to get the pid of the
                                # active window if running X11
                                # and ewmh is installed

        self.execute()          # Takes a pid and a command to run
                                # from the given instance

        self.open()             # Takes a pid and a file_path to be
                                # openend in the given instance

        self.pid_search()       # Runs when class is created
                                # adds a list of zpids to self.pids

        self.remove_tmp_files() # Removes all files in self.files_to_remove

        self.zathura_search()   # Takes a pid and optionaly a search file
                                # and tries to find a zathura instance
                                # that has that file currently open
    attributes:
        self.pids list          # Is a list of pids that belong to
                                # running zathura instances

        self.has_ewmh bool      # True if user has ewmh installed

        self.epid int           # Is a pid value stored after running
                                # self.ewmh_get_pid()

        self.pid_files dict     # Is a dictionary of pids keys with
                                # file values

        self.pid_dict dict      # Is a dictionary of pid keys with
                                # a list value where the first value in
                                # the list is the currently open file
                                # and the second value is the pid tied
                                # to the file. Multiple pids may have the
                                # same file open and this ensures the desired
                                # pid is chosen

        self.files_to_remove    # Is a list of files that need to be removed
                                # if self.z_search is run
    """

    def __init__(self):
        self.has_ewmh = has_ewmh
        self.pid_search()

    def _mk_pid_file(self, file_path):
        """Create the given file if it does not exist"""
        if os.path.isfile(file_path):
            return
        fp = pathlib.Path(file_path).touch(mode=0o600)
        return

    def ewmh_get_pid(self):
        """
        Use ewmh to get the pid of the focused window.
        This should be zathura assuming znp was run from
        zathura and user is using X11
        """
        if not self.has_ewmh:
            return False
        ewmh = EWMH()
        win = ewmh.getActiveWindow()
        pid = ewmh.getWmPid(win)
        if pid in self.pids:
            self.epid = pid
            return True
        self.epid = None
        return False

    def execute(self, pid, command):
        """
        Execute a zathura command. Requires the given zpid to send
        the command to.
        """
        zathuraName = "org.pwmt.zathura.PID-" + str(pid)
        zathuraObject = dbus.SessionBus().get_object(zathuraName, "/org/pwmt/zathura")
        zathuraDBus = dbus.Interface(zathuraObject, "org.pwmt.zathura")
        zathuraDBus.ExecuteCommand(command)
        return 0

    def open(self, file_path, pid=None):
        """
        Open file in zathura optionally open the next file in
        the directory of the given file
        """
        # If zathura isn't open we can open it
        if not pid:
            zathuraPopen = subprocess.Popen(["zathura", file_path])
            return 0
        # Open the given file
        zathuraName = "org.pwmt.zathura.PID-" + str(pid)
        zathuraObject = dbus.SessionBus().get_object(zathuraName, "/org/pwmt/zathura")
        zathuraDBus = dbus.Interface(zathuraObject, "org.pwmt.zathura")
        zathuraDBus.OpenDocument(file_path, "", 0)
        return 0

    def pid_search(self, name="zathura"):
        """
        Search for zathura pid(s). Used when:
            1. User is using Wayland
            2. ewmh fails for some reason
            3. If the user did not provide a PID at runtime
        """
        pids = []
        for proc in psutil.process_iter():
            try:
                p_name = proc.name()
            except psutil.NoSuchProcess:
                continue
            if p_name == name:
                pids.append(proc.pid)
        self.pids = pids
        self.pid_count = len(pids)
        return None

    def query(self, search_file):
        """
        Query zathura instances for the instance with search_file open.
        If found prints the pid, else nothing and exits with status 1.
        """
        if self.pid_count == 0:
            return 1
        elif self.pid_count == 1:
            print(self.pids[0])
            return 0
        elif self.zathura_search(self.pids, search_file=search_file):
            print(self.search_pid)
            return 0

        return 1

    def zathura_search(self, pids, search_file=None, prog="znp"):
        """
        Search for an instance of zathura using bad means.
        This creates a dictionary of zathura instances if multiple exist:
            >>> zathura = Zathura()
            >>> print(zathura.pid_dict)
            >>> '{ "123456": ["/path/to/file.pdf", "123456: /path/to/file.pdf"]
                   "154684": ["/path/to/file.epub", "154684: /path/to/file.epub"] }'
        """
        # Create temp dir for placing socket
        tdir = tempfile.gettempdir()
        tdir = os.path.join(tdir, prog)
        server_address = os.path.join(tdir, "znp_socket")
        if not os.path.isdir(tdir):
            os.mkdir(tdir, mode=0o700)
        # Start SocketListener and expect as many messages as pids
        pid_count = len(pids)
        server = SocketListener(
            server_address=server_address,
            expected_messages=pid_count,
        )
        # Give server some time to start
        time.sleep(0.05)
        # Get pid of current script in case client fails it will kill
        # this script so user is not left with a hanging process/socket
        ppid = os.getpid()
        # Run clients to find current files in each pid
        for pid in pids:
            self.execute(
                pid, f"exec znp -P {pid} -s {ppid} -c {server_address} '$FILE'"
            )
        # Wait for server to get all client messages
        while server.recieved < pid_count:
            pass
        # Server must have recieved all messages, store it's data
        self.pid_dict = server.pid_dict
        self.search_pid = None
        # If not searching for a specific file return True
        if not search_file:
            return True
        # Search the pid_dict for the desired file
        for key, value in server.pid_dict.items():
            if value[0] == search_file:
                # Search_file found set search_pid and return True
                self.search_pid = key
                return True
        # Desired instance wasn't found return False
        return False
