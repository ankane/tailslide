from setuptools import setup

setup(
    name='tailslide',
    version='0.1.0',
    description='Median and percentile for Django models and MongoEngine documents',
    url='https://github.com/ankane/tailslide',
    author='Andrew Kane',
    author_email='andrew@ankane.org',
    license='MIT',
    packages=[
        'tailslide',
        'tailslide.mongoengine'
    ],
    python_requires='>=3.6',
    install_requires=[],
    zip_safe=False
)
