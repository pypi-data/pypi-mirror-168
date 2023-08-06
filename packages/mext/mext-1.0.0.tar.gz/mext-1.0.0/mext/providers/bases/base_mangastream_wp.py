import re
from datetime import datetime
from bs4 import BeautifulSoup

from mext import enums, models, client, utils
from mext.provider import Provider


class MangaStreamBase(Provider):

    def __init__(self, name, siteUrl):
        self.name = name
        super(MangaStreamBase, self).__init__(name, siteUrl)

        self.selenium = client.Selenium()

    @utils.data_page
    def get_manga(self):
        manga = models.Manga(self)

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        wrong_field_values = ['-', 'N/A']

        # ID
        id_element = soup.select_one('div.rt div.bookmark[data-id]')

        if id_element:
            id_text = id_element.attrs['data-id']
            
            if id_text:
                manga.id = id_text.strip()

        # Title
        title_element = soup.select_one('h1.entry-title')

        title_text = title_element.string if title_element else ''
        if title_text:
            manga.title = title_text
        else:
            raise Exception('Could not get title for comic')

        # Status
        status_element = soup.select('div.tsinfo div.imptdt')[0]

        status_text = status_element.select_one('i').string if status_element else ''
        if status_text:
            manga.status = status_text

        # Type
        type_element = soup.select('div.tsinfo div.imptdt')[1]
        type_text = type_element.select_one('a').string if type_element else ''
        if type_text:
            manga.comic_type = type_text
        
        # Language
        if type_text:
            type_text = type_text.strip().lower()
            if type_text in enums.ComicTypesLanguage.dict():
                manga.language = enums.ComicTypesLanguage[type_text]

        # Alternative Titles
        alt_element = soup.select_one('div.infox div.wd-full')

        alt_names = []
        if alt_element and \
            alt_element.select_one('b') and \
            alt_element.select_one('b').string.strip() == 'Alternative Titles':
            alt_text = alt_element.select_one('span').string.strip()

            if alt_text and alt_text not in wrong_field_values:
                for alt_name in alt_text.split(','):
                    alt_names.append(alt_name.strip())
        
        manga.alt = alt_names
        
        # Description
        description_element = soup.select_one(
            'div.infox div.entry-content.entry-content-single'
        )

        description_text = description_element.text if description_element else ''
        if description_text:
            trans = description_text.maketrans({
                "‘": "'",
                "’": "'",
                "“": "'",
                "”": "'",
            })
            manga.description = description_text.strip('\n')\
                                                        .translate(trans)

        # Author
        author_element = soup.select('div.infox div.fmed')[1]

        author_names = []
        if author_element and \
            author_element.select_one('b').string.strip() == 'Author' and \
            author_element.select_one('span').string.strip() not in wrong_field_values:

            author_names_text = author_element.select_one('span').text.strip()

            for name in author_names_text.split('/'):
                if name:
                    person = models.Person(self)
                    person.name = name.strip()
                    author_names.append(person)

        manga.authors = author_names

        # Artist
        artist_element = soup.select('div.infox div.fmed')[2]

        artist_names = []
        if artist_element and \
            artist_element.select_one('b').string.strip() == 'Artist' and \
            artist_element.select_one('span').string.strip() not in wrong_field_values:

            artist_names_text = artist_element.select_one('span').text.strip()

            for name in artist_names_text.split('/'):
                if name:
                    person = models.Person(self)
                    person.name = name.strip()
                    artist_names.append(person)
        
        manga.artists = artist_names

        # Genres
        genre_elements = soup.select('span.mgen > a')

        genres = []
        if genre_elements:
            for genre_element in genre_elements:
                name = genre_element.text.strip()
                if name:
                    genre = models.Genre(self)
                    genre.name = name
                    genres.append(genre)

        manga.genres = genres

        ## Extra data

        # Followers
        followers_element = soup.select_one('div.rt div.bmc')

        if followers_element:
            followers_text = followers_element.text.strip()
            followers_find = re.findall('Followed by ([\d]+) people', followers_text)

            if followers_find:
                manga.followers = int(followers_find[0])

        # Rating
        rating_element = soup.select_one('div.rating div[itemprop="ratingValue"]')

        if rating_element:
            rating_text = rating_element.text.strip()
            
            if rating_text:
                manga.rating = float(rating_text)

        # Posted On
        posted_on_element = soup.select('div.infox div.fmed')[5]

        if posted_on_element and \
            posted_on_element.select_one('b').string.strip() == 'Posted On' and \
            posted_on_element.select_one('span').text.strip() not in wrong_field_values:

            posted_on_dt = posted_on_element.attrs.get('datetime')

            if posted_on_dt:
                manga.created_at = datetime.fromisoformat(posted_on_dt)

        # Updated On
        updated_on_element = soup.select('div.infox div.fmed')[6]

        if updated_on_element and \
            updated_on_element.select_one('b').string.strip() == 'Posted On' and \
            updated_on_element.select_one('span').text.strip() not in wrong_field_values:

            updated_on_dt = updated_on_element.attrs.get('datetime')

            if posted_on_dt:
                manga.created_at = datetime.fromisoformat(updated_on_dt)

        # Return complete Manga data
        return manga

    @utils.data_page
    def get_chapter(self):

        data = {
            'attributes': {}
        }
        attributes = data['attributes']

        soup = BeautifulSoup(self.selenium.source, 'lxml')

        self.chapter_data = models.Chapter(self)

        return self.chapter_data

    @utils.data_page
    def get_manga_chapters(self):
        self.chapter_list = []

        for chapter in []:
            data = {
                'attributes': {}
            }
            attributes = data['attributes']

            soup = BeautifulSoup(self.selenium.source, 'lxml')

            self.chapter_list.append(models.Chapter(self))

        return self.chapter_list
