import logging
import os
import sys
from bs4 import BeautifulSoup
import re

logging.basicConfig(filename=os.path.join(sys.path[0], 'find_similar_element.log'), format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


class FileUtils(object):

    @staticmethod
    def get_absolute_path(relative_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, relative_path)


class FindSimilarElement:

    @staticmethod
    def main():
        try:
            source_file, target_file, selector = sys.argv[1], sys.argv[2], sys.argv[3]
        except Exception:
            print('Three positional arguments are required: source_file, target_file and element_selector')

        with open(FileUtils.get_absolute_path(source_file)) as s:
            source_file_content = s.read()
            source_file_html = BeautifulSoup(source_file_content, 'html.parser')
            element = source_file_html.select_one(selector)
            if not element:
                msg = 'Could not find element matching selector "{}" on source file'.format(selector)
                print(msg)
                raise Exception(msg)

        with open(FileUtils.get_absolute_path(target_file)) as t:
            target_file_content = t.read()
            target_file_html = BeautifulSoup(target_file_content, 'html.parser')

        criteria = FindSimilarElement.get_lookup_criteria(element)

        elements = target_file_html.find_all(**criteria)

        if not elements:
            print('Could not find any element, please update criteria:\n {}'.format(criteria))
            return

        print('Found matching element(s):')

        for el in elements:
            print('{}\n'.format(FindSimilarElement.xpath_soup(el)))

        print('Used criteria was:\n {}'.format(criteria))


    @staticmethod
    def get_lookup_criteria(element):
        tag = element.name
        first_css_class = element.attrs.get('class', ['btn'])[0]
        href = element.attrs.get('href')
        href_regex = re.compile(href.replace('#', ''))
        has_rel = 'rel' in element.attrs
        # TODO: Obtain this one dynamically too
        onclick = re.compile('ok')

        return {
            'name': tag,
            'attrs': {
                'href': href_regex,
                'class': first_css_class,
                'rel': has_rel,
                'onclick': onclick
            }
        }


    @staticmethod
    def xpath_soup(element):
        """
        Generate xpath from BeautifulSoup4 element
        :param element: BeautifulSoup4 element.
        :type element: bs4.element.Tag or bs4.element.NavigableString
        :return: xpath as string
        :rtype: str
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name
                if siblings == [child] else
                '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)


if __name__ == '__main__':
    """
    Takes a source file and a css selector and finds a similar element on the target file.
    Outputs the html path to the similar element:

    Usage:
    $ python3 find_similar_element.py html/sample-0-origin.html html/sample-1-evil-gemini.html #make-everything-ok-button
    """
    try:
        FindSimilarElement.main()
    except Exception as e:
        logging.exception('Unhandled exception')


