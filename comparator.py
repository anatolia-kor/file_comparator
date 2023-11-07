import os.path as pth
from os import getcwd, startfile, walk, system

from easygui import diropenbox

import comparator_texts as ct


class Comparator(object):
    def __init__(self):
        self.global_answer = ''
        self.old_set_path = None
        self.new_set_path = None
        self.do_compare_size = None
        self.new_files = dict()
        self.script_dir = getcwd()
        self.bs = '\\'
        self.size_sep = ' {***} '
        self.texts = dict()
        self.text_names = {key: eval(f'ct.{key}') for key in dir(ct) if not key.startswith('__')}

    def __str__(self):
        return f'Comparator {self.old_set_path} with {self.new_set_path}'

    def __getitem__(self, item):
        if 'text' in item:
            return self.text_names[item]
        else:
            return self.__dict__[item]

    def work(self) -> None:
        self.global_answer = ''
        while not self.global_answer == 'exit!':
            self.global_answer = input(self.text_names['text_commands_instruction'])
            match self.global_answer:
                case 'choose':
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
                    print(self.text_names['text_gb'])
                case _:
                    print(self.text_names['text_err'])

    def ex_input(self, text) -> str:
        try:
            answer = input(text)
            if answer == 'exit!':
                raise Exit(self)
            return answer
        except Exit:
            return 'n'

    def asker(self, text_name) -> str:
        answer = self.ex_input(self[text_name])
        while not (answer == 'y' or answer == 'n'):
            answer = self.ex_input(f'{self.text_names["text_err"]}{self[text_name]}')
        return answer

    def file_namer(self, address, set_name, d_or_f) -> str:
        local_path = address.replace(self.script_dir + self[set_name], '')
        path = f'{local_path}{self.bs}{str(d_or_f)}'
        if self.do_compare_size:
            path += self.size_sep + str(pth.getsize(self.script_dir + self[set_name] + path))
        return path

    def set_by_path(self, set_name) -> set:
        abs_path_os = pth.abspath(self.script_dir + self[set_name])
        file_sys_gen = walk(abs_path_os)
        cur_set = set()
        print(self.text_names['text_fetching'])
        for address, dirs, files in file_sys_gen:
            [cur_set.add(self.file_namer(address, set_name, d)) for d in dirs]
            [cur_set.add(self.file_namer(address, set_name, f)) for f in files]
        return cur_set

    def choose(self) -> None:
        self.old_set_path, self.new_set_path, self.do_compare_size, self.new_files = None, None, None, dict()
        answer = self.asker('text_choose_dirs')
        if answer == 'n':
            return
        while self.old_set_path is None:
            print(self.text_names['text_choose_old_dir'])
            self.old_set_path = diropenbox(title=self.text_names['text_choose_old_dir'])
        self.old_set_path = self.old_set_path.replace(self.script_dir, '')
        while self.new_set_path is None:
            print(self.text_names['text_choose_new_dir'])
            self.new_set_path = diropenbox(title=self.text_names['text_choose_new_dir'])
        self.new_set_path = self.new_set_path.replace(self.script_dir, '')
        answer = self.asker('text_do_compare_size')
        self.do_compare_size = answer == 'y'
        print(self.text_names['text_size_check_alarm'].format('enabled' if self.do_compare_size else 'disabled'))

    def compare(self) -> None:
        if self.old_set_path is None or self.new_set_path is None or self.do_compare_size is None:
            print(self.text_names['text_dir_err'])
            return
        answer = self.asker('text_compare')
        if answer != 'y':
            return
        self.new_files = dict()
        old_set = self.set_by_path('old_set_path')
        print(self.text_names['text_old_set_alarm'].format(len(old_set)))
        new_set = self.set_by_path('new_set_path')
        print(self.text_names['text_new_set_alarm'].format(len(new_set)))
        new_files_set = new_set - old_set
        print(self.text_names['text_sets_diff_alarm'].format(len(new_files_set)))
        sorted_list = list(new_files_set)
        sorted_list.sort()
        self.new_files = dict(zip(range(1, len(sorted_list)+1), sorted_list))

    def watch(self) -> None:
        if len(self.new_files) == 0:
            print(self.text_names['text_havent_new_files'])
            return
        answer = self.asker('text_dialog_watch')
        if answer == 'n':
            return
        print(self.text_names['text_new_files_list_open'])
        [print(f'{i} elem: {elem}') for i, elem in self.new_files.items()]
        print(self.text_names['text_new_files_list_close'])

    def open(self) -> None:
        if len(self.new_files) == 0:
            print(self.text_names['text_havent_new_files'])
            return
        answer = self.asker('text_dialog_open')
        if answer == 'n':
            return
        answer = self.ex_input(self.text_names['text_file_open_instruction'])
        while not (answer == 'exit' or self.global_answer == 'exit!'):
            if answer.endswith('e') and answer.replace('e', '').isdigit():
                file_number = int(answer.replace('e', ''))
                if file_number in self.new_files.keys():
                    system(f'explorer.exe /select, {self.script_dir + self.new_set_path + self.new_files[file_number]}')
                else:
                    print(self.text_names['text_open_file_err'].format(file_number))
            elif answer.isdigit():
                file_number = int(answer)
                if file_number in self.new_files.keys():
                    startfile(self.script_dir + self.bs + self.new_set_path + self.new_files[int(answer)])
                else:
                    print(self.text_names['text_open_file_err'].format(file_number))
            else:
                print(self.text_names['text_open_file_err'].format(answer))
            answer = self.ex_input(self.text_names['text_file_open_instruction'])

    def copy(self):
        pass


class Exit(Exception):
    def __init__(self, comp: Comparator):
        comp.global_answer = 'exit!'
        print(ct.text_gb)
