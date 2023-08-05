use rayon::prelude::*;
use crate::box_def::Box;
use crate::box_intersector::BoxIntersector;


pub fn find_intersecting_boxes_asym(boxes_src: &[Box],boxes_dest: &[Box])->Vec<Vec<u32>>{
    /* Returns a directed bipartite graph from src to dest */
    let intersect_finder = BoxIntersector::new(boxes_dest);
    boxes_src.par_iter().map(|b1|{
        let mut outs:Vec<u32> = intersect_finder.find_intersections(b1);
        outs.sort();// sorts for predictable output
        outs
    })
    .collect()
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;
    use rand::{Rng};
    use crate::intersect_calc::does_intersect;

    fn find_intersecting_boxes_asym_gold(boxes_src: &[Box],boxes_dest: &[Box])->Vec<Vec<u32>>{
        boxes_src.iter().map(| b1|{
            boxes_dest.iter()
            .enumerate()
            .filter(|(_, b2)| does_intersect(b1,b2))
            .map(|(idx,_)|idx as u32)  
            .collect()
        })
        .collect()
    }
    #[test]
    fn test_boxes_asym_acc(){
        let mut rng = rand::thread_rng();
        let region_size = 400;
        let num_boxes = 1000;
        let max_box_size = 100;
        let boxes_src:Vec<Box> = (0..num_boxes).map(|_|Box{
            x1:rng.gen_range(0..region_size-max_box_size),
            y1:rng.gen_range(0..region_size-max_box_size),
            xs:rng.gen_range(1..max_box_size as u32),
            ys:rng.gen_range(1..max_box_size as u32),
        })
        .collect();
        let boxes_dest:Vec<Box> = (0..num_boxes).map(|_|Box{
            x1:rng.gen_range(0..region_size-max_box_size),
            y1:rng.gen_range(0..region_size-max_box_size),
            xs:rng.gen_range(1..max_box_size as u32),
            ys:rng.gen_range(1..max_box_size as u32),
        })
        .collect();
        let gold_result = find_intersecting_boxes_asym_gold(&boxes_src, &boxes_dest);
        let test_result = find_intersecting_boxes_asym(&boxes_src, &boxes_dest);
        let num_intersections:usize = test_result.iter().map(|l|l.len()).sum();
        assert_eq!(gold_result, test_result);
        //sanity check
        assert!(num_intersections > 0);
    }
}