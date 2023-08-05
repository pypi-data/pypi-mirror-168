#import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
#sys.path.pop(0)
from setuptools import setup, find_packages

setup(
    name='waitless-sviz',
    packages=find_packages(),
    #packages=['waitless-sviz'],
    package_dir = {'': '.'},
    py_modules=['main',
    		'configure',
    		'lcd_i2c_printer',
    		'urbanbus',
    		'lib.pico_i2c_lcd',
    		'lib.lcd_api'], 
    #package_data = {"waitless-sviz": ['waitless-sviz.res/*',
    #					'waitless-sviz.res.css/*']
    #		   },
    include_package_data=True, 
    version='0.4.1a13',
    description='MicroPython app to monitorize time arrivals of each bus stop in Madrid Region',
    long_description='This package runs as APP for Raspberry Pi Pico. This APP monitorize each bus stop in Madrid Region (Spain) and get time of arrival estimated which is showed in a LCD 16x2',
    keywords='bus arrivals madrid micropython',
    url='https://github.com/modl-ideas/WAITLESS_SVIZ',
    author='Miguel Palomino Civantos',
    author_email='miguelpalominocivantos@gmail.com',
    maintainer='Miguel Palomino Civantos',
    maintainer_email='miguelpalominocivantos@gmail.com',
    license='MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires = [],	
    platforms = "any"#,
    #cmdclass={'sdist': sdist_upip.sdist}
)
