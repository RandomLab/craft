import pickle

class FileIO(object):
    @staticmethod
    def loadStegano(f):
        im = Image.open(f)
        o = stepic.decode(im)
        o = bytes(o, 'UTF-8')
        return pickle.loads(o)

    @staticmethod
    def saveStegano(o):
        s = str(pickle.dumps(o))
        im = Image.open(os.path.join("ressources",o.icon))
        secret = stepic.encode(im, s)
        secret.save(o.id + ".png")
    @staticmethod
    def saveBinaryFile(o):
        pickle.dump(o, open(o.id, "wb"))
    @staticmethod
    def loadBinaryFile(f):
        try:
            return pickle.load(open(f, "rb"))
        except Exception as e:
            print("ERROR : ", e)
            return None
    @staticmethod
    def save(o):
        FileIO.saveBinaryFile(o)
    @staticmethod
    def load(f):
        return FileIO.loadBinaryFile(f)
