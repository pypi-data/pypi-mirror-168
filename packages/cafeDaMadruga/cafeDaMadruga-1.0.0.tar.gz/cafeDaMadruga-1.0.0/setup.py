from setuptools import setup

with open('README.md', 'r') as readmeArq:
    readme = readmeArq.read()

setup(
    name='cafeDaMadruga',
    version='1.0.0',
    author='Wanderson Renê',
    author_email='wanderson.rene12@gmail.com',
    packages=['cafeDaMadruga'],

    description='Um coletor de vogais de uma string.',
    long_description=readme,
    long_description_content_type='text/markdown',

    license='MIT License',

    keywords='coletar vogal ou vogais da string rene cafeDaMadruga',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Database'
    ],

    install_requires=['unicodedata']
)
