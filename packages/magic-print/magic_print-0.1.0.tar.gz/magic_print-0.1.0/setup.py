from setuptools import setup

setup(
    name='magic_print',
    version='0.1.0',    
    description='Magic printing nested type',
    url='https://github.com/crsegerie/magic_print',
    author='Charbel-Raphael Segerie',
    author_email='charbilalo@gmail.com',
    license='BSD 2-clause',
    packages=['magic_print'],
    install_requires=['torch',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)