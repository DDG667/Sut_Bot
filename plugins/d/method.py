from pickle import load,dump

def oper_date(path:str,data='',mode:str='r'):
    if data!='':
        with open(path,mode+'b') as file:
            dump(data,file)
    with open(path,mode+'b') as file:
        return load(file)


