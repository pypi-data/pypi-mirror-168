# DBLP ranking using CORE Rank and SJR

## Install

``` bash
pip install get_rankings
```

## Run

```
get_rankings DBLP_URL
```

Gives and overview of a dblp account. The first run will be slow as some data will be cached.

For example

```
get_rankings https://dblp.org/pid/37/2282.html
```

## Usage
```
usage: get_rankings [-h] [--start START] [--end END] [-o output.csv] [-d] url

Get ranking from DBLP and show a small summary

positional arguments:
  url            DBLP url

options:
  -h, --help     show this help message and exit
  --start START  starting year
  --end END      ending year
  -o output.csv  output csv file
  -d             display conference and journal list
```

## Thanks

Thanks for Laurent Reveillere ([dblp_ranker](https://github.com/reveillere/dblp_ranker) and Xavier Blanc [dblp_ranker](https://github.com/xblanc33/dblp_ranker) for their initial version in nodejs.
