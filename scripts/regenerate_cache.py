import os
import utils
from hyperparameter4pred import HyperParameter

def regenerate():
    print("Initializing regeneration...")
    hp = HyperParameter()
    
    print(f"Dataset Name: {hp.pred_dataset}")
    print(f"Drug File: {hp.pred_drug_dir}")
    print(f"Prot File: {hp.pred_prot_dir}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    targets = [
        f"{hp.pred_dataset}_mol_pretrain.pkl",
        f"{hp.pred_dataset}_esm_pretrain.pkl"
    ]
    
    for t in targets:
        path = os.path.join(base_dir, t)
        if os.path.exists(path):
            print(f"Removing old cache: {t}")
            os.remove(path)

    if os.path.exists(hp.pred_drug_dir):
        print(f"Regenerating Mol2Vec from {hp.pred_drug_dir}...")
        try:
            utils.get_mol2vec(hp.word2vec_pth, hp.pred_drug_dir, hp.pred_dataset, sep=hp.sep, col_names=hp.d_col_name)
        except Exception as e:
            print(f"MOL2VEC ERROR: {e}")

    if os.path.exists(hp.pred_prot_dir):
        print(f"Regenerating ESM from {hp.pred_prot_dir}...")
        try:
            utils.get_esm_pretrain(hp.pred_prot_dir, hp.pred_dataset, sep=hp.sep, col_names=hp.p_col_name)
        except Exception as e:
            print(f"ESM ERROR: {e}")

    print("Regeneration Complete.")

if __name__ == "__main__":
    regenerate()
