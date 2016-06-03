from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='persiantools',
      version='0.0.7',
      description='Python Library for Persian',
      long_description=readme(),
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Persian',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Localization',
          'Topic :: Utilities',
      ],
      keywords='persian digits characters converter jalali date shamsi jdate',
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
