import torch
import esm
import pandas as pd
from tqdm import tqdm
import pickle
import numpy as np
from gensim.models import word2vec
from mol2vec.features import mol2alt_sentence
from rdkit import Chem
import os


def _find_pretrain_file(base_dir, db_name, kind):
    candidates = [
        os.path.join(base_dir, f'{db_name}_{kind}_pretrain.pkl'),
        os.path.join(base_dir, f'{str(db_name).lower()}_{kind}_pretrain.pkl'),
        os.path.join(base_dir, f'{str(db_name).upper()}_{kind}_pretrain.pkl')
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # 兜底：任意同类缓存
    try:
        for fname in os.listdir(base_dir):
            if fname.endswith(f'_{kind}_pretrain.pkl'):
                return os.path.join(base_dir, fname)
    except Exception:
        pass
    return None


def get_esm_pretrain(df_dir, db_name, sep=' ', header=None,
                    col_names=['drug_id', 'prot_id', 'drug_smile', 'prot_seq', 'label'], is_save=True):
    # load data
    # Use CWD explicitly to avoid unicode issues in __file__ path
    base_dir = os.getcwd() 
    file_path = os.path.join(base_dir, f'{db_name}_esm_pretrain.pkl')
    if not os.path.exists(file_path):
        # Fallback to search relative to script if CWD fails? 
        # But here logic was searching for alternate names.
        alt_path = _find_pretrain_file(base_dir, db_name, 'esm')
        if alt_path:
            file_path = alt_path

    data_cache = None
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb+') as f:
                data_cache = pickle.load(f)
                print(f"Load pretrained feature: {file_path}.", flush=True)
        except Exception:
            data_cache = None
            
    if data_cache is None:
        data_cache = {"vec_dict": {}, "mat_dict": {}, "length_dict": {}}

    df = pd.read_csv(df_dir, sep=sep)
    df.columns = col_names
    df.drop_duplicates(subset='prot_id', inplace=True)
    prot_ids = df['prot_id'].tolist()
    prot_seqs = df['prot_seq'].tolist()

    emb_dict = data_cache.get("vec_dict", {})
    emb_mat_dict = data_cache.get("mat_dict", {})
    length_target = data_cache.get("length_dict", {})
    
    missing_indices = []
    for i, pid in enumerate(prot_ids):
        if str(pid) not in emb_dict:
            missing_indices.append(i)
            
    if not missing_indices and emb_dict:
        return data_cache

    print(f"Updating cache for {len(missing_indices)} new proteins...", flush=True)
    
    # Load ESM-2 model
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()  # disables dropout for deterministic results

    data = []
    for i in missing_indices:
        seq_len = min(len(prot_seqs[i]), 1022)
        data.append((prot_ids[i], prot_seqs[i][:seq_len]))

    for d in data:
        prot_id = str(d[0])
        batch_labels, batch_strs, batch_tokens = batch_converter([d])
        batch_lens = (batch_tokens != alphabet.padding_idx).sum(1)
        # Extract per-residue representations (on CPU)
        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[33], return_contacts=True)
        token_representations = results["representations"][33].numpy()

        sequence_representations = []
        for i, tokens_len in enumerate(batch_lens):
            sequence_representations.append(token_representations[i, 1: tokens_len - 1].mean(0))

        emb_dict[prot_id] = sequence_representations[0]
        emb_mat_dict[prot_id] = token_representations[0]
        length_target[prot_id] = len(d[1])

    # save
    dump_data = {
        "dataset": db_name,
        "vec_dict": emb_dict,
        "mat_dict": emb_mat_dict,
        "length_dict": length_target
    }
    if is_save:
        with open(file_path, 'wb+') as f:
            pickle.dump(dump_data, f)
            print(f"Updated cache saved to {file_path}")
            
    return dump_data


def get_mol2vec(word2vec_pth, df_dir, db_name, sep=' ',
                col_names=['drug_id', 'prot_id', 'drug_smile', 'prot_seq', 'label'], embedding_dimension=300,
                is_debug=False, is_save=True):
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, f'{db_name}_mol_pretrain.pkl')
    if not os.path.exists(file_path):
        alt_path = _find_pretrain_file(base_dir, db_name, 'mol')
        if alt_path:
            file_path = alt_path

    data_cache = None
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb+') as f:
                data_cache = pickle.load(f)
                print(f"Load pretrained feature: {file_path}.", flush=True)
        except Exception:
            data_cache = None
            
    if data_cache is None:
        data_cache = {"vec_dict": {}, "mat_dict": {}, "length_dict": {}}

    mol2vec_model = word2vec.Word2Vec.load(word2vec_pth)
    df = pd.read_csv(df_dir, sep=sep)
    df.columns = col_names
    df.drop_duplicates(subset='drug_id', inplace=True)
    drug_ids = df['drug_id'].tolist()
    drug_seqs = df['drug_smile'].tolist()

    emb_dict = data_cache.get("vec_dict", {})
    emb_mat_dict = data_cache.get("mat_dict", {})
    length_dict = data_cache.get("length_dict", {})

    missing_indices = []
    for idx, did in enumerate(drug_ids):
        if str(did) not in emb_dict:
            missing_indices.append(idx)
            
    if not missing_indices and emb_dict:
         return data_cache
         
    print(f"Updating cache for {len(missing_indices)} new drugs...", flush=True)

    percent_unknown = []
    bad_mol = 0

    # get pretrain feature
    for idx in missing_indices:
        flag = 0
        mol_miss_words = 0

        drug_id = str(drug_ids[idx])
        molecule = Chem.MolFromSmiles(drug_seqs[idx])
        length_dict # preserve ref? no, bug in old code lines 129
        try:
            # Get fingerprint from molecule
            sub_structures = mol2alt_sentence(molecule, 2)
        except Exception as e:
            if is_debug:
                print(e)
            percent_unknown.append(100)
            # Fallback for failed molecules: use UNK or zeros
            emb_dict[drug_id] = np.zeros(embedding_dimension)
            emb_mat_dict[drug_id] = np.zeros((1, embedding_dimension))
            length_dict[drug_id] = 1
            bad_mol += 1
            continue

        # 存储该分子的子结构特征矩阵
        emb_mat = np.zeros((len(sub_structures), embedding_dimension))
        length_dict[drug_id] = len(sub_structures)

        # 遍历分子中每个子结构
        for i, sub in enumerate(sub_structures):
            # Check to see if substructure exists
            try:
                emb_dict[drug_id] = emb_dict.get(drug_id, np.zeros(embedding_dimension)) + mol2vec_model.wv[sub]
                emb_mat[i] = mol2vec_model.wv[sub]
                # If not, replace with UNK (unknown)
            except Exception as e:
                # if is_debug: print(e)
                emb_dict[drug_id] = emb_dict.get(drug_id, np.zeros(embedding_dimension)) + mol2vec_model.wv['UNK']
                emb_mat[i] = mol2vec_model.wv['UNK']
                flag = 1
                mol_miss_words = mol_miss_words + 1
        emb_mat_dict[drug_id] = emb_mat

        if len(sub_structures) > 0:
            percent_unknown.append((mol_miss_words / len(sub_structures)) * 100)
        else:
            percent_unknown.append(0)

        if flag == 1:
            bad_mol = bad_mol + 1

    # print(f'All Bad Mol: {bad_mol}, Avg Miss Rate: ...')
    dump_data = {
        "dataset": db_name,
        "vec_dict": emb_dict,
        "mat_dict": emb_mat_dict,
        "length_dict": length_dict
    }
    if is_save:
        with open(file_path, 'wb+') as f:
            pickle.dump(dump_data, f)
            print(f"Updated cache saved to {file_path}")
            
    return dump_data


def get_pairs(drug_dir, prot_dir, sep, d_col_names, p_col_names):
    d_df = pd.read_csv(drug_dir, sep=sep)
    d_df.columns = d_col_names
    p_df = pd.read_csv(prot_dir, sep=sep)
    p_df.columns = p_col_names

    pair_dict = {'drug_id': [], 'prot_id': [], 'drug_smile': [], 'prot_seq': []}
    for i, row_d in d_df.iterrows():
        for j, row_p in p_df.iterrows():
            pair_dict['drug_id'].append(row_d['drug_id'])
            pair_dict['prot_id'].append(row_p['prot_id'])
            pair_dict['drug_smile'].append(row_d['drug_smile'])
            pair_dict['prot_seq'].append(row_p['prot_seq'])

    pair_df = pd.DataFrame(pair_dict, index=None)
    return pair_df