import comparator


def work_comparator():
    comp = comparator.Comparator()
    comp.work()


def test_comparator_dont_fill_paths():
    comp = comparator.Comparator()
    comp.old_set_path = '\\test_sets\\test_set_old'
    comp.new_set_path = '\\test_sets\\test_set_new'
    comp.do_compare_size = True
    # comp.compare()
    comp.work()


if __name__ == '__main__':
    test_comparator_dont_fill_paths()
