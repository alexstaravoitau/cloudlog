from setuptools import setup

setup(
    name='cloudlog',
    version='0.1.1',
    description='A simple logger that duplicates console logs to a file, Dropbox and Telegram.',
    url='http://github.com/navoshta/cloudlog',
    author='Alex Staravoitau',
    author_email='alex.staravoitau@gmail.com',
    license='MIT',
    packages=['cloudlog'],
    install_requires=[
        'dropbox',
        'matplotlib',
        'twx.botapi'
    ],
    zip_safe=False
)