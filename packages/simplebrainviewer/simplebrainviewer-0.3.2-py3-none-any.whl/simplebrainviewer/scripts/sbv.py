import argparse
import nibabel as nib
from simplebrainviewer import plot_brain


def main() -> None:
    # parse arguments
    parser = argparse.ArgumentParser(description="View a brain volume")
    parser.add_argument("volume", help="brain volume to view")
    args = parser.parse_args()

    # load data with nibabel
    data = nib.load(args.volume)
    data = nib.as_closest_canonical(data)
    plot_brain(data)
