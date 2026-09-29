import book_config
from dataclasses import dataclass
from contextlib import suppress
import re



# Pass 2: extract individual numbers/times from a sentence
NUMBER_PATTERN = re.compile(
    r'\b((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(?:st|nd|rd|th)?'
    r'(?:\s*:\s*\d{2}(?::\d{2})?)?\b'
)


# Pass 1: split text into sentences while protecting decimal points
# and times from being treated as sentence endings.
SENTENCE_PATTERN = re.compile(
    r'(?=[^.!?]*\d)'
    r'(?:(?![.!?]|\d+\.\d+|\d+:\d+(?::\d+)?(?:st|nd|rd|th)?)[\s\S]'
    r'|\d+\.\d+'
    r'|\d+:\d+(?::\d+)?)'
    r'+[.!?]'
)


def extract_numeric_sentences(text):
    results = {"sentence":[], "numbers":[]}

    for sentence_match in SENTENCE_PATTERN.finditer(text):
        sentence = sentence_match.group(0).strip()

        numbers = NUMBER_PATTERN.findall(sentence)

        if numbers and len(sentence) > 3: # >3 removes some artifacts from the OCR of the book
#
            results["sentence"].append(sentence)
            results["numbers"].append(numbers)

    return results

@dataclass
class BookInfo:
    name: str
    book_num: int
    start_page: int
    end_page: int
    path: str


class BookReader:
    def __init__(self, book: BookInfo):
        self.book = book
        
    def read(self):
        data = []
        for page_number in range(self.book.start_page, self.book.end_page + 1):
            page_path = f"{self.book.path}/page_{page_number}.html"
            #print(page_path)
            with suppress(FileNotFoundError):
                with open(page_path, 'r', encoding='utf-8') as page:
                    content = page.readlines()
                    book_data = self._parse(content)
                    if book_data['sentence']:
                        data.append(book_data)
                    
                    
        return data
    
        
        
    def _parse(self, content: str):
        
        page_number_string = content[book_config.TITLE_PAGE_TAG - 1]
        #print(page_number_string)
        page_number_string = page_number_string.replace("<title>Page ", "")
        page_number_string = page_number_string.replace("</title>", "")
        page_number_string = page_number_string.strip()
        page_content_string = content[book_config.P_TAG - 1]
        page_content_string = page_content_string.replace("OceanofPDF.com", "")
        page_content_string = page_content_string.replace("<p>", "")
        page_content_string = page_content_string.replace("</p>", "")

        
        #print(page_content_string)
        
        number_data = extract_numeric_sentences(page_content_string)
        
        #numerics = re.findall("(?i)(?=[^.!?]*\d)(?:(?![.!?](?!\d)|\d+\.\d+|\d+:\d+(?::\d+)?)[\s\S])+[.!?]", page_content_string)
        #numerics = re.findall("(?=[^.!?]*\d)[^.!?]*[.!?]", page_content_string)
        #print(numerics)
        if number_data["sentence"]:
            number_data['page_number'] = page_number_string
            #print(number_data)
            
        return number_data
        
    
    