from .text_tilling import auto_text_tilling,text_tilling
from bs4 import BeautifulSoup
from tkitreadability import tkitReadability
"""段落分割，并且对图片进行提取

"""

def auto_cut_markdown(text):
    """
    段落分割，并且对图片进行提取
    The auto_cut_markdown function takes a string of markdown text as input, and returns a list of dictionaries. Each dictionary contains the following key-value pairs:
        - images: A list of image URLs found in the markdown text.
        - text: The plaintext extracted from the markdown body.

    :param text: Used to Specify the text to be processed.
    :return: A generator object.

    :doc-author: Trelent
    """

    Readability = tkitReadability()
    out=text_tilling(text)
    for it in out:
        # print("================================")
        # print(it)
        item={"images":[],"text":''}
        html=Readability.markdown2Html(it)
        soup = BeautifulSoup(html,features="lxml")
        for ii,img in enumerate(soup.find_all('img')):

            img_info={
                "src":img.get("src"),
                "title":img.get("title"),
                "alt":img.get("alt"),
                # "width":img['width'],
                # "height":img['height']
                }
            item['images'].append(img_info)

        text=soup.get_text()
        item['text']=text
        yield item