import pandas as pd
import os
# IMPORTANT! pip install openpyxl


def checkdir(modelname):
    rootpath = os.path.expanduser('~\.cache/mahaNLP')
    childpathstr = '~\.cache/mahaNLP/'+modelname
    childpath = os.path.expanduser(childpathstr)
    if os.path.isdir(rootpath):
        if not os.path.isdir(childpath):  # mkdir for model
            os.chdir(rootpath)
            os.makedirs(modelname)
    else:  # mkdir mahaNLP and model folder
        path = os.path.expanduser('~\.cache')
        os.chdir(path)
        os.makedirs("mahaNLP/"+modelname)


def downloadMahasent():
    dataset_type = {
        'tweets-train.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3CubeMahaSent%20Dataset/tweets-train.csv',
        'tweets-test.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3CubeMahaSent%20Dataset/tweets-test.csv',
        'tweets-valid.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3CubeMahaSent%20Dataset/tweets-valid.csv',
        'tweets-extra.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3CubeMahaSent%20Dataset/tweets-extra.csv'
    }
    result = {}
    checkdir('mahaSent')
    childpath = os.path.expanduser('~\.cache/mahaNLP/mahaSent')
    os.chdir(childpath)
    for key in dataset_type:
        df = pd.read_csv(dataset_type[key])
        csv_df = df.to_csv(key, index=False, encoding='UTF-16')
        result[key.split(".")[0]] = df  # add df to an dictionary
    return result


def downloadMahahate():
    class_2 = {
        'hate_bin_train.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/2-class/hate_bin_train.xlsx?raw=true',
        'hate_bin_test.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/2-class/hate_bin_test.xlsx?raw=true',
        'hate_bin_valid.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/2-class/hate_bin_valid.xlsx?raw=true',
    }
    class_4 = {
        'hate_train.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/4-class/hate_train.xlsx?raw=true',
        'hate_test.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/4-class/hate_test.xlsx?raw=true',
        'hate_valid.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaHate/4-class/hate_valid.xlsx?raw=true',
    }
    result = {'2-class': {}, '4-class': {}}
    checkdir('mahaHate')
    checkdir('mahaHate/2-class')
    checkdir('mahaHate/4-class')

    childpath = os.path.expanduser('~\.cache/mahaNLP/mahaHate/2-class')
    os.chdir(childpath)
    for key in class_2:
        df = pd.read_excel(class_2[key])
        xlsx_df = df.to_excel(key, index=False, encoding='UTF-16')
        result['2-class'][key.split(".")[0]] = df  # add df to an dictionary

    childpath = os.path.expanduser('~\.cache/mahaNLP/mahaHate/4-class')
    os.chdir(childpath)
    for key in class_4:
        df = pd.read_excel(class_4[key])
        xlsx_df = df.to_excel(key, index=False, encoding='UTF-16')
        result['4-class'][key.split(".")[0]] = df  # add df to an dictionary
    return result


def downloadMahaner():
    iob = {
        'train_iob.txt': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaNER/IOB/train_iob.txt?raw=true',
        'test_iob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3Cube-MahaNER/IOB/test_iob.txt',
        'valid_iob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3Cube-MahaNER/IOB/valid_iob.txt',
    }
    non_iob = {
        'train_noniob.txt': 'https://github.com/l3cube-pune/MarathiNLP/blob/main/L3Cube-MahaNER/NON_IOB/train_noniob.txt?raw=true',
        'test_noniob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3Cube-MahaNER/NON_IOB/test_noniob.txt',
        'valid_noniob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/main/L3Cube-MahaNER/NON_IOB/valid_noniob.txt',
    }
    result = {'iob': {}, 'non_iob': {}}
    checkdir('mahaNER')
    checkdir('mahaNER/IOB')
    checkdir('mahaNER/NON_IOB')

    childpath = os.path.expanduser('~\.cache/mahaNLP/mahaNER/IOB')
    os.chdir(childpath)
    for key in iob:
        df = pd.read_csv(iob[key], sep=" ")
        txt_df = df.to_csv(key, index=False, encoding='UTF-16')
        result['iob'][key.split(".")[0]] = df  # add df to an dictionary

    childpath = os.path.expanduser('~\.cache/mahaNLP/mahaNER/NON_IOB')
    os.chdir(childpath)
    for key in non_iob:
        df = pd.read_csv(non_iob[key], sep="\t")
        txt_df = df.to_csv(key, index=False, encoding='UTF-16', sep="\t")
        result['non_iob'][key.split(".")[0]] = df  # add df to an dictionary
    return result


def loadDatasets(name):

    if name == 'mahaSent':
        res_dict = downloadMahasent()
        return res_dict
    elif name == 'mahaHate':
        res_dict = downloadMahahate()
        print(res_dict['4-class']['hate_valid'])
        return res_dict
    elif name == 'mahaNER':
        res_dict = downloadMahaner()
        print(res_dict['non_iob']['valid_noniob'])
        return res_dict
