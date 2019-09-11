# coding=utf-8
import os


def findAllFiles(root_dir, filter):
    """
    在指定目录查找指定类型文件

    :param root_dir: 查找目录
    :param filter: 文件类型
    :return: 路径、名称、文件全路径

    """

    print("Finding files ends with \'" + filter + "\' ...")
    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(filter):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    print (names.__len__().__str__() + " files have been found.")
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files


def splitName(name):
    year = name[:4]
    month = name[5:7]
    day = name[8:10]
    title = name[11:].split(".")[0]
    url = year + "/" + month + "/" + day + "/" + title
    return url


if __name__ == '__main__':
    _, names, _ = findAllFiles("F:\\zhaoxuhui.github.io\\_posts", "")
    urls = []
    for item in names:
        urls.append(splitName(item))

    f = open("F:\\zhaoxuhui.github.io\\posts.idx", 'w')
    f.write(len(urls).__str__() + "\n")
    for item in urls:
        f.write(item + "\n")
    f.close()
