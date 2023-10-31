import comparator


def test_comparator():
    # experiment 1
    # set_a = set([f'abc\\'])
    # set_b = set([f'abc\\', f'bca\\'])
    # set_c = set_b - set_a
    # print('Experiment 1 ', set_c)
    #
    # experiment 2
    # per1 = f'D:\\_python\\_projects\\file_comparator\\test_sets\\test_set_new1\\Новая папка'
    # per2 = 'bca'
    # per3 = f'D:\\_python\\_projects\\file_comparator\\test_sets\\test_set_new1'
    # per4 = f'\\Новая папка'
    # per5 = per3 + per4
    # set_a = set()
    # set_a.add(per1)
    # set_b = set()
    # set_b.add(per3)
    # set_b.add(per5)
    # set_c = set_b - set_a
    # print('Experiment 2 ', set_c)


    comp = comparator.Comparator('\\test_sets\\test_set_old', '\\test_sets\\test_set_new')
    print(comp)
    comp.compare()


if __name__ == '__main__':
    test_comparator()
