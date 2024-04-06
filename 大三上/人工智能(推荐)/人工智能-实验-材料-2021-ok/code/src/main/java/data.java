import java.util.Arrays;

public class data {
    int type;//种类
    double[] classify;//特征

    public data(String s) {
        String[] temp = s.split("\t");
        classify = new double[4];
        for (int i = 0; i < 4; i++) {
            classify[i] = Double.parseDouble(temp[i]);
        }
        type = Integer.parseInt(temp[4]);
    }

    @Override
    public String toString() {
        return "种类:" + type + "\n数据:" + Arrays.toString(classify) + "\n";
    }
}
