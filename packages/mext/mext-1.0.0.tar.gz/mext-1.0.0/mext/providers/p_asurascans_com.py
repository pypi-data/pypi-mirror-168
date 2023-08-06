from mext.providers.bases.base_mangastream_wp import MangaStreamBase


class AsuraScansCom(MangaStreamBase):

    def __init__(self, name, siteUrl):
        self.language = 'en'
        super(AsuraScansCom, self).__init__(name, siteUrl)

    def get_manga(self, *args, **kwargs):
        return super(AsuraScansCom, self).get_manga(*args, **kwargs)

    def get_chapter(self, *args, **kwargs):
        return super(AsuraScansCom, self).get_chapter(*args, **kwargs)

    def get_manga_chapters(self, *args, **kwargs):
        return super(AsuraScansCom, self).get_manga_chapters(*args, **kwargs)
