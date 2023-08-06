# Sequence alignment algorithm

## Gotoh Local Alignment  
Classical gotoh local algorithm 

```python
In [1]: import seq_aligner

In [2]: r=seq_aligner.gotoh_local_align("CCAGCT", "AGCCTA", 1,-1,-3,-1)

In [3]: seq_aligner.print_align_map(r[0],r[1][0])
3     AGC     5 Score:3
      |||      
1     AGC     3
```

## Gotoh Semi-Global Alignment  
Classical gotoh semi-global algorithm.  
Initialize the top row and leftmost column to zero and terminate end at either the bottom row or rightmost column [[ref](https://bio.libretexts.org/Bookshelves/Computational_Biology/Book%3A_Computational_Biology_-_Genomes_Networks_and_Evolution_(Kellis_et_al.)/03%3A_Rapid_Sequence_Alignment_and_Database_Search/3.03%3A_Global_alignment_vs._Local_alignment_vs._Semi-global_alignment)].

```python
In [4]: r=seq_aligner.gotoh_semi_global_align("CCAGCT", "AGCCTA", 1,-1,-3,-1)

In [5]: seq_aligner.print_align_map(r[0],r[1][0])
3     AGCT     6        Score:2
      |||*      
1     AGCC     4
```

## Gotoh Local Global Alignment  
Variants of the local and semi-global algorithms

```python
In [6]: r=seq_aligner.gotoh_local_global_align("CCAGCT", "AGCCTA", 1,-1,-3,-1)

In [7]: seq_aligner.print_align_map(r[0],r[1][0])
3     AGC---     5      Score:-3
      |||         
1     AGCCTA     6

```