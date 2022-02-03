import distribute


def test_gather_from_files():
    """Given a directory of JSON files it should be able to identify them
    based on a pattern and convert them into dictionaries."""
    pieces = distribute.gather_from_files()
    assert len(pieces) > 0
    assert type(pieces[0]) == dict


def test_build_front_page():
    """Given one or more dictionaries with some kind of heading,
    a name and body, build a page which displays the headings
    and links to the body."""
    pass


def test_build_piece_page():
    """Given a dictionary with a name and a body, write an HTML file with the
    body as the body and the name as the filename"""
    pass
