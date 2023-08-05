use std::borrow::Borrow;
use std::ptr::slice_from_raw_parts;

use ndarray;
use ndarray::{ArrayView, ArrayViewD, IxDyn, s};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArrayDyn, PyReadonlyArray2, PyReadonlyArrayDyn};
use pyo3::prelude::*;
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn rustil(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn psum<'py>(py: Python<'py>, x: PyReadonlyArray2<f64>) -> &'py PyArray2<f64> {
        let array = x.as_array();
        let n = array.shape()[0];
        let n2 = n * (n - 1) / 2;
        let mut v = vec![0.; n * n2];
        let mut m = unsafe { ndarray::Array::from_shape_vec_unchecked((n2, n), v) };
        let mut c: usize = 0;
        for i in 0..n {
            for j in (i + 1)..n {
                let mut sl = m.slice_mut(s![c, ..]);
                sl += &array.slice(s![i, ..]);
                sl += &array.slice(s![j, ..]);
                c += 1
            }
        }
        m.into_pyarray(py)
    }

    Ok(())
}
