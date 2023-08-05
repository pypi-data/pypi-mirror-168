#!/usr/bin/python3
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
"""Compressed file iterator module and sample code.

Example code to create an iterator (for use in a for-loop). Uses a JSON
configuration file to define known extensions and appropriate handling
program and required options. (A default handler, such as 'cat' on *nix
systems, MUST be defined.) File contents are returned line by line,
WITH CR/LF CHARACTERS ('\r' and '\n') STRIPPED.

For testing (os.name = 'posix' ONLY), module will generate a basic
configuration file ('foo.json') defining only a default handler ('/bin/cat')
and 'numbers.txt' (a text file containing the numbers 1 to 50_000 in order,
each on a single line).
"""

# Subprocess code based on:
#     https://stackoverflow.com/questions/11728915/python-iterate-on-subprocess-popen-stdout-stderr

# import async
# import collections
import collections.abc
# from configparser import ConfigParser, ExtendedInterpolation
import json
import os
# import os.path
import pathlib
import pprint
import subprocess
# import sys


def left_join(strings: list[str]):
    """
    Joins together an list of strings, returning as a single string.

    (Thanks to the members of #python on Libera.Chat for this
    function's base code.)

    Args:
        strings: List of strings

    Yields:
        acc: String
    """
    acc = ""
    for s in strings:
        acc = s + acc
        yield acc


def flatten(x):
    """
    Merge possibly multi-level lists into a single list.

    (Thanks to the members of #python on Libera.Chat for this
    function's base code.)

    Args:
        x: List of strings and/or lists

    Returns:
        result: List
    """
    result = []
    for el in x:
        if isinstance(x, collections.abc.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

# print(flatten(["junk",["nested stuff"],[],[[]]]))


class Shell:
    """
    Run a command as a subprocess and iterate over the stdout/stderr lines.
    """

    def __init__(self, args, cwd="./"):
        """
        Initialize the object by creating an appropriate subprocess.

        Args:
            args: List consisting of the subprocess executable at
                index 0, executable options at indicies [1 .. (n-1)],
                and file name at index n.
            cwd: Current working directory for subprocess
                (default: current directory ("./")).
        """
        self.args = args

        self.pro_cess = subprocess.Popen(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.line = ""
        self.code = ""

    def __iter__(self):
        """
        Returns the iterator object itself. Required for the iterator protocol.

        Returns:
            self: Object
        """
        return self

    def __next__(self):
        """
        Returns the next item from the iterator. Required for the iterator
        protocol.

        Returns:
            self.line: String (with CRs/LFs stripped)

        Raises:
            StopIteration: Program has ended (self.code is None) and
                subprocess pipe is empty.
        """
        self.line = self.pro_cess.stdout.readline()
        self.code = self.pro_cess.poll()

        do_it_001 = False
        # do_it_001 = True
        if do_it_001:
            print("self.code = ")
            pprint.pprint(self.code)
            print("self.line = ")
            pprint.pprint(self.line)

        if len(self.line) == 0 or self.code is not None:
            if len(self.line) == 0:
                raise StopIteration
        return str(self.line, encoding="utf-8").rstrip("\r\n")


class MyFile:
    """
    Open a file and iterate over the lines. (UNUSED)
    """

    def __init__(self, args, cwd="./"):
        """
        Initialize the object by opening a file.

        Args:
            args: List consisting of the file name at index 0.
            cwd: Current working directory (UNUSED)
                (default: current directory ("./")).
        """
        self.args = args
        self.cwd = cwd
        self.fn = args[0]
        self.fh = open(self.fn, "r", encoding="utf-8")
        self.line = ""

    def __iter__(self):
        """
        Returns the iterator object itself. Required for the iterator protocol.

        Returns:
            self: Object
        """
        return self

    def __next__(self):
        """
        Returns the next item from the iterator. Required for the iterator
        protocol.

        Returns:
            self.line: String (with CRs/LFs stripped)

        Raises:
            StopIteration: Program has ended (self.code is None) and
                subprocess pipe is empty.
        """
        if self.fh.closed() is True:
            raise StopIteration

        if self.fh.readable():
            self.line = self.fh.readline()

        if self.line == "":
            raise StopIteration
        return str(self.line).rstrip("\r\n")

    def __del__(self):
        """
        Close file before object destruction.
        """
        self.fh.close()


class MyIterator:
    """
    Hide use of 'Shell' or 'MyFile' classes behind a common interface.
    """

    def __init__(self, args, cwd="./",
                 config_file='compressed_file_iterator.json',
                 case_sensitive=True,
                 ):
        """
        Determining the configuration to use and creates an appropriate object.

        Args:
            args: List consisting of the file name at index 0.
            cwd: Current working directory for subprocess
                (default: current directory ("./")).
            case_sensitive: Should comparison of file extension to 
                configurations be case sensitive? (default: True)
        """
        self.args = args
        self.args = args
        self.cwd = cwd
        self.case_sensitive = case_sensitive

        config = {}
        config_cf = {}
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)

        for k in config.keys():
            config_cf[k.casefold()] = {}
            config_cf[k.casefold()] = config[k]

        suffix = pathlib.Path(args[0]).suffixes
        suffix_len = len(suffix)

        suffix_str = []
        suffix_str_cf = []
        for i in range(suffix_len):
            suffix_str.append("")
            suffix_str_cf.append("")
            for j in range(i, suffix_len):
                suffix_str[i] += suffix[j]
                suffix_str_cf[i] += suffix[j].casefold()

        # # foo = ['as', 'df', 'gh', 'jk']
        # # print(list(left_join(reversed(foo))))
        suffix_str = list(reversed(list(left_join(reversed(suffix)))))
        for i in range(suffix_len):
            suffix_str_cf[i] = suffix_str[i].casefold()

        my_os = os.name
        my_args = list()
        for i in range(len(suffix_str)):
            flag = suffix_str[i] in config
            if not self.case_sensitive:
                flag = suffix_str_cf[i] in config_cf

            if flag:
                if not self.case_sensitive:
                    print(suffix_str[i], " matches")
                    my_args = flatten(
                        (
                            config_cf[suffix_str_cf[i]]["base_command"][my_os],
                            config_cf[suffix_str_cf[i]]["base_options"][my_os],
                            args[0],
                        )
                    )
                else:
                    print(suffix_str[i], " matches")
                    my_args = flatten(
                        (
                            config[suffix_str[i]]["base_command"][my_os],
                            config[suffix_str[i]]["base_options"][my_os],
                            args[0],
                        )
                    )
                break
        else:
            print("Using default configuration")
            my_args = flatten(
                (
                    config[".*"]["base_command"][my_os],
                    config[".*"]["base_options"][my_os],
                    args[0],
                )
            )

        self.mi = None

        self.mi = Shell(my_args)

        # if 'gz' in args[0]:
        #     self.mi = Shell(args)
        # else:
        #     self.mi = MyFile(args)

    def __iter__(self):
        """
        Returns the iterator object itself. Required for the iterator protocol.

        Returns:
            self: Object
        """
        return self.mi

    def __next__(self):
        """
        Returns the next item from the iterator. Required for the iterator
        protocol.

        Returns:
            self.line: String (with CRs/LFs stripped)

        Raises:
            StopIteration: Program has ended (self.code is None) and
                subprocess pipe is empty, or end of file is reached.
        """
        line = self.__next__()
        if line == "":
            raise StopIteration
        return line


def main():
    """
    Basic testing routine.
    """

    if not os.path.exists('numbers.txt'):
        with open('numbers.txt', 'w', encoding='utf-8', ) as file:
            for i in range(1, 10001):
                file.write(str(i) + "\n")
    if not os.path.exists('foo.json'):
        dictionary = {
                '.*': {
                    'base_command': {
                        'posix': '/bin/cat',
                        },
                    'base_options': {
                        'posix': [],
                        },
                    'type': 'Plain',
                    },
                }
        json_object = json.dumps(dictionary, indent=4)
        with open('foo.json', 'w', encoding='utf-8', ) as file:
            file.write(json_object)

    tests = [
        (False, "numbers.7z"),
        (False, "numbers.zip"),
        (False, "numbers.tar"),
        (False, "numbers.tar.Z"),
        (False, "numbers.tar.bz2"),
        (False, "numbers.tar.gz"),
        (False, "numbers.tar.lz"),
        (False, "numbers.tar.lzma"),
        (False, "numbers.tar.lzo"),
        (False, "numbers.tar.xz"),
        (False, "numbers.tar.zst"),
        (True,  "numbers.txt"),
        (False, "numbers.txt.Z"),
        (False, "numbers.txt.bz2"),
        (False, "numbers.txt.gz"),
        (False, "numbers.txt.lz"),
        (False, "numbers.txt.lz4"),
        (False, "numbers.txt.lzma"),
        (False, "numbers.txt.lzo"),
        (False, "numbers.txt.xz"),
        (False, "numbers.txt.zst"),
    ]
    for go, fn in tests:
        if go:
            args = [fn, ]
            # shell = MyIterator(args,
            #                    config_file='foo.json',
            #                    case_sensitive=False,
            #                    )
            shell = MyIterator(args, config_file='foo.json',)
            if shell is not None:
                c = 0
                for line in shell:
                    if len(line):
                        c = c + int(line)
                print(fn, ": ", c)


if __name__ == "__main__":
    main()
