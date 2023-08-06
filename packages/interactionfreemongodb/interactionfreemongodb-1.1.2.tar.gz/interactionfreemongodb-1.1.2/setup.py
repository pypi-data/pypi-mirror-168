import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
version = '1.1.2'

setuptools.setup(
    name='interactionfreemongodb',
    version=version,
    author='Hwaipy',
    author_email='hwaipy@gmail.com',
    description='A storage service for InteractionFree based on MongoDB.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='gpl-3.0',
    url='https://github.com/hwaipy/InteractionFreeMongoDB',
    download_url='https://github.com/hwaipy/InteractionFreeMongoDB/archive/v{}.tar.gz'.format(version),
    keywords=['interactionfreepy', 'service', 'mongodb', 'rpc'],
    packages=setuptools.find_packages(),
    install_requires=[
        'interactionfreepy',
        'motor',
        'pytz',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)


