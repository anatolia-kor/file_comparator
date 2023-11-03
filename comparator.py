import os.path as pth
from os import getcwd, startfile, walk, system


class Comparator(object):
    def __init__(self, old_set_path, new_set_path, do_compare_size=False):
        self.old_set_path = old_set_path
        self.new_set_path = new_set_path
        self.new_files = dict()
        self.script_dir = getcwd()
        self.set_names = {'old_set_path': self.old_set_path,
                          'new_set_path': self.new_set_path}
        self.do_compare_size = do_compare_size
        self.bs = '\\'
        self.text_err = 'Cant parse your answer.'
        self.text_dialog_watch = 'Would you like to watch new files list? ("y" - yes, "n" - no)'
        self.text_dialog_open = 'Would you like to open some files? ("y" - yes, "n" - no)'
        self.text_file_open_instruction = ('To open file enter file number.\n'
                                           'To show file in catalog enter file number and "e".\n'
                                           'To finish opening files print "exit"\n')

    def __str__(self):
        return f'Comparator {self.old_set_path} with {self.new_set_path}'

    def __getitem__(self, item):
        return self.set_names[item]

    def file_namer(self, address, set_name, d_or_f):
        local_path = address.replace(self.script_dir + self[set_name], '')
        sep = self.bs
        path = f'{local_path}{sep}{str(d_or_f)}'
        return path + (str(pth.getsize(path)) if self.do_compare_size else '')

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
        print(f'Checking size of files is {"enabled" if self.do_compare_size else "disabled"}')
        new_files_set = new_set - old_set
        print(f'Difference contains {len(new_files_set)} files and directories')
        sorted_list = list(new_files_set)
        sorted_list.sort()
        self.new_files = dict(zip(range(1, len(sorted_list)+1), sorted_list))

    def dialog_watch(self):
        answer = input(self.text_dialog_watch)
        while not (answer == 'y' or answer == 'n'):
            answer = input(f'{self.text_err}\n{self.text_dialog_watch}')
        if answer == 'y':
            print('-----------new-files-list-----------')
            [print(i, 'elem: ', elem, end='\n') for i, elem in self.new_files.items()]
            print('------------------------------------')

    def dialog_open(self):
        answer = input(self.text_dialog_open)
        while not (answer == 'y' or answer == 'n'):
            answer = input(f'{self.text_err}\n{self.text_dialog_open}')
        if answer == 'n':
            return
        answer = input(self.text_file_open_instruction)
        while not answer == 'exit':
            if 'e' in answer:
                file_number = int(answer.replace('e', ''))
                if file_number in self.new_files.keys():
                    system(f'explorer.exe /select, {self.script_dir + self.new_set_path + self.new_files[file_number]}')
                else:
                    print(self.text_err)
            elif int(answer) in self.new_files.keys():
                startfile(self.script_dir + self.bs + self.new_set_path + self.new_files[int(answer)])
            else:
                print(self.text_err)
            answer = input(self.text_file_open_instruction)
