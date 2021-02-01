'''
Author: William Wright
'''

import re


class clean_description(object):
    '''clean_description docstring'''
    def __init__(self, desc, regex_dict, logger=None):
        self.desc = desc
        self.regex_dict = regex_dict
        self.logger = logger

    def clean(self):
        self.d = self.flight_chars_dict()
        self.desc = self.remove_content()
        self.desc = self.substitution()
        if len(self.d) > 0:
            self.desc = self.add_flight_chars(self.d)
        return self.desc

    def flight_chars_dict(self):
        patterns = [
            'title="speed-(.+?)gif', 'title="glide-(.+?)gif',
            'title="turn-(.+?)gif', 'title="fade-(.+?)gif'
        ]
        cats = ['speed', 'glide', 'turn', 'fade']
        d = {}
        match_test = re.findall(patterns[0], self.desc)
        if len(match_test) == 1:
            for pattern, cat in zip(patterns, cats):
                match = re.findall(pattern, self.desc)
                if len(match) > 0:
                    d[cat] = match[0][:-1]
                else:
                    d[cat] = 'NA'
        else:
            try:
                pattern = '<li.+?Flight Characteristics:(.+?)</li>'
                match = [
                    i.strip()
                    for i in re.findall(pattern, self.desc)[0].split('/')
                ]
                d = {i: j for i, j in zip(cats, match)}
            except IndexError as e:
                try:
                    pattern = '<li.+?Flight characteristics:(.+?)</li>'
                    match = [
                        i.strip()
                        for i in re.findall(pattern, self.desc)[0].split('/')
                    ]
                    d = {i: j for i, j in zip(cats, match)}
                except IndexError as e:
                    pass
                    self.logger.error(
                        str(e) +
                        ' - no "Flight Chars" match in product description')
        return d

    def remove_content(self):
        ''' docstring for remove_content
        - remove "Info about plastic" section
        - remove everything after "more information"
        - remove everything before the first paragraph tag
        '''
        for pattern in self.regex_dict:
            self.desc = re.sub(pattern, self.regex_dict[pattern], self.desc)
        i = self.desc.find('<p>')
        if i == -1:
            pass
        else:
            self.desc = self.desc[i:]
        return self.desc

    def sub_pattern(self, pattern, sub1, sub2, funk):
        '''sub_pattern docstring'''
        pattern_list = re.findall(pattern, self.desc)
        if len(pattern_list) > 0:
            for i, j in zip(pattern_list, [funk(i) for i in pattern_list]):
                try:
                    self.desc = re.sub(sub1.format(i), sub2.format(j),
                                       self.desc)
                except re.error as e:
                    self.logger.error('sub_pattern')
                    self.logger.error(e)

    def substitution(self):
        '''substitution docstring'''
        pattern = '<h3>(.+?)</h3>'
        sub1 = '<h3>{}</h3>'
        sub2 = '<h2>{}</h2>'
        funk = str.title
        self.sub_pattern(pattern, sub1, sub2, funk)

        pattern = '<li>(.+?)</li>'
        sub1 = '<li>{}</li>'
        funk = str.capitalize
        self.sub_pattern(pattern, sub1, sub1, funk)

        pattern = '<p><span style.+?;">([A-Z].+?)</span></p>'
        sub1 = '<p><span style.+?;">{}</span></p>'
        sub2 = '<p>{}</p>'
        funk = str
        self.sub_pattern(pattern, sub1, sub1, funk)

        return self.desc

    def add_flight_chars(self, d):
        '''add_chars docstring
        appends bullet list of flight chars to end'''
        s1 = ' / '.join([d[i] for i in d])
        s2 = ' / '.join([i for i in d])
        s3 = '<li>Flight characteristics: {} ({})</li>'.format(s1, s2)
        s3 = s3.replace('zero', '0')
        s3 = s3.replace('minus', '')
        pattern = '<h2>Specifications</h2> <ul> {}<li>Best'
        self.desc = re.sub(pattern.format(''), pattern.format(s3), self.desc)
        if 'Please note: stamp & exact color may vary' in self.desc:
            self.logger.error(
                '"please note" already present, likely this product id was already cleaned'
            )
            pass
        else:
            note = '<li>Please note: stamp & exact color may vary</li></ul>'
            self.desc = re.sub('</ul>', note, self.desc)
        return self.desc
