from glob import glob
from tqdm import tqdm
import click
import os
import pandas as pd
import statistics as st


@click.command()
@click.argument("PATH")
@click.option("--output", "-o", default="all_data.csv", help="Concatenar archivos .csv")
def main(path, output):
    """ Colecciona los archivos .csv """
    dfs = []
    for file in tqdm(glob(os.path.join(path, "*.csv"))):
        dfs.append(pd.read_csv(file))
    all_data = pd.concat(dfs, ignore_index=True)
    print(all_data.describe())
    # print(st.median(all_data["Nodes Complet"]))
    all_data.to_csv(output)


if __name__ == "__main__":
    main()
