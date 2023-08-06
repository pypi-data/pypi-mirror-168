import io

from typing import List
from datetime import datetime

from mext import enums


class Model:

    def __init__(self, provider):
        self.name = provider.name

    @property
    def __dict__(self):
        return self.to_dict()

    def __iter__(self):
        for field in self.__slots__:
            yield (field, getattr(self, field))

    def __str__(self):
        return "{} {}".format(self.name, self.__class__.__name__)

    def to_dict(self):
        return {field: getattr(self, field) for field in self.__slots__}


class Cover(Model):
    """Represents a Cover."""
    __slots__ = (
        "id", "description", "volume", "file_bytes", "url", "url_256", "url_512",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.description: str = ""
        self.volume: float = 0.0
        self.file_bytes: io.BytesIO = io.BytesIO()
        self.url: str = ""
        self.url_256: str = ""
        self.url_512: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return str(self)


class Tag(Model):
    """Represents a Manga Tag."""
    __slots__ = (
        "id", "name", "description",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.description: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Genre(Model):
    """Represents a Manga Tag."""
    __slots__ = (
        "id", "name", "description",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.description: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Person(Model):
    """Represents a Author or Artist or any related Person"""
    __slots__ = (
        "id", "name", "image", "bio",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = None
        self.name: str = ""
        self.image: str = ""
        self.bio: str = ""
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Manga(Model):
    """Represents a Manga."""
    __slots__ = (
        "id", "title", "alt", "description", "links", "language", "comic_type", "status",
        "year", "rating", "followers", "genres", "tags", "authors", "artists", "cover",
        "first_chapter", "last_chapter",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = ""
        self.title: str = ""
        self.alt: List[str] = []
        self.description: str = ""
        self.links: List[str] = []
        self.language: str = ""
        self.comic_type: enums.ComicTypesLanguage = None
        self.status: enums.StatusTypes = None
        self.year: int = datetime.now().year
        self.rating: float = 0.0
        self.followers: int = 0
        self.genres: List[Genre] = []
        self.tags: List[Tag] = []
        self.authors: List[Person] = []
        self.artists: List[Person] = []
        self.cover: Cover = None
        self.first_chapter: str = ""
        self.last_chapter: str = ""
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return str(self)


class Chapter(Model):
    """Represents a Chapter."""
    __slots__ = (
        "id", "url", "name", "volume", "language", "pages_external",
        "manga", "group", "uploader", "created_at", "updated_at",
        "provider", "instance"
    )

    def __init__(self, provider):
        super().__init__(provider)
        self.id: str = ""
        self.url: str = ""
        self.name: str = ""
        self.number: str = ""
        self.volume: float = 0.0
        self.language: str = ""
        self.pages_external: str = ""
        self.manga: Manga = None
        self.group: str = None
        self.uploader: str = None
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
        self.provider = provider
        self.instance = self

    def __str__(self) -> str:
        return "Chapter {self.number}"

    def __repr__(self) -> str:
        return str(self)
