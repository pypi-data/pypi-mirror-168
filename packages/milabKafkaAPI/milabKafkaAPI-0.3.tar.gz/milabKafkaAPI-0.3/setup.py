from setuptools import setup, find_packages


setup(
    name='milabKafkaAPI',
    version='0.3',
    license='MIT',
    author="milab",
    author_email='omer.sadeh@milab.idc.ac.il',
    packages=find_packages('src'),
    package_dir={'': 'milabKafkaAPI'},
    url='https://github.com/idc-milab/Kafka-API',
    keywords='kafka api milab butter',
    install_requires=[
        'kafka-python',
        'lxml',
        'butter.mas-api',
      ],

)