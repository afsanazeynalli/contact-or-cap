from __future__ import annotations

import argparse

from .contacts import detect_contacts, well_contact_summary
from .connectivity import connectivity_screening
from .io import read_input, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Screen fluid contacts and static interwell connectivity."
    )
    parser.add_argument("--input", required=True, help="Input CSV path.")
    parser.add_argument("--output", default="outputs", help="Output directory.")
    parser.add_argument("--min-uncertainty", type=float, default=5.0)
    parser.add_argument("--uncertainty-fraction", type=float, default=0.03)
    args = parser.parse_args()

    df = read_input(args.input)
    contacts = detect_contacts(
        df,
        minimum_uncertainty_m=args.min_uncertainty,
        uncertainty_fraction=args.uncertainty_fraction,
    )
    summary = well_contact_summary(contacts)
    connectivity = connectivity_screening(df)
    write_outputs(contacts, summary, connectivity, args.output)

    print(f"Input records: {len(df)}")
    print(f"Candidate contacts: {len(contacts)}")
    print(f"Outputs written to: {args.output}")


if __name__ == "__main__":
    main()
