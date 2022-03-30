import gzip

from Bio import SeqIO


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def yield_sequences(reference_file):
    with gzip.open(reference_file, 'rt') as trans_stream:
        for r in SeqIO.parse(trans_stream, "fasta"):
            yield r


def sequences_to_list(reference_file):
    sequences = []
    with gzip.open(reference_file, 'rt') as trans_stream:
        for r in SeqIO.parse(trans_stream, "fasta"):
            sequences.append(r)
    return sequences
