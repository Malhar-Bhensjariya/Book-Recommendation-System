import pickle
import os

def load_pickle(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            print("File found")
            return pickle.load(file)
    else:
        print(f"File not found: {file_path}")
        return None

book_name = load_pickle('artifacts/books_name.pkl')
