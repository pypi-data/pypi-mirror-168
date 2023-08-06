import setuptools

README = open('README.md').read()

setuptools.setup(
    name='mext',
    version='1.0.0',
    url='https://github.com/modbender/manga-extractor',
    description='A simple manga extractor. Extracts any comic info, chapter list and chapter pages. In development.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    install_requires=[
        'requests>=2.25.0',
    ],
    python_requires='>=3.5',
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
