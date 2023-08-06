import logging
import pathlib

from erasudy import commands


logger = logging.getLogger(__name__)


def is_rotational(volume_name):
    """Validates that the volume selected is HDD (magnetic) disks. If
    its disks, it can rotate.

    :param volume_name:
    :return:
    """
    # Get volume data.
    volume_name = pathlib.Path(volume_name).name

    # Detect what kind of volume is.
    with open(f"/sys/block/{volume_name}/queue/rotational", "r") as f:
        return f.read().strip() == "1"


def umount_all(volume):
    """Ensures the drive is not mounted.

    :param volume: Path to the volume.
    :type volume: str

    """


