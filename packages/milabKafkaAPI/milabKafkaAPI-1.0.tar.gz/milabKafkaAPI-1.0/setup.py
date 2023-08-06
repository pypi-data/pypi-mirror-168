from setuptools import setup, find_packages


setup(
    name='milabKafkaAPI',
    version='1.0',
    description='An API for the milab projects with the kafka server.',
    license='MIT',
    author="milab",
    author_email='omer.sadeh@milab.idc.ac.il',
    packages=['milabKafkaAPI'],
    url='https://github.com/idc-milab/Kafka-API',
    keywords='kafka api milab butter',
    install_requires=[
        'kafka-python',
        'lxml',
        'butter.mas-api',
      ],
)
