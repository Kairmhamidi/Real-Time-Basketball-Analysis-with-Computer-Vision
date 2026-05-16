import os
import pickle

def Write_sub(subPath, obj):
    if subPath is None:
        return
    folder = os.path.dirname(subPath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(subPath, 'wb') as f:
        pickle.dump(obj, f)
def ReadSub(ReadFrom_sub, subPath):
    if subPath is None:
        return None
    if ReadFrom_sub and os.path.exists(subPath):
        with open(subPath, 'rb') as f:
            return pickle.load(f)

    return None