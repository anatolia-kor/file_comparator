import comparator


def work_comparator():
    comp = comparator.Comparator()
    comp.work()


def test_comparator_dont_fill_paths():
    comp = comparator.Comparator()
    comp.old_set_path = ''
    comp.new_set_path = ''
    comp.do_compare_size = True
    comp.work()


if __name__ == '__main__':
    work_comparator()
