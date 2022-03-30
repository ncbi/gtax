import argparse
import gzip
import os
import uuid
from functools import partial
from multiprocessing import Pool

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from gtax.utils import chunks, sequences_to_list


def binning(transcript, bin, step):
    seq_len = len(transcript.seq)
    for i in range(1, seq_len - bin, step):
        yield SeqRecord(Seq(transcript.seq[i: i + bin]), id='{}_{}'.format(transcript.id, i),
                        description='')


def sequence_binning_to_tmpfile(transcripts, bin, step):
    pre = uuid.uuid4()
    with gzip.open('temp_{}.fa.gz'.format(pre), 'wt') as fout:
        sequences = {}
        for r in transcripts:
            for s in binning(r, bin, step):
                if not sequences.setdefault(str(s.seq), False):
                    sequences[str(s.seq)] = True
                    fout.write(s.format("fasta"))
    return pre


def sequence_binning(reference_file, output, seq_len, step, threads):
    print("Creating sequences")
    with Pool(processes=threads) as p:
        results = p.map(partial(sequence_binning_to_tmpfile,
                                bin=seq_len,
                                step=step),
                        [d for d in list(chunks(sequences_to_list(reference_file), 1000))])
    print('Printing final files')
    print('Creating file {}'.format(output))
    with gzip.open('{}'.format(output), 'wt') as fout2:
        sequences = {}
        for pre in results:
            with gzip.open('temp_{}.fa.gz'.format(pre), 'rt') as fin:
                for r in SeqIO.parse(fin, "fasta"):
                    if not sequences.setdefault(str(r.seq), False):
                        sequences[str(r.seq)] = True
                        fout2.write(r.format('fasta'))
            os.remove('temp_{}.fa.gz'.format(pre))


def sequence_binning_main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--reference', help='Reference Transcriptome gzip file',
                        required=True)
    parser.add_argument('--output', help='Output file prefix', required=True)
    parser.add_argument('--threads', help='Number of threads',
                        type=int, required=True)
    parser.add_argument('--seq_len', help='Length of the short sequence',
                        default=100, type=int, required=True)
    parser.add_argument('--step',
                        help='Sequence step to move the bin',
                        type=int, required=True)
    args = parser.parse_args()

    sequence_binning(args.reference,
                     args.output,
                     args.seq_len,
                     args.step,
                     args.threads)
