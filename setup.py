from setuptools import setup


version = '1.0b1'


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='persiantools',
      version=version,
      description='Jalali date and datetime with other tools',
      long_description=readme(),
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Persian',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Localization',
          'Topic :: Utilities',
      ],
      keywords='jalali shamsi persian digits characters converter jalalidate jalalidatetime date datetime',
      url='https://github.com/mhajiloo/persiantools',
      author='Majid Hajiloo',
      author_email='majid.hajiloo@gmail.com',
      license='MIT',
      packages=['persiantools'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)
