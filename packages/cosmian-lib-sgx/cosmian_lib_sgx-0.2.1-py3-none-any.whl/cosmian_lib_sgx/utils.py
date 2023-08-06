"""cosmian_lib_sgx.utils module."""

from pathlib import Path
import re
from secrets import compare_digest
from typing import List

from cosmian_lib_sgx.error import InternalError, SecurityError
from cosmian_lib_sgx.key_info import KeyInfo

INSTANT_RE = re.compile(r"""(?P<instant>[0-9]{13,20})""")
FINGERPRINT_RE = re.compile(r"""(?P<fingerprint>[0-9a-zA-Z]{16})""")


def ctime_in_path(path: Path) -> int:
    """Extract ctime which is part of `path` as string."""
    p: Path = path.resolve()
    parts = [part for part in p.parts if not FINGERPRINT_RE.search(part)]
    ctimes = [part for part in parts if INSTANT_RE.match(part)]

    if len(ctimes) == 1:
        return int(ctimes[0])

    raise InternalError("creation time of input data not found")


def psk_check(keys: List[KeyInfo]) -> bool:
    """Check that all pre-shared keys are the same in `keys`."""
    wit, *_ = keys

    for k in keys:
        if not compare_digest(wit.psk, k.psk):
            raise SecurityError("Different pre-shared key found!")

    return True
