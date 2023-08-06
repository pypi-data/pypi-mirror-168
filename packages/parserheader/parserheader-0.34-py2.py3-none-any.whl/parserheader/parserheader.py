#!/usr/bin/env python

from __future__ import print_function

import re
import click
from pprint import pprint
try:
    from pause import pause
except:
    def pause(*args, **kwargs):
        input("enter to continue")
try:
    from pydebugger.debug import debug
except:
    def debug(*args, **kwargs):
        for i in kwargs:
            print(i, "=", kwargs.get(i), type(kwargs.get(i)))

class Parserheader(object):

    headers = {}

    def __init__(self, headers = None):
        self.headers = headers or self.headers
        super(Parserheader, self)

        self.headers = self.parserheader(self.headers)

        for i in list(self.headers.keys()):
            key = "_".join([x.title() for x in re.split("-", i)])
            value = self.headers.get(i)
            if not key.lower() == 'user-agent':
                setattr(self, key, value)
                setattr(self, key.lower(), value)

    @classmethod
    def __str__(self):
        return str(self.headers)

    def __repr__(self):
        return str(self.headers)

    @classmethod
    def __setitem__(self, key, value):
        if not key.lower() in [i.lower() for i in list(self.headers.keys())]:
            key = "-".join([x.title() for x in re.split("-|_", key)])
            self.headers.update({key:value})
        else:
            for i in list(self.headers.keys()):
                if key.lower() == i.lower():
                    self.headers.update({i:value})

        return self

    @classmethod
    def __getitem__(self, key):
        if key.lower() in [i.lower() for i in list(self.headers.keys())]:
            index = [i.lower() for i in list(self.headers.keys())].index(key.lower())
            key = list(self.headers.keys())[index]
            return self.headers.get(key)
        return ''

    def __delitem__(self, key):
        if key.lower() in [i.lower() for i in list(self.headers.keys())]:
            del self.headers[key]
        return self

    def __len__(self):
        return len(list(self.headers.keys()))

    def __contains__(self, key):
        if key.lower() in [i.lower() for i in list(self.headers.keys())]:
            # return self.headers.get(key)
            return True
        return False

    def __add__(self, data):
        if isinstance(data, dict):
            check = list(filter(lambda k: k in [i.lower() for i in list(data.keys())], [i.lower() for i in list(self.headers.keys())]))
            if not check:
                self.headers.update(data)
            else:
                for i in data:
                    self.__setitem__(i, data.get(i))
            return self
        elif isinstance(data, Parserheader):
            return self.__add__(data.headers)

        print("data is not dictionary or Parserheader object !")
        return self

    def __iadd__(self, data):
        return self.__add__(data)

    def __call__(self, **kwargs):
        if kwargs:
            for i in kwargs:
                key = "-".join([x.title() for x in re.split("-|_", i)])
                value = kwargs.get(i)
                self.__setitem__(key, value)

        return self.headers

    @classmethod
    def setCookies(self, cookies_str_or_dict, dont_format=False, **kwargs):
        cookie_dict = {}
        cookie_str = ''
        # if not cookies_str_or_dict:
        #     cookies_str_or_dict = "ym_uid=1532996994661863820; _ym_d=1532996994; _ym_isad=2; tr=2 4 6 8 9 10"
        if __name__ == '__main__':
            click.secho("Example Input string cookies:", fg='black', bg='cyan')
            print((cookies_str_or_dict or ''))

        if isinstance(cookies_str_or_dict, str) or isinstance(cookies_str_or_dict, unicode):
            cookies_str_or_dict = re.split("; ", cookies_str_or_dict)
            for i in cookies_str_or_dict:
                if i.strip():
                    key,value = str(i).strip().split("=")
                    cookie_dict.update({key.strip():value.strip()})
            

        elif isinstance(cookies_str_or_dict, dict):
            for i in cookies_str_or_dict:
                cookie_str += str(i) + "=" + cookies_str_or_dict.get(i) + "; "
            cookie_str = cookie_str.strip()
            
            if cookie_str:
                if cookie_str[-1] == ";":
                    cookie_str = cookie_str[:-1]
            cookie_dict = cookies_str_or_dict

        if not cookie_str:
            cookie_str = cookies_str_or_dict

        if __name__ == '__main__':
            click.secho("Example Output Dictionary cookies:", fg='black', bg='green')
            print((cookie_dict or ''))
            print("-" * (click.get_terminal_size()[0] - 1))
            print("\n")
        
        if kwargs:
            for i in kwargs:
                if not dont_format:
                    key = "-".join([x for x in re.split("_", i)])
                else:
                    key = str(i)
                value = kwargs.get(i)
                cookie_dict.update({key:value})
            return self.setCookies(cookie_dict)
        return cookie_dict, cookie_str

    @classmethod
    def parserheader(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        # cookies_dict_str example: _ym_uid=1532996994661863820; _ym_d=1532996994; _ym_isad=2;
        #
        string_headers_example = """
        Host: ''
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Referer: ''
        Accept-Encoding: gzip, deflate
        Accept-Language: en-US,en;q=0.9
        Cookie: ''
        """
        headers_dict = {}
        string_headers = string_headers or self.headers or string_headers_example

        if isinstance(string_headers, bytes):
            string_headers = string_headers.decode('utf-8')

        if isinstance(string_headers, unicode):
            string_headers = string_headers.encode('utf-8')
        
        if isinstance(string_headers, str):
            data = re.split("\n|\r", string_headers)
            
            data = [i.strip() for i in data]
            
            data = list(filter(None, data))
            
            
            for i in data:
                key, value = '', ''
                if ": " in i:
                    data_split = re.split(": ", i)
                    if len(data_split) == 2:
                        key, value = data_split
                        key = key.strip()
                        value = value.strip()
                        # if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
                        #     value = value[1:-1]
                        if value == "''" or value == '""': value = ''
                        key = "-".join([x.title() for x in re.split("-|_", key)])
                        headers_dict.update({key: value,})
                else:
                    if ":" in i:
                        data_split = re.split(":", i)
                        key, value = data_split[0], ":".join(data_split[1:])
            
        elif isinstance(string_headers, dict):
            headers_dict = string_headers

        if kwargs:
            for i in kwargs:
                # key = "-".join([x.title() for x in re.split("_", i)])
                key = "-".join([x.title() for x in re.split("-|_", i)])
                value = kwargs.get(i)
                headers_dict.update({key:value})
 
        self.headers = headers_dict
 
        if cookies_dict_str:
            self.__setitem__('cookie', self.setCookies(cookies_dict_str)[1])
        
        return self.headers

    @classmethod
    def useragent(self, user_agent = None):
        '''Get User-Agent
        
        Get or Set user agent string from/to header (parserHeader Object)
        
        Arguments:
            user_agent (str) set update `User-Agent` to self.headers
        '''

        if isinstance(user_agent, str):
            if user_agent:
                self.__setitem__('User-Agent', user_agent)
        elif isinstance(user_agent, dict):
            if 'user-agent' in [i.lower() for i in list(user_agent.keys())]:
                index = [i.lower() for i in list(user_agent.keys())].indent('user-agent')
                self.__setitem__('User-Agent', user_agent.get(list(user_agent.keys())[indent]))

        if __name__ == '__main__':
            click.secho("Example Output Get User-Agent:", fg='black', bg='yellow')
            print("user_agent =", self.__getitem__('User-Agent'))
            print("-" * (click.get_terminal_size()[0] - 1))
            print("\n")
        return self.__getitem__('User-Agent')

    @classmethod
    def UserAgent(self, user_agent = None):
        '''
            useragent alias
        '''
        return self.useragent(user_agent)

    @classmethod
    def User_Agent(self, user_agent = None):
        '''
            useragent alias
        '''
        return self.useragent(user_agent)

    @classmethod
    def user_agent(self, user_agent = None):
        '''
            useragent alias
        '''
        return self.useragent(user_agent)    

    @classmethod
    def ParserHeader(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        '''
            parserheader alias
        '''

        return self.parserheader(string_headers, get_path, cookies_dict_str, **kwargs)

    @classmethod
    def Parser_Header(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        '''
            parserheader alias
        '''

        return self.parserheader(string_headers, get_path, cookies_dict_str, **kwargs)

    @classmethod
    def parserHeader(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        '''
            parserheader alias
        '''

        return self.parserheader(string_headers, get_path, cookies_dict_str, **kwargs)

    @classmethod
    def parser_Header(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        '''
            parserheader alias
        '''

        return self.parserheader(string_headers, get_path, cookies_dict_str, **kwargs)

    @classmethod
    def parser_header(self, string_headers = None, get_path='/', cookies_dict_str='', **kwargs):
        '''
            parserheader alias
        '''

        return self.parserheader(string_headers, get_path, cookies_dict_str, **kwargs)

class parserheader(Parserheader):

    def __init__(self, *args, **kwargs):
        super(parserheader, self).__init__()

class Parser(Parserheader):

    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__()

        
        if self.headers:
            self.parser(*args, **kwargs)

    @classmethod
    def parser(self, *args, **kwargs):
        return self.parserheader(*args, **kwargs)

if __name__ == '__main__':
    headers = """accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9,id;q=0.8,ru;q=0.7
cache-control: max-age=0
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36
origin: www.google.com"""
    click.secho("Example Output:", fg='black', bg='green')
    click.secho(str(Parserheader.parserheader(headers)), fg = 'black', bg = 'yellow')
    # import sys
    # if len(sys.argv) == 1:
    #     click.secho("Example Get Input Data headers string:", fg='black', bg='cyan')
    #     example_header = """
    #     Host: ''
    #     Connection: keep-alive
    #     Upgrade-Insecure-Requests: 1
    #     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    #     Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    #     Referer: ''
    #     Accept-Encoding: gzip, deflate
    #     Accept-Language: en-US,en;q=0.9
    #     Cookie: ''
    # """
    #     click.secho("Example Output Dictionary Headers:", fg='white', bg='magenta')
    #     c = Parserheader()
    #     print(c.parserHeader())
    #     print("-" * (click.get_terminal_size()[0] - 1))
    #     print("\n")
    #     c.setCookies(None)
    #     c.UserAgent(example_header)
    #     sys.exit(0)
    # data = ''
    # try:
    #     import clipboard
    #     data = clipboard.paste()
    # except:
    #     try:
    #         data = sys.argv[1]
    #     except:
    #         pass
    # try:
    #     data = sys.argv[1]
    # except:
    #     pass
    
    # headers = c.parserHeader(data)
    # print(headers)
    # import traceback
    # try:
    #     clipboard.copy(str(headers))
    # except:
    #     print(traceback.format_exc())