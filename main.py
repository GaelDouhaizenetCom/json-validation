from pydantic import BaseModel, HttpUrl, conlist, constr
from typing import List, Optional
from datetime import datetime
import json
from pprint import pprint

"""
This is a script demonstrating json validation with pydantic.
"""


# Validation classes must inherit from pydantic.BaseModel
class Photo(BaseModel):
    """
    This class is meant to be nested in the main class for further validation.
    """
    # Fields are simply type-hinted like in plain python
    caption: Optional[str]
    url: HttpUrl


class Article(BaseModel):
    """
    This is the main validation class
    """
    id: int
    source: str
    timestamp: datetime
    # 'constr' stands for 'constrained string' and enables specific controls on the string
    title: constr(max_length=90)
    text: str
    tags: List[str]
    # Note the usage of the above-declared Photo class
    photos: Optional[List[Photo]]
    # Constrained list
    authors: conlist(item_type=str, min_items=1)
    links: Optional[List[HttpUrl]]


if __name__ == '__main__':

    print('Example of successful validation')

    # Load an article with valid json formatting
    with open('./valid_article.json', 'r') as f:
        valid_json = json.load(f)

    # Instantiate an Article object with the dictionary to perform validation (the dict must be unpacked as kwargs)
    valid_article = Article(**valid_json)

    # json keys have become Article properties
    print(valid_article.title)
    print(valid_article.tags)

    # The object can be converted back to a dictionary.
    # Note that omitted 'Optional' fields are present with value None.
    # Also note how timestamp and urls have been transformed.
    valid_dict = valid_article.dict()
    pprint(valid_dict, indent=4)

    print(f'\n{"*" * 80}\nExample of failed validation')

    # Load an article with an invalid json.
    with open('./invalid_article.json', 'r') as f:
        invalid_json = json.load(f)

    # On validation, an exception is raised with detail of issues.
    try:
        invalid_article = Article(**invalid_json)
    except Exception as e:
        print(e)

    # By examining the error output, some corrective action might be considered.
    invalid_json['id'] = 2
    invalid_json['title'] = invalid_json['title'][:87] + '...'

    corrected_article = Article(**invalid_json)

    print(f'\n{"*" * 80}\nCorrected article')
    # Let's omit the article text to limit output
    pprint(corrected_article.dict(exclude={'text'}))
