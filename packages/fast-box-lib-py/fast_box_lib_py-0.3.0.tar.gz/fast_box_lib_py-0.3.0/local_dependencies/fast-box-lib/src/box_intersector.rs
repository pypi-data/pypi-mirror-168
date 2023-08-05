use crate::interval_tree::{IntervalTree,Interval};
use crate::box_def::Box;

pub struct BoxIntersector{
    tree: IntervalTree<i32, (Box, u32)>,
}
fn get_interval(b: &Box)->Interval<i32>{
    Interval { left: b.x1, right: b.x2() }
}
impl BoxIntersector {
    pub fn new(boxes:&[Box])->BoxIntersector{
        let enumerated_boxes = boxes.iter().cloned().zip(0..boxes.len() as u32);
        BoxIntersector{
            tree: IntervalTree::create_from_fn(enumerated_boxes, |(b,_)|get_interval(b))
        }
    }
    pub fn find_intersections(&self, b2: &Box)->Vec<u32>{
        let mut intersections: Vec<u32> = Vec::new();
        self.tree.find_overlaps_visitor(&get_interval(b2),&mut |(b1, idx)|{
            if b1.y2() > b2.y1 && b1.y1 < b2.y2(){
                intersections.push(*idx);
            }
        });
        intersections
    }
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;
    use rand::{Rng};
    use crate::find_intersecting::find_intersecting_boxes;

    fn find_intersecting_boxes_test(boxes: &[Box])->Vec<Vec<u32>>{
        let intersect_finder = BoxIntersector::new(boxes);
        boxes.iter().enumerate().map(|(idx1, b1)|{
            let mut outs:Vec<u32> = intersect_finder.find_intersections(b1).iter()
                .filter(|x|**x != idx1 as u32)
                .map(|x|*x as u32).collect();
            outs.sort();
            outs
        })
        .collect()
    }
    #[test]
    fn test_box_intersector_acc(){
        let mut rng = rand::thread_rng();
        let region_size = 8000;
        let num_boxes = 10000;
        let max_box_size = 100;
        let boxes:Vec<Box> = (0..num_boxes).map(|_|Box{
            x1:rng.gen_range(0..region_size-max_box_size),
            y1:rng.gen_range(0..region_size-max_box_size),
            xs:rng.gen_range(1..max_box_size as u32),
            ys:rng.gen_range(1..max_box_size as u32),
        })
        .collect();
        let gold_result = find_intersecting_boxes(&boxes);
        let test_result = find_intersecting_boxes_test(&boxes);
        let num_intersections:usize = test_result.iter().map(|l|l.len()).sum();
        assert_eq!(gold_result, test_result);
        //sanity check
        assert!(num_intersections > 10000);
    }
}