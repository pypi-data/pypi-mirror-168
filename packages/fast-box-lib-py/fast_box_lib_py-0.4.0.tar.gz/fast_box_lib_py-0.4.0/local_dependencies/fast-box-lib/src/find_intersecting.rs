use crate::box_def::Box;
use rayon::prelude::*;
use voracious_radix_sort::RadixSort;

/*
 * Some tests suggest that using CalcBox over Box gives a ~30% performance boost.
 */
#[derive(Clone, Copy)]
struct CalcBox {
    x1: i32,
    y1: i32,
    x2: i32,
    y2: i32,
}
fn to_calc_box(b: &Box) -> CalcBox {
    CalcBox {
        x1: b.x1,
        x2: b.x1 + b.xs as i32,
        y1: b.y1,
        y2: b.y1 + b.ys as i32,
    }
}

pub fn find_intersecting_boxes(raw_boxes: &[Box]) -> Vec<Vec<u32>> {
    // setting this keeps rayon from spawning new threads on small inputs
    let inputs_per_thread = 100;
    let boxes: Vec<CalcBox> = raw_boxes.iter().map(to_calc_box).collect();
    assert!(
        (boxes.len() as u64) < ((1_u64) << 32),
        "Only supports 4 billion boxes"
    );
    let mut sorted_boxes: Vec<(CalcBox, u32)> = boxes
        .iter()
        .enumerate()
        .map(|(idx, b)| (*b, idx as u32))
        .collect();
    sorted_boxes.sort_unstable_by_key(|(b, _)| b.x1);

    // only stores boxes to the left ot itself
    let nodes_to_left: Vec<Vec<u32>> = sorted_boxes
        .par_iter()
        .with_min_len(inputs_per_thread)
        .enumerate()
        .map(|(sidx, (b1, _))| {
            sorted_boxes[sidx + 1..]
                .iter()
                .take_while(|(b2, _)| b2.x1 < b1.x2)
                .filter(|(b2, _)| b1.y2 > b2.y1 && b1.y1 < b2.y2)
                .map(|(_, item)| *item)
                .collect()
        })
        .collect();
    let mut graph = vec![Vec::new(); raw_boxes.len()];
    // mirror over all directed connections so that boxes intersect with those to the right of themselves
    for (l, (_, bidx)) in nodes_to_left.iter().zip(sorted_boxes.iter()) {
        for i in l.iter() {
            graph[*i as usize].push(*bidx as u32);
            graph[*bidx as usize].push(*i as u32);
        }
    }
    //sort output lists so output is well defined and easy to test
    graph
        .par_iter_mut()
        .with_min_len(inputs_per_thread)
        .for_each(|l| {
            l.voracious_sort();
        });
    graph
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;
    use crate::intersect_calc::does_intersect;
    use rand::Rng;

    fn find_intersecting_boxes_gold(boxes: &[Box]) -> Vec<Vec<u32>> {
        boxes
            .iter()
            .enumerate()
            .map(|(idx1, b1)| {
                boxes
                    .iter()
                    .enumerate()
                    .filter(|(idx2, b2)| idx1 != *idx2 && does_intersect(b1, b2))
                    .map(|(idx, _)| idx as u32)
                    .collect()
            })
            .collect()
    }
    #[test]
    fn test_boxes_acc() {
        let mut rng = rand::thread_rng();
        let region_size = 400;
        let num_boxes = 100;
        let max_box_size = 100;
        let boxes: Vec<Box> = (0..num_boxes)
            .map(|_| Box {
                x1: rng.gen_range(0..region_size - max_box_size),
                y1: rng.gen_range(0..region_size - max_box_size),
                xs: rng.gen_range(1..max_box_size as u32),
                ys: rng.gen_range(1..max_box_size as u32),
            })
            .collect();
        let gold_result = find_intersecting_boxes_gold(&boxes);
        let test_result = find_intersecting_boxes(&boxes);
        let num_intersections: usize = test_result.iter().map(|l| l.len()).sum();
        assert_eq!(gold_result, test_result);
        //sanity check
        assert!(num_intersections > 0);
    }
}
