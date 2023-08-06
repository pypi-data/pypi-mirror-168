"""
Tests the FileStag class
"""

from scistag.filestag import FileStag, ZIP_SOURCE_PROTOCOL
from scistag.common.test_constants import TestConstants
from scistag.common.essential_data import ESSENTIAL_DATA_ARCHIVE_NAME, get_edp


def test_file_stag():
    """
    Test the base functionality of the FileStag class
    """
    # load file from disk
    ed = FileStag.load_file(ESSENTIAL_DATA_ARCHIVE_NAME)
    assert len(ed) == 13754681
    # load file from the web
    stag_image = FileStag.load_file(TestConstants.STAG_URL)
    assert len(stag_image) == 308019
    # load file directly from archive
    readme = FileStag.load_file(ZIP_SOURCE_PROTOCOL + ESSENTIAL_DATA_ARCHIVE_NAME + "/README.md")
    assert len(readme) == 2234
    edp = get_edp()
    mdi = FileStag.load_file(edp + "/data/material_design/material_design_icon_names.json")
    assert len(mdi) == 227233
    # exists
    assert FileStag.exists(ESSENTIAL_DATA_ARCHIVE_NAME)
    assert not FileStag.load_file(ESSENTIAL_DATA_ARCHIVE_NAME + "nonsense")
    assert FileStag.exists(ZIP_SOURCE_PROTOCOL + ESSENTIAL_DATA_ARCHIVE_NAME + "/README.md")
    assert not FileStag.exists(ZIP_SOURCE_PROTOCOL + ESSENTIAL_DATA_ARCHIVE_NAME + "/READMExk.md")
    assert FileStag.exists(TestConstants.STAG_URL)
    assert not FileStag.exists(TestConstants.STAG_URL + "nonsense")
