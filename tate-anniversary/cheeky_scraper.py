import re
import pathlib
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

works_dir = pathlib.Path("works")
img_dir = works_dir / "images"

# create directories for images and markdown files
works_dir.mkdir(exist_ok=True)
img_dir.mkdir(exist_ok=True)

# url of the Tate Modern Anniversary Highlights page
base_url = 'https://www.tate.org.uk'
url = 'https://www.tate.org.uk/visit/tate-modern/anniversary-highlights'

# set up urllib3 PoolManager
http = urllib3.PoolManager()

# fetch the page content
response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')

# find all artwork containers (assuming each artwork is within a specific HTML structure)
# this selector may need to be adjusted based on the actual HTML structure
artworks_divs = soup.select('.card--artwork')  # example class name

for i, art_div in enumerate(artworks_divs):

    # extract id, artist name and artwork title
    title_tag = art_div.select_one('.card__title')  # Example class name
    artist_tag = art_div.select_one('.card__title--artwork-artist')   # Example class name
    if not title_tag or not artist_tag:
        print(f"title or artist not found")
        continue

    title = title_tag.get_text(strip=True)
    artist = artist_tag.get_text(strip=True)
    print(f"{i+1:>2} | {title}, by {artist}")

    card_inner = art_div.select_one(".card__inner")
    if not card_inner or not card_inner.has_attr('data-slide-id'):
        print(f"    card__inner id not found")
        continue

    card_id = card_inner['data-slide-id']

    # now find the corresponding .slick-slide by ID
    slick_slide = soup.select_one(f'.slick-slide[data-slide-id="{card_id}"]')
    if not slick_slide:
        print(f"     slick-slide with id {card_id} not found")
        continue

    source_tag = slick_slide.select_one('picture source')
    if not source_tag or not source_tag.has_attr('srcset'):
        print(f"     source with srcset not found in slick-slide {card_id}")
        continue

    srcset = source_tag['srcset']
    images = [s.strip() for s in srcset.split(',') if s.strip()]
    max_img = max(images, key=lambda s: int(s.split()[-1].replace('w', '')))
    largest_img_link = max_img.split()[0]
    print(f"     largest image: {largest_img_link}")

    # Format filename
    filename_base = f"{artist.lower().replace(' ', '-')}.{title.lower().replace(' ', '-')}"
    image_filename = f"{filename_base}.jpg"
    markdown_filename = f"{filename_base}.md"

    # Download the image
    img_response = http.request('GET', largest_img_link)
    if img_response.status == 200:
        print(f"     image downloaded, writing to {img_dir}/{image_filename}")
        with open(img_dir / image_filename, 'wb') as o:
            o.write(img_response.data)
    else:
        print(f"     image url response status {img_response.status}")

    slick_slide_contents = slick_slide.select_one('.quicklook--description')

    slick_slide_ps = slick_slide_contents.select("p")
    # for p in slick_slide_ps:
    #     print(p)

    markdown_string = f"# {title}\n\n"

    # add the file
    markdown_string +=f"![A picture of {title} by {artist}]({img_dir.stem}/{image_filename})\n\n"

    for p in slick_slide_ps:
        html_string = p.decode_contents().strip()
        # replace <span/em/i>test</span/em/i> by *test*
        md = re.sub(r"<(?:span|em|i)>(.*?)</(?:span|em|i)>", "*\\1*", html_string, flags=re.DOTALL)
        # replace <a href="link">test</a> by [test](link)
        md = re.sub(r"<a\s+href=[\"'](.*?)[\"'].*?>(.*?)</a>", "[\\2](\\1)", md, flags=re.DOTALL)
        markdown_string += f"{md}\n\n"
    # print()
    # print(markdown_string)

    # extract 'Explore Artwork' link
    explore_url = slick_slide_contents.select_one(".btn")['href']
    explore_link = urljoin(base_url, explore_url)
    # print(f"     {explore_link}")

    markdown_string += f"More on the work [here]({explore_link})."

    # save markdown file
    with open(works_dir / markdown_filename, 'w') as o:
        print(f"     description processed, writing to {works_dir}/{markdown_filename}")
        o.write(markdown_string)
