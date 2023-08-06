from enum import Enum
from typing import overload

class BaseEnum(Enum):

    @classmethod
    def __contains__(cls, name):
        return name in [c.name for c in cls]

    @classmethod
    def list(cls):
        return [c.value for c in cls]

    @classmethod
    def keys(cls):
        return [c.name for c in cls]

    @classmethod
    def dict(cls):
        return {c.name: c.value for c in cls}

    @classmethod
    def reverse_dict(cls):
        return {c.value: c.name for c in cls}

class AttributeEnum(str, BaseEnum):
    pass

class Datacall(BaseEnum):
    latest_list = ('get_latest', 'latest_list')
    manga = ('get_manga', 'manga')
    manga_list = ('get_manga_list', 'manga_list')
    chapter = ('get_chapter', 'chapter')
    chapter_list = ('get_manga_chapters', 'chapter_list')
    cover = ('get_cover', 'cover')

DatacallAttributes = {v[0]: v[1] for v in Datacall.list()}

class StatusTypes(AttributeEnum):
    Ongoing = 'Ongoing'
    Completed = 'Completed'
    Haitus = 'Haitus'
    Dropped = 'Dropped'
    ComingSoon = 'Comic Soon'
    

class ComicTypesLanguage(AttributeEnum):
    manga = 'jp'
    manhua = 'zh'
    manhwa = 'ko'
    webtoon = 'en'