from alignment import align
import os
import math as m

def read_fasta(filepath):
    sequences = {}
    current_header = None
    current_seq = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                # Save previous sequence
                if current_header:
                    sequences[current_header] = ''.join(current_seq)
                # Start new sequence
                current_header = line[1:]  # Remove the '>'
                current_seq = []
            else:
                # Add to current sequence
                current_seq.append(line)
        
        # Don't forget the last sequence
        if current_header:
            sequences[current_header] = ''.join(current_seq)
    
    return sequences

def main():
    seqs = read_fasta('lct_exon8.txt')
    unknown_header, unknown_seq = seqs.popitem()
    best = m.inf
    for header, sequence in seqs.items():
        path, s1, s2 = align(sequence, unknown_seq)
        print(f"{header}: {path}")
        if path < best:
            best = path
            culprit = header
    
    print(f"culpirt: {culprit}")






if __name__ == "__main__":
    main()