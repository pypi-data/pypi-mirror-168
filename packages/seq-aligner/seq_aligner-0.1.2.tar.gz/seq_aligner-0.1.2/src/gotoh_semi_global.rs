use crate::utils::{align_path_to_align_map, AlignType, AlignerConfig, BaseAlign, Matrix};
use pyo3::prelude::*;
use std::cmp;
use std::rc::Rc;

#[derive(Debug)]
struct GotohSemiGlobal {
    config: AlignerConfig,
    seq1: Vec<char>,
    seq2: Vec<char>,
    scoring_matrix: Vec<Vec<isize>>,
    horizontal_matrix: Vec<Vec<isize>>, //horizontal gap 水平缺失 seq1 gap
    vertical_matrix: Vec<Vec<isize>>,   //vertical gap 垂直缺失 seq2 gap
    max_score: isize,
    sub_score: isize,
    max_score_positions: Vec<(usize, usize)>,
}

impl GotohSemiGlobal {
    fn new(seq1: &str, seq2: &str, config: AlignerConfig) -> Self {
        Self {
            config: config,
            seq1: seq1.chars().collect(),
            seq2: seq2.chars().collect(),
            scoring_matrix: Vec::new(),
            horizontal_matrix: Vec::new(),
            vertical_matrix: Vec::new(),
            max_score: std::isize::MIN,
            sub_score: std::isize::MIN,
            max_score_positions: Vec::new(),
        }
    }

    fn cmp_chr(chr1: char, chr2: char) -> bool {
        if chr1 == chr2 {
            true
        } else {
            false
        }
    }

    /// [[0, 0, 0, 0, 0, 0, 0, 0],
    ///  [0, 0, 0, 1, 0, 0, 0, 0],
    ///  [0, 0, 0, 0, 0, 1, 0, 0],
    ///  [0, 1, 1, 0, 0, 0, 2, 0],
    ///  [0, 0, 0, 0, 1, 0, 0, 3],
    ///  [0, 0, 0, 1, 0, 0, 0, 0],
    ///  [0, 1, 1, 0, 0, 0, 1, 0],
    ///  [0, 0, 0, 0, 1, 0, 0, 2]]
    ///
    fn compute_scoring_matrix(&mut self) {
        let seq1_len = self.seq1.len();
        let seq2_len = self.seq2.len();
        //i row index, j column index
        for i in 0..(seq1_len + 1) {
            self.scoring_matrix.push(vec![0; seq2_len + 1]);
            self.horizontal_matrix.push(vec![0; seq2_len + 1]);
            self.vertical_matrix.push(vec![0; seq2_len + 1]);
            for j in 0..(seq2_len + 1) {
                if i == 0 {
                    //i equal 0, j increase from 0 to seq2_len
                    self.scoring_matrix[i][j] = 0;
                    self.vertical_matrix[i][j] = if let 0 = j {
                        0
                    } else {
                        self.config.gap_open + self.config.gap_open * seq1_len as isize
                    };
                    self.horizontal_matrix[i][j] = self.scoring_matrix[i][j];
                } else if j == 0 {
                    // j equal 0, i increase from 1 to seq1_len
                    self.scoring_matrix[i][j] = 0;
                    self.vertical_matrix[i][j] = self.scoring_matrix[i][j];
                    self.horizontal_matrix[i][j] = if let 0 = i {
                        0
                    } else {
                        self.config.gap_open + self.config.gap_open * seq2_len as isize
                    };
                } else {
                    let _diagonal_value: isize = if let true =
                        GotohSemiGlobal::cmp_chr(self.seq1[i - 1], self.seq2[j - 1])
                    {
                        self.scoring_matrix[i - 1][j - 1] + self.config.chr_match
                    } else {
                        self.scoring_matrix[i - 1][j - 1] + self.config.chr_mismatch
                    };
                    self.vertical_matrix[i][j] = cmp::max(
                        self.vertical_matrix[i - 1][j] + self.config.gap_extend,
                        self.scoring_matrix[i - 1][j]
                            + self.config.gap_open
                            + self.config.gap_extend,
                    );
                    self.horizontal_matrix[i][j] = cmp::max(
                        self.horizontal_matrix[i][j - 1] + self.config.gap_extend,
                        self.scoring_matrix[i][j - 1]
                            + self.config.gap_open
                            + self.config.gap_extend,
                    );
                    self.scoring_matrix[i][j] = cmp::max(
                        _diagonal_value,
                        cmp::max(self.horizontal_matrix[i][j], self.vertical_matrix[i][j]),
                    );
                }
            }
        }
        let j = seq2_len;
        for i in 0..(seq1_len + 1) {
            if self.scoring_matrix[i][j] > self.max_score {
                self.sub_score = self.max_score;
                self.max_score = self.scoring_matrix[i][j];
                self.max_score_positions.clear();
            }
            if self.scoring_matrix[i][j] == self.max_score {
                self.max_score_positions.push((i, j))
            }
        }
        let i = seq1_len;
        for j in 0..(seq2_len + 1) {
            if self.scoring_matrix[i][j] > self.max_score {
                self.sub_score = self.max_score;
                self.max_score = self.scoring_matrix[i][j];
                self.max_score_positions.clear();
            }
            if self.scoring_matrix[i][j] == self.max_score {
                self.max_score_positions.push((i, j))
            }
        }
    }

    fn _get_vertical_neighboured(
        &self,
        i: usize,
        j: usize,
        neighboured_list: &mut Vec<Rc<BaseAlign>>,
    ) {
        // seq2 deletion
        let _chr1 = self.seq1[i - 1];
        if self.vertical_matrix[i][j] == self.vertical_matrix[i - 1][j] + self.config.gap_extend {
            neighboured_list.push(Rc::new(BaseAlign::new(
                i - 1,
                j,
                Matrix::Vertical,
                i,
                j,
                Matrix::Vertical,
                Some(_chr1),
                None,
                AlignType::Deletion,
            )));
        };
        if self.vertical_matrix[i][j]
            == self.scoring_matrix[i - 1][j] + self.config.gap_open + self.config.gap_extend
        {
            neighboured_list.push(Rc::new(BaseAlign::new(
                i - 1,
                j,
                Matrix::Score,
                i,
                j,
                Matrix::Vertical,
                Some(_chr1),
                None,
                AlignType::Deletion,
            )));
        };
    }

    fn _get_horizontal_neighboured(
        &self,
        i: usize,
        j: usize,
        neighboured_list: &mut Vec<Rc<BaseAlign>>,
    ) {
        // seq2 insertion
        let _chr2 = self.seq2[j - 1];
        if self.horizontal_matrix[i][j] == self.horizontal_matrix[i][j - 1] + self.config.gap_extend
        {
            neighboured_list.push(Rc::new(BaseAlign::new(
                i,
                j - 1,
                Matrix::Horizontal,
                i,
                j,
                Matrix::Horizontal,
                None,
                Some(_chr2),
                AlignType::Insertion,
            )));
        };
        if self.horizontal_matrix[i][j]
            == self.scoring_matrix[i][j - 1] + self.config.gap_open + self.config.gap_extend
        {
            neighboured_list.push(Rc::new(BaseAlign::new(
                i,
                j - 1,
                Matrix::Score,
                i,
                j,
                Matrix::Horizontal,
                None,
                Some(_chr2),
                AlignType::Insertion,
            )));
        };
    }

    fn get_neighboured(&self, i: usize, j: usize, matrix: &Matrix) -> Vec<Rc<BaseAlign>> {
        let mut _neighboured_list: Vec<Rc<BaseAlign>> = Vec::new();
        match matrix {
            //Diagonal
            Matrix::Score => {
                if i > 0 && j > 0 {
                    // middle cell
                    let _chr1 = self.seq1[i - 1];
                    let _chr2 = self.seq2[j - 1];
                    // diagonal match
                    if true == GotohSemiGlobal::cmp_chr(_chr1, _chr2) {
                        if self.scoring_matrix[i][j]
                            == self.scoring_matrix[i - 1][j - 1] + self.config.chr_match
                        {
                            _neighboured_list.push(Rc::new(BaseAlign::new(
                                i - 1,
                                j - 1,
                                Matrix::Score,
                                i,
                                j,
                                Matrix::Score,
                                Some(_chr1),
                                Some(_chr2),
                                AlignType::ChrMatch,
                            )));
                        };
                    } else {
                        // diagonal mismatch
                        if self.scoring_matrix[i][j]
                            == self.scoring_matrix[i - 1][j - 1] + self.config.chr_mismatch
                        {
                            _neighboured_list.push(Rc::new(BaseAlign::new(
                                i - 1,
                                j - 1,
                                Matrix::Score,
                                i,
                                j,
                                Matrix::Score,
                                Some(_chr1),
                                Some(_chr2),
                                AlignType::ChrMismatch,
                            )));
                        };
                    };
                };
                if i > 0 && self.scoring_matrix[i][j] == self.vertical_matrix[i][j] {
                    // seq2 deletion
                    self._get_vertical_neighboured(i, j, &mut _neighboured_list)
                };
                if j > 0 && self.scoring_matrix[i][j] == self.horizontal_matrix[i][j] {
                    // seq2 insertion
                    self._get_horizontal_neighboured(i, j, &mut _neighboured_list)
                };
            }
            //Up
            Matrix::Vertical => {
                // seq2 deletion
                self._get_vertical_neighboured(i, j, &mut _neighboured_list)
            }
            //Left
            Matrix::Horizontal => {
                // seq2 insertion
                self._get_horizontal_neighboured(i, j, &mut _neighboured_list)
            }
        };
        _neighboured_list
    }

    fn traceback(&self, mut i: usize, mut j: usize) -> Vec<Rc<BaseAlign>> {
        let mut align_path: Vec<Rc<BaseAlign>> =
            Vec::with_capacity(cmp::max(self.seq1.len(), self.seq2.len()));
        let mut matrix = Matrix::Score;
        loop {
            // println!("{} {} {:?} {}", i, j, matrix, self.scoring_matrix[i][j]);
            if i == 0 || j == 0 {
                break;
            }
            let neighboured = self.get_neighboured(i, j, &matrix);
            if neighboured.len() == 1 {
                align_path.insert(0, neighboured[0].clone());
                i = neighboured[0].upos1;
                j = neighboured[0].upos2;
                matrix = neighboured[0].umatrix;
            } else if neighboured.len() > 1 {
                align_path.insert(0, neighboured[0].clone());
                i = neighboured[0].upos1;
                j = neighboured[0].upos2;
                matrix = neighboured[0].umatrix;
            } else {
                let chr1: Option<char> = if let true = i > 1 {
                    Some(self.seq1[i])
                } else {
                    None
                };
                let chr2: Option<char> = if let true = j > 1 {
                    Some(self.seq2[j])
                } else {
                    None
                };
                panic!(
                    "Can't get neighboured i:{i} {j} {matrix:?} {chr1:?} {chr2:?} {score_ij} {score_i1j} {score_ij1} {score_i1j1} {v_i1j} {h_ij1}",
                    i=i,
                    j=j,
                    matrix=matrix,
                    chr1=chr1,
                    chr2=chr2,
                    score_ij=self.scoring_matrix[i][j],
                    score_i1j=self.scoring_matrix[i-1][j],
                    score_ij1=self.scoring_matrix[i][j-1],
                    score_i1j1=self.scoring_matrix[i-1][j-1],
                    v_i1j=self.vertical_matrix[i-1][j],
                    h_ij1=self.horizontal_matrix[i][j-1]
                );
            }
        }
        align_path
    }

    fn traceback_all(&self, i: usize, j: usize, matrix: &Matrix) -> Vec<Vec<Rc<BaseAlign>>> {
        let mut align_paths: Vec<Vec<Rc<BaseAlign>>> = Vec::new();
        if i == 0 || j == 0 {
            align_paths.push(Vec::with_capacity(cmp::max(
                self.seq1.len(),
                self.seq2.len(),
            )));
        } else {
            let neighboureds = self.get_neighboured(i, j, &matrix);
            if neighboureds.len() == 0 {
                panic!("Neighboureds is zero: {} {} {:?}", i, j, matrix);
            }
            for neighboured in neighboureds {
                for mut path in
                    self.traceback_all(neighboured.upos1, neighboured.upos2, &neighboured.umatrix)
                {
                    path.push(neighboured.clone());
                    align_paths.push(path);
                }
            }
        }
        align_paths
    }
}

/// Do gotoh local alignment
#[pyfunction]
pub fn gotoh_semi_global_align(
    seq1: &str,
    seq2: &str,
    chr_match: isize,
    chr_mismatch: isize,
    gap_open: isize,
    gap_extend: isize,
) -> PyResult<(isize, Vec<Vec<(String, usize, usize, char, char, char)>>)> {
    let config = AlignerConfig {
        chr_match: chr_match,
        chr_mismatch: chr_mismatch,
        gap_open: gap_open,
        gap_extend: gap_extend,
        ..Default::default()
    };
    let mut align = GotohSemiGlobal::new(seq1, seq2, config);
    align.compute_scoring_matrix();
    // print_matrix("vertical", &align.vertical_matrix);
    // print_matrix("score", &align.scoring_matrix);
    // print_matrix("horizontal", &align.horizontal_matrix);
    // println!(
    //     "Max score {}, positions {:?}",
    //     align.max_score, align.max_score_positions
    // );
    let mut align_result_list: Vec<Vec<(String, usize, usize, char, char, char)>> = Vec::new();
    for pos in &align.max_score_positions {
        let align_path = align.traceback(pos.0, pos.1);
        align_result_list.push(align_path_to_align_map(&align_path));
    }
    Ok((align.max_score, align_result_list))
}

/// Do gotoh local alignment all alignment
#[pyfunction]
pub fn gotoh_semi_global_align_all(
    seq1: &str,
    seq2: &str,
    chr_match: isize,
    chr_mismatch: isize,
    gap_open: isize,
    gap_extend: isize,
) -> PyResult<(isize, Vec<Vec<(String, usize, usize, char, char, char)>>)> {
    let config = AlignerConfig {
        chr_match: chr_match,
        chr_mismatch: chr_mismatch,
        gap_open: gap_open,
        gap_extend: gap_extend,
        ..Default::default()
    };
    let mut align = GotohSemiGlobal::new(seq1, seq2, config);
    align.compute_scoring_matrix();
    let mut align_result_list: Vec<Vec<(String, usize, usize, char, char, char)>> = Vec::new();
    for pos in &align.max_score_positions {
        for align_path in align.traceback_all(pos.0, pos.1, &Matrix::Score) {
            align_result_list.push(align_path_to_align_map(&align_path))
        }
    }
    Ok((align.max_score, align_result_list))
}
