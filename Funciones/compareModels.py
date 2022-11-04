

def compareModelsDT(models):
    result=None
    f1_list=[]
    keylist=models.keys()
    keylist=list(keylist)
    for n in models:
        f1_list.append(models[n][-1])
    maxidx=f1_list.index(max(f1_list))
    result=models[keylist[maxidx]]
    return result