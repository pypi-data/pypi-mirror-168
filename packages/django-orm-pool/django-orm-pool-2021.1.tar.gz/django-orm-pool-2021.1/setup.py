from setuptools import setup, find_packages

description = """
DB-API2 connection pool for Django (for postgresql, mysql and sqlite)
"""

setup(
    name="django-orm-pool",
    version='2021.1',
    url='https://github.com/djangonauts/djorm-ext-pool',
    license='BSD',
    platforms=['OS Independent'],
    description=description.strip(),
    author='Andrey Antukh',
    author_email='niwi@niwi.be',
    maintainer='Andrey Antukh',
    maintainer_email='niwi@niwi.be',
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'sqlalchemy >= 1.3.3',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
