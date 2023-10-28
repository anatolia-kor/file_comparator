import os
import os.path as pth
import sys
from os import getcwd


class ComparedString(str):

    def __init__(self, text):
        self.text = sys.intern(text)

    def __hash__(self) -> int:
        return hash(self.text)

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other) -> bool:
        return self.text == other.text


class Comparator(object):
    def __init__(self, old_set_path, new_set_path, compare_size=False):
        self.old_set_path = old_set_path
        self.new_set_path = new_set_path
        self.set_names = {'old_set_path': self.old_set_path,
                          'new_set_path': self.new_set_path}
        self.compare_size = compare_size

    def __str__(self):
        return f'Comparator {self.old_set_path} with {self.new_set_path}'

    def __getitem__(self, item):
        return self.set_names[item]

    def file_namer(self, address, d_or_f):
        f_path = f'{str(address)}\\{str(d_or_f)}'
        return f_path + (str(pth.getsize(f_path)) if self.compare_size else '')

    def set_by_path(self, set_name):
        abs_path_os = pth.abspath(getcwd() + self[set_name])
        file_sys_gen = os.walk(abs_path_os)
        cur_set = set()
        for address, dirs, files in file_sys_gen:
            [cur_set.add(self.file_namer(address, d)) for d in dirs]
            [cur_set.add(self.file_namer(address, f)) for f in files]
        return cur_set

    def compare(self):
        old_set = self.set_by_path('old_set_path')
        print(f'Old set is {len(old_set)} size')
        new_set = self.set_by_path('new_set_path')
        print(f'New set is {len(new_set)} size')
        print(f'Checking size of files is {"enabled" if self.compare_size else "disabled"}')
        new_files_set = new_set - old_set
        answer = input(f'Would you like to watch new files? ("y" - yes, "n" - no)')
        while not (answer == 'y' or answer == 'n'):
            answer = input(f'Cant parse your answer. Would you like to watch new files? ("y" - yes, "n" - no)')
        if answer == 'y':
            sorted_list = list(new_files_set)
            sorted_list.sort()
            [print(i, sep='\n') for i in sorted_list]






