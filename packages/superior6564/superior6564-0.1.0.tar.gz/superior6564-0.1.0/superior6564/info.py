def get_version():
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
        version = version[0] + version[1] + version[2] + version[3] + version[4]
    return version


def get_info():
    with open('info.txt') as f:
        info = f.read()
    return info

