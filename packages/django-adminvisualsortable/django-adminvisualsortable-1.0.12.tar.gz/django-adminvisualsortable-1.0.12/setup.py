#!/usr/bin/env python

if __name__ == "__main__":
    import setuptools
    setuptools.setup(
        package_data={
            '': [ 'templates/*.html', 
                  'templates/adminvisualsortable/*.html', 
                  'static/adminvisualsortable/css/yui/*.css',
                  'static/adminvisualsortable/css/*.css',
                  'static/adminvisualsortable/js/*.js',
                  'static/adminvisualsortable/js/*.map',
                  'static/adminvisualsortable/img/*.png'
                ]
            },
    )
