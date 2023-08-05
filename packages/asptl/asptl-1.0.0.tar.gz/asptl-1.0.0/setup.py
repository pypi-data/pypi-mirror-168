import setuptools

with open('README.md','r') as f:
    long_description=f.read()

setuptools.setup(
    name='asptl',
    version='1.0.0',
    author='Amir',
    author_email='hi-amir@outlook.com',
    url='pypi.org',
    description='''
Exclusively developed by AmirSong (pypi)

It encapsulates many common components

Including file read-write list, etc''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Imdependent',
    ],)
