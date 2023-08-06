from .core import logger_methode


@logger_methode
def log(*args, level=0, c_out=True):
    """Logs 'str_in' in the current log file (log_path)

    - level: log level. Current log level is the attribute level of the current logger.
    You can get the current loger by using the get_logger function. Nothing is logged if logger level < level
    - c_out: specifies if something should be printed in the console or not
    """


@logger_methode
def log_print(*args, level=0, c_out=True, nb_tab=0, dashes=0):
    """Prints something in the current log file (log_path)

    - level: log level. Current log level is the attribute level of the current logger.
    You can get the current loger by using the get_logger function. Nothing is logged if logger level < level
    - c_out: specifies if something should be printed in the console or not
    - nb_tab: number of tab indentations
    - dashes: total length of the input string extended with dashes ('-')
    """


def log_input(str_in):
    """Same as input but traced in the log file"""

    log_print(str_in, c_out=False)
    command = input(str_in + '\n')
    log_print(command, c_out=False)
    return command


def log_array(array, nb_tab=0):
    for elt in array:
        log_print(elt, nb_tab=nb_tab)


def log_dict(dict, nb_tab=0):
    for key in dict:
        log_print(f'{key}: {dict[key]}', nb_tab=nb_tab)


def log_example(list_in, what="duplicates", n_print=5):
    if not list_in:
        return

    log_print(f"Examples of {what} (limited to {n_print}):")
    log_array(list_in[:n_print])
