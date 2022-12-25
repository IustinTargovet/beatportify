def get_third_string_from_href(href: str):
    return href.split("/")[2]


def remove_feat(title):
    words = title.split()

    # Find the index of the word "feat"
    feat_index = words.index("feat")

    # Join the words before "feat" back together, excluding "feat" and the words after it
    new_string = " ".join(words[:feat_index])

    return new_string


def get_title_from_contents(p_tag):
    href = p_tag.contents[1].attrs['href']
    title = get_third_string_from_href(href).replace("-", " ")
    if "feat" in title:
        title = remove_feat(title)
    return title


def get_artist_from_contents(p_tag):
    href = p_tag.contents[1].attrs['href']
    return get_third_string_from_href(href).replace("-", " ")


class Track:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    @classmethod
    def from_title_and_artist(cls, title: str, artist: str):
        return cls(title, artist)

    @classmethod
    def from_title(cls, title: str):
        return cls(title, None)

    @classmethod
    def from_buk_track_meta_parent_element(cls, element):
        title = get_title_from_contents(element.contents[1])
        artist = get_artist_from_contents(element.contents[3])
        return cls(title, artist)

    def __str__(self):
        return f"{self.title} - {self.artist}"
