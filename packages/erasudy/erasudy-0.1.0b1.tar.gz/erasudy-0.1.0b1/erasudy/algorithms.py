import logging

from erasudy import validations, commands

logger = logging.getLogger(__name__)


# https://en.wikipedia.org/wiki/Data_erasure#Standards


def _hdd_pre_steps(volume):
    """Pre steps to prepare the HDDs drive to be re-written
    (securely wipe).

    :param volume: Path to the volume.
    :type volume: str
    """
    # Validation steps.
    if not validations.is_rotational(volume):
        logger.error("This erasure process only works with rotational disks.")
        exit(1)

    # Umount volumes before starting to re-write.
    commands.umount_all(volume)


def bruce_schneier(volume):
    """
    Erasure Standard: Bruce Schneier's Algorithm
    Description: All ones, all zeros, pseudo-random sequence five times.

    :param volume: Path to the volume.
    :type volume: str
    """
    logger.info(f"Starting Bruce Schneier's Algorithm on {volume}")
    _hdd_pre_steps(volume)

    # One time with all Zeros
    commands.erase(volume, "1")
    # One time with all Zeros
    commands.erase(volume, "0")
    commands.erase(volume, "random", steps=5)
