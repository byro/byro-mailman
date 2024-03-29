import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1, interactive=False)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="byro-mailman",
    version="1.0.1",
    description="Mailing list integration for byro",
    long_description=long_description,
    url="https://github.com/byro/byro-mailman",
    author="rixx",
    author_email="r@rixx.de",
    license="Apache Software License",
    install_requires=["requests"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[byro.plugin]
byro_mailman=byro_mailman:ByroPluginMeta
""",
)
