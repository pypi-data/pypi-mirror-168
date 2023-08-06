#!/usr/bin/env python3
from setuptools import setup
import setuptools
import os
import shutil
from pathlib import Path


# python3 setup.py bdist_wheel

# f = open("version.txt","r")
# _version = f.read()
# f.close()

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# package_name = "mtxp"
# version = ""
# with open(f'__init__.py', 'r') as fd:
#     version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
#                         fd.read(), re.MULTILINE).group(1)

package_name = "mtxp"
version_file = Path(__file__).parent.joinpath("version.txt")
# print(f"version file : {version_file}")
f = open(version_file, "r")
version = f.read()
f.close()


def gen_data_files(*dirs):
    print("gen_data_files =========================================================", dirs)
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: root + "/" + f, files)))
    print("gen_data_files result ===============", results)
    return results


# 上一个构建的残留会影响打包文件，所以这里先清除。
print("清理目录")
build_dir = os.path.join(os.getcwd(), "build")
if Path(build_dir).exists():
    shutil.rmtree(build_dir)

packages = setuptools.find_packages(
    exclude=("test", "mtxcms*", "mtx_cloud.*", "mtxauth*", "gallery*"))
print("all packages", packages)


def requirements():
    requirements_path = os.path.join(f"{package_name}/requirements.txt")
    if os.path.exists(requirements_path):
        install_requires = open(requirements_path).read().split("\n")
        install_requires = [
            item for item in install_requires if not item.startswith("-r ")]
    else:
        install_requires = [
            "flask",
            "mtlibs",
            "pyyaml",
            "docker",
            "markupsafe",
            "paramiko",
        ]
    return install_requires


reqs = requirements()
print(f"requirements: {requirements()}")

setup(name=package_name,
      version=version,
      description='The funniest joke in the world',
      long_description='long_description',  # readme(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6"
      ],

      keywords='funniest joke comedy flying circus',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      # packages=[
      #     "mtxcli"
      # ],
      # package_dir={
      #     'mtxcli': '.'
      # },

      package_dir={
          'mtxp': 'mtxp'
      },
      #   packages=packages,
      packages=['mtxp',
                # 'mtxp.commands',
                "mtxp.mtxp",
                "mtxp.services",
                "mtxp.setup",
                "mtxp.cli"
                ],

      install_requires=requirements(),       # 常用
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      package_data={
          #   'demo': ['data/*.txt'],
          'mtxp': ['data/*'],
      },
      # package_dir={'mtxp': '.'},
      zip_safe=True,
      entry_points={
          'console_scripts': [
              # 'mtxp=mtxp.app:main',
              # 'mtcontenful2=mtxp.contentful:main',
              'mtxp=mtxp.cli.cli:main',
          ],
          'flask.commands': [
              'cmd1=mtxp.commands:cli',
              # 'mtxpagent_flask=mtxp.app:entry_agent'
          ],
      },
      # scripts=['mtxcli/dc.py'],
      )
