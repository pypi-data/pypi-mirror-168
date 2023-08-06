"""cosmian_lib_sgx.crypto_lib module."""

from ctypes import (POINTER, c_ubyte, c_int, cdll,
                    c_ulonglong, cast, c_char, c_char_p)
import inspect
from pathlib import Path

from cosmian_lib_sgx.error import CryptoError, SGXError

current_frame = inspect.currentframe()

if not current_frame:
    raise Exception("Frame object not available in your Python interpreter!")

sgx_crypto_lib_path = (Path(inspect.getabsfile(current_frame)).parent /
                       "libcs_sgx_crypto.so")

if not sgx_crypto_lib_path.exists():
    raise FileNotFoundError(f"Can't find '{sgx_crypto_lib_path}'")

crypto_lib = cdll.LoadLibrary(str(sgx_crypto_lib_path))

# int cs_sgx__init()
crypto_lib.cs_sgx__init.argtypes = []
crypto_lib.cs_sgx__init.restype = c_int

# int cs_sgx__running_inside_enclave()
crypto_lib.cs_sgx__running_inside_enclave.argtypes = []
crypto_lib.cs_sgx__running_inside_enclave.restype = c_int

# int cs_sgx__enclave_ed25519_pubkey(unsigned char *pk);
crypto_lib.cs_sgx__enclave_ed25519_pubkey.argtypes = [POINTER(c_ubyte)]
crypto_lib.cs_sgx__enclave_ed25519_pubkey.restype = c_int

# int cs_sgx__encrypt_with_sealed_key(unsigned char *encrypted_data,
#                                     const unsigned char *data,
#                                     unsigned long long data_len,
#                                     const unsigned char uuid[static 16],
#                                     unsigned char *signed_seal_box,
#                                     unsigned long long signed_seal_box_len,
#                                     const unsigned char signer_pk);
crypto_lib.cs_sgx__encrypt_with_sealed_key.argtypes = [
    POINTER(c_ubyte),  # encrypted_data
    POINTER(c_ubyte),  # data
    c_ulonglong,  # data_len
    POINTER(c_ubyte),  # uuid
    POINTER(c_ubyte),  # signed_sealed_symkey
    c_ulonglong,  # signed_sealed_symkey_len
    POINTER(c_ubyte)  # signer_pk
]
crypto_lib.cs_sgx__encrypt_with_sealed_key.restype = c_int

# int cs_sgx__decrypt_with_sealed_key(unsigned char *data,
#                                     const unsigned char *encrypted_data,
#                                     unsigned long long encrypted_data_len,
#                                     const unsigned char uuid[static 16],
#                                     const unsigned char *signed_seal_box,
#                                     unsigned long long signed_seal_box_len,
#                                     const unsigned char signer_pk);
crypto_lib.cs_sgx__decrypt_with_sealed_key.argtypes = [
    POINTER(c_ubyte),  # data
    POINTER(c_ubyte),  # encrypted_data
    c_ulonglong,  # encrypted_data_len
    POINTER(c_ubyte),  # uuid
    POINTER(c_ubyte),  # signed_seal_box
    c_ulonglong,  # signed_seal_box_len
    POINTER(c_ubyte)  # signer_pk
]
crypto_lib.cs_sgx__decrypt_with_sealed_key.restype = c_int

# int cs_sgx__verify(unsigned char *unsigned_message,
#                    const unsigned char *signed_message,
#                    const unsigned long long signed_message_length,
#                    const unsigned char *signer_pk);
crypto_lib.cs_sgx__verify.argtypes = [
    POINTER(c_ubyte),  # unsigned_message
    POINTER(c_ubyte),  # signed_message
    c_ulonglong,  # signed_message_length
    POINTER(c_ubyte)  # signer_pk
]
crypto_lib.cs_sgx__verify.restype = c_int

# int cs_sgx__recover_psk(unsigned char *psk,
#                         const unsigned char *signed_seal_box,
#                         unsigned long long signed_seal_box_len,
#                         unsigned char uuid[static 16],
#                         const unsigned char *signer_pk);
crypto_lib.cs_sgx__recover_psk.argtypes = [
    POINTER(c_ubyte),  # psk
    POINTER(c_ubyte),  # signed_seal_box
    c_ulonglong,  # signed_seal_box_len
    POINTER(c_ubyte),  # uuid
    POINTER(c_ubyte)  # signer_pk
]
crypto_lib.cs_sgx__recover_psk.restype = c_int

# int cs_sgx__get_quote(const unsigned char* user_report_data_str,
#                       char* b64_quote);
crypto_lib.cs_sgx__get_quote.argtypes = [
    POINTER(c_ubyte), c_char_p
]
crypto_lib.cs_sgx__get_quote.restype = c_int

if crypto_lib.cs_sgx__init() != 0:
    raise CryptoError("Failed to init libsodium!")


def is_running_in_enclave() -> bool:
    """Check whether the code is running in SGX enclave."""
    if crypto_lib.cs_sgx__running_inside_enclave() == 0:
        return True

    raise SGXError("You're code is not running inside SGX enclave!")


def enclave_ed25519_pubkey() -> bytes:
    """Get enclave's public key for X25519."""
    assert is_running_in_enclave()

    pk = (c_ubyte * 32)()

    if crypto_lib.cs_sgx__enclave_ed25519_pubkey(cast(pk, POINTER(c_ubyte))) != 0:
        raise CryptoError("Failed to get enclave's Ed25519 pubkey!")

    return bytes(pk)


def enclave_encrypt(data: bytes,
                    computation_uuid: bytes,
                    signed_seal_box: bytes,
                    signer_pubkey: bytes) -> bytes:
    """Encrypt using the sealed symmetric key in `sealed_key`."""
    assert is_running_in_enclave()

    data_len = len(data)
    data_c_array = (c_ubyte * data_len)(*data)

    uuid_len = len(computation_uuid)
    uuid_c_array = (c_ubyte * uuid_len)(*computation_uuid)

    signed_seal_box_len = len(signed_seal_box)
    signed_seal_box_c_array = (c_ubyte * signed_seal_box_len)(*signed_seal_box)

    signer_pubkey_len = len(signer_pubkey)
    signer_pubkey_c_array = (c_ubyte * signer_pubkey_len)(*signer_pubkey)

    # crypto_box_NONCEBYTES (24) + crypto_box_MACBYTES (16) = 40
    encrypted_data = (c_ubyte * (data_len + 40))()

    if n := crypto_lib.cs_sgx__encrypt_with_sealed_key(
            cast(encrypted_data, POINTER(c_ubyte)),
            data_c_array,
            data_len,
            uuid_c_array,
            signed_seal_box_c_array,
            signed_seal_box_len,
            signer_pubkey_c_array):
        raise CryptoError(f"Failed to encrypt data! (error code {n})")

    return bytes(encrypted_data)


def enclave_decrypt(encrypted_data: bytes,
                    computation_uuid: bytes,
                    signed_seal_box: bytes,
                    signer_pubkey: bytes) -> bytes:
    """Decrypt with sealed symmetric key if signature is verified."""
    assert is_running_in_enclave()

    encrypted_data_len = len(encrypted_data)
    encrypted_data_c_array = (c_ubyte * encrypted_data_len)(*encrypted_data)

    uuid_len = len(computation_uuid)
    uuid_c_array = (c_ubyte * uuid_len)(*computation_uuid)

    signed_seal_box_len = len(signed_seal_box)
    signed_seal_box_c_array = (c_ubyte * signed_seal_box_len)(*signed_seal_box)

    signer_pubkey_len = len(signer_pubkey)
    signer_pubkey_c_array = (c_ubyte * signer_pubkey_len)(*signer_pubkey)

    # crypto_box_NONCEBYTES (24) + crypto_box_MACBYTES (16) = 40
    data = (c_ubyte * (encrypted_data_len - 40))()

    if n := crypto_lib.cs_sgx__decrypt_with_sealed_key(
            cast(data, POINTER(c_ubyte)),
            encrypted_data_c_array,
            encrypted_data_len,
            uuid_c_array,
            signed_seal_box_c_array,
            signed_seal_box_len,
            signer_pubkey_c_array):
        raise CryptoError(f"Failed to decrypt data! (error code {n})")

    return bytes(data)


def verify(message: bytes, signature: bytes, pubkey: bytes) -> bytes:
    """Check Ed25519 signature of `message` with `pubkey`."""
    assert is_running_in_enclave()

    sm: bytes = signature + message
    sm_len = len(sm)
    sm_c_array = (c_ubyte * sm_len)(*sm)

    signer_pubkey_c_array = (c_ubyte * len(pubkey))(*pubkey)

    # crypto_sign_BYTES (64)
    m = (c_ubyte * (len(sm) - 64))()

    if crypto_lib.cs_sgx__verify(
            cast(m, POINTER(c_ubyte)),
            sm_c_array,
            sm_len,
            signer_pubkey_c_array
    ) != 0:
        raise CryptoError("Failed to verify signature!")

    return bytes(m)


def recover_psk(signed_seal_box: bytes,
                computation_uuid: bytes,
                signer_pk: bytes) -> bytes:
    """Retrieve the pre-shared secret in the seal box."""
    assert is_running_in_enclave()

    signed_seal_box_len = len(signed_seal_box)
    signed_seal_box_c_array = (c_ubyte * signed_seal_box_len)(*signed_seal_box)

    uuid_c_array = (c_ubyte * len(computation_uuid))(*computation_uuid)

    signer_pubkey_c_array = (c_ubyte * len(signer_pk))(*signer_pk)

    psk = (c_ubyte * 32)()

    if n := crypto_lib.cs_sgx__recover_psk(cast(psk, POINTER(c_ubyte)),
                                           signed_seal_box_c_array,
                                           signed_seal_box_len,
                                           uuid_c_array,
                                           signer_pubkey_c_array):
        raise CryptoError(f"Failed to recover pre-shared key! (error code {n})")

    return bytes(psk)


def enclave_get_quote(user_report_data: bytes) -> str:
    """Enclave's quote generation by SGX enclave within `user_report_data`."""
    assert is_running_in_enclave()

    if len(user_report_data) > 64:
        raise CryptoError("sgx_report_data_t can't exceed 64 bytes!")

    # pad with '\0'
    user_report_data = b"\0" * (64 - len(user_report_data)) + user_report_data

    quote = (c_char * 8192)()
    public_key_c_array = (c_ubyte * 64)(*user_report_data)

    if crypto_lib.cs_sgx__get_quote(public_key_c_array, cast(quote, c_char_p)) != 0:
        raise CryptoError("Failed to retrieve enclave's quote!")

    return bytes(quote).decode("utf-8").rstrip("\0")
