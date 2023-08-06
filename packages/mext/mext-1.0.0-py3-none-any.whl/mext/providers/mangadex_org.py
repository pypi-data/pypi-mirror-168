import time

from typing import List, Dict, Union, Type

from mext.provider_template import Provider

#Taken from https://github.com/Proxymiity/MangaDex.py

INCLUDE_ALL = ["cover_art", "manga", "chapter", "scanlation_group", "author", "artist", "user", "leader", "member"]


class NetworkChapter:
    """Represents a link between the MD@H Network and a Chapter."""
    __slots__ = (
        "valid_thru", "chapter", "node_url", "hash",
        "files", "files_redux", "pages", "pages_redux", "client"
    )

    def __init__(self, data, chapter, client):
        self.valid_thru = int(time.time()) + 900
        self.chapter = chapter
        self.node_url = data.get("baseUrl")
        _ch = data.get("chapter")
        self.hash = _ch.get("hash")
        self.files = _ch.get("data")
        self.files_redux = _ch.get("dataSaver")
        self.pages = [f"{self.node_url}/data/{self.hash}/{x}" for x in self.files]
        self.pages_redux = [f"{self.node_url}/data-saver/{self.hash}/{x}" for x in self.files_redux]
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }

    def report(self, url, success, cache_header, req_bytes, req_duration):
        return self.client.network_report(url, success, cache_header, req_bytes, req_duration)


class Cover:
    """Represents a MangaDex Cover."""
    __slots__ = (
        "id", "desc", "volume", "file", "manga", "url", "url_512",
        "url_256", "created_at", "updated_at", "client"
    )

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships", [])
        self.desc = _attrs.get("description")
        self.volume = _attrs.get("volume")
        self.file = _attrs.get("fileName")
        self.manga = next((x["id"] for x in _rel if x["type"] == "manga"), None)
        self.url = f"https://uploads.mangadex.org/covers/{self.manga}/{self.file}"
        self.url_512 = f"{self.url}.512.jpg"
        self.url_256 = f"{self.url}.256.jpg"
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }


class Author:
    """Represents a MangaDex Author or Artist."""
    __slots__ = ("id", "name", "image", "bio", "created_at", "updated_at", "client")

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        self.name = _attrs.get("name")
        self.image = _attrs.get("imageUrl")
        self.bio = _attrs.get("biography")
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }


class User:
    """Represents a MangaDex User."""
    __slots__ = ("id", "username", "roles", "client")

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        self.username = _attrs.get("username")
        self.roles = _attrs.get("roles", [])
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }


class Group:
    """Represents a MangaDex Group."""
    __slots__ = (
        "id", "name", "desc", "website", "irc_server", "irc_channel", "discord", "email",
        "locked", "official", "verified", "leader", "members", "created_at", "updated_at", "client"
    )

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships", [])
        self.name = _attrs.get("name")
        self.desc = _attrs.get("description")
        self.website = _attrs.get("website")
        self.irc_server = _attrs.get("ircServer")
        self.irc_channel = _attrs.get("ircChannel")
        self.discord = _attrs.get("discord")
        self.email = _attrs.get("contactEmail")
        self.locked = _attrs.get("locked")
        self.official = _attrs.get("official")
        self.verified = _attrs.get("verified")
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        try:
            _members = [x["attributes"] for x in _rel if x["type"] == "member"]
            self.members = [User(x, client) for x in _rel if x["type"] == "member"]
        except (IndexError, KeyError):
            self.members = [x["id"] for x in _rel if x["type"] == "member"]
        try:
            _leader = [x["attributes"] for x in _rel if x["type"] == "leader"]
            self.leader = next((User(x, client) for x in _rel if x["type"] == "leader"), None)
        except (IndexError, KeyError):
            self.leader = next((x["id"] for x in _rel if x["type"] == "leader"), None)
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }


class Chapter:
    """Represents a MangaDex Chapter."""
    __slots__ = (
        "id", "volume", "chapter", "title", "language", "pages_external",
        "published_at", "created_at", "updated_at", "manga", "group", "uploader", "client"
    )

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships", [])
        self.volume = _attrs.get("volume")
        self.chapter = _attrs.get("chapter")
        self.title = _attrs.get("title")
        self.language = _attrs.get("translatedLanguage").lower()
        self.pages_external = _attrs.get("externalUrl")
        self.published_at = _attrs.get("publishAt")
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        try:
            _manga = [x["attributes"] for x in _rel if x["type"] == "manga"]
            self.manga = next((Manga(x, client) for x in _rel if x["type"] == "manga"), None)
        except (IndexError, KeyError):
            self.manga = next((x["id"] for x in _rel if x["type"] == "manga"), None)
        try:
            _group = [x["attributes"] for x in _rel if x["type"] == "scanlation_group"]
            self.group = [Group(x, client) for x in _rel if x["type"] == "scanlation_group"]
        except (IndexError, KeyError):
            self.group = [x["id"] for x in _rel if x["type"] == "scanlation_group"]
        try:
            _uploader = [x["attributes"] for x in _rel if x["type"] == "user"]
            self.uploader = next((User(x, client) for x in _rel if x["type"] == "user"), None)
        except (IndexError, KeyError):
            self.uploader = next((x["id"] for x in _rel if x["type"] == "user"), None)
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }

    def get_md_network(self, force_443: bool = False):
        return self.client.read_chapter(self, force_443)


class Manga:
    """Represents a MangaDex Manga."""
    __slots__ = (
        "id", "title", "titles", "desc", "links", "language", "last_volume", "last_chapter", "type",
        "status", "year", "content", "tags", "created_at", "updated_at", "author", "artist", "cover", "client"
    )

    def __init__(self, data, client):
        self.id = data.get("id")
        _attrs = data.get("attributes")
        _rel = data.get("relationships", [])
        self.title = _attrs.get("title")
        self.titles = _attrs.get("altTitles")
        self.desc = _attrs.get("description")
        self.links = _attrs.get("links")
        self.language = _attrs.get("originalLanguage").lower()
        self.last_volume = _attrs.get("lastVolume")
        self.last_chapter = _attrs.get("lastChapter")
        self.type = _attrs.get("publicationDemographic")
        self.status = _attrs.get("status")
        self.year = _attrs.get("year")
        self.content = _attrs.get("contentRating")
        self.tags = [MangaTag(x) for x in _attrs.get("tags")]
        self.created_at = _attrs.get("createdAt")
        self.updated_at = _attrs.get("updatedAt")
        try:
            _author = [x["attributes"] for x in _rel if x["type"] == "author"]
            self.author = [Author(x, client) for x in _rel if x["type"] == "author"]
        except (IndexError, KeyError):
            self.author = [x["id"] for x in _rel if x["type"] == "author"]
        try:
            _artist = [x["attributes"] for x in _rel if x["type"] == "artist"]
            self.artist = [Author(x, client) for x in _rel if x["type"] == "artist"]
        except (IndexError, KeyError):
            self.artist = [x["id"] for x in _rel if x["type"] == "artist"]
        try:
            _cover = [x["attributes"] for x in _rel if x["type"] == "cover_art"]
            _related_cover = next((x for x in _rel if x["type"] == "cover_art"), None)
            if _related_cover is not None:
                _related_cover["relationships"] = [{"type": "manga", "id": self.id}]
                _related_cover = Cover(_related_cover, client)
            self.cover = _related_cover
        except (IndexError, KeyError):
            self.cover = next((x["id"] for x in _rel if x["type"] == "cover_art"), None)
        self.client = client

    @property
    def __dict__(self):
        return {
            field: getattr(self, field) for field in self.__slots__
        }

    def get_chapters(self, params=None, includes=None):
        includes = self.client.constants.get("INCLUDE_ALL") if not includes else includes
        return self.client.get_manga_chapters(self, params, includes)

    def get_covers(self, params=None):
        return self.client.get_manga_covers(self, params)


class MangaTag:
    """Represents a MangaDex Manga Tag."""
    __slots__ = ("id", "name")

    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("attributes").get("name")


class MangadexOrg(Provider):

    def __init__(self, *args, **kwargs):
        super(MangadexOrg, self).__init__(*args, **kwargs)
        self.name = "Mangadex"
        self.domain = "mangadex.org"
        self.baseUrl = f"https://{self.domain}"
        self.language = "en"
        self.client = None

        self.api_url = "https://api.mangadex.org"
        self.net_api_url = "https://api.mangadex.network"

        self.uuid = self.get_uuid()


    def get_uuid(self):
        return self.parsed_url.path.split('/')[2]

    def get_manga(self, includes: list = None):
        """Gets a manga with a specific uuid."""

        uuid = self.uuid
        includes = INCLUDE_ALL if not includes else includes
        params = None
        if includes:
            params = {"includes[]": includes}
        req = self.session.get(f"{self.api_url}/manga/{uuid}", params=params)
        if req.status_code == 200:
            resp = req.json()
            return Manga(resp["data"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_chapter(self, includes: list = None) -> Chapter:
        """Gets a chapter with a specific uuid."""

        uuid = self.uuid
        includes = INCLUDE_ALL if not includes else includes
        params = None
        if includes:
            params = {"includes[]": includes}
        req = self.session.get(f"{self.api_url}/chapter/{uuid}", params=params)
        if req.status_code == 200:
            resp = req.json()
            return Chapter(resp["data"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_manga_chapters(self, params: dict = None, includes: list = None) -> List[Chapter]:
        """Gets chapters associated with a specific Manga."""
        includes = INCLUDE_ALL if not includes else includes
        params = params or {}
        if includes:
            params["includes[]"] = includes
        return self._retrieve_pages(f"{self.api_url}/manga/{self.uuid}/feed", Chapter, call_limit=100, params=params)

    def get_cover(self) -> Cover:
        """Gets a cover with a specific uuid."""
        req = self.session.get(f"{self.api_url}/cover/{uuid}")
        if req.status_code == 200:
            resp = req.json()
            return Cover(resp["data"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def read_chapter(self, force_443: bool = False) -> NetworkChapter:
        """Pulls a chapter from the MD@H Network."""
        data = {"forcePort443": force_443}
        req = self.session.get(f"{self.api_url}/at-home/server/{self.uuid}", params=data)
        if req.status_code == 200:
            resp = req.json()
            ch = self.get_chapter()
            return NetworkChapter(resp, ch, self)
        else:
            raise APIError(req)

    def search(self, obj: str, params: dict,
               limit: int = 100) -> List[Union[Manga, Chapter, Group, Author, Cover, User]]:
        """Searches an object."""
        m = SearchMapping(obj)
        return self._retrieve_pages(f"{self.api_url}{m.path}", m.object, limit=limit, call_limit=100, params=params)

    def _retrieve_pages(self, url: str, obj: Type[Union[Manga, Chapter, Group, Author, Cover]],
                        limit: int = 0, call_limit: int = 500,
                        params: dict = None) -> List[Union[Manga, Chapter, Group, Author, Cover]]:
        params = params or {}
        data = []
        offset = 0
        resp = None
        remaining = True
        if "limit" in params:
            params.pop("limit")
        if "offset" in params:
            params.pop("offset")
        while remaining:
            p = {"limit": limit if limit <= call_limit and limit != 0 else call_limit, "offset": offset}
            p = {**p, **params}
            req = self.session.get(url, params=p)
            if req.status_code == 200:
                resp = req.json()
                data += [x for x in resp["data"]]
            elif req.status_code == 204:
                pass
            else:
                raise APIError(req)
            if limit and len(data) >= limit:
                break
            if resp is not None:
                remaining = resp["total"] > offset + call_limit
                offset += call_limit
            else:
                remaining = False
            if remaining:
                time.sleep(self.rate_limit)
        if not data:
            raise NoResultsError()
        return [obj(x, self) for x in data]
