from .jk_contract import Contract
from .jk_contract import Contracts

import sys

__all__ = ('Contracts', 'Contract')

def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    chapter = sys.argv[3]
    sections = list(sys.argv[4:])

    contracts = Contracts(in_path)
    contracts.to_excel(contracts.get_df(contracts.get_sections(chapter, sections)), out_path)