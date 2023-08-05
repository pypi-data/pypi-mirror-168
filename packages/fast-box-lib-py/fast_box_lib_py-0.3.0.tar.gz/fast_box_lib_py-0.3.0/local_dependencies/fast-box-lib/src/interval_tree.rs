use std::cmp::{max, min};

#[derive(Clone)]
pub struct Interval<K:Clone+Ord>{
    pub left: K,
    pub right: K,
}
pub struct IntervalTree<K:Clone+Ord,V>{
    data: Vec<V>,
    tree: Vec<Vec<Interval<K>>>,
}
fn cdiv(x:usize, y:usize)->usize{
    (x+y-1)/y
}
fn overlaps<K:Clone+Ord>(i1: &Interval<K>,i2: &Interval<K>)->bool{
    i1.right > i2.left && i1.left < i2.right
}

const B:usize = 8;
impl<K:Clone+Ord,V> IntervalTree<K,V>{
    pub fn create_from_intervals<ValIntIter>(values: ValIntIter)->IntervalTree<K,V>
        where ValIntIter: Iterator<Item = (Interval<K>,V)>
    {
        let mut vals = Vec::from_iter(values);
        vals.sort_by_key(|v|v.0.left.clone());
        let mut tree: Vec<Vec<Interval<K>>> = vec![vals.iter().map(|(interval, _)|interval.clone()).collect()];
        while tree.last().unwrap().len() > 1{
            let last_layer = tree.last().unwrap();
            let next_size = cdiv(last_layer.len(),B);
            let next_layer: Vec<Interval<K>> = (0..next_size).map(|i|{
                last_layer[i*B..].iter().take(B).map(|x|x.clone()).reduce(|accum, next|{ Interval{left:min(accum.left, next.left), right: max(accum.right, next.right)}}).unwrap()
            }).collect();
            tree.push(next_layer);
        }
        tree.reverse();
        let mut valsonly:Vec<V> = Vec::with_capacity(vals.len());
        for v in vals{
            valsonly.push(v.1);
        }
        IntervalTree{
            data: valsonly,
            tree: tree,
        }
    }
    pub fn create_from_fn<Func, VIter>(values: VIter, get_bounds: Func)->IntervalTree<K,V>
        where Func: Fn(&V)->Interval<K>, VIter: Iterator<Item = V>
    {
        IntervalTree::create_from_intervals(values.map(|v|(get_bounds(&v),v)))
    }
    fn find_overlaps_recursive<'a,F>(&'a self, interval: &Interval<K>, idx: usize, depth: usize, vistor: &mut F)
        where F: FnMut(&'a V)->(){
            if depth >= self.tree.len() || idx >= self.tree[depth].len(){
                return;
            }
            let my_interval = &self.tree[depth][idx];
            if overlaps(&interval,my_interval){
                if depth == self.tree.len()-1{
                    vistor(&self.data[idx]);
                }
                //this code block for optimization purposes only, gives ~50% speedup
                else if depth == self.tree.len() - 2{
                    let tree_vec = &self.tree[depth+1];
                    for i in idx*B..std::cmp::min((idx+1)*B,tree_vec.len()){
                        let cur_interval = &tree_vec[i];
                        if overlaps(&interval,cur_interval){
                            vistor(&self.data[i]);
                        }
                    }
                }
                else{
                    for i in 0..B{
                        self.find_overlaps_recursive(interval, idx*B+i, depth+1, vistor);
                    }
                }
            }
    }
    pub fn find_overlaps_visitor<'a,F>(&'a self, interval: &Interval<K>, vistor:&mut F)
        where F: FnMut(&'a V)->(){
            self.find_overlaps_recursive(interval, 0, 0, vistor)
    }
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;
    use rand::{Rng};

    pub fn find_overlaps_i<'a,K:Clone+Ord,V>(interval_t:&'a IntervalTree<K,V>, interval: &Interval<K>)->Vec<&'a V>{
        let mut v:Vec<&'a V> = Vec::new();
        interval_t.find_overlaps_visitor(interval, &mut |x|{
            v.push(x);
        });
        v
    }
    fn find_intersecting_intervals_gold(intervals: &[Interval<u32>])->Vec<Vec<u32>>{
        intervals.iter().enumerate().map(|(idx1, b1)|{
            intervals.iter()
            .enumerate()
            .filter(|(idx2, b2)| idx1 != *idx2 && overlaps(b1,b2))
            .map(|(idx,_)|idx as u32)  
            .collect()
        })
        .collect()
    }
    fn find_intersecting_intervals_test(intervals: &[Interval<u32>])->Vec<Vec<u32>>{
        let intersect_finder = IntervalTree::create_from_intervals(intervals.iter().cloned().zip(0..intervals.len()));
        intervals.iter().enumerate().map(|(idx1, b1)|{
            let mut outs:Vec<u32> = find_overlaps_i(&intersect_finder,b1).iter()
                .filter(|x|***x != idx1)
                .map(|x|**x as u32).collect();
            outs.sort();
            outs
        })
        .collect()
    }
    #[test]
    fn test_interval_tree_acc(){
        let mut rng = rand::thread_rng();
        let region_size = 5000;
        let num_boxes = 1000;
        let max_box_size = 100;
        let boxes:Vec<Interval<u32>> = (0..num_boxes).map(|_|{
            let l = rng.gen_range(0..region_size-max_box_size);
            Interval{
            left:l ,
            right:l + rng.gen_range(0..max_box_size),
         }})
        .collect();
        let gold_result = find_intersecting_intervals_gold(&boxes);
        let test_result = find_intersecting_intervals_test(&boxes);
        let num_intersections:usize = test_result.iter().map(|l|l.len()).sum();
        assert_eq!(gold_result, test_result);
        //sanity check
        assert!(num_intersections > 0);
    }
}