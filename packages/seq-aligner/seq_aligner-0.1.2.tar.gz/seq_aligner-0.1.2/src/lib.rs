use pyo3::prelude::*;
pub mod gotoh_local;
pub mod gotoh_local_global;
pub mod gotoh_semi_global;
pub mod utils;
use gotoh_local::{gotoh_local_align, gotoh_local_align_all};
use gotoh_local_global::{gotoh_local_global_align, gotoh_local_global_align_all};
use gotoh_semi_global::{gotoh_semi_global_align, gotoh_semi_global_align_all};
use utils::print_align_map;

/// A Python module implemented in Rust.
#[pymodule]
fn seq_aligner(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(print_align_map, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_local_align, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_local_align_all, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_local_global_align, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_local_global_align_all, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_semi_global_align, m)?)?;
    m.add_function(wrap_pyfunction!(gotoh_semi_global_align_all, m)?)?;
    Ok(())
}
