# -*- coding: utf-8 -*-

from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-hotlinks",
    version="1.0.0",
    description="Hot links to your Django models",
    author="Olof Sjöbergh",
    author_email="olof@agoodid.se",
    maintainer="AGoodId",
    maintainer_email="teknik@agoodid.se",
    url="https://github.com/agoodid/django-hotlinks",
    license="MIT",
    packages=[
        "hotlinks",
        "hotlinks.templatetags",
    ],
    long_description=read("README.markdown"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
