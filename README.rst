python-streamlike
=============

Python wrapper for Streamlike API

Installation
------------

Method with pip: if you have pip installed, just type this in a terminal
(sudo is optional on some systems)

::

    pip install python-bright

Method by hand: download the sources, either on PyPI or (if you want the
development version) on Github, unzip everything in one folder, open a
terminal and type

::

    python setup.py install

Basic Usage
-----------

API Documentation: http://connect.streamlike.com/en/page/backend-api-v1-uptodate

.. code:: python

    from streamlike import Streamlike
    api = Streamlike(LOGIN,PASSWORD,API_KEY)
    api.search_media()

Add a Media
~~~~~~~~~~~

.. code:: python
    
    api.add_media(media_url="https://yourorigin.com/video.mp4",
                    permalink="video-mp4",
                    name="anon video",
                    status="online",
                    description="my vacation video",
                    media_type="video")