package nopattern;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Transport {
    public String name; public double price;
    public Transport(String name, double price) { this.name = name; this.price = price; }
    @Override public String toString() { return name + " (+" + price + "$)"; }
}

class Hotel {
    public String name, photoUrl; public double price;
    public Hotel(String name, double price, String photoUrl) { this.name = name; this.price = price; this.photoUrl = photoUrl; }
    @Override public String toString() { return name + " (+" + price + "$/н)"; }
}

class TravelInfo {
    public String city, traveltime, date, cityPhoto;
    public double basePrice;
    public List<Transport> transports = new ArrayList<>();
    public List<Hotel> hotels = new ArrayList<>();

    public TravelInfo(String c, double bp, String t, String d, String tStr, String hStr, String cp) {
        city = c; basePrice = bp; traveltime = t; date = d; cityPhoto = cp;
        for (String ts : tStr.split(";")) { String[] p = ts.split(":"); transports.add(new Transport(p[0], Double.parseDouble(p[1]))); }
        for (String hs : hStr.split(";")) { String[] p = hs.split(":"); hotels.add(new Hotel(p[0], Double.parseDouble(p[1]), p[2] + ":" + p[3])); }
    }
}

class RealDBService {
    public TravelInfo getTravel(String city) {
        try { Thread.sleep(50); } catch (Exception e) {}
        try (Scanner scanner = new Scanner(new File("travel_db.csv"), "UTF-8")) {
            if (scanner.hasNextLine()) scanner.nextLine();
            while (scanner.hasNextLine()) {
                String[] d = scanner.nextLine().split(",");
                if (d.length >= 7 && d[0].equalsIgnoreCase(city)) return new TravelInfo(d[0], Double.parseDouble(d[1]), d[2], d[3], d[4], d[5], d[6]);
            }
        } catch (Exception e) { System.err.println("Ошибка БД: " + e.getMessage()); }
        return null;
    }
}

public class AppNoPattern extends JFrame {
    private JComboBox<String> cityPicker = new JComboBox<>(new String[]{"Moscow", "Paris", "Tokyo", "Dubai"});
    private JPanel cardPanel = new JPanel(new BorderLayout());
    private RealDBService dbService = new RealDBService(); // ПРЯМАЯ ЗАВИСИМОСТЬ

    public AppNoPattern() {
        super("NoPattern");
        setDefaultCloseOperation(EXIT_ON_CLOSE); setSize(550, 850);

        JPanel top = new JPanel(new FlowLayout(FlowLayout.LEFT));
        top.setBorder(new EmptyBorder(10, 10, 10, 10));
        top.add(new JLabel("Город:")); top.add(cityPicker);
        JButton btn = new JButton("Поиск"); top.add(btn);

        add(top, BorderLayout.NORTH); add(new JScrollPane(cardPanel), BorderLayout.CENTER);

        btn.addActionListener(e -> {
            cardPanel.removeAll();
            cardPanel.add(new JLabel("Загрузка", SwingConstants.CENTER));
            cardPanel.revalidate(); cardPanel.repaint();
            new Thread(() -> {
                TravelInfo info = dbService.getTravel((String) cityPicker.getSelectedItem());
                SwingUtilities.invokeLater(() -> showInfo(info));
            }).start();
        });

        setLocationRelativeTo(null); setVisible(true);
    }

    private void showInfo(TravelInfo info) {
        cardPanel.removeAll();
        if (info != null) {
            JPanel p = new JPanel(); p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
            p.setBorder(new EmptyBorder(20, 20, 20, 20)); p.setBackground(Color.WHITE);

            JLabel title = new JLabel(info.city.toUpperCase()); title.setFont(new Font("Arial", Font.BOLD, 26));
            p.add(title); p.add(Box.createVerticalStrut(10));
            p.add(new JLabel(createIcon(info.cityPhoto, 450, 200))); p.add(Box.createVerticalStrut(20));

            p.add(new JLabel("Время: " + info.traveltime + " | Дата: " + info.date)); p.add(Box.createVerticalStrut(20));

            JComboBox<Transport> transBox = new JComboBox<>(info.transports.toArray(new Transport[0]));
            transBox.setMaximumSize(new Dimension(450, 30)); p.add(transBox); p.add(Box.createVerticalStrut(10));

            JComboBox<Hotel> hotelBox = new JComboBox<>(info.hotels.toArray(new Hotel[0]));
            hotelBox.setMaximumSize(new Dimension(450, 30)); p.add(hotelBox); p.add(Box.createVerticalStrut(10));

            JLabel hotelImgLabel = new JLabel(createIcon(info.hotels.get(0).photoUrl, 250, 150));
            p.add(hotelImgLabel); p.add(Box.createVerticalStrut(20));

            JLabel priceLabel = new JLabel(); priceLabel.setFont(new Font("Arial", Font.BOLD, 22)); p.add(priceLabel);

            Runnable updater = () -> {
                double total = info.basePrice + ((Transport)transBox.getSelectedItem()).price + ((Hotel)hotelBox.getSelectedItem()).price;
                priceLabel.setText(String.format("Итого: %.2f $", total));
                new Thread(() -> {
                    ImageIcon icn = createIcon(((Hotel)hotelBox.getSelectedItem()).photoUrl, 250, 150);
                    SwingUtilities.invokeLater(() -> hotelImgLabel.setIcon(icn));
                }).start();
            };

            transBox.addActionListener(e -> updater.run()); hotelBox.addActionListener(e -> updater.run());
            updater.run();
            cardPanel.add(p, BorderLayout.NORTH);
        }
        cardPanel.revalidate(); cardPanel.repaint();
    }

    private ImageIcon createIcon(String url, int w, int h) {
        try { return new ImageIcon(new ImageIcon(new URL(url)).getImage().getScaledInstance(w, h, Image.SCALE_SMOOTH)); }
        catch (Exception e) { return new ImageIcon(); }
    }

    public static void main(String[] args) { new AppNoPattern(); }
}