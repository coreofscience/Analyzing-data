from glob import glob
from tqdm import tqdm
import click
import os
import pandas as pd
import statistics as st


@click.group()
def main():
    pass


@main.command()
@click.argument("PATH")
@click.option(
    "--output1", "-o1", default="all_data.csv", help="Concatenar archivos .csv"
)
def all_data(path, output1):
    """ Colecciona los archivos .csv """
    dfs = []
    for file in tqdm(glob(os.path.join(path, "*.csv"))):
        dfs.append(pd.read_csv(file))
    all_data = pd.concat(dfs, ignore_index=True)
    print(all_data.describe())
    # print(st.median(all_data["Nodes Complet"]))
    all_data.to_csv(output1)


@main.command()
@click.option(
    "--output2", "-o2", default="features.csv", help="Caracteristicas de las redes"
)
def features(all_data, output2):
    """ Extrae las caracteristicas estadisticas básicas de las redes """


if __name__ == "__main__":
    main()
