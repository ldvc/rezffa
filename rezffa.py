#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
    Récupération des résultats d'un club
    sur le site de la FFA.
"""

import argparse
import datetime
import json
import requests

from bs4 import BeautifulSoup
from config import PATH

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--numero", help="numéro du club (ex: 069094)",
                    required=True)
args = parser.parse_args()
club_number = args.numero

YEAR = datetime.date.today().year
URL = (
    'http://bases.athle.com/asp.net/liste.aspx'
    '?frmpostback=true&frmbase=resultats&frmmode=1&frmespace=0&frmsaison={}'
    '&frmclub={}'.format(YEAR, club_number)
)

club_name = None
ligue = None
dept = None


def parse_html():
    """
        Sur le site, les résultats sont affichés dans un tableau.
        On le parcours, et on extrait les colonnes qui nous intéressent.

        Retourne: une liste de dict
    """

    global club_name, ligue, dept
    r = requests.get(URL)
    results = []
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        table = soup.find_all('table')[1]
    except IndexError:
        print("No results found for team #{}.".format(club_number))
        results.append({'status': "Error"})
        return results

    for row in table.find_all('tr'):
        # a priori les données intéressantes
        # ne sont que dans les colonnes avec classe datas0
        info = row.find('div', {'class': 'subheaders'})
        if info:
            #['Beaujolais Runners', 'ARA', '069']
            club_name, ligue, dept = [i.strip() for i in info.text.split('|')]
            club_name = club_name.lower().replace(' ', '-')

        cells = row.findAll('td', {'class' : 'datas0'})
        if len(cells) > 1:
            #print(cells)
            #print("La ligne contient {} colonnes".format(len(cells)))
            column_title = [
                'date', 'runner', 'race', 'comment', 'ranking', 'duration',
                'ranking2', 'category', 'ffa_level', 'location'
            ]

            data = [c.text.strip() for c in cells]
            result = dict(zip(column_title, data))
            results.append(result)

    return results


def write_json(data):
    """
        Stocke `data` sous forme de JSON.
    """

    fname = '{}/{}-{}.json'.format(PATH, club_name, YEAR)
    with open(fname, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    #print(URL)
    rez = parse_html()
    write_json(rez)
