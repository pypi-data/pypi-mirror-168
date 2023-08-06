from setuptools import find_packages, setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        print("Testing")
        install.run(self)



setup(
  name = 'mianutils',
  packages=find_packages(),
  version = '0.94',
  description = 'Yes.',
  author = 'haha.',
  cmdclass={
    'install': CustomInstallCommand,
  },
  author_email = 'mianism@outlook.com',
  url = 'https://github.com',
  keywords = [],
  classifiers = [],
)
