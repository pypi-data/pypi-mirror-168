"""cosmian_lib_sgx.reader module."""

from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Iterator

from cosmian_lib_sgx.error import InternalError, UserError, CryptoError
from cosmian_lib_sgx.side import Side
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.crypto_lib import enclave_decrypt
from cosmian_lib_sgx.utils import FINGERPRINT_RE, ctime_in_path


class InputData:
    """InputData class for Data Providers input.

    Parameters
    ----------
    root_path : Path
        The root path with input data.
    keys : Dict[Side, List[KeyInfo]]
        Participants keys.

    Attributes
    ----------
    root_path : Path
        The root path of the program.
    input_path : Path
        The input path with DPs data.
    keys : Dict[Side, List[KeyInfo]]
        Participants keys.

    """

    def __init__(self,
                 root_path: Path,
                 keys: Dict[Side, List[KeyInfo]]) -> None:
        """Init constructof of InputData."""
        self.root_path: Path = root_path
        self.input_path: Path = self.root_path / "data"
        assert Side.DataProvider in keys, "Need at least 1 DP key"
        self.keys: List[KeyInfo] = keys[Side.DataProvider]

    @staticmethod
    def fingerprint_from_path(path: Path) -> str:
        """Extract public key fingerprint in `path`."""
        for part in path.parts:
            if m := FINGERPRINT_RE.match(part):
                return m.group()

        raise InternalError(
            f"can't find public key fingerprint for '{path.name}'"
        )

    @staticmethod
    def find_fingerprint(
            fingerprint: str,
            keys: List[KeyInfo]
    ) -> Tuple[int, KeyInfo]:
        """Recover index and KeyInfo of a specific public key fingerprint."""
        for i, key_info in enumerate(keys):
            if key_info.fingerprint == fingerprint:
                return i, key_info

        raise InternalError(
            f"public key fingerprint '{fingerprint}' does not exist"
        )

    def read(self, n: Optional[int] = None) -> Iterator[BytesIO]:
        """Read data of all Data Providers or optionally a specific one `n`."""
        if n is not None and not 0 <= n < len(self.keys):
            raise UserError(f"bad Data Provider index '{n}'")

        for path in sorted(self.input_path.rglob("*.enc"), key=ctime_in_path):
            if path.is_file():
                fingerprint: str = InputData.fingerprint_from_path(path)
                pos, key_info = InputData.find_fingerprint(
                    fingerprint,
                    self.keys
                )  # type: int, KeyInfo

                if n is None or n == pos:
                    try:
                        data = enclave_decrypt(encrypted_data=path.read_bytes(),
                                               computation_uuid=key_info.computation_uuid,
                                               signed_seal_box=key_info.signed_seal_box,
                                               signer_pubkey=key_info.pubkey)
                    except CryptoError as exc:
                        raise CryptoError(f"Failed to decrypt: {path}") from exc

                    yield BytesIO(data)
