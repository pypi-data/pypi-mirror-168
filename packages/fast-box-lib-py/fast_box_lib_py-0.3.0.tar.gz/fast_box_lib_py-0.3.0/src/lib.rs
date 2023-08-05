use pyo3::prelude::*;
use numpy::{PyArray, PyReadonlyArray1, PyReadonlyArray2, PyArray1};
use pyo3::types::PyList;
use pyo3::exceptions::PyAssertionError;
use fast_box_lib;
use fast_box_lib::Box;


fn generate_boxes<Func>(array: &PyReadonlyArray2<i32>, func: &mut Func)-> PyResult<()>
    where Func: FnMut(Box)->(){
    let dims = array.dims();
    let lenx= dims[1];
    let leny= dims[0];
    if lenx != 4{
        return Err(PyAssertionError::new_err("Expects 2nd dimension of box array to be size 4 (x, y, width, height)"));
    }
    if leny == 0{
        return Ok(())
    }
    let arr = array.as_array();
    let contig_arr = arr.as_standard_layout();
    let slice = contig_arr.as_slice().unwrap();
    for i in 0..leny{
        let barr = &slice[i*4..(i+1)*4];
        let (x1, y1, width, height) = (barr[0], barr[1], barr[2], barr[3]);
        if width <= 0 || height <= 0{
            return Err(PyAssertionError::new_err("Expects width and hight of boxes to be greater than 0"));
        }
        func(Box{x1:x1, y1:y1, xs:width as u32, ys: height as u32});
    }
    Ok(())
}

fn np_arr_to_boxes(array: &PyReadonlyArray2<i32>)->PyResult<Vec<Box>>{
    let mut boxes:Vec<Box> = Vec::with_capacity(array.dims()[0]);
    generate_boxes(array, &mut |b|{
        boxes.push(b);
    })?;
    Ok(boxes)
}

fn np_arr_to_box<'a>(array: &'a PyReadonlyArray1<i32>)->PyResult<Box>{
    let dims = array.dims();
    let len= dims[0];
    if len != 4{
        return Err(PyAssertionError::new_err("Expects box array to be size 4 (x, y, width, height)"));
    }
    let arr = array.as_array();
    if arr[2] <= 0 || arr[3] <= 0{
        return Err(PyAssertionError::new_err("Expects width and hight of boxes to be greater than 0"));
    }
    let box_ = Box{
        x1: arr[0],
        y1: arr[1],
        xs: arr[2] as u32,
        ys: arr[3] as u32,
    };
    Ok(box_)
}

fn adj_list_to_py_list<'py>(py: Python<'py>,adj_list: Vec<Vec<u32>>)->PyResult<&'py PyList> {
    Ok(PyList::new(py,
        adj_list.iter()
        .map(|x|PyArray::from_vec(py, x.clone()))
    ))
}

#[pyfunction]
fn find_intersecting_boxes<'py>(
    py: Python<'py>,
    boxes_array: PyReadonlyArray2<i32>) -> PyResult<&'py PyList> {
    let boxes = np_arr_to_boxes(&boxes_array)?;
    let adj_list = fast_box_lib::find_intersecting_boxes(&boxes);
    Ok(adj_list_to_py_list(py, adj_list)?)
}

#[pyfunction]
fn find_intersecting_boxes_asym<'py>(
    py: Python<'py>,
    boxes_array_src: PyReadonlyArray2<i32>,
    boxes_array_dest: PyReadonlyArray2<i32>
) -> PyResult<&'py PyList> {
    let adj_list = fast_box_lib::find_intersecting_boxes_asym(
        &np_arr_to_boxes(&boxes_array_src)?,
        &np_arr_to_boxes(&boxes_array_dest)?,
    );
    Ok(adj_list_to_py_list(py, adj_list)?)
}

#[pyfunction]
fn intersect_area<'py>(
    py: Python<'py>,
    box1: PyReadonlyArray1<i32>,
    boxes: PyReadonlyArray2<i32>
) -> PyResult<&'py PyArray1<u64>> {
    let box_ =np_arr_to_box(&box1)?;
    let mut area_vec:Vec<u64> = Vec::with_capacity(boxes.dims()[0]);
    generate_boxes(&boxes, &mut |b|{
        area_vec.push(fast_box_lib::intersect_area(&box_, &b));
    })?;
    Ok(PyArray::from_vec(py, area_vec))
}

#[pyclass]
struct BoxIntersector {
    inner: fast_box_lib::BoxIntersector
}

#[pymethods]
impl BoxIntersector {
    #[new]
    pub fn new(boxes_arr: PyReadonlyArray2<i32>)->PyResult<Self>{
        Ok(BoxIntersector{
            inner: fast_box_lib::BoxIntersector::new(&np_arr_to_boxes(&boxes_arr)?)
        })
    }
    pub fn find_intersections<'py>(&self, py: Python<'py>, x1: i32, y1: i32, width: u32, height: u32)->PyResult<&'py PyArray1<u32>>{
        Ok(PyArray::from_vec(py,self.inner.find_intersections(&Box{x1:x1, y1:y1, xs:width, ys:height})))
    }
}

#[pyfunction]
fn find_non_max_suppressed<'py>(
    py: Python<'py>,
    boxes_array: PyReadonlyArray2<i32>,
    scores: PyReadonlyArray1<f64>,
    iou_threshold: f64,
    overlap_threshold: f64,
) ->  PyResult<&'py PyArray1<bool>> {
    let adj_list = fast_box_lib::find_non_max_suppressed(
        &np_arr_to_boxes(&boxes_array)?,
        scores.as_array().as_standard_layout().as_slice().unwrap(),
        iou_threshold,
        overlap_threshold
    );
    Ok(PyArray::from_vec(py, adj_list))
}

/// A Python module implemented in Rust.
#[pymodule]
fn fast_box_lib_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_intersecting_boxes, m)?)?;
    m.add_function(wrap_pyfunction!(find_intersecting_boxes_asym, m)?)?;
    m.add_function(wrap_pyfunction!(find_non_max_suppressed, m)?)?;
    m.add_function(wrap_pyfunction!(intersect_area, m)?)?;
    m.add_class::<BoxIntersector>()?;
    Ok(())
}
