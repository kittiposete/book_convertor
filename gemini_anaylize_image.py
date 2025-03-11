import PIL.Image
from google import genai

import ai_key


def analyze_image(path):
    return """This document shows Venn diagrams illustrating set theory concepts like set A, complement of A, disjoint sets, subset, union, and intersection."""
    # this line added for avoiding the API call when testing for saving cost

    image = PIL.Image.open(path)

    client = genai.Client(api_key=ai_key.api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["This is an image of document that will convert to "
                  "brail for blind people with automatic software."
                  "Please write a description of this document in "
                  "very short for this people better understand the "
                  "document before read it.", image])

    response = (response.text)
    print("response: ", response)
    return response


if __name__ == '__main__':
    analyze_image('/Users/kittipos/Developer/book_convertor/Set-Theory.png')
