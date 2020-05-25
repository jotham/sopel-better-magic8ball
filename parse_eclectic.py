import bs4
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json


def read_contents(filename):
    with open(filename, 'r') as fin:
        return fin.read()


def write_contents(filename, contents, overwrite=True):
    with open(filename, "w") as fout:
        fout.write(contents)


def get_filepath(iching_configuration_number):
    filepath = Path("iching_{}.txt".format(iching_configuration_number))
    return filepath


def check_file_for_number(filepath):
    """ Checks whether or not we have already downlaoded an I Ching configuration """
    print("Checking if {} exists...".format(filepath.absolute()), end="")
    if filepath.exists():
        print("YES")
        return True
    else:
        print("NO")
        return False


def get_text_for_number(eclectic_url_format, iching_configuration_number):

    filepath = get_filepath(iching_configuration_number)
    if not check_file_for_number(filepath):
        eclectic_url = eclectic_url_format.format(iching_configuration_number)
        print("Crawling from {}".format(eclectic_url))

        crawler = requests.get(eclectic_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
            "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*; q=0.8, application/signed-exchange; v=b3; q=0.9",
            'Referer': 'https: // www.eclecticenergies.com/iching/lines'
        })

        crawler.raise_for_status()
        write_contents(filepath.absolute(), crawler.text)

        return crawler.text
    else:
        return read_contents(filepath.absolute())


def extract_article(iching_text):
    soup = BeautifulSoup(iching_text, 'lxml')
    article = soup.find("article")

    return article


def extract_yinyang_from_hexagram_table(hexagram_table):

    yinyang = []
    for hex_children in hexagram_table:
        if type(hex_children) is bs4.element.Tag:
            yinyang.append(hex_children['class'][0])

    return yinyang


def extract_hexagrams(article):

    hexagrams = []
    article_box = article.find("div", {"id": "box"})

    hexagram_id = -1
    for tag in article_box:
        # print(tag.name, " = ", tag)

        if tag.name == "h2":
            hexagram_id += 1

            hexagrams.append({
                'id': hexagram_id,
                'hex_name': tag.string,
                'phrases': [],
                'table': []
            })

        elif tag.name == 'p' and tag.string is not None:
            hexagrams[hexagram_id]['phrases'].append(tag.string)

    hexagram_tables = article.find_all("div", {"class": "hexagram"})
    if len(hexagram_tables) != 2:
        print("WARN: Could not extract 2 hexagram tables. Data will be incomplete")
    else:

        hexagrams[0]['table'] = extract_yinyang_from_hexagram_table(
            hexagram_tables[0])

        hexagrams[1]['table'] = extract_yinyang_from_hexagram_table(
            hexagram_tables[1])

    return hexagrams


def run_import_by_number(eclectic_url_format, iching_config_number):

    iching_text = get_text_for_number(
        eclectic_url_format, iching_config_number)

    article = extract_article(iching_text)
    hexagrams = extract_hexagrams(article)

    print("I Ching: #{}".format(iching_config_number))
    # for h in hexagrams:
    #    print("    Hexagram {}: {}".format((h['id'] + 1), h['hex_name']))

    #    for p in h['phrases']:
    #        print("        \"{}\",".format(p))

    # Print the table structure
    # for i in range(0, 6):
    #    print("    {:4s} -> {:4s}".format(
    #        hexagrams[0]['table'][i],
    #        hexagrams[1]['table'][i]
    #    ))

    write_contents(Path("parsed_{}.json".format(
        iching_config_number)).absolute(), json.dumps(hexagrams, indent=4))

    return hexagrams


def run_import():

    eclectic_url_format = "https://www.eclecticenergies.com/iching/consultation?lns={}"
    iching_config_number = 788995

    gen_numbers = []
    for n1 in range(6, 10):
        for n2 in range(6, 10):
            for n3 in range(6, 10):
                for n4 in range(6, 10):
                    for n5 in range(6, 10):
                        for n6 in range(6, 10):
                            gen_numbers.append(int("{}{}{}{}{}{}".format(
                                n1, n2, n3, n4, n5, n6)))

    start = 0
    length = 4100
    check_numbers = gen_numbers[start:(start+length-1)]

    phrases = []

    print(check_numbers)

    for i in check_numbers:
        iching_config_number = i
        print("Consultation #{}".format(iching_config_number))
        try:
            hexagrams = run_import_by_number(
                eclectic_url_format, iching_config_number)

            for h in hexagrams:
                for p in h['phrases']:
                    phrases.append("{}".format(p))

        except:
            print("Could not extract consultation #{}".format(iching_config_number))

    print("Showing phrases:")
    # phrases = sorted(set(phrases), key=str.lower)
    individual_phrases = []
    for p in phrases:
        separate_phrases = p.split(". ")
        for sp in separate_phrases:
            individual_phrases.append(sp)

    individual_phrases = sorted(set(individual_phrases), key=str.lower)
    for ip in individual_phrases:
        print(ip)

    write_contents("prophecies.json", json.dumps(individual_phrases, indent=4), True)

if __name__ == "__main__":
    print("Importing from eclectic energies")
    run_import()
