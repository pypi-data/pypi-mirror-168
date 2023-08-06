import logging
import pathlib
import subprocess

logger = logging.getLogger(__name__)


def umount_all(volume: str):
    """Command to unmount the device.

    :param volume: Name of the volume disk.
    :type volume: str
    """
    output = subprocess.check_output(["lsblk", "-tno", "mountpoint", volume])
    mountpoints = output.decode("utf-8").strip().split("\n")
    for path in mountpoints:
        if path and pathlib.Path(path).exists():
            subprocess.run(["umount", path])

    subprocess.run(["sync"])


def erase(volume: str, mode: str = "0", steps: int = 1):
    """

    :param volume: Path to the volume.
    :type volume: str
    :param mode:
    :type mode: str
    :param steps: Number of times to re-write the disk.
    :type steps: int
    """
    logger.debug(f"Trying to erase {volume} in mode {mode}")
    subprocess.call(
        [
            "pkexec", "badblocks",
            "-t", mode,
            "-p", str(steps),
            volume
        ]
    )
