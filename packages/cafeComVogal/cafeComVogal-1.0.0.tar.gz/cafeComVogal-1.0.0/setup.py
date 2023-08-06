from setuptools import setup

setup(
    name='cafeComVogal',
    version='1.0.0',
    author='Wanderson Renê',
    author_email='wanderson.rene12@gmail.com',
    packages=['cafeComVogal'],

    description='Um coletor de vogais de uma string.',
    long_description='Um coletor de vogais de uma string passada como parâmetro '
                     + 'na função vogais, '
                     + 'a fim de coletar até mesmo as vogais com acentos',

    license='MIT',

    keywords='coletar vogal ou vogais da string rene cafeComVogal',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Database'
    ]
)
