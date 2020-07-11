# MusicianFamilyTree
A galaxy of 6491 musicians and their pupils, showing the complicated web of the history of music. 

## Overview
* The code scrapes data from Wikipedia, from the articles listing *music students by teacher* (e.g, 
[from A to B](https://en.wikipedia.org/wiki/List_of_music_students_by_teacher:_A_to_B)), using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Requests](https://requests.readthedocs.io/en/master/) 
modules respectively). 
* This was originally scraped into a csv format, with the format:

| Line   |                |                |                |                |
| -------|:--------------:|:--------------:|:--------------:|:--------------:|
| 1      | teacher_name   |                |                | ...            |
| 2      | teacher_href   |                |                | ...            |
| 3      | pupil_name_0   | pupil_name_1   | pupil_name_2   | ...            |
| 4      | pupil_href_0   | pupil_href_1   | pupil_href_2   | ...            |
| 5      |                |                |                |                |

* Then, the wonderful [NetworkX](https://networkx.github.io/documentation/stable/) module is used to create a
graph object, and [MatPlotLib](https://matplotlib.org/) is used to create beautiful styling. 
