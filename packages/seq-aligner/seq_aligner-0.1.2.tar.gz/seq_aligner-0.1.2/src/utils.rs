use pyo3::prelude::*;
use std::rc::Rc;

#[derive(Debug)]
pub struct AlignerConfig {
    pub chr_match: isize,
    pub chr_mismatch: isize,
    pub gap_open: isize,
    pub gap_extend: isize,
}

impl Default for AlignerConfig {
    fn default() -> Self {
        Self {
            chr_match: 1,
            chr_mismatch: -1,
            gap_open: -3,
            gap_extend: -1,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum Matrix {
    Vertical,   //Up
    Horizontal, //Left
    Score,      //Diagonal
}

#[derive(Debug, Clone, Copy)]
pub enum AlignType {
    ChrMatch,
    ChrMismatch,
    Insertion,
    Deletion,
}

#[derive(Debug, Clone, Copy)]
pub struct BaseAlign {
    pub upos1: usize,
    pub upos2: usize,
    pub umatrix: Matrix,
    pub pos1: usize,
    pub pos2: usize,
    pub matrix: Matrix,
    pub chr1: Option<char>,
    pub chr2: Option<char>,
    pub atype: AlignType,
}

impl BaseAlign {
    pub fn new(
        upos1: usize,
        upos2: usize,
        umatrix: Matrix,
        pos1: usize,
        pos2: usize,
        matrix: Matrix,
        chr1: Option<char>,
        chr2: Option<char>,
        mode: AlignType,
    ) -> Self {
        Self {
            upos1,
            upos2,
            umatrix,
            pos1,
            pos2,
            matrix,
            chr1,
            chr2,
            atype: mode,
        }
    }
}

pub fn print_matrix(label: &str, matrix: &Vec<Vec<isize>>) {
    println!("{}:", label);
    let row_count = matrix.len();
    assert_ne!(row_count, 0);
    let column_count = matrix[0].len();
    print!("{:>3}", "");
    for j in 0..column_count {
        print!("{:>8},", j);
    }
    println!("");
    for (i, row) in matrix.into_iter().enumerate() {
        print!("{:>3}", i);
        for cell in row {
            print!("{:>8},", cell);
        }
        println!("");
    }
}

pub fn align_path_to_align_map(
    align_path: &Vec<Rc<BaseAlign>>,
) -> Vec<(String, usize, usize, char, char, char)> {
    let mut align_result: Vec<(String, usize, usize, char, char, char)> = Vec::new();
    for align in align_path {
        let mtype = match align.matrix {
            Matrix::Score => "diagonal",
            Matrix::Vertical => "up",
            Matrix::Horizontal => "left",
        };
        let atype = match align.atype {
            AlignType::ChrMatch => '|',
            AlignType::ChrMismatch => '*',
            AlignType::Insertion => ' ',
            AlignType::Deletion => ' ',
        };
        let chr1 = match align.chr1 {
            Some(x) => x,
            None => '-',
        };
        let chr2 = match align.chr2 {
            Some(x) => x,
            None => '-',
        };
        align_result.push((mtype.to_string(), align.pos1, align.pos2, chr1, chr2, atype))
    }
    align_result
}

#[pyfunction]
pub fn print_align_map(max_score: isize, align_map: Vec<(String, usize, usize, char, char, char)>) {
    let seq1_start = align_map.first().unwrap().1;
    let seq1_end = align_map.last().unwrap().1;
    assert!(seq1_start <= seq1_end);
    let seq2_start = align_map.first().unwrap().2;
    let seq2_end = align_map.last().unwrap().2;
    assert!((seq2_start <= seq1_end));
    let mut seq1_list: Vec<char> = vec![];
    let mut seq2_list: Vec<char> = vec![];
    let mut match_list: Vec<char> = vec![];
    for align in align_map {
        seq1_list.push(align.3);
        seq2_list.push(align.4);
        match_list.push(align.5);
    }
    let seq1 = format!(
        "{seq1_start:<5} {seq1} {seq1_end:>5}\tScore:{max_score}",
        seq1_start = seq1_start,
        seq1 = seq1_list.iter().collect::<String>(),
        seq1_end = seq1_end,
        max_score = max_score
    );
    let seqm = format!(
        "{blank:<5} {match} {blank:>5}",
        blank=' ',
        match=match_list.iter().collect::<String>(),
    );
    let seq2 = format!(
        "{seq2_start:<5} {seq2} {seq2_end:>5}",
        seq2_start = seq2_start,
        seq2 = seq2_list.iter().collect::<String>(),
        seq2_end = seq2_end,
    );
    println!("{}\n{}\n{}", seq1, seqm, seq2);
}
