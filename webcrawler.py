import sys
import requests
import bs4
import matplotlib
from RequestGuard import RequestGuard

# Define global variables
args = sys.argv
request_guard = RequestGuard(args[2])


# Parse user input
def parse_commands(user_args):
    if user_args[1] == '-c':
        count_links(sys.argv[2])
    elif user_args[1] == '-p':
        plot_data()
    elif user_args[1] == '-i':
        if user_args[3] == '-s':
            manipulate_image(user_args[3])
        elif user_args[3] == '-p':
            manipulate_image(user_args[3])
        elif user_args[3] == '-i':
            manipulate_image(user_args[3])
    else:
        return False


# Main functions
def count_links(url):

    links_dict = {}
    def visit_link(start):
        response = requests.get(start)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        # Build list of links to visit
        links_to_visit = []
        for tag in soup.find_all('a', href=True):
            links_to_visit.append(tag['href'])

        for url in links_to_visit:
            # TODO: Check if the link is forbidden, stop if it is
            if links_dict[url]:
                links_dict[url] += 1
            else:
                links_dict[url] = 1
                visit_link(url)
    # TODO: Call helper
    # TODO: plot the results from our dictionary



def plot_data():
    pass


def manipulate_image(flag):
    pass



