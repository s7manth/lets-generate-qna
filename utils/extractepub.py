from html.parser import HTMLParser
import ebooklib
from ebooklib import epub

FILE_IN = "/Users/s7manth/Documents/fyp/lets-generate-qna/data/nlp_with_pytorch.epub"
FILE_OUT = "/Users/s7manth/Documents/fyp/lets-generate-qna/data/nlp_with_pytorch.txt"

class HTMLFilter(HTMLParser):
  text = ""

  def handle_data(self, data):
    self.text += data

def extract_text_from_epub(file_in, file_out):
  book = epub.read_epub(file_in)
  content = ""

  for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
      body = item.get_body_content().decode()
      f = HTMLFilter()
      f.feed(body)
      content += f.text

  with open(file_out, 'w', encoding='utf-8') as fout:
    fout.write(content)

if __name__ == "__main__":
  extract_text_from_epub(FILE_IN, FILE_OUT)

