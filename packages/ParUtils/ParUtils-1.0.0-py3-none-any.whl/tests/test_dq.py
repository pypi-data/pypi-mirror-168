import parutils as u
from tests import test_0

FILES_DIR = 'tests/files/'
OUT_DIR = test_0.TESTS_OUT_DIR
DUP_IN = FILES_DIR + 'dup_in.csv'
DUP_OUT = OUT_DIR + '/out_dup.csv'
DUP_OUT_REF = FILES_DIR + 'dup_out_ref.csv'
IN_1 = FILES_DIR + 'in1.csv'
IN_2 = FILES_DIR + 'in2.csv'


def test_dq():

    logger = u.Logger('TEST_DQ', True)
    u.log_print("Test toolDup - find_dup_list", dashes=100)
    list_in = u.load_csv(DUP_IN)
    dup_list = u.find_dup_list(list_in)
    u.log_example(dup_list)
    u.save_csv(dup_list, DUP_OUT)
    u.file_match(DUP_OUT, DUP_OUT_REF, del_dup=True)
    u.diff_list(['1'], ['2'])

    e_ref = "Files don't match"
    u.ttry(u.file_match, e_ref, IN_1, IN_2)

    assert u.find_dup_list([]) == []
    assert u.del_dup_list([]) == []
    logger.close()


if __name__ == '__main__':
    u.logging.const.DEFAULT_DIR = test_0.TESTS_LOG_DIR
    u.dq.OUT_DIR = test_0.TESTS_OUT_DIR

    test_dq()
