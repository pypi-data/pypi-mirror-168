"""Utilities for tests."""


def get_file_bytes(path: str) -> bytes:
    """Return file content as bytes."""
    with open(path, 'rb') as handle:
        return handle.read()
