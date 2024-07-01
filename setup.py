from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='tailslide',
    version='0.2.0',
    description='Median and percentile for Django and MongoEngine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ankane/tailslide',
    author='Andrew Kane',
    author_email='andrew@ankane.org',
    license='MIT',
    packages=[
        'tailslide',
        'tailslide.mongoengine'
    ],
    python_requires='>=3.8',
    install_requires=[],
    zip_safe=False
)
