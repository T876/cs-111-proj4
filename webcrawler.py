import sys
import requests
import bs4
import matplotlib.pyplot as plt
from RequestGuard import RequestGuard
import re
import numpy as np
from image_processing import sepia, grayscale, flipped, mirrored
import shutil


# Parse user input
def parse_commands(user_args):
    # Checks if the flag is valid and that the right number of arguments have been given to run
    if not check_valid(user_args):
        print('Invalid Arguments: Review flag or that there are all 4 positional arguments')
        return
    # Runs the count links function
    if user_args[1] == '-c':
        count_links(sys.argv[2], sys.argv[3], sys.argv[4])
    # Runs the extract and plot data function
    elif user_args[1] == '-p':
        plot_data(sys.argv[2], sys.argv[3], sys.argv[4])
    # Allows for selection of image filter
    elif user_args[1] == '-i':
        # Activates the sepia filter
        if user_args[4] == '-s':
            manipulate_image(sys.argv[2], user_args[4], user_args[3])
        # Activates the grayscale filter
        elif user_args[4] == '-g':
            manipulate_image(user_args[2], user_args[4], user_args[3])
        # Activates the vertical flip filter
        elif user_args[4] == '-f':
            manipulate_image(user_args[2], user_args[4], user_args[3])
        # Activates the mirror (horizontal flip) filter
        elif user_args[4] == '-m':
            manipulate_image(user_args[2], user_args[4], user_args[3])
        # Errors out if secondary flag is invalid
        else:
            print('Invalid Arguments: Secondary flag is not valid')
            return


def check_valid(commands):
    # Checks if there are the required number of arguments
    if len(commands) == 5:
        # Checks if the initial flag is valid
        if commands[1] in ['-c', '-p', '-i']:
            return True
    return False


def make_rg_obj(url):
    # Get the domain and prepare the request guard object
    domain_finder = re.compile(r'https://.*?/')
    domain = re.match(domain_finder, url).group()
    rg_obj = RequestGuard(domain)
    return rg_obj, domain


def make_soup_obj(rg_obj, link):
    # Uses Request Guard to verify link is not forbidden to access
    if rg_obj.can_follow_link(link):
        # Get the HTML and return the usable soup object
        page = requests.get(link)
        html = bs4.BeautifulSoup(page.text, "html.parser")
        return html


def process_url(link, og_domain, the_current_url):
    # Get the link into the processable format
    # Return complete links
    if link.startswith('http') or link.startswith('https'):
        # Remove ending fragments from completed links
        if '#' in link:
            parts = link.split('#')
            return parts[0]
        return link
    # Process within a domain
    if link.startswith('/'):
        return og_domain + link[1:]
    # Process link fragments
    if link.startswith('#'):
        return the_current_url
    else:
        # Find the base URL for internal links
        url_match = re.compile(r'(https://.*/).*')
        final_url = re.match(url_match, args[2]).group(1)
        return final_url + link


# Main functions
def count_links(url, plot_file, csv_file):
    # Helper functions
    def make_links_to_visit(soup_obj, og_domain, the_current_url):
        # Find all the links on a page
        for tag in soup_obj.find_all('a'):
            href = tag.get('href')
            # Get the link into a usable format
            to_append = process_url(href, og_domain, the_current_url)
            # Add to the list of links that must be visited
            links_to_visit.append(to_append)

    def update_link_visits(link):
        # Add links to the dictionary the first time they are visited
        if link not in link_visits:
            link_visits[link] = 0
        # Update the number of times links are visited each time they are visited
        link_visits[link] += 1

    def make_hist(visits, o_plot_file):
        # Get the number of visits information from the link_visits list
        final_data = list(visits.values())
        # Get the range of bins for the histogram by getting arranging the final visit counts and going from one to +2
        # of the highest value in the list
        bins = np.arange(1, max(final_data) + 2)
        # Create the histogram using the created list of values and the list of bins
        plt.clf()
        plt.hist(final_data, bins=bins)
        plt.savefig(o_plot_file)
        plt.clf()
        # Return the values used in the histogram for use in the csv
        hist, bin_edges = np.histogram(final_data, bins=bins)
        return hist, bin_edges

    def make_csv_output(hist, bin_edges, o_csv_file):
        # Open the output file and prepare it to write to a csv file
        with open(o_csv_file, 'w') as file:
            for x in range(len(hist)):
                # Writing the start of the bin and the count as a csv float pair
                file.write(f'{float(bin_edges[x])},{float(hist[x])}\n')

    # Main body
    r_obj, domain = make_rg_obj(url)
    # Prepare lists and dictionary
    links_to_visit = [url]
    link_visits = {}
    visited_urls = set()
    # Initialize counter loop
    i = 0
    while i < len(links_to_visit):
        # Verify what link is being processed
        current_url = links_to_visit[i]
        # Add or update the dictionary
        update_link_visits(current_url)
        # Verifies link is not on the robots.txt
        if current_url not in visited_urls:
            temp = True
            for forbidden_url in r_obj.forbidden:
                if forbidden_url in current_url:
                    temp = False
            if temp:
                html = make_soup_obj(r_obj, current_url)
            else:
                html = None
            # Update lists and dictionary
            if html is not None:
                make_links_to_visit(html, domain, current_url)
            visited_urls.add(current_url)
        # Increase counter for the loop
        i += 1
    # Make histogram and get the values for the csv files
    histo, edges = make_hist(link_visits, plot_file)
    # Create csv output
    make_csv_output(histo, edges, csv_file)


def plot_data(url, data_plot_file, data_csv):
    r_obj, domain = make_rg_obj(url)
    try:
        requests.get(url)
    except:
        print(f'{url} doesn\'t exist')
    html = make_soup_obj(r_obj, url)
    table = html.find(id='CS111-Project4b')
    rows = table.find_all('tr')
    x_vals = []
    points_1 = []
    points_2 = []
    points_3 = []
    points_4 = []
    for row in rows:
        data = row.find_all('td')
        x_val = data[0]
        y_vals = data[1:]
        x_vals.append(float(x_val.get_text()))
        points_1.append(float(y_vals[0].get_text()))
        points_2.append(float(y_vals[1].get_text()))
        if len(y_vals) > 2:
            points_3.append(float(y_vals[2].get_text()))
        if len(y_vals) > 3:
            points_4.append(float(y_vals[3].get_text()))

    # Plot points
    plt.plot(x_vals, points_1, 'b')
    plt.plot(x_vals, points_2, 'g')
    if len(points_3) > 0:
        plt.plot(x_vals, points_3, 'r')
    if len(points_4) > 0:
        plt.plot(x_vals, points_3, 'k')
    plt.savefig(data_plot_file)
    plt.clf()

    # Make a CSV with the points
    with open(data_csv, 'w') as file:
        for x in range(len(x_vals)):
            # Writing the start of the bin and the count as a csv float pair
            if len(points_4) > 0:
                file.write(f'{x_vals[x]},{points_1[x]},{points_2[x]},{points_3[x]},{points_4[x]}\n')
            elif len(points_3) > 0:
                file.write(f'{x_vals[x]},{points_1[x]},{points_2[x]},{points_3[x]}\n')
            else:
                file.write(f'{x_vals[x]},{points_1[x]},{points_2[x]}\n')


def manipulate_image(url, flag, output_prefix):
    r_obj, domain = make_rg_obj(url)
    html = make_soup_obj(r_obj, url)
    image_tags = html.find_all('img', )
    image_half_urls = []
    image_urls = []
    for tag in image_tags:
        image_half_urls.append(tag['src'])
    for image in image_half_urls:
        image_urls.append(process_url(image, domain, image))
    for i in range(len(image_half_urls)):
        output_filename = output_prefix + image_half_urls[i]
        response = requests.get(image_urls[i], stream=True)
        with open(output_filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        if flag == '-g':
            grayscale(output_filename, output_filename)
        if flag == '-f':
            flipped(output_filename, output_filename)
        if flag == '-m':
            mirrored(output_filename, output_filename)
        if flag == '-s':
            sepia(output_filename, output_filename)


# Define global variables
args = sys.argv
# Run commands
parse_commands(args)
