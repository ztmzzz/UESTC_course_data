import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import static java.lang.Math.log;


public class node {
    node parent, child_left, child_right;
    int classify = -1;//分类的种类
    double flag;//分类的值
    data[] train_data;
    ArrayList<data> test_data = new ArrayList<>();
    double entropy;//信息熵

    public node(data[] train_data) {
        this.train_data = train_data;
        this.entropy = calculate_entropy();
    }

    public boolean is_leaf() {
        return child_left == null && child_right == null;
    }

    private double calculate_entropy() {
        int total = train_data.length;
        Map<Integer, Integer> count = get_count();
        double entropy = 0;
        for (int value : count.values()) {
            double p = (double) value / total;
            entropy -= p * (log(p) / log(2));
        }
        return entropy;
    }

    public boolean is_one_type() {
        int classify = train_data[0].type;
        for (data t : train_data) {
            if (t.type != classify)
                return false;
        }
        return true;
    }
    //获取节点中最多的种类
    public int get_max_type() {
        int total = train_data.length;
        int max_count = -1;
        int max_type = -1;
        Map<Integer, Integer> count = get_count();

        for (Integer key : count.keySet()) {
            if (count.get(key) >= total / 2)
                return key;
            if (max_count < count.get(key)) {
                max_count = count.get(key);
                max_type = key;
            }
        }
        return max_type;
    }


    //种类-数量映射
    private Map<Integer, Integer> get_count() {
        Map<Integer, Integer> count = new HashMap<>();
        for (data i : train_data) {
            if (count.containsKey(i.type)) {
                int temp = count.get(i.type);
                count.put(i.type, ++temp);
            } else {
                count.put(i.type, 1);
            }
        }
        return count;
    }


}
