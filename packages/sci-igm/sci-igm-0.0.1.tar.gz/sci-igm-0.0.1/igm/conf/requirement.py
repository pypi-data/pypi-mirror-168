import pathlib
import subprocess
import sys
from typing import List

import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def load_req(filename: str) -> List[str]:
    with pathlib.Path(filename).open() as reqfile:
        return list(map(str, pkg_resources.parse_requirements(reqfile)))


def pip(*args):
    process = subprocess.run(
        [sys.executable, '-m', 'pip', *args],
        stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
    )
    process.check_returncode()


def check_req(reqs: List[str]) -> bool:
    try:
        pkg_resources.require(reqs)
    except (DistributionNotFound, VersionConflict):
        return False
    else:
        return True
