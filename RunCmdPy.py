#!/usr/bin/python

from subprocess import Popen, PIPE
import datetime



class RunCmd:
    DEBUG_MODE = "D"
    NORMAL_MODE = "N"

    def __init__(self):
        """
            Constructor for RunCmd object. KWR
        """

        self.cmd = ""
        self.rc = 0
        self.stdout = []
        self.stderr = []
        self.so_line_count = -1
        self.se_line_count = -1
        self.good_cmds = []
        self.bad_cmds = []

    def run(self, cmd, mode=NORMAL_MODE):
        """
        Run a command and capture stdout, stderr and return code.

        :rtype: int
        :param cmd: command string to pass to shell
        :type cmd:  basestring
        """

        if len(cmd) > 0:
            self.cmd = cmd
            self.so_line_count = 0
            self.se_line_count = 0
            self.stderr = []
            self.stdout = []
            if mode == RunCmd.DEBUG_MODE:
                print("<mode={}> <cmd={}>".format(mode, self.cmd))
                self.rc = 0
                return

            p = Popen(self.cmd, shell=True, stdout=PIPE, stderr=PIPE)
            self.rc = p.wait()
            self.stdout, self.stderr = p.communicate()
            
            # print('>>> DBUG: <stdout={}/{}>'.format(self.stdout.decode("utf-8") , type(self.stdout)))
            
            # Python 3 has stdout and stderr as <class btytes> need to decode them.
            self.stdout = self.stdout.decode("utf-8").split('\n')
            
            # Need to check for empty string as element of list.
            list_len = len(self.stdout)
            if list_len > 1 and len(self.stdout[-1]) == 0:
                # Last element is null string so remove it.
                self.stdout = self.stdout[: list_len - 1] 
            # Recalculate number of elements in list now.
            self.so_line_count = len(self.stdout)
            
            self.stderr = self.stderr.decode("utf-8").split('\n')
            list_len = len(self.stderr)
            if list_len > 1 and len(self.stderr[-1]) == 0:
                # Last element is null string so remove it.
                self.stderr = self.stderr[: list_len - 1] 
            # Recalculate number of elements in list now.
            self.se_line_count = len(self.stderr)
            
            # 
            #  Need to check for no output in stderr.
            #   If no output in stderr, there is one item in list that is null string
            
            if self.stderr[0] == "":
                self.se_line_count = 0
                self.stderr = []
            else:
                self.se_line_count = len(self.stderr)
            if self.rc == 0:
                self.good_cmds.append(cmd)
            else:
                self.bad_cmds.append(cmd)
        else:
            self.rc = 254
            if mode == RunCmd.DEBUG_MODE:
                print("Comand string is empty")
                return self.rc

        return self.rc

    def elaspe_time_run(self, cmd, mode=NORMAL_MODE):
        
        startt = stopt = datetime.datetime.now()
            
        self.run(cmd, mode)
        
        if mode == RunCmd.NORMAL_MODE:
            stopt = datetime.datetime.now()
            diff = stopt - startt
            return diff.total_seconds() * 1000
        else:
            return 0

    @property
    def get_cmd(self):
        """
        Returns the value passed to run() command
        :return:    command just executed
        :rtype:     basestring
        """

        return self.cmd

    @property
    def get_rc(self):
        """
        Return the shell return code from the previous command
        :return:    shell return code
        :rtype:     int
        """

        return self.rc

    @property
    def get_stdout(self):

        """
        Returns a list representing the lines found in stdout.
        :return:    a list with output of command (stdout).
        :rtype:     list of basestring
        """
        return self.stdout

    @property
    def get_stderr(self):
        return self.stderr

    @property
    def get_num_lines_stdout(self):
        return self.so_line_count

    @property
    def get_num_lines_stderr(self):
        return self.se_line_count

    @staticmethod
    def num_words(a_string):
        return [len(sentence.split()) for sentence in a_string]

    @staticmethod
    def as_word_list(a_string):
        return a_string.split()

    @staticmethod
    def list_as_string(alist):
        n = 0
        retstr = ""
        for item in alist:
            retstr += "{:>4}:<{}>\n".format(n, item)
            n += 1
        return retstr

    def dump_stdout(self):
        s = self.list_as_string(self.stdout)
        print("{}".format(s))

    def dump_stderr(self):
        s = self.list_as_string(self.stderr)
        print("{}".format(s))


    def ms_2_human_readable(self, ms):
        """
        This converts micro-seconds to ms/sec/mn/hrs string.
            Example:    "3000 ms/3.00 sec/0.50 min/xx.yy hrs"

        :param ms: micro-seconds
        :return: human readable ms/sec/min/hrs string
        """
        secs = ms / 1000
        mins = secs / 60
        hrs = mins / 60

        return "{0:.2f} ms/{1:.2f} sec/{2:.2f} min/{3:.2f} hrs".format(ms, secs, mins, hrs)


def test1():
    c1 = RunCmd()
    c1.run("ls -l /home/kurtis")
    print("<rc={:d}> <so_num_lines={:d}> <se_num_lines={:d}>".format(c1.get_rc, c1.get_num_lines_stdout,
                                                                     c1.get_num_lines_stderr))
    print("\n>>> stdout >>>")
    c1.dump_stdout()
    print("<<< stdout <<<")
    print("\n>>> stderr >>>")
    c1.dump_stderr()
    print("<<< stderr <<<")
    return 0


def test2():
    c1 = RunCmd()
    c1.run("lxddd -l /home/kurtis")
    print("<rc={:d}> <so_num_lines={:d}> <se_num_lines={:d}>".format(c1.get_rc, c1.get_num_lines_stdout,
                                                                     c1.get_num_lines_stderr))
    print("\n>>> stdout >>>")
    c1.dump_stdout()
    print("<<< stdout <<<")
    print("\n>>> stderr >>>")
    c1.dump_stderr()
    print("<<< stderr <<<")
    return 0


def test3():
    c1 = RunCmd()
    c1.run("ls -l /home/kurtis")
    print("<rc={:d}> <so_num_lines={:d}> <se_num_lines={:d}>".format(c1.get_rc, c1.get_num_lines_stdout,
                                                                     c1.get_num_lines_stderr))
    print("\n>>> stdout >>>")
    c1.dump_stdout()
    print("<<< stdout <<<")
    print("\n>>> stderr >>>")
    c1.dump_stderr()
    print("<<< stderr <<<")
    if c1.get_rc != 0:
        print("Command error.")
        return 1
    if c1.get_num_lines_stdout == 0:
        print("No output")
        return 2

    out = c1.get_stdout
    n = 0
    for line in out:
        if n > 0:
            print("<line={0:s}>".format(line))
            tokens = c1.as_word_list(line)
            print("  <tok8={:s}>".format(tokens[8]))
        n += 1

    return 0


def main():
    #    test1()
    #    test2()
    test3()

    return 0


if __name__ == "__main__":
    # execute only if run as a script
    main()
    exit(0)
