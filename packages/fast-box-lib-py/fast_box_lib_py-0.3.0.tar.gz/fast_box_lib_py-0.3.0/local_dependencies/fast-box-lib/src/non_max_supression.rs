use crate::find_intersecting::find_intersecting_boxes;
use crate::box_def::Box;
use crate::intersect_calc::*;
use std::cmp::min;

fn overlap_meets_threshold(b1: &Box, b2: &Box, iou_threshold: f64, overlap_threshold: f64)->bool{
    let intersect = intersect_area(b1, &b2) as f64;
    let union_a = union_area(b1, &b2) as f64;
    let min_area = min(b1.area(), b2.area()) as f64;
    intersect > union_a * iou_threshold || intersect > min_area * overlap_threshold
}

pub fn find_non_max_suppressed(all_boxes: &[Box], scores: &[f64], iou_threshold: f64, overlap_threshold: f64)->Vec<bool>{
    assert_eq!(all_boxes.len(), scores.len());
    let intersect_graph = find_intersecting_boxes(all_boxes);
    let mut pruned_graph: Vec<Vec<u32>> = intersect_graph.iter().zip(all_boxes.iter()).map(|(idxlist, b1)|{
        idxlist.iter()
            .filter(|idx|overlap_meets_threshold(b1, &all_boxes[**idx as usize], iou_threshold, overlap_threshold))
            .copied()
            .collect()
    }).collect();

    let mut mask = vec![true; scores.len()];
    let mut local_max = vec![false; scores.len()];
    let mut valid_idxs:Vec<usize> = (0..scores.len()).collect();
    while valid_idxs.len() > 0{
        //a node is not suppressed if it is better than all its non-suppresed neighbors
        let new_local_best:Vec<usize> = valid_idxs.iter().filter(|idxp|{
            let idx = **idxp;
            let myscore = scores[idx];
            pruned_graph[idx].iter().all(|edge|myscore >= scores[*edge as usize])
        })
        .copied()
        .collect();
        for bidx in new_local_best.iter(){
            local_max[*bidx] = true;
            mask[*bidx as usize] = false;
            for i in pruned_graph[*bidx].iter(){
                mask[*i as usize] = false;
            }
        }
        //remove masked nodes from list
        valid_idxs.retain(|idx|mask[*idx]);
        //remove masked edges from list
        for idx in valid_idxs.iter(){
            pruned_graph[*idx].retain(|edge|mask[*edge as usize]);
        }
    }

    local_max
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;
    use rand::{Rng, SeedableRng, rngs::StdRng};
    use std::cmp::Ordering;
    pub fn find_non_max_suppressed_gold(all_boxes: &[Box], scores: &[f64], iou_threshold: f64, overlap_threshold: f64)->Vec<bool>{
        let mut sorted_items:Vec<(f64, Box, usize)> = all_boxes.iter().zip(scores.iter()).enumerate().map(|(idx, (b,s))|(*s,*b,idx)).collect();
        sorted_items.sort_by(|(s1,_,_), (s2,_,_)| s1.partial_cmp(s2).unwrap_or(Ordering::Equal));
        sorted_items.reverse();
        let mut suppressed = vec![false; all_boxes.len()];
        for (sidx1,(s1, b1, idx1)) in sorted_items.iter().enumerate(){
            if !suppressed[*idx1]{
                for (_, (s2, b2, idx2)) in sorted_items[sidx1+1..].iter().enumerate(){
                    if !suppressed[*idx2] 
                        && *s1 > *s2 // in theory not necessary due to sorting
                        && (overlap_meets_threshold(b1, &b2, iou_threshold, overlap_threshold)){
                            suppressed[*idx2] = true;
                        }
                }
            }
        }
        let non_suppressed = suppressed.iter().map(|s|!*s).collect();
        non_suppressed
    }
    #[test]
    fn test_nms_acc(){
        let mut rng = rand::thread_rng();
        let region_size = 400;
        let num_boxes = 1000;
        let max_box_size = 100;
        let boxes:Vec<Box> = (0..num_boxes).map(|_|Box{
            x1:rng.gen_range(0..region_size-max_box_size),
            y1:rng.gen_range(0..region_size-max_box_size),
            xs:rng.gen_range(1..max_box_size as u32),
            ys:rng.gen_range(1..max_box_size as u32),
        })
        .collect();
        let scores: Vec<f64> = (0..num_boxes).map(|_|rng.gen()).collect();
        let gold_result = find_non_max_suppressed_gold(&boxes, &scores, 0.1, 0.5);
        let test_result = find_non_max_suppressed(&boxes, &scores, 0.1, 0.5);
        let num_survivors:usize = gold_result.iter().map(|x|if *x {1} else {0}).sum();
        assert_eq!(gold_result, test_result);
        //sanity check on gold impl
        assert!(num_survivors > 5 && num_survivors < num_boxes - 5);
    }

    #[test]
    fn test_nms_perf(){
        let seed = 42;
        let mut rng = StdRng::seed_from_u64(seed);
        let region_size = 30000;
        let num_boxes = 100000;
        let max_box_size = 100;
        let boxes:Vec<Box> = (0..num_boxes).map(|_|Box{
            x1:rng.gen_range(0..region_size-max_box_size),
            y1:rng.gen_range(0..region_size-max_box_size),
            xs:rng.gen_range(1..max_box_size as u32),
            ys:rng.gen_range(1..max_box_size as u32),
        })
        .collect();
        let scores: Vec<f64> = (0..num_boxes).map(|_|rng.gen()).collect();
        let test_result = find_non_max_suppressed(&boxes, &scores, 0.1, 0.5);
        let num_survivors:usize = test_result.iter().map(|x|if *x {1} else {0}).sum();
        //sanity check on gold impl
        assert_eq!(num_survivors, 80225);
    }
}