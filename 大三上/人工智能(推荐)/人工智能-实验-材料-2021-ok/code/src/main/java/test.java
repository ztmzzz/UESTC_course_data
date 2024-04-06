import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class test extends JFrame {
    int width = 200;
    int height = 200;
    int node_width = 50;
    int node_height = 30;
    int offset_x = 150, offset_y = 100;
    node root;

    public test(node root, String title) {
        super();
        this.root = root;
        init(title);
        add(new mycanvas());
    }

    private void init(String title) {
        this.setTitle(title);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        this.setSize(width, height);
    }
    public static void main ( String[] args ) throws IOException
    {
        final BufferedImage image = new BufferedImage ( 1000, 1000, BufferedImage.TYPE_INT_ARGB );
        final Graphics2D graphics2D = image.createGraphics ();
        graphics2D.setPaint ( Color.WHITE );
        graphics2D.fillRect ( 0,0,1000,1000 );
        graphics2D.setPaint ( Color.BLACK );
        graphics2D.drawOval ( 0, 0, 1000, 1000 );
        graphics2D.dispose ();

        ImageIO.write ( image, "png", new File ( "image.png" ) );
    }

    private class mycanvas extends Canvas {
        Graphics2D g2;
        int i = 0;

        public void paint(Graphics g) {
            g2 = (Graphics2D) g;

            g2.drawLine(1, 1, (int) root.flag, 100);


        }


    }
}
