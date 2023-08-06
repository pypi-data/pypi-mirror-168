from setuptools import setup

name = "types-emoji"
description = "Typing stubs for emoji"
long_description = '''
## Typing stubs for emoji

This is a PEP 561 type stub package for the `emoji` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `emoji`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/emoji. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `4746f9b238611ec12fa9a2e8666674628f49b5fb`.
'''.lstrip()

setup(name=name,
      version="2.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/emoji.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['emoji-stubs'],
      package_data={'emoji-stubs': ['__init__.pyi', 'core.pyi', 'unicode_codes/__init__.pyi', 'unicode_codes/data_dict.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
