import sys
import requests
import bs4
import matplotlib.pyplot as plt
from RequestGuard import RequestGuard
import csv

# Define global variables
args = sys.argv
request_guard = RequestGuard(args[2])


# Parse user input
def parse_commands(user_args):
    if user_args[1] == '-c':
        count_links(sys.argv[2], sys.argv[3], sys.argv[4])
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
def count_links(url, plot_file, csv_file):

    links_dict = {}

    def visit_link(start):
        if request_guard.can_follow_link(start):
            response = requests.get(start)
        else:
            return
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
    visit_link(url)
    # TODO: plot the results from our dictionary
    plt.hist(links_dict)
    plt.savefig(plot_file)
    plt.clf()
    with open(csv_file, 'w') as file2:
        writer = csv.DictWriter(file2, links_dict)
        writer.writerow(links_dict)


def plot_data():
    pass


def manipulate_image(flag):
    pass
