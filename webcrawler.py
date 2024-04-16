import sys
import requests
import bs4
import matplotlib.pyplot as plt
from RequestGuard import RequestGuard
import csv
import re

# Define global variables
args = sys.argv
url_match = re.compile(r'(https://.*/).*')
final_url = re.findall(url_match, args[2])
print(final_url)
request_guard = RequestGuard(final_url[0])


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
    #
    # links_dict = {}
    # print(request_guard.domain)
    #
    # def visit_link(start):
    #
    #      # Get the URL, construct bs4 object
    #     response = requests.get(start)
    #     print('good')
    #     soup = bs4.BeautifulSoup(response.content, 'html.parser')
    #
    #     # Build list of links to visit
    #     links_to_visit = []
    #     for tag in soup.find_all('a', href=True):
    #         print('hit')
    #         # partialUrlMatch = re.compile(r'.*\.html')
    #         if 'https://' not in tag['href']:
    #             to_visit = final_url[0] + tag['href']
    #         else:
    #             to_visit = tag['href']
    #         print(to_visit)
    #         print(request_guard.can_follow_link(to_visit))
    #         if request_guard.can_follow_link(to_visit):
    #             links_to_visit.append(to_visit)
    #     print(links_to_visit)
    #
    #
    #
    #     for thing in links_to_visit:
    #         # TODO: Check if the link is forbidden, stop if it is
    #         print(thing)
    #         if thing in links_dict:
    #             links_dict[thing] += 1
    #         else:
    #             links_dict[thing] = 1
    #             visit_link(thing)
    # # TODO: plot the results from our dictionary
    # visit_link(url)
    # print(links_dict)
    #
    # plt.hist(links_dict)
    # plt.savefig(plot_file)
    # plt.clf()
    # with open(csv_file, 'w') as file2:
    #     writer = csv.DictWriter(file2, links_dict)
    #     writer.writerow(links_dict)


def plot_data():
    pass


def manipulate_image(flag):
    pass

parse_commands(args)
