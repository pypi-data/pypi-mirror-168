# MEXT - Manga/Manhua/Manhwa Extractor

A simple manga extractor. Extracts any comic info, chapter list and chapter pages. This is an app that strictly provides API.

**Still in development.**

This has been tested only on Windows 11 64-bit.

## Installations

`pip install mext`

Important Steps:
- Have Chrome browser installed, download chromedriver matching your Chrome browser version.
- Add chromedriver location to PATH environment variable for this to work


## Usage

This package uses multiple provider codes to extract manga/manhua/manhwa data from online sites.

The providers and it's usage is listed below.

It's easy to use from python code.

**Steps:**
1. Import `Mext` like this

   `from mext import Mext`

2. Get the URL of manga or chapter and pass it to `Mext`

  ```python
  manga_url = 'xxx1'
  chapter_url = 'xxx2'

  # Initialize
  me = Mext()

  # To get manga
  me.populate(['manga'], manga_url)
  manga = me.manga

  # To get one particular chapter
  me.populate(['chapter'], chapter_url)
  chapter = me.chapter

  # Pass manga url to get chapter list belonging to manga
  me.populate(['chapter_list'], manga_url)
  chapters = me.chapter_list

  # Pass manga url when you need both manga and chapter
  me.populate(['manga', 'chapter_list'], manga_url)
  manga = me.manga
  chapters = me.chapter_list
  ```

  If you are using Mext for one time data collection you could directly pass the arguments given to `populate` to `Mext` directly at initialization.

## Providers

1. MangaDex
2. AsuraScans

...others coming soon

### Mangadex

Get Manga using Manga URL

```python
from mext import Mext

manga_url = 'https://mangadex.org/title/d1c0d3f9-f359-467c-8474-0b2ea8e06f3d/bocchi-sensei-teach-me-mangadex'

me = Mext(['manga'], manga_url) # You'll get back a instance of Mext with Manga data
manga = me.manga
print(manga.to_dict())
```

Get Chapter using Chapter URL

```python
from mext import Mext

chapter_url = 'https://mangadex.org/chapter/e183d3f4-fde0-4288-a1ed-8547490f84b3'

me = Mext(['chapter'], chapter_url) # You'll get back a instance of Mext with Chapter data
chapter = me.chapter
print(chapter.to_dict())
```

Get Chapters List belonging to a manga using Manga URL
```python
from mext import Mext

manga_url = 'https://mangadex.org/title/f7972eed-0040-4aac-b8de-fc99c522c25a/anti-kissmanga-anthology'

me = Mext(['chapter_list'], manga_url) # You'll get back a list of instances of Mext with a list of Chapter data
chapter_list = me.chapter_list
print(chapter_list.to_dict())
```

## Credits

- Mangadex API - [MangaDex.py](https://github.com/Proxymiity/MangaDex.py)
