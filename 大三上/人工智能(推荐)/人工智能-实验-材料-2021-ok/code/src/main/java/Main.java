import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class Main {
    static ArrayList<node> tree = new ArrayList<>();
    static double[][] classify_flag = new double[4][];

    public static void main(String[] args) {
        ArrayList<data> train_data = new ArrayList<>();
        ArrayList<data> test_data = new ArrayList<>();
        //读取文件
        try {
            List<String> train_lines = Files.readAllLines(Paths.get("traindata.txt"));
            List<String> test_lines = Files.readAllLines(Paths.get("testdata.txt"));
            for (String e : train_lines) {
                train_data.add(new data(e));
            }
            for (String e : test_lines) {
                test_data.add(new data(e));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        //计算分类点
        for (int i = 0; i < 4; i++) {
            ArrayList<Double> temp_classify_flag = new ArrayList<>();
            ArrayList<Double> temp = new ArrayList<>();
            for (data t : train_data)
                if (!temp.contains(t.classify[i]))
                    temp.add(t.classify[i]);
            temp.sort(Comparator.naturalOrder());
            for (int t = 0; t < temp.size() - 1; t++) {
                temp_classify_flag.add((temp.get(t) + temp.get(t + 1)) / 2);
            }
            double[] toArray = new double[temp_classify_flag.size()];
            for (int j = 0; j < temp_classify_flag.size(); j++)
                toArray[j] = temp_classify_flag.get(j);
            classify_flag[i] = toArray;
        }

        data[] train_data_array = new data[train_data.size()];
        train_data.toArray(train_data_array);
        //构建决策树
        node root = new node(train_data_array);
        root.parent = null;
        create_tree(root);
        new draw_tree(root, "剪枝前.jpg");

        //测试决策树
        data[] test_data_array = new data[test_data.size()];
        test_data.toArray(test_data_array);
        test_tree(root, test_data_array);

        //剪枝
        post_pruning(root);
        new draw_tree(root, "剪枝后.jpg");
        test_tree(root, test_data_array);

    }

    static public node[] generate_child(node father_node, int classify, double flag) {
        node[] result = new node[2];
        father_node.flag = flag;
        father_node.classify = classify;
        ArrayList<data> left_data = new ArrayList<>();
        ArrayList<data> right_data = new ArrayList<>();
        for (data i : father_node.train_data) {
            if (i.classify[classify] <= flag)
                left_data.add(i);
            else
                right_data.add(i);
        }
        data[] left_data_array = new data[left_data.size()];
        data[] right_data_array = new data[right_data.size()];
        left_data.toArray(left_data_array);
        right_data.toArray(right_data_array);
        node left_node = new node(left_data_array);
        node right_node = new node(right_data_array);
        left_node.parent = father_node;
        right_node.parent = father_node;
        father_node.child_left = left_node;
        father_node.child_right = right_node;
        result[0] = left_node;
        result[1] = right_node;
        return result;
    }

    static public double caculate_gain(node father_node, int classify, double flag) {
        node[] temp = generate_child(father_node, classify, flag);
        int total = father_node.train_data.length;
        double gain = father_node.entropy;
        for (node i : temp) {
            gain -= ((double) i.train_data.length / total) * i.entropy;
        }
        return gain;
    }

    static public void create_tree(node root) {
        double max_gain = -99999;
        int max_classify = -1;
        double max_flag = -1;
        if (root.is_one_type())
            return;
        //找到信息增益最大的分类方式
        for (int i = 0; i < 4; i++) {
            for (double flag : classify_flag[i]) {
                double gain = caculate_gain(root, i, flag);
                if (gain > max_gain) {
                    max_gain = gain;
                    max_classify = i;
                    max_flag = flag;
                }
            }
        }
        node[] temp = generate_child(root, max_classify, max_flag);
        create_tree(temp[0]);
        create_tree(temp[1]);
    }

    static public void post_pruning(node root) {
        //若此节点的孩子不是叶节点，就递归调用
        if (!root.child_left.is_leaf()) {
            post_pruning(root.child_left);
        }
        if (!root.child_right.is_leaf()) {
            post_pruning(root.child_right);
        }
        //此节点的孩子都是叶节点
        if (root.child_left.is_leaf() && root.child_right.is_leaf()) {
            //统计错误情况
            int wrong_without_pruning = 0;
            int wrong_with_pruning = 0;
            ArrayList<data> after_pruning_test_data = new ArrayList<>();
            after_pruning_test_data.addAll(root.child_left.test_data);
            after_pruning_test_data.addAll(root.child_right.test_data);
            root.test_data = after_pruning_test_data;
            for (data test : root.child_left.test_data) {
                if (test.type != root.child_left.get_max_type())
                    wrong_without_pruning++;
            }
            for (data test : root.child_right.test_data) {
                if (test.type != root.child_right.get_max_type())
                    wrong_without_pruning++;
            }
            for (data test : after_pruning_test_data) {
                if (test.type != root.get_max_type())
                    wrong_with_pruning++;
            }
            if (wrong_without_pruning >= wrong_with_pruning) {
                //剪枝
//                System.out.println("剪枝了"+root.classify+root.flag);
                root.classify = -1;
                root.flag = 0;
                ArrayList<data> list = new ArrayList<>();
                list.addAll(Arrays.asList(root.child_left.train_data));
                list.addAll(Arrays.asList(root.child_right.train_data));
                data[] temp = new data[list.size()];
                list.toArray(temp);
                root.train_data = temp;
                root.child_left = null;
                root.child_right = null;
            }
        }
    }

    static public void test_tree(node root, data[] test_data) {
        int wrong = 0, right = 0;
        for (data test : test_data) {
            node state = root;
            while (state.classify != -1) {
                if (test.classify[state.classify] < state.flag)
                    state = state.child_left;
                else
                    state = state.child_right;
            }
            state.test_data.add(test);
            if (state.get_max_type() != test.type) {
                wrong++;
                System.out.println("错误数据:\n" + test + "误分类为:" + state.get_max_type());
            } else
                right++;
        }
        System.out.println("准确率:" + (double) right / (right + wrong) * 100 + "%");
    }
}
