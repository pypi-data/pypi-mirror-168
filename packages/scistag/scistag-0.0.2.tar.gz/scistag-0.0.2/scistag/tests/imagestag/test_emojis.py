from scistag.imagestag.emoji import EmojiDb


def test_svg_emoji():
    """
    Tests if an SVG emoji can be loaded from the EmojiDB
    """
    svg_data = EmojiDb.get_emoji_svg(["1f3c3"])
    assert svg_data is not None
    assert len(svg_data) == 13716


def test_markdown_dict():
    """
    Tests if the markdown dictionary is valid
    """
    md_dict = EmojiDb.get_markdown_dict()
    assert len(md_dict) > 0
    deer_emoji = EmojiDb.get_emoji_sequence(":deer:")
    assert deer_emoji == ["1F98C"]
    assert deer_emoji == EmojiDb.get_unicode_dict()["deer"].split("_")


def test_unicode_dict():
    """
    Tests if the unicode dictionary is valid
    """
    unicode_dict = EmojiDb.get_unicode_dict()
    assert len(unicode_dict) > 3600
    assert EmojiDb.get_emoji_sequence("deer") == ["1F98C"]
    assert EmojiDb.get_emoji_sequence("flag: Germany") == ['1F1E9', '1F1EA']
