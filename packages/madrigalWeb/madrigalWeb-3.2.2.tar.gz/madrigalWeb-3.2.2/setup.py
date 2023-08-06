"""set up file for the Python Madrigal Remote API

$Id: setup.py 7455 2022-09-19 20:40:42Z brideout $
"""
import os, os.path, sys

from distutils.core import setup
    
setup(name="madrigalWeb",
      version="3.2.2",
      description="Remote Madrigal Python API",
      author="Bill Rideout",
      author_email="brideout@haystack.mit.edu",
      url="http://cedar.openmadrigal.org",
      packages=["madrigalWeb"],
      keywords = ['Madrigal'],
      scripts=['madrigalWeb/globalIsprint.py', 'madrigalWeb/globalDownload.py',
               'madrigalWeb/globalCitation.py',
               'madrigalWeb/examples/exampleMadrigalWebServices.py']
      )

    