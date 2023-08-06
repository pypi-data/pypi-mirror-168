# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/8 10:03
# __fileName__ : CrawlSpider twineUtils.py
# __devIDE__ : PyCharm
from twine.commands.upload import upload as twine_upload
from twine.settings import Settings as TwineSetting
from twine.commands.check import check as twine_check
from twine.commands.register import register as twine_register
import datetime
import fire
import os
"""
[options.entry_points]
twine.registered_commands = 
	check = twine.commands.check:main
	upload = twine.commands.upload:main
	register = twine.commands.register:main
console_scripts = 
	twine = twine.__main__:main
"""


def build(username=None, password=None, version=None, distDir=None, is_publish=False, **kwargs):

    if distDir:
        projectDir = os.path.join(distDir, '../')
    else:
        projectDir = os.getcwd()
        distDir = os.path.join(projectDir, 'dist')
    print(projectDir, distDir)
    about = {}

    with open(os.path.join(projectDir, "__version__.py"), "r", encoding="utf-8") as f:
        exec(f.read(), about)
    if version:
        about['__version__'] = version
        _buildVersion_ = datetime.datetime.strftime(datetime.datetime.strptime(version.replace('.', ':'), '%H:%M:%S'), '%H:%M:%S')
        buildVersion = f"0x{_buildVersion_.replace(':', '')}"
        about['__build__'] = buildVersion
        with open(os.path.join(projectDir, "__version__.py"), "w", encoding="utf-8") as f:
            _about = {
                k: (k == '__version__' and version) or (k == '__build__' and buildVersion) or about[k]
                for k in about if k not in {'__builtins__'}
            }
            newLines = [
                f'{k} = "{_about[k]}"' if k != '__build__' else f'{k} = {_about[k]}'
                for k in _about
            ]
            f.write('\n\n')
            f.write('\n'.join(newLines))
            f.write('\n\n')


    os.system(f"python {os.path.join(projectDir, 'setup.py')} sdist bdist_wheel")
    if is_publish:


        version = version or about['__version__']


        dists = [os.path.join(distDir, filePath) for filePath in os.listdir(distDir) if version in filePath]

        twine_upload(
            TwineSetting(
                username=username,
                password=password,
                **kwargs
            ),
            dists
        )


if __name__ == '__main__':
    fire.Fire({
        'build': build
    })








