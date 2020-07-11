###MusicFamilyTree, a project by OrigamiDrag0n, 08/07/20 - 

##Importing the data from Wikipedia, the source of all good things
##Using text editing and BeautifulSoup to parse the dataset cleanly
##Each element will be of the form
'''
`teacher_name`
`teacher_href`
`pupil_name_0`, `pupil_name_1`, ...
`pupil_href_0`, `pupil_href_1`, ...

'''
##I have chosen not to pickle the data, since this will make it harder
##to retrieve for other programs which might need to analyse this.
##Furthermore, parsing the data is quick, so it probably won't be too much
##faster than unpickling the data.

import requests
from bs4 import BeautifulSoup
from progressbar import progressbar

RAW_DATA = './raw_data.txt'
ENCODING = 'utf-8'

def import_musicians(start, stop):

    '''
    Imports all musicians on the Music Students By Teacher Wikipedia page,
    with initials between `start` and `stop` and writes them to a text file.
    '''
    
    url = f'https://en.wikipedia.org/wiki/List_of_music_students_by_teacher:_{start}_to_{stop}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', {'id': 'mw-content-text'})
        elements = main_content.prettify().split('<h3>')[1:]
        elements[-1] = elements[-1].split('<div aria-labelledby="toc-title-text"')[0]
        with open(RAW_DATA, 'a+', encoding = ENCODING) as write_file:
            for element in progressbar(elements):
                teacher_string, pupils_string = element.split('</h3>')
                teacher_element, pupils_element = BeautifulSoup(teacher_string, 'html.parser'), BeautifulSoup(pupils_string.split('<h2>')[0], 'html.parser')

                teacher_link = teacher_element.find('a')
                teacher_name = teacher_link.contents[0].strip()
                teacher_href = 'https://en.wikipedia.org/' + teacher_link['href']
                write_file.write(f'{teacher_name}\n')
                write_file.write(f'{teacher_href}\n')
                
                pupil_links = [element.find('a') for element in pupils_element.findAll('li')]
                pupil_names = [link.contents[0].strip() for link in pupil_links if link != None]
                pupil_hrefs = ['https://en.wikipedia.org' + str(link['href']) for link in pupil_links if link != None and link['href'] != None]
                write_file.write(f'{", ".join(pupil_names)}\n')
                write_file.write(f'{", ".join(pupil_hrefs)}\n\n')            

if __name__ == '__main__':
    
    import_musicians('A', 'B')
    import_musicians('C', 'F')
    import_musicians('G', 'J')
    import_musicians('K', 'M')
    import_musicians('N', 'Q')
    import_musicians('R', 'S')
    import_musicians('T', 'Z')
