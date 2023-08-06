import shutil


def tqdm_ncols(maxwidth: int = 80):
    """
    Overview:
        Get number of columns in terminal for tqdm.

    :param maxwidth: Max column widths.
    :return: Number of columns for tqdm's ``ncols`` argument.

    Examples::
        >>> from igm.utils import tqdm_ncols
        >>> tqdm_ncols()
        80
        >>> tqdm_ncols(40)
        40
    """
    width, _ = shutil.get_terminal_size()
    return min(maxwidth, width)
