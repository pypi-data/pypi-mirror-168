from . import file

SEPARATOR = ';'
E_WRONG_TYPE_LIST = "List elements must be of type list (if you want to save a list of strings, please use the save_list function)"


def get_csv_fields_dict(in_path):
    """Returns a dictionary whose keys are the csv fields of the 'in_path' file
    and elements are the columns index.
    """

    fields = {}
    line_list = get_header(in_path, True)
    for i, elt in enumerate(line_list):
        fields[elt] = i

    return fields


def load_csv(in_path):
    """Loads a csv file and returns a list whose elements correspond to the
    lines of the 'in_path' file.
    Each element is also a list whose elements correspond to the csv fields.
    """

    out_list = []
    with open(in_path, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            line_list = csv_to_list(line)
            out_list.append(line_list)

    return out_list


def csv_to_list(line_in):
    """Converts a csv line to a list using SEPARATOR as separator"""

    return line_in.strip('\n').split(SEPARATOR)


def save_csv(array_in, out_path, mode='w'):
    """Saves a list to a csv file

    - mode: mode for the open methode.
    """
    import os.path as p

    file.mkdirs(p.dirname(out_path))
    with open(out_path, mode, encoding='utf-8') as out_file:
        for row in array_in:
            write_csv_line(row, out_file)


def write_csv_line(row, out_file):
    """Writes a line to a csv file

    - row: has to be a list
    """

    if not isinstance(row, list):
        raise Exception(E_WRONG_TYPE_LIST)
    else:
        line_out = SEPARATOR.join(row)
    line_out += '\n'
    out_file.write(line_out)


def csv_clean(s):
    """Cleans a csv field by removing csv separators and new line characters"""

    out = s.replace('\r', '')
    out = out.replace('\n', '')
    out = out.replace(SEPARATOR, '')
    return out


def get_header(in_path, csv=False):
    """Returns the header of a file

    - csv: if True, the returned header is a list containing each csv field
    """
    with open(in_path, 'r', encoding='utf-8') as in_file:
        header = in_file.readline().strip('\n')

    if csv:
        header = csv_to_list(header)

    return header
