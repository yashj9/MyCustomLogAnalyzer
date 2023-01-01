import os
import tarfile
import shutil
import re
import copy

saf_keywords = ['SAF','SAF_NUM', 'dns', 'DNS', 'qorUPgBA8aJ9Dc3PEs2aRcFLl6RvZaCby']
path = r'C:\Users\yashj1\Downloads\m440_saf_logs_4\tgzfiles'

def extract(path):
    if not os.path.exists('temp//'):
        os.makedirs('temp//')
    shutil.move(path,'./temp/'+path.split('\\')[-1])
    if not os.path.exists(path+'//'):
        os.makedirs(path+'//')
    tgz_in_fhandle = tarfile.open('./temp/'+path.split('\\')[-1], "r:gz")
    tgz_in_fhandle.list(verbose=True)
    tgz_in_fhandle.extractall(path+'//')
    tgz_in_fhandle.close()
    os.remove('./temp/'+path.split('\\')[-1])
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.strip().endswith(('.tgz','.tar','.tgx')):#
                extract(os.path.join(root,file))
    if os.path.exists('temp//'):
        os.removedirs('temp//')

def main():
    output = []
    out_path = 'extract'
    if os.path.exists(out_path+'//'):
        shutil.rmtree(out_path+'//')
    os.makedirs(out_path+'//')
    for tgz_file in os.listdir(path):
        tgz_file = os.path.join(path,tgz_file)
        if os.path.exists('temp//'):
            os.removedirs('temp//')
        new_path = './'+out_path +'/' + tgz_file.split('\\')[-1]
        shutil.copy(tgz_file, new_path)
        extract(out_path +'\\' + tgz_file.split('\\')[-1])
        word = ''
        for root, dirs, files in os.walk(out_path +'\\' + tgz_file.split('\\')[-1]):
            for file in files:
                if file.strip().startswith('scaapp') and file.strip().endswith('.log'):
                    with open(os.path.join(root, file)) as f:
                        string = f.read()
                        if re.search('|'.join(['\\b'+item+'\\b' for item in saf_keywords]),string):
                            tempdict = {'File Name' : tgz_file.split('\\')[-1],
                                        'log file' : file,
                                        'Keyword':','.join(set(re.findall('|'.join(['\\b'+item+'\\b' for item in saf_keywords]),string)))}
                            output.append(copy.deepcopy(tempdict))
        if len(output) == 0 or output[-1]['File Name'] != tgz_file.split('\\')[-1]:
            output.append({'File Name' : tgz_file.split('\\')[-1],
                            'log file' : '',
                            'Keyword':'No Keyword Found'})
    try:
        import pandas as pd
        pd.DataFrame(output).to_excel("output.xlsx", index=False)
    except:
        with open('output.txt','w') as f:
            for tempdict in output:
                f.write(str(tempdict)+'\n')

    if os.path.exists(out_path+'//'):
        shutil.rmtree(out_path+'//')

if __name__ == '__main__':
    main()