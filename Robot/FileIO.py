import pickle
import sys, os
from struct import pack, unpack
"""
def writeToFile(o,f):
    o = pickle.dumps(o)
    nb = sys.getsizeof(o)
    print("Size :", nb)
    with open(f, "r+b") as input:
        input.seek(0)
        input.seek(offset)
        input.write(pack(">i",nb))
        input.write(o)

def readFromFile(f):
    with open(f, "rb") as input:
        input.seek(0)
        input.seek(offset)
        s, = unpack(">i", input.read(4))
        o = input.read(s)
    return pickle.loads(o)


"""



offset = 100

class FileIO(object):
    @staticmethod
    def loadFromBinaryImage(f):
        print("Try to load", f)
        with open(f, "rb") as input:
            input.seek(0)
            input.seek(offset)
            s, = unpack(">i", input.read(4))
            o = input.read(s)
        return pickle.loads(o)
    def writeToBinaryImage(o):
        p = pickle.dumps(o)
        nb = sys.getsizeof(p)
        print("Size :", nb)
        #destination = open(o.id, "wb")
        #source = open(os.path.join("ressources", o.icon))
        try:
            # Try to open existing file
            destination = open(o.id, "r+b")
        except Exception as e:
            # Pas de fichier, il faut copier depuis
            # le dossier ressources
            destination = open(o.id, "wb")
            with open(os.path.join("ressources",o.icon), "rb") as source:
                 destination.write(source.read())

        destination.close()
        with open(o.id, "r+b") as input:
            input.seek(0)
            input.seek(offset)
            input.write(pack(">i",nb))
            input.write(p)
    @staticmethod
    def loadStegano(f):
        im = Image.open(f)
        o = stepic.decode(im)
        o = bytes(o, 'UTF-8')
        return pickle.loads(o)
    """
    @staticmethod
    def saveStegano(o):
        s = str(pickle.dumps(o))
        im = Image.open(os.path.join("ressources",o.icon))
        secret = stepic.encode(im, s)
        secret.save(o.id + ".png")
    @staticmethod
    def saveEntite(o):
        #pickle.dump(o, open(o.id, "wb"))
        try:
            os.mkdir(os.path.join(o.path, o.name))
        except Exception as e:
            # print(e)
            pass
        pickle.dump(o, open(os.path.join(o.path, o.name, ".config"), "wb"))
    """
    @staticmethod
    def loadEntite(f):
        try:
            return pickle.load(open(f, "rb"))
        except Exception as e:
            print("ERROR : ", e)
            return None
    @staticmethod
    def save(o):
        #FileIO.saveBinaryFile(o)
        if "Entite" in o.__class__.__bases__:
            FileIO.saveEntite(o)
        else:
            FileIO.writeToBinaryImage(o)
    @staticmethod
    def load(f):
        #return FileIO.loadBinaryFile(f)
        if ".config" in f:
            return FileIO.loadEntite(f)
        else:
            return FileIO.loadFromBinaryImage(f)
