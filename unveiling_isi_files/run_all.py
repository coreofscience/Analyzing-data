from glob import glob
import click
import os
from tqdm import tqdm
import pandas as pd


@click.command()
@click.argument("PATH")
def main(path):
    """ Aplica main.py a cada uno de los archivos .txt """
    files = glob(os.path.join(path, "*.txt"))
    for file in tqdm(files):
        output = file.replace(".txt", ".csv")
        os.system(f"python main.py  -o {output} {file}")


if __name__ == "__main__":
    main()
