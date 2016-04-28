import json
import sys


def parse(json_file_path):
    ''' add nodes based on scraped json '''
    with open(json_file_path) as data_file:
        data = json.load(data_file)

        entries = {}
        for demon, dates in data.items():
            key = '%d,%d' % (min(dates), max(dates))
            entries[key] = entries[key] + [demon] if key in entries else [demon]

        for dates, demons in entries.items():
            dates = dates.split(',')
            print "%s, %s, %s" % ('/'.join(demons), dates[0], dates[1])
if __name__ == '__main__':
    parse(sys.argv[1])

