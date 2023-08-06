import hashlib


def hash_file(path: str, buf_size: int = 65536) -> str:
    """
    Hash a file on disk

    Args:
        path: Path of file to hash
        buf_size: Size of buffer in bytes, default `65536`
    """
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(buf_size):
            md5.update(chunk)
    return md5.hexdigest()
