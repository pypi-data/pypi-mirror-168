import parutils as u


def test_msc():
    lst = ['key1=value1', 'key2=value2']
    out = u.list_to_dict(lst)

    d = {'key1': 'value1', 'key2': 'value2'}
    assert out == d

    out = u.replace_from_dict('Hello @@VAR@@', {'VAR': 'world'})
    assert out == 'Hello world'


if __name__ == '__main__':
    test_msc()
