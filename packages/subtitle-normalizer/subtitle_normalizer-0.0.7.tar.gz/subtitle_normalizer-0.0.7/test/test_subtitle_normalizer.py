import pytest
import pysrt
from pathlib import Path
from subtitle_normalizer.normalizer import resegment_sub


@pytest.fixture()
def blanks_original():
    return pysrt.from_string(
        Path(".").absolute().joinpath("test", "data", "input", "blanks.srt").read_text()
    )


@pytest.fixture()
def blanks_resegmented():
    return pysrt.from_string(
        Path(".")
        .absolute()
        .joinpath("test", "data", "output", "blanks.srt")
        .read_text()
    )


def test_resegment_sub0(blanks_original, blanks_resegmented):
    assert resegment_sub(blanks_original) == blanks_resegmented
