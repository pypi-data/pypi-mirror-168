# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import errno
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


VERSION = "0.0.2a1663451108"
PLUGIN_VERSION = "0.0.2-alpha.1663451108+66e50782"

class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        try:
            check_call(['pulumi', 'plugin', 'install', 'resource', 'launchdarkly', PLUGIN_VERSION, '--server', 'github://api.github.com/lbrlabs'])
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f"""
                There was an error installing the launchdarkly resource provider plugin.
                It looks like `pulumi` is not installed on your system.
                Please visit https://pulumi.com/ to install the Pulumi CLI.
                You may try manually installing the plugin by running
                `pulumi plugin install resource launchdarkly {PLUGIN_VERSION}`
                """)
            else:
                raise


def readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "launchdarkly Pulumi Package - Development Version"


setup(name='lbrlabs_pulumi_launchdarkly',
      version=VERSION,
      description="A Pulumi package for creating and managing launch darkly cloud resources.",
      long_description=readme(),
      long_description_content_type='text/markdown',
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi launchdarkly lbrlabs',
      url='https://www.pulumi.com',
      project_urls={
          'Repository': 'https://github.com/lbrlabs/pulumi-launchdarkly'
      },
      packages=find_packages(),
      package_data={
          'lbrlabs_pulumi_launchdarkly': [
              'py.typed',
              'pulumi-plugin.json',
          ]
      },
      install_requires=[
          'parver>=0.2.1',
          'pulumi>=3.0.0,<4.0.0',
          'semver>=2.8.1'
      ],
      zip_safe=False)
