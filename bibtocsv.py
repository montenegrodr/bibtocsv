from __future__ import unicode_literals

import argparse
import os
import codecs
import re
import csv


def main(args):
    if not os.path.exists(args.file):
        raise Exception('{} not exists'.format(args.file))

    pattern = '{(.|\n)*}'
    record = ""
    records = {}
    columns = set()
    with codecs.open(args.file, 'r', encoding='utf-8') as bibtex_file:
        for _, line in enumerate(bibtex_file):
            if line.encode('ascii', 'ignore').strip().startswith('@'):
                line = line.lstrip()
                if record:
                    m = re.search(pattern, record)
                    if m:
                        for i, feat in enumerate(m.group(0).split('\r\n')):
                            feat = feat.strip('{},')
                            if i == 0:
                                id = feat.encode('ascii', 'ignore')
                                records[id] = {}
                            else:
                                s = feat.split(' = ')
                                if len(s) == 2:
                                    key, value = s[0].encode('ascii', 'ignore'), s[1].encode('ascii', 'ignore')
                                    if key not in records[id]:
                                        records[id][key] = value
                                    else:
                                        records[id][key] += ',' + value
                                    columns.add(key)
                    record = ""
            record += line

    with codecs.open(args.output, 'w', encoding='utf-8') as f:
        csvwriter = csv.writer(f, delimiter=str(','))
        csvwriter.writerow(['id'] + list(columns))
        row = []
        for id, values in records.iteritems():
            row.append(id)
            for c in columns:
                if c in values:
                    row.append(values[c])
                else:
                    row.append('')
            csvwriter.writerow(row)
            row = []


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--output', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
