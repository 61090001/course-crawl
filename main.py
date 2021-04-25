import argparse
import logger
import sys

argparser = argparse.ArgumentParser()

argparser.add_argument('-o', '--output', help='outputs log')
argparser.add_argument('-v', '--verbose', action='store_true', help='prints output to stdout')

args = argparser.parse_args()

if __name__ == '__main__':
    if args.output:
        logger.set_output(args.output)
    if args.verbose:
        logger.set_verbose()

    from scraper import Course, Crawler, ICKMITLParser, MITParser, UCBerkeleyParser

    log = logger.get_logger(__name__)

    url = 'https://www.ic.kmitl.ac.th/index.php/programs/undergraduate/software-engineering'
    crawler = Crawler(url=url, parser=ICKMITLParser, max_depth=1)
    crawler.run()
    for item in crawler.get_crawled_data():
       log.debug(f'Item: {len(item.professors)} {str(item)}')

    url = 'http://catalog.mit.edu/subjects/'
    crawler = Crawler(url=url, parser=MITParser, max_depth=1)
    crawler.run()
    for item in crawler.get_crawled_data():
        log.debug(f'Item: {len(item.professors)} {str(item)}')

    url = 'http://guide.berkeley.edu/courses/'
    crawler = Crawler(url=url, parser=UCBerkeleyParser, max_depth=1)
    crawler.run()
    for item in crawler.get_crawled_data():
        log.debug(f'Item: {len(item.professors)} {str(item)}')
