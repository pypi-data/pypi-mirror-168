#!/usr/bin/env python

if __name__ == "__main__":
    import setuptools
    setuptools.setup(
        package_data = {
            'static': ['*'],
            'templates': ['*']
        }
    )
