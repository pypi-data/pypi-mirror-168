from glob import iglob
from pathlib import Path

import setuptools

with open('requires.txt', encoding='UTF-8') as f:
    requires = f.read().strip().splitlines()
with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

extras_require = {}
for require in iglob('extra_requires/*_*.txt'):
    with open(require, encoding='UTF-8') as f:
        extras_require[
            Path(require).name.split('.')[0].split('_')[-1].casefold()] = f.read().strip().splitlines()
extras_require['all'] = requires
for req in extras_require.values():
    extras_require['all'] += req

setuptools.setup(
    name="PyFastDub",
    version="3.1.0",

    description="A Python CLI package "
                "for voice over subtitles, with the ability to embed in video, audio ducking, "
                "and dynamic voice changer for a single track; "
                "auto translating; "
                "download and upload to YouTube supports",

    long_description=readme,

    long_description_content_type="text/markdown",

    author="Nikita (NIKDISSV)",

    install_requires=requires,

    extras_require=extras_require,

    author_email='nikdissv@proton.me',

    project_urls={
        'Download Voices': 'https://rhvoice.su/voices/',
        'GitHub': 'https://github.com/NIKDISSV-Forever/FastDub/',
        'YouTube': 'https://www.youtube.com/channel/UC8JV3zPSVm9EKSWD1XdkQvw/',
    },

    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Natural Language :: English',
        'Natural Language :: Russian',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',


        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Utilities',

        'Typing :: Typed',
    ],

    keywords=['dubbing', 'voicing',
              'fastdub', 'JustDub', 'SpeedDub',
              'offline', 'free', 'easiest',
              'subtitles', 'videos', 'veed'],
)
