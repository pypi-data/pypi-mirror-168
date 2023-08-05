from setuptools import setup

setup(
    name='simple_cicd',
    version='0.0.6',    
    description='Dead simple CI/CD pipeline executor',
    url='https://gitlab.com/FrancoisSevestre/simple-ci',
    author='François Sevestre',
    author_email='francois.sevestre.35@gmail.com',
    license='GPLv3',
    packages=['simple_cicd'],
    install_requires=['numpy'],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'simpleci = simple_cicd.simple_cicd:main'
            ]
        },
)
