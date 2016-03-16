from setuptools import setup

setup(name='animemon',
      version='0.1.1',
      description='Everything about your anime within the command line.',
      url='https://github.com/nims11/animemon',
      author='Nimesh Ghelani',
      author_email='nimeshghelani@gmail.com',
      license='MIT',
      packages=['animemon'],
      entry_points={
               'console_scripts': ['animemon=animemon:main'],
           },
      install_requires=[
          'guessit<2',
          'terminaltables',
          'docopt',
          'tqdm',
          'colorama'
      ],
      keywords=['anime', 'CLI', 'anime-within-CLI', 'python'],
      classifiers=[
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Version Control',
      ],)
