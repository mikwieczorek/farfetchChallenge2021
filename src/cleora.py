import os

import numpy as np


def train_cleora(
    dim: int,
    iter_: int,
    columns: str,
    input_filename: str,
    working_dir: str,
    emb_name: str,
):
    """
    Training Cleora. See more details: https://github.com/Synerise/cleora/
    """
    command = [
        "./cleora-v1.1.1-x86_64-unknown-linux-gnu",
        "--columns",
        columns,
        "--dimension",
        str(dim),
        "-n",
        str(iter_),
        "--input",
        input_filename,
        "--output-dir",
        working_dir,
        "-r",
        emb_name,
    ]

    s = [str(item) for item in command]
    s = " ".join(s)
    os.system(s)


def get_cleora_output_directed(filename: str):
    """
    Read embeddings from file generated by cleora.
    """
    id2embedding = {}
    with open(filename, "r") as f:
        next(f)  # skip cleora header
        for index, line in enumerate(f):
            line_splitted = line.split(sep=" ")
            id = str(line_splitted[0])
            embedding = np.array([float(i) for i in line_splitted[2:]])
            id2embedding[id] = embedding

    return list(id2embedding.keys()), np.stack(list(id2embedding.values()))


def run_cleora_directed(
    working_dir: str, input_file: str, dim: int, iter_: int, columns: str, emb_name: str
):
    train_cleora(dim, iter_, columns, input_file, working_dir, emb_name)
    return get_cleora_output_directed(
        working_dir / str(emb_name + "__product_id__product_id.out")
    )