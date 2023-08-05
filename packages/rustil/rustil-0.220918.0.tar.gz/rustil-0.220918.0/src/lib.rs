use std::borrow::Borrow;
use std::ptr::slice_from_raw_parts;
use pyo3::prelude::*;

use ndarray;
use ndarray::{ArrayView, ArrayViewD, IxDyn, s};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArrayDyn, PyReadonlyArray2, PyReadonlyArrayDyn};
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

    #[pyfn(m)]
    fn double_and_random_perturbation(
        _py: Python<'_>,
        x: &PyArrayDyn<f64>,
        perturbation_scaling: f64,
    ) {
        // First we convert the Python numpy array into Rust ndarray
        // Here, you can specify different array sizes and types.
        let mut array = unsafe { x.as_array_mut() }; // Convert to ndarray type

        // Mutate the data
        // No need to return any value as the input data is mutated
        rust_fn::double_and_random_perturbation(&mut array, perturbation_scaling);
    }

    #[pyfn(m)]
    fn eye<'py>(py: Python<'py>, size: usize) -> &PyArray2<f64> {
        // Simple demonstration of creating an ndarray inside Rust and return
        let array = ndarray::Array::eye(size);
        array.into_pyarray(py)
    }

    Ok(())
}

// The rust side functions
// Put it in mod to separate it from the python bindings
// These are just some random operations
// you probably want to do something more meaningful.
mod rust_fn {
    use ndarray::{arr1, Array1};
    use numpy::ndarray::{ArrayViewD, ArrayViewMutD};
    use ordered_float::OrderedFloat;
    use rand::Rng;

    // If we wanted to do something like this in python
    // we probably would want to generate matrices and add them
    // together. This can be problematic in terms of memory if working with large
    // matrices. And looping is usually painfully slow.
    // Rayon could be used here to run the mutation in parallel
    // this may be good for huge matrices
    pub fn double_and_random_perturbation(x: &mut ArrayViewMutD<'_, f64>, scaling: f64) {
        let mut rng = rand::thread_rng();
        x.iter_mut()
            .for_each(|x| *x = *x * 2. + (rng.gen::<f64>() - 0.5) * scaling);
    }

    pub fn max_min(x: &ArrayViewD<'_, f64>) -> Array1<f64> {
        if x.len() == 0 {
            return arr1(&[]); // If the array has no elements, return empty array
        }
        let max_val = x
            .iter()
            .map(|a| OrderedFloat(*a))
            .max()
            .expect("Error calculating max value.")
            .0;
        let min_val = x
            .iter()
            .map(|a| OrderedFloat(*a))
            .min()
            .expect("Error calculating min value.")
            .0;
        let result_array = arr1(&[max_val, min_val]);
        result_array
    }
}
