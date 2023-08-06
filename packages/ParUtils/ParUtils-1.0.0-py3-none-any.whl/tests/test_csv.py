import parutils as u

IN1_PATH = 'tests/files/in1.csv'
OUT_PATH = 'tests/files/out.csv'


def test_csv():

    d = u.get_csv_fields_dict(IN1_PATH)
    assert d == {'ID': 0, 'NAME': 1}

    s = u.csv_clean('FIELD1;\n')
    assert s == 'FIELD1'

    e_ref = u.csv.E_WRONG_TYPE_LIST
    u.ttry(u.save_csv, e_ref, ['1'], OUT_PATH)


if __name__ == '__main__':
    test_csv()
