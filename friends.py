import pickle

if __name__ == "__main__":
    with open("friends.txt", "wb") as wf:
        pickle.dump(set(), wf)
