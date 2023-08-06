import os
from scistag.gitstag import GitScanner


def test_repo_validity():
    if int(os.environ.get("TEST_GIT_INTEGRITY", "0")) != 1:
        return
    scanner = GitScanner()
    base_path = os.path.normpath(os.path.dirname(__file__) + "/../../../")
    scanner.scan(base_path)
    # check the repo does not exceed a reasonable size and has a reasonable count of files and directories
    if scanner.total_size > 1000000:
        print("\n", flush=True)
        print(scanner.file_list_by_size[0:20], flush=True)
    assert scanner.total_size < 1000000
    assert 195 < scanner.file_count < 260
    assert 109 < scanner.dir_count < 180
    lf_ignore_list = ["*/poetry.lock", "*/web/icons/Icon*", "*/AppIcon.appiconset/Icon*", "*/project.pbxproj",
                      "*/data_stag_connection.py", "*/data_stag_vault.py",
                      "*/imagestag/image.py", "*/slidestag/widget.py",
                      "*/data/scistag_essentials.zip",
                      "*/data/scistag_vector_emojis_0_0_2.zip",
                      ]

    too_large_files = scanner.get_large_files(min_size=15000, hard_limit_size=200000, ignore_list=lf_ignore_list)
    if len(too_large_files):
        print(too_large_files, flush=True)
    assert len(too_large_files) == 0
