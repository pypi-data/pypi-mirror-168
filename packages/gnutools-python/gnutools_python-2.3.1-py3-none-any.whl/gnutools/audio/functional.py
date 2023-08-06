import numpy as np
import datetime


def name_it(id, start, stop):
    """
    Automatically name a sound file with respect to (start, stop) slice audio

    :param id:
    :param start:
    :param stop:
    :return string:
    """
    return "{}_{}_{}_{}".format(id,
                                int(start * pow(10, 6)),
                                int(stop * pow(10, 6)),
                                int(stop - start))

def timedelta(string):
    """

    :param string:
    :return:
    """
    splits = np.array(string.split(":"), dtype=int)
    return datetime.timedelta(hours=int(splits[0]), minutes=int(splits[1]), seconds=int(splits[2]))

