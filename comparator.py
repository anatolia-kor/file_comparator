import os.path as pth
from os import getcwd, startfile, walk, system
from easygui import diropenbox
from sys import stdout


class Exit(Exception):
    def __init__(self, variable_set_expected=None):
        if variable_set_expected is not None:
            self.txt = f'You must set {variable_set_expected}.\n'
            stdout.write(self.txt)
        stdout.write('Good bye!')


class Comparator(object):
    def __init__(self, old_set_path=None, new_set_path=None, do_compare_size=None):
        self.global_answer = ''
        self.old_set_path = old_set_path
        self.new_set_path = new_set_path
        self.do_compare_size = do_compare_size
        self.new_files = dict()
        self.script_dir = getcwd()
        self.set_names = {'old_set_path': self.old_set_path,
                          'new_set_path': self.new_set_path}
        self.bs = '\\'
        self.text_commands_instruction = ('---------------Command-menu---------------\n'
                                          'To choose directories to compare enter "choose"\n'
                                          'To compare directories enter "compare"\n'
                                          'To watch file list enter "watch"\n'
                                          'To open files enter "open"\n'
                                          'To copy files to new directory enter "copy"\n'
                                          'To exit the program enter "exit!"\n'
                                          '------------------------------------------\n')
        self.text_err = 'Cant parse your answer.\n'
        self.text_dir_err = 'First you must choose directories to compare.\n'
        self.text_choose_old_dir = 'Choose old directory to compare.\n'
        self.text_choose_new_dir = 'Choose new directory to compare.\n'
        self.text_choose_dirs = ('You will be asking to choose directories to compare.\n'
                                 'Would you like to proceed? ("y" - yes, "n" - no)\n')
        self.text_compare = 'Would you like to compare files? ("y" - yes, "n" - no)\n'
        self.text_dialog_watch = 'Would you like to watch new files list? ("y" - yes, "n" - no)\n'
        self.text_dialog_open = 'Would you like to open some files? ("y" - yes, "n" - no)\n'
        self.text_do_compare_size = 'Would you like to compare files by its size? ("y" - yes, "n" - no)\n'
        self.text_file_open_instruction = ('To open file enter file number.\n'
                                           'To show file in catalog enter file number and "e".\n'
                                           'To finish opening files print "exit"\n')
        self.text_names = {'text_err': self.text_err,
                           'text_choose_dirs': self.text_choose_dirs,
                           'text_compare': self.text_compare,
                           'text_dialog_watch': self.text_dialog_watch,
                           'text_dialog_open': self.text_dialog_open,
                           'text_do_compare_size': self.text_do_compare_size,
                           'text_file_open_instruction': self.text_file_open_instruction}

    def __str__(self):
        return f'Comparator {self.old_set_path} with {self.new_set_path}'

    def __getitem__(self, item):
        if 'path' in item:
            return self.set_names[item]
        elif 'text' in item:
            return self.text_names[item]

    def work(self):
        self.global_answer = ''
        while not self.global_answer == 'exit!':
            self.global_answer = input(self.text_commands_instruction)
            match self.global_answer:
                case 'choose':
                    self.old_set_path, self.new_set_path, do_compare_size = None, None, None
                    self.choose()
                case 'compare':
                    self.compare()
                case 'watch':
                    self.watch()
                case 'open':
                    self.open()
                case 'copy':
                    self.copy()
                case 'exit!':
                    pass
                case _:
                    stdout.write(self.text_err)
        self.exit()

    def exit(self):
        self.global_answer = 'exit!'

    def choose(self):
        if self.old_set_path is None or self.new_set_path is None:
            answer = self.asker('text_choose_dirs')
            if answer == 'n':
                return
        while self.old_set_path is None:
            stdout.write(self.text_choose_old_dir)
            self.old_set_path = diropenbox(title=self.text_choose_old_dir)
        self.old_set_path.replace(self.script_dir, '')
        while self.new_set_path is None:
            stdout.write(self.text_choose_new_dir)
            self.new_set_path = diropenbox(title=self.text_choose_new_dir)
        self.new_set_path.replace(self.script_dir, '')
        if self.do_compare_size is None:
            answer = self.asker('text_do_compare_size')
            self.do_compare_size = answer == 'y'
        print(f'Checking size of files is {"enabled" if self.do_compare_size else "disabled"}')

    def asker(self, text_name):
        answer = input(self[text_name])
        while not (answer == 'y' or answer == 'n' or answer == 'exit!'):
            if answer == 'exit!':
                self.global_answer = 'exit!'
                return answer
            answer = input(f'{self.text_err}{self[text_name]}')
        return answer

    def file_namer(self, address, set_name, d_or_f):
        local_path = address.replace(self.script_dir + self[set_name], '')
        path = f'{local_path}{self.bs}{str(d_or_f)}'
        if self.do_compare_size:
            path += ' {***} ' + str(pth.getsize(self.script_dir + self[set_name] + path))
        return path

    def set_by_path(self, set_name):
        abs_path_os = pth.abspath(self.script_dir + self[set_name])
        file_sys_gen = walk(abs_path_os)
        cur_set = set()
        counter = 0
        for address, dirs, files in file_sys_gen:
            stdout.flush()

            stdout.write(f'Fetching {counter} catalogs and files')
            [cur_set.add(self.file_namer(address, set_name, d)) for d in dirs]
            [cur_set.add(self.file_namer(address, set_name, f)) for f in files]
            counter += 1
        return cur_set

    def compare(self):
        if self.old_set_path is None or self.new_set_path is None or self.do_compare_size is None:
            stdout.write(self.text_dir_err)
            return
        answer = self.asker('text_compare')
        if answer != 'y':
            return
        self.new_files = dict()
        old_set = self.set_by_path('old_set_path')
        print(f'Old set contains {len(old_set)} files and directories')
        new_set = self.set_by_path('new_set_path')
        print(f'New set contains {len(new_set)} files and directories')
        new_files_set = new_set - old_set
        print(f'Difference contains {len(new_files_set)} files and directories')
        sorted_list = list(new_files_set)
        sorted_list.sort()
        self.new_files = dict(zip(range(1, len(sorted_list)+1), sorted_list))

    def watch(self):
        answer = self.asker('text_dialog_watch')
        if answer == 'y':
            print('-----------new-files-list-----------')
            [print(i, 'elem: ', elem, end='\n') for i, elem in self.new_files.items()]
            print('------------------------------------')

    def open(self):
        answer = self.asker('text_dialog_open')
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

    def copy(self):
        pass
