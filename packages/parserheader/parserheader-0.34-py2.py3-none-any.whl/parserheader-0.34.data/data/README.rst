parserheader
==================

Parsing headers from string or dictionary


Installing
----------

Install and update using `pip`_:

.. code-block:: bash

    $ pip install parserheader

parserheader supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple parserheader program:

.. code-block:: python

    import parserheader
    
    ...

    def setHeaders():
        ph = parserheader.parserheader()
        header_str = """
            POST /upload/ HTTP/1.1
            Host: google.com.com
            Connection: keep-alive
            Content-Length: 1220
            Cache-Control: max-age=0
            Origin: http://www.google.com.com
            Upgrade-Insecure-Requests: 1
            Content-Type: application/x-www-form-urlencoded
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
            Referer: http://www.google.com/
            Accept-Encoding: gzip, deflate
            Accept-Language: en-US,en;q=0.9,id;q=0.8
            Cookie: PHPSESSID=41a0f0ac4545d3f5ba9a4ba415b777e9
        """
        headers = ph.parserHeader(header_str)
        print("headers =", headers)
        return headers

    setHeaders()


And what it looks like when run:

.. code-block:: bash

    $ python test.py 
    headers = {'Origin': 'http://www.google.com', 'Content-Length': '1220', 'Accept-Language': 'en-US,en;q=0.9,id;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 'Host': 'google.com', 'Referer': 'http://www.google.com/', 'Cache-Control': 'max-age=0', 'Cookie': 'PHPSESSID=41a0f0ac4545d3f5ba9a4ba415b777e9', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded'}


Support
--------

*   Python 2.7 +, Python 3.x
*   Windows, Linux

Links
------

*   License: `MIT <https://github.com/cumulus13/parserheader/src/default/LICENSE.rst>`_
*   Code: https://github.com/cumulus13/parserheader
*   Issue tracker: https://github.com/cumulus13/parserheader/issues