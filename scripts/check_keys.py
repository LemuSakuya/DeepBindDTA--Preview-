import pickle
import os

def inspect_pkl(name):
    path = f"{name}_pretrain.pkl"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
            
        print(f"\n--- {name} keys ---")
        if 'vec_dict' in data:
            keys = list(data['vec_dict'].keys())
            print(f"Total count: {len(keys)}")
            print(f"First 10 examples: {keys[:10]}")
            if 'AURKA' in keys:
                 print("AURKA is in cache!")
            else:
                 print("AURKA is NOT in cache.")
            if 'Acemetacin' in keys:
                 print("Acemetacin is in cache!")
            else:
                 print("Acemetacin is NOT in cache.")

        else:
            print("No 'vec_dict' found in pkl.")
            
    except Exception as e:
        print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    inspect_pkl("egfr_mol")
    inspect_pkl("egfr_esm")
