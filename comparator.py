import os.path as pth
from os import getcwd, startfile, walk
from easygui import fileopenbox


class Comparator(object):
    def __init__(self, old_set_path, new_set_path, compare_size=False):
        self.old_set_path = old_set_path
        self.new_set_path = new_set_path
        self.new_files = dict()
        self.script_dir = getcwd()
        self.set_names = {'old_set_path': self.old_set_path,
                          'new_set_path': self.new_set_path}
        self.compare_size = compare_size

    def __str__(self):
        return f'Comparator {self.old_set_path} with {self.new_set_path}'

    def __getitem__(self, item):
        return self.set_names[item]

    def file_namer(self, address, set_name, d_or_f):
        local_path = address.replace(self.script_dir + self[set_name], '')
        sep = '\\'
        path = f'{local_path}{sep}{str(d_or_f)}'
        return path + (str(pth.getsize(path)) if self.compare_size else '')

    def set_by_path(self, set_name):
        abs_path_os = pth.abspath(self.script_dir + self[set_name])
        file_sys_gen = walk(abs_path_os)
        cur_set = set()
        for address, dirs, files in file_sys_gen:
            [cur_set.add(self.file_namer(address, set_name, d)) for d in dirs]
            [cur_set.add(self.file_namer(address, set_name, f)) for f in files]
        return cur_set

    def compare(self):
        old_set = self.set_by_path('old_set_path')
        print(f'Old set contains {len(old_set)} files and directories')
        new_set = self.set_by_path('new_set_path')
        print(f'New set contains {len(new_set)} files and directories')
        print(f'Checking size of files is {"enabled" if self.compare_size else "disabled"}')
        new_files_set = new_set - old_set
        print(f'Difference contains {len(new_files_set)} files and directories')
        sorted_list = list(new_files_set)
        sorted_list.sort()
        self.new_files = dict(zip(range(1, len(sorted_list)+1), sorted_list))

    def dialog_watch(self):
        answer = input('Would you like to watch new files list? ("y" - yes, "n" - no)')
        while not (answer == 'y' or answer == 'n'):
            answer = input('Cant parse your answer. Would you like to watch new files list? ("y" - yes, "n" - no)')
        if answer == 'y':
            print('-----------new-files-list-----------')
            [print(i, 'elem: ', elem, end='\n') for i, elem in self.new_files.items()]
            print('------------------------------------')

    def dialog_open(self):
        answer = input('Would you like to open some files? ("y" - yes, "n" - no)')
        while not (answer == 'y' or answer == 'n'):
            answer = input('Cant parse your answer. Would you like to open some files? ("y" - yes, "n" - no)')
        if answer == 'n':
            return
        answer = input('To open file enter file number.\n'
                       'To show file in catalog enter file number and "e".\n'
                       'To finish opening files print "exit"\n')
        while not answer == 'exit':
            if int(answer) in self.new_files.keys():
                startfile(self.script_dir + '\\' + self.new_set_path + self.new_files[int(answer)])
            elif int(answer.replace('e', '')) in self.new_files.keys():
                fileopenbox(self.script_dir + '\\' + self.new_set_path + self.new_files[int(answer)])
            answer = input('To open file enter file number. To finish opening files print "exit"')
