from contextlib import contextmanager
from typing import Mapping, ContextManager, Callable, Tuple, Optional

from igm.env.inquire import user_inq_with


@contextmanager
def with_user_inquire(v: Mapping) -> ContextManager:
    """
    Overview:
        Hang the user inquire information up for templating.

    :param v: New user inquire information.

    Examples::
        >>> from igm.env import user
        >>> user
        UserInquire({})
        >>>
        >>> from igm.conf.inquire import with_user_inquire
        >>> with with_user_inquire({'a': 1, 'b': 'hansbug'}):
        ...     user
        ...
        UserInquire({'a': 1, 'b': 'hansbug'})
        >>>
        >>> user
        UserInquire({})
    """
    with user_inq_with(v):
        yield


class InquireCancel(Exception):
    pass


class InquireRestart(Exception):
    pass


def _add_end(s: str) -> str:
    return s if s.endswith('.') else f'{s}.'


def inquire_call(inquire_func: Callable[[], Mapping]) -> Tuple[bool, Optional[Mapping]]:
    """
    Overview:
        Inquire call for given function.

    :param inquire_func:
    :return: Final inquire result.
    """
    while True:
        try:
            return True, inquire_func()
        except (InquireCancel, KeyboardInterrupt) as err:
            if err.args:
                print(f'Cancelled: {_add_end(err.args[0])}')
            else:
                print(f'Cancelled.')

            return False, None

        except InquireRestart as err:
            if err.args:
                print(f'Restarting... {err.args[0]}')
            else:
                print(f'Restarting...')
