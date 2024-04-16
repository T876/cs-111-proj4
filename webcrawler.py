import sys
import requests
import bs4
import matplotlib.pyplot as plt
from RequestGuard import RequestGuard
import csv
import re

# Define global variables
args = sys.argv

# print(final_url)
# request_guard = RequestGuard(final_url[0])


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
    # Construct request guard
    domain_finder = re.compile(r'https://.*?/')
    domain = re.match(domain_finder, url).group()
    rg_obj = RequestGuard(domain)
    links_to_visit = [url]
    link_visits = {}

    def process_url(link):
        if 'http' in link:
            if '#' in link:
                parts = link.split('#')
                return parts[0]
            return link
        if link[0] == '/':
            return domain + link[1:]
        if '#' in link:
            return url
        else:
            # Find the base URL for internal links
            url_match = re.compile(r'(https://.*/).*')
            final_url = re.findall(url_match, args[2])
            return final_url[0] + link

    for link in links_to_visit:
        if rg_obj.can_follow_link(link):
            page = requests.get(link)
            html = bs4.BeautifulSoup(page.text, "html.parser")
            for tag in html.find_all('a'):
                href = tag.get('href')
                to_append = process_url(href)
                if to_append not in links_to_visit:
                    links_to_visit.append(to_append)

                if to_append not in link_visits:
                    link_visits[to_append] = 1
                else:
                    link_visits[to_append] += 1
    print(links_to_visit)
    print(link_visits)

    final_data = list(link_visits.values())
    print(final_data)
    bins = [1, 2, 3, 4, 5, 6]

    plt.hist(final_data, bins=bins)
    plt.savefig(plot_file)
    plt.clf()

    with open(csv_file, "w") as file:
        for x in bins[:-1]:
            count = 0
            for item in final_data:
                if x == item:
                    count += 1
            file.write(f'{float(x)},{float(count)}\n')


def plot_data():
    pass


def manipulate_image(flag):
    pass


parse_commands(args)
