from bib_process import bib_processer
from spider import Spider
from config import SCRAP_API_KEY
import argparse


def check(args):
    bib = bib_processer(args.bib_file_path)
    entries = bib.get_entries()

    print('='*50 + "\nCheck Fake Citations Settings\n" + '='*50)
    print(f"Bibliography file path: {args.bib_file_path}")
    print(f"Output file path: {args.output_path}")
    print(f"Number of entries in bibliography: {len(entries)}")
    print('='*50)
    print()

    sp = Spider()

    output_file = args.output_path
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('Index,Status,Title,PDF link\n')
    
    for i,entry in enumerate(entries):
        print(f"Searching for: {entry['title']}")
        res = sp.search(entry['title'])
        match_mark = False
        for item in res:
            if item['title'].strip() == entry['title'].strip():
                match_mark = True
                res_block = item.get('resources', {})
                pdf_link = res_block.get('link', 'No PDF link available')
                break
        if match_mark:
            with open('results.txt', 'a', encoding='utf-8') as f:
                f.write(f"{i+1},OK,{entry['title']},{pdf_link}\n")
        else:
            with open('results.txt', 'a', encoding='utf-8') as f:
                f.write(f"{i+1},Fake,{entry['title']},\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fake Citation Check Tool')

    # basic config
    parser.add_argument('--bib_file_path', type=str, required=True, default='./ref.bib', help='Path to the bibliography file')
    parser.add_argument('--output_path', type=str, required=False, default='./results.csv', help='Path to the output file')
    
    args = parser.parse_args()

    check(args)