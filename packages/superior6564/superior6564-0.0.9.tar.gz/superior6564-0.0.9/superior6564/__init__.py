"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""

# import degget
# import games_help
# import packages


# from degget import show
# from games_help import gen_ru_words
# from packages import install, pip_upgrade, required


with open('info.txt') as f:
    sum_letters = ""
    version = []
    while sum_letters != "Version":
        line = f.readline()
        if len(line) >= 7:
            sum_letters = ""
            for i in range(7):
                sum_letters += line[i]
                if sum_letters == "Version":
                    for j in range(5):
                        version.append(line[j + 22])


__author__ = 'Superior_6564'
__version__ = version[0] + version[1] + version[2] + version[3] + version[4]
__email__ = 'vip.klochayil@gmail.com'
