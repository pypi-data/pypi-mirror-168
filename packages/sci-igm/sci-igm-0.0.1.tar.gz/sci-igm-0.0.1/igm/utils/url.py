import mimetypes
import os.path
from typing import Optional
from urllib.parse import urlparse, unquote

from .file import get_file_ext, splitext


def get_url_filename(url: str, content_type: Optional[str] = None) -> str:
    """
    Overview:
        Get filename from ``url`` and ``content_type``.

    :param url: Original url.
    :param content_type: Content-Type information from remote.
    :return: Filename with correct extension name.

    Examples::
        >>> from igm.utils import get_url_filename
        >>> get_url_filename('http://mysite.com/files/filename.csv')
        'filename.csv'
        >>> get_url_filename('http://mysite.com/files/filename', 'application/pdf')
        'filename.pdf'
        >>> get_url_filename('http://mysite.com/files/filename.csv', 'application/pdf')
        'filename.csv'
    """
    url_parsed = urlparse(url)
    filename = os.path.basename(unquote(url_parsed.path))
    _, ext = splitext(filename)
    if content_type and not ext:
        actual_ext = mimetypes.guess_extension(content_type)
        if actual_ext and not os.path.normcase(filename).endswith(actual_ext):
            filename = f'{filename}{actual_ext}'

    return filename


def get_url_ext(url: str, content_type: Optional[str] = None) -> str:
    """
    Overview:
        Get extension of url, based on url filename and content type.

    :param url: Original url.
    :param content_type: Content-Type information from remote.
    :return: File extension, including ``.tar.gz``.

    Examples::
        >>> from igm.utils import get_url_ext
        >>> get_url_ext('http://mysite.com/files/filename.csv')
        '.csv'
        >>> get_url_ext('http://mysite.com/files/filename', 'application/pdf')
        '.pdf'
        >>> get_url_ext('http://mysite.com/files/filename.tar.gz')
        '.tar.gz'
    """
    filename = get_url_filename(url, content_type)
    return get_file_ext(filename)
