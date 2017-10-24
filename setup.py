from setuptools import setup

setup(name='iterative_set_expansion',
      version='0.1',
      description="Information Extraction system that performs Iterative Set Expansion over Google results with Stanford NLP tools",
      author='Jerome Kafrouni',
      author_email='j.kafrouni@columbia.edu',
      url='https://github.com/jkafrouni',
      packages=['iterative_set_expansion'],
      install_requires=[
          # add here any tool that you need to install via pip 
          # to have this package working
          'google-api-python-client',
      ],
      entry_points={
          'console_scripts': [
              'run = iterative_set_expansion.__main__:main'
          ]
      },
)