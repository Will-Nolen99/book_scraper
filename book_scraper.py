import book_config
import zipfile
from book_reader import BookInfo
from book_reader import BookReader
import json






def main():
    
    # open each epub file
    minute_times = [str(f"0{x}")if x < 10 else str(x) for x in range(60)]
    hour_times = [str(x) for x in range(10)]
    times = minute_times + hour_times
    

    
    full_data_page = {time: [] for time in times}
    
    for (i, book_name) in enumerate(book_config.BOOK_NAMES):
        book_directory = f"books/book{i + 1}"
        
        book_info = BookInfo(book_name, i + 1, book_config.BOOK_START_STOP_PAGES[i][0], book_config.BOOK_START_STOP_PAGES[i][1], book_directory)
        print(book_info)
        book_reader = BookReader(book_info)
        
        book_data = book_reader.read()
        #print(book_data)
        
            
        """
    
    After getting the data from each book they will need post processing. 
    For each number in a sentence they need to be put into a category placing that number somewhere from 00, 01, 02, 03, 04 to 59. and then 1 to 12. 
    Each sentence could be in multiple slots.
    
    Then each entry needs formatted into a dictionary
    
    dictionary where the time numbers are keys and lists of dictionaries with sentences corresponding to those times are values
    
    {
        "00": [{"sentence": sentence, "page": page_num, "book": book}]
        "01": ...
        
        
        
        ...
        "60":[{"sentence": sentence, "page": page_num, "book": book}]
        "1":...
        "9"
        
    }
    
    
    """

        
        for entry in book_data:
            for i in range(len(entry["numbers"])):
                for number in entry["numbers"][i]:
                    for time_number in times:
                        if time_number in number:
                            full_data_page[time_number].append({"sentence": entry["sentence"][i], "page":entry["page_number"], "book":book_name})
                            
                            
        #print(full_data_page['0'])
            
            
    
        
        
        
        
        
        
    with open(f"output/dungeon_crawler_carl.json", 'w') as file:
        json.dump(full_data_page, file, indent=4)
            

    





if __name__ == "__main__":
    main()