import io
import json
from threading import RLock
from typing import List, Optional, Set, Dict

import scistag.addons
from scistag.common.essential_data import get_edp
from scistag.filestag import FileStag
from scistag.imagestag import Image
from scistag.imagestag import svg

EMOJI_SVG_ADDON = "emojis.svg"
"Addon name for SVG emojis"

_EMOJI_DB_NAME = "data/emoji/emoji_db.json"
"Main emoji database file, containing detailed information about all Emojis"
_EMOJI_NAMES = "data/emoji/emoji_names.json"
"Emoji conversion dictionary. Containing the unicode codes for all unicode codes as defined by unicode.org"
_EMOJI_NAMES_MARKDOWN = "data/emoji/markdown_emoji_names.json"
"Markdown emoji conversion dictionary. Containing the unicode codes for common Emoji names used in markdown"


class EmojiDb:
    """
    The Emoji DB provides Emoji and country flag graphics.
    By default it uses the Noto Emoji dataset embedded into the SciStag module.
    """

    _access_lock = RLock()
    "Shared access lock"
    _initialized = False
    "Defines if the emoji db was initialized"
    _extensions = {}
    "List of known emoji addon packages"
    _svg_emojis = False
    "Defines if SVG emojis are available"
    _markdown_names = {}
    "Markdown name conversion dictionary"
    _unicode_names = {}
    "Unicode name conversion dictionary"

    @classmethod
    def get_markdown_dict(cls) -> dict:
        """
        Returns the markdown name dictionary. Contains all common markdown emoji names as key and their corresponding
        unique sequence as value

        :return: The dictionary
        """
        with cls._access_lock:
            if len(cls._markdown_names) > 0:
                return cls._markdown_names
            edp = get_edp()
            file_data = FileStag.load_file(edp + _EMOJI_NAMES_MARKDOWN)
            cls._markdown_names = json.load(io.BytesIO(file_data))
            return cls._markdown_names

    @classmethod
    def get_unicode_dict(cls) -> dict:
        """
        Returns the unicode name dictionary. Contains all common emoji names as key and their corresponding
        unique sequence as value for more than 3600 emojis. See unicode.org for more details.
        :return: The dictionary
        """
        with cls._access_lock:
            if len(cls._unicode_names) > 0:
                return cls._unicode_names
            edp = get_edp()
            file_data = FileStag.load_file(edp + _EMOJI_NAMES)
            cls._unicode_names = json.load(io.BytesIO(file_data))
            return cls._unicode_names

    @classmethod
    def get_emoji_sequence(cls, identifier: str) -> List:
        """
        Returns the unicode sequence for given unicode identifier

        :param identifier: Either the full qualified identifier as defined by unicode.org supporting all >3600 emojis,
        see get_unicode_dict() for the full list or the markdown shortcode enclosed by two colons such as ":deer:"
        as defined in get_markdown_dict().
        :return: The unicode sequence if the emoji could be found, otherwise an empty list
        """
        if identifier.startswith(":") and identifier.endswith(":"):
            return cls.get_markdown_dict().get(identifier[1:-1], "").split("_")
        return cls.get_unicode_dict().get(identifier, "").split("_")

    @classmethod
    def get_extensions(cls) -> Dict:
        """
        Returns all available emoji extensions

        :return: Dictionary of extensions and their corresponding FileStag path to access their data
        """
        with cls._access_lock:
            if not cls._initialized:
                cls._extensions = scistag.addons.AddonManager.get_addons_paths("emojis.*")
                cls._initialized = True
                cls._svg_emojis = EMOJI_SVG_ADDON in cls._extensions and svg.SvgRenderer.available()
        return cls._extensions

    @classmethod
    def get_svg_support(cls) -> bool:
        """
        Returns if SVG rendering is supported tne SVG repo installed

        :return: True if high quality rendering is possible
        """
        cls.get_extensions()
        return cls._svg_emojis

    @classmethod
    def get_emoji_svg(cls, sequence: List[str]) -> Optional[bytes]:
        """
        Tries to read the SVG of an emoji from the database
        :param sequence: The unicode sequence, e.g. ["u1f98c"] for a stag
        :return: The SVG data on success, otherwise None
        """
        extensions = cls.get_extensions()
        if EMOJI_SVG_ADDON not in extensions:
            return None
        lower_cased = [element.lower() for element in sequence]
        combined = "_".join(lower_cased)
        emoji_path = extensions[EMOJI_SVG_ADDON] + f"images/noto/emojis/svg/emoji_u{combined}.svg"
        return FileStag.load_file(emoji_path)

    @classmethod
    def get_emoji_png(cls, sequence: List[str]) -> Optional[bytes]:
        """
        Tries to read the SVG of an emoji from the database
        :param sequence: The unicode sequence, e.g. ["1f98c"] for a stag
        :return: The SVG data on success, otherwise None
        """
        lower_cased = [element.lower() for element in sequence]
        combined = "_".join(lower_cased)
        edp = get_edp()
        emoji_path = edp + f"images/noto/cpngs/emoji_u{combined}.png"
        return FileStag.load_file(emoji_path)

    @classmethod
    def render_emoji(cls, identifier: str = "", sequence: Optional[List[str]] = None, size=128) -> Optional[Image]:
        """
        Tries to read an emoji and render it to a transparent image
        :param identifier: The emoji's identifier such as :deer:
        :param sequence: The unicode sequence, e.g. ["u1f98c"] for a stag
        :param size: The size in pixels in which the emoji shall be rendered
        :return: The SVG data on success, otherwise None
        """
        svg_renderer_available = svg.SvgRenderer.available()
        if sequence is None:
            sequence = cls.get_emoji_sequence(identifier)
        svg_data = cls.get_emoji_svg(sequence=sequence) if svg_renderer_available else None
        png_data = None
        if not svg_data:
            png_data = cls.get_emoji_png(sequence=sequence)
        if svg_data is not None:
            image = svg.SvgRenderer.render(svg_data, size, size)
            if image is not None:
                return image
        if png_data is not None:
            image = Image(png_data)
            image.resize((size, size))
            return image
        return None
