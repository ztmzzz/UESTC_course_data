import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class draw_tree {
    int width = 2048;
    int node_width = 50;
    int node_height = 30;
    int offset_x = 150, offset_y = 100;
    node root;
    Graphics2D g2;

    public draw_tree(node root, String path) {
        this.root = root;
        final BufferedImage image = new BufferedImage(2048, 1024, BufferedImage.TYPE_INT_ARGB);
        g2 = image.createGraphics();
        g2.setFont(new Font(null, Font.PLAIN, 13));
        g2.setPaint(Color.white);
        g2.fillRect(0, 0, 2048, 1024);
        g2.setPaint(Color.black);
        draw_node(root, width / 2, 10, 1);
        g2.dispose();

        try {
            ImageIO.write(image, "png", new File(path));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void draw_node(node root, int x, int y, int depth) {
        StringBuilder sb = new StringBuilder();
        if (root.classify == -1) {
            sb.append("类别").append(root.get_max_type());
            node_width = 50;
        } else {
            sb.append("第").append(root.classify + 1).append("类的").append(root.flag).append("为界");
            node_width = 100;
        }
        //绘制此节点
        g2.drawRect(x - node_width / 2, y, node_width, node_height);
        g2.drawString(sb.toString(), x - node_width / 2, y + node_height / 2);
        int start_point_x = x;
        int start_point_y = y + node_height;
        if (root.child_left != null) {
            offset_x = (int) (width / Math.pow(2, depth + 1));
            g2.drawLine(start_point_x, start_point_y, x - offset_x, y + node_height + offset_y);
            draw_node(root.child_left, x - offset_x, y + node_height + offset_y, depth + 1);
        }
        if (root.child_right != null) {
            offset_x = (int) (width / Math.pow(2, depth + 1));
            g2.drawLine(start_point_x, start_point_y, x + offset_x, y + node_height + offset_y);
            draw_node(root.child_right, x + offset_x, y + node_height + offset_y, depth + 1);
        }
    }

}
