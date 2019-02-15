import pickle

def create_or_load_pickle(data_path, create_func, create_new=False):
    try:
        if create_new: raise FileNotFoundError
        with open(data_path, "rb") as f:
            obj = pickle.load(f)
            print(data_path, "was loaded from the pickle file.")
    except FileNotFoundError:
        obj = create_func()
        with open(data_path, "wb") as f:
            pickle.dump(obj, f)
        print(f"New pickle file {data_path} created.")
    
    return obj

def p(*args):
    print(*args)