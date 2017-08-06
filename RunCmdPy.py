#!/usr/bin/python

from subprocess import Popen, PIPE
from urlparse import urlparse
import argparse


class RunCmd:
    def __init__(self):
        # type: (object) -> object
        self.cmd = ""
        self.rc = 0
        self.stdout = []
        self.stderr = []
        self.so_line_count=-1
        self.se_line_count=-1
        self.good_cmds=[]
        self.bad_cmds=[]

    def run(self,cmd):
        # type: () -> object
        # type: () -> object
        """Run a command
        :type cmd: object
        """
        if (len(cmd) > 0):
            self.cmd=cmd
            print("Running <cmd=%s>" % (self.cmd))

            p = Popen(self.cmd, shell=True, stdout=PIPE, stderr=PIPE)
            self.rc = p.wait()
            self.stdout, self.stderr = p.communicate()
            self.stdout = self.stdout.rstrip().split('\n')
            self.so_line_count=len(self.stdout)
            self.stderr = self.stderr.rstrip().split('\n')

            # Need to check for no output in stderr.
            #   If no output in stderr, there is one item in list that is null string
            if (self.stderr[0] == ""):
                self.se_line_count = 0;
                self.stderr = []
            else:
                self.se_line_count=len(self.stderr)
            if (self.rc == 0):
                self.good_cmds.append(cmd)
            else:
                self.bad_cmds.append(cmd)

        else:
            print("Comand string is empty")

    @property
    def get_cmd(self):
        # type: () -> object
        return self.cmd

    @property
    def get_rc(self):
        return self.rc

    @property
    def get_stdout(self):
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

    @property
    def num_words(self, str):
        return [len(str.split()) for sentence in mylist]

    def as_word_list(self, str):
        return str.split()

    def list_as_string(self,alist):
        # type: (object) -> object
        n=0
        retstr=""
        for item in alist:
            retstr+="{:>4}:<{}>\n".format(n,item)
            n+=1
        return retstr

    def dump_stdout(self):
        s=self.list_as_string(self.stdout)
        print("{}".format(s))

    def dump_stderr(self):
        s=self.list_as_string(self.stderr)
        print("{}".format(s))


def test1():
    c1 = RunCmd()
    c1.run("ls -l /home/kurtis")
    print("<rc={:d}> <so_num_lines={:d}> <se_num_lines={:d}>".format(c1.get_rc,c1.get_num_lines_stdout,c1.get_num_lines_stderr))
    print("\n>>> stdout >>>"); c1.dump_stdout(); print("<<< stdout <<<")
    print("\n>>> stderr >>>"); c1.dump_stderr(); print("<<< stderr <<<")
    return 0

def test2():
    c1 = RunCmd()
    c1.run("lxddd -l /home/kurtis")
    print("<rc={:d}> <so_num_lines={:d}> <se_num_lines={:d}>".format(c1.get_rc, c1.get_num_lines_stdout,
                                                                     c1.get_num_lines_stderr))
    print("\n>>> stdout >>>"); c1.dump_stdout(); print("<<< stdout <<<")
    print("\n>>> stderr >>>"); c1.dump_stderr(); print("<<< stderr <<<")

    # Iterate through stdout getting file name



    return(0);

def main():
    test1()
    test2()
    return(0);

if __name__ == "__main__":
    # execute only if run as a script
    main()
    exit(0)
