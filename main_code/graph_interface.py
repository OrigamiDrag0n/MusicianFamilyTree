###MusicFamilyTree, a project by OrigamiDrag0n, 08/07/20 - 10/07/20

##Importing the data from Wikipedia, the source of all good things
##Using text editing and BeautifulSoup to parse the dataset cleanly,
##and NetworkX to display the plot.

##The code here, since it uses matplotlib, works best if launched
##from terminal.

import requests
from bs4 import BeautifulSoup
from progressbar import progressbar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors, cm
import pylab

GRAPH = nx.DiGraph()

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
        for element in progressbar(elements):
            teacher_string, pupils_string = element.split('</h3>')
            teacher_element, pupils_element = BeautifulSoup(teacher_string, 'html.parser'), BeautifulSoup(pupils_string.split('<h2>')[0], 'html.parser')
            teacher_link = teacher_element.find('a')
            teacher = teacher_link.contents[0].strip()
            pupil_links = [element.find('a') for element in pupils_element.findAll('li')]
            pupil_names = [link.contents[0].strip() for link in pupil_links if link != None]
            for pupil in pupil_names:
                GRAPH.add_edge(teacher, pupil)
    
def display_graph(colormap):

    '''
    Displays the graph, through use of NetworkX. The code for the
    hover element was adapted from https://stackoverflow.com/questions/
    61604636/adding-tooltip-for-nodes-in-python-networkx-graph
    '''

    print(f'{len(GRAPH.nodes)} musicians identified')
    print(f'{len(GRAPH.edges)} connections identified')
    print(f'{round(len(GRAPH.edges)/len(GRAPH.nodes), 2)} pupils per given teacher')
    print('Please wait a moment while the graph renders...')
    
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.set_facecolor('black')
    ax.axis('off')
    fig.set_facecolor('black')

    def size(degree):
        return 2*degree**1.5

    def color(degree):
        return degree**0.5
    
    pos = nx.spring_layout(GRAPH)
    degrees = dict(GRAPH.degree)
    low, high = color(min(degrees.values())), color(max(degrees.values()))
    norm = colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=eval(f'cm.{colormap}'))
    nodes = nx.draw_networkx_nodes(GRAPH, pos, ax = ax,
                                   nodelist=degrees.keys(),
                                   node_size=[size(v) for v in degrees.values()],
                                   node_color=[mapper.to_rgba(color(i)) for i in degrees.values()])
    nx.draw_networkx_edges(GRAPH, pos, ax = ax,
                           edge_color='w',
                           arrows=False,
                           width = 0.1)
    annot = ax.annotate('', xy=(0,0), xytext=(20,20),textcoords='offset points',
                    bbox=dict(boxstyle='round', fc='w'),
                    arrowprops=dict(arrowstyle='->'))
    annot.set_visible(False)

    graph_nodes = list(GRAPH.nodes)
    
    def update_annot(ind):
        node = graph_nodes[ind['ind'][0]]    #Fix this!!!
        xy = pos[node]
        annot.xy = xy
        text = f'{node}\nTaught {GRAPH.out_degree(node)}\nTaught by {GRAPH.in_degree(node)}'
        annot.set_text(text)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = nodes.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hover)

    plt.tight_layout()
    pylab.show()
    plt.savefig(f'graph_{colormap}.png', bbox_inches='tight')
    
if __name__ == '__main__':
    
    import_musicians('A', 'B')
    import_musicians('C', 'F')
    import_musicians('G', 'J')
    import_musicians('K', 'M')
    import_musicians('N', 'Q')
    import_musicians('R', 'S')
    import_musicians('T', 'Z')
    
    display_graph('jet')            #'viridis' and 'autumn' are also nice!
