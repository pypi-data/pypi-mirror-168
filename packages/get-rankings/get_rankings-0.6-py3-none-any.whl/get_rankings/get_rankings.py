#!/usr/bin/python3

import os
import requests
import datetime
from dateutil.parser import parse as parsedate
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import json
import argparse

def default_cache():
    return os.environ['HOME']+'/.local/state/pyrank'

def get_dblp(url, cache=True, cache_dir = None):
    if cache_dir is None:
        cache_dir = default_cache()
    _, target = url.split('//')
    filename = '%s/%s' % (cache_dir, target.replace('/', '_'))
    os.makedirs(cache_dir, exist_ok=True)
    if not os.path.exists(filename) or not cache:
        with open(filename, "wb") as file:
            response = requests.get(url)
            data = response.content
            file.write(data)
    else:
        with open(filename, "rb") as file:
            data = file.read()
            
    soup = BeautifulSoup(data, 'html.parser')

    articles = soup.find_all("li", class_="entry")

    res = []
    for a in articles:
        if 'inproceedings' in a['class'] or 'article' in a['class']:
            name = a.find("span", itemprop = 'isPartOf').find("span", itemprop = 'name').text
            year = a.find("span", itemprop = 'datePublished').text
            venue, second_name, _ = a['id'].split('/')
            res.append([venue, name, second_name, year])
    return soup.title.text, res

def get_core_year(year):
    if year >= 2021:
        return 'CORE2021'
    if year >= 2020:
        return 'CORE2020'
    if year >= 2018:
        return 'CORE2018'
    if year >= 2017:
        return 'CORE2017'
    if year >= 2014:
        return 'CORE2014'
    if year >= 2013:
        return 'CORE2013'
    if year >= 2010:
        return 'ERA2010'
    return "CORE2008"

def get_core_rank(name, year):

    source = get_core_year(int(year))
    url = "http://portal.core.edu.au/conf-ranks/?search=%s&by=all&source=%s&page=1" % (name, source)

    response = requests.get(url)
    data = response.content
    cc_soup = BeautifulSoup(data, 'html.parser')
    table = cc_soup.find_all('table')
    if len(table) == 0:
        return None
    df = pd.read_html(str(table))[0]

    for index, row in df.iterrows():
        #print(name, year, '    ', row.Title, row.Acronym, row.Rank)

        if row.Title.lower() == name.lower() or row.Acronym.lower() == name.lower():
            return row.Rank, row.Title, row.Acronym
    return None

def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def list_to_hash(content):
    return {tuple(elem[0]):elem[1] for elem in content}
    
def load_ranking_caches(basename, cache_dir = None):
    if cache_dir is None:
        cache_dir = default_cache()
    core = '%s/%s.json' % (cache_dir, basename)
    if os.path.exists(core):
        with open(core, 'r') as fid:
            #for elem in
            return list_to_hash(json.load(fid))
    return {}

def hash_to_list(content):
    return [[a,content[a]] for a in content] 

def save_ranking_caches(cache, basename, cache_dir = None):
    if cache_dir is None:
        cache_dir = default_cache()
    os.makedirs(cache_dir, exist_ok=True) 
    core = '%s/%s.json' % (cache_dir, basename)
    with open(core, 'w') as fid:
        json.dump(hash_to_list(cache), fid)
        
def get_sjr_in_cache(rankings, str_year):
    year = int(str_year)
    if rankings == []:
        return None
    current = rankings[0]
    for elem in rankings[1:]:
        if year < elem[0]:
            return current
        current = elem
    return current

def get_sjr_rank(name):
    url = "https://www.scimagojr.com/journalsearch.php?q=%s" % name.replace(' ', '+')
    response = requests.get(url)
    data = response.content
    sjr_soup = BeautifulSoup(data, 'html.parser')

    revues = sjr_soup.find('div', class_='search_results')
    dist = -1
    reference = None
    best_name = None
    for revue in revues.find_all('a'):
        tmp = revue.find('span').text
        lev = levenshteinDistanceDP(tmp, name)
        if dist == -1 or lev < dist:
            dist = lev
            best_name = tmp
            reference = "https://www.scimagojr.com/%s" % revue['href']
    if reference is None:
        return []

    response = requests.get(reference)
    data = response.content
    sjr_soup = BeautifulSoup(data, 'html.parser')
    table = sjr_soup.find_all('table')
    if len(table) == 0:
        return []

    df = pd.read_html(str(table))[0]
    df['Rank'] = [int(val[1]) for val in df.Quartile]

    mins = df.groupby('Year').min().Rank
    maxs = df.groupby('Year').max().Rank.to_dict()
    result = []
    for (y, v) in mins.items():
        if v == maxs[y]:
            ranking = 'Q%s' % v
        else:
            ranking = 'Q%s-Q%s' % (v, maxs[y])
        result.append((y, best_name, ranking))

    return result

def main():
    sjr_ranking_caches = load_ranking_caches('sjr')
    core_ranking_caches = load_ranking_caches('core')
    
    parser = argparse.ArgumentParser(description='Get ranking from DBLP and show a small summary')
    parser.add_argument('url', help='DBLP url')
    parser.add_argument('--start', type=int, default = -1, help='starting year')
    parser.add_argument('--end', type=int, default = 10000, help='ending year')
    parser.add_argument('-o', metavar=('output.csv'), default = None, help='output csv file')
    parser.add_argument('-d', action='store_true', help='display conference and journal list')
    args = parser.parse_args()

    url = args.url
    end_year = args.end
    csv_output = args.o
    start_year = args.start
    display_list = args.d
    
    username, elements = get_dblp(url)
    print(username)
    
    result = []
    for venue, name, second_name, year in elements:
        if venue == 'conf':
            if (name, second_name, year) in core_ranking_caches:
                rank = core_ranking_caches[(name, second_name, year)]
            else:
                rank = get_core_rank(name, year)
                if rank is None:
                    rank = get_core_rank(second_name, year)
                core_ranking_caches[(name, second_name, year)] = rank
            if rank is None:
                result.append(['C', name, second_name, int(year), None, None, None])
            else:
                result.append(['C', name, second_name, int(year), rank[1], rank[2], rank[0]])

        else:
            if (name, second_name) in sjr_ranking_caches:
                rankings = sjr_ranking_caches[(name, second_name)]
            else:
                rankings = get_sjr_rank(name)
                sjr_ranking_caches[(name, second_name)] = rankings
            rank = get_sjr_in_cache(rankings, year)
            if rank is None:
                result.append(['J', name, second_name, int(year), None, None, None])
            else:
                result.append(['J', name, second_name, int(year), rank[1], None, rank[2]])
    save_ranking_caches(sjr_ranking_caches, 'sjr')
    save_ranking_caches(core_ranking_caches, 'core')
    
    df = pd.DataFrame(result, columns=['type', 'name', 'short', 'year', 'longname', 'acronym', 'rank'])

    if start_year != -1 :
        print('Starting year', start_year)
    else:
        print('Starting year', min(df['year']))
    
    if end_year != 10000:
        print('Ending year', end_year)
    else:
        print('Ending year', max(df['year']))

    selection = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    print('Not found', 
          len(selection) - selection['rank'].count(), 
          'out of a total of', 
          len(selection))

    
    evaluation = selection.groupby('rank').count()
    print(evaluation.drop(['name', 'short', 'year', 'longname', 'acronym'], axis=1).rename(columns={'type':'number'}))
    
    if not csv_output is None:
        selection.to_csv(csv_output, index=False)
    
    if display_list:
        pd.set_option('display.max_rows', len(selection))
        print(selection)
    
if __name__ == '__main__':
    main()
    
