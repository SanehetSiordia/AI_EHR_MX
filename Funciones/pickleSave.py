import pickle

def pickleExport(diccionario,name):
    file= open('PickleSaves\\'+str(name)+'.pickle','wb')
    pickle.dump(diccionario, file)
    file.close()
    return None