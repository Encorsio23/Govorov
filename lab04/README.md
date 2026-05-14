# Лабораторная работа 4 Фиктивная служба (Service stub)

### Проблема:

### 1. Замедление процесса разработки и тестирования
Работа с бд требует времени на загрузку и поиск. Это приводит к:
* Фризам (зависаниям) интерфейса при каждой попытке отладить визуальное отображение.
* Потере времени: разработчику приходится ждать реального парсинга данных там, где достаточно просто проверить, правильно ли отрисовалась кнопка или шрифт.
паттерн возвращает данные мгновенно, обеспечивая высокую скорость итераций разработки.

### 2. Блокировка параллельной работы
Часто разработка визуальной части (Frontend/GUI) опережает наполнение базы данных или написание сложного алгоритма парсинга (Backend). Без паттерна разработчик интерфейса вынужден ждать готовности модуля `RealTravelService`. Использование заглушки позволяет проектировать GUI, имея на руках лишь согласованный интерфейс `Itravel Service`.

### 3. Сложность тестирования крайних случаев
Трудно найти в реальной базе данных специфические условия для теста (например город с очень длинным названием). В паттерн можно легко «зашить» любые тестовые данные для проверки того, как интерфейс справляется с нестандартными ситуациями.

<img width="629" height="422" alt="4 лаба-классы лаб 2-4" src="https://github.com/user-attachments/assets/fc5146c3-972a-4d6b-b9fa-9f0cda099d83" />


```
package pattern;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

// Модель данных
class TravelInfo {
    public String city, traveltime, date, cityPhoto, transportsRaw, hotelsRaw;
    public double basePrice;

    public TravelInfo(String city, double basePrice, String traveltime, String date, String transportsRaw, String hotelsRaw, String cityPhoto) {
        this.city = city; this.basePrice = basePrice; this.traveltime = traveltime;
        this.date = date; this.transportsRaw = transportsRaw; this.hotelsRaw = hotelsRaw;
        this.cityPhoto = cityPhoto;
    }
}

// Интерфейс сервиса
interface ItravelService {
    TravelInfo getTravelInfo(String city);
}

// Менеджер базы данных
class DBmanager {
    public String dbPath;

    public DBmanager(String dbPath) {
        this.dbPath = dbPath;
    }

    public TravelInfo getTravel(String city) {
        try (Scanner scanner = new Scanner(new File(dbPath), "UTF-8")) {
            if (scanner.hasNextLine()) scanner.nextLine();
            while (scanner.hasNextLine()) {
                String[] d = scanner.nextLine().split(",");
                if (d.length >= 7 && d[0].equalsIgnoreCase(city)) {
                    return new TravelInfo(d[0], Double.parseDouble(d[1]), d[2], d[3], d[4], d[5], d[6]);
                }
            }
        } catch (Exception e) { System.err.println("Ошибка БД: " + e.getMessage()); }
        return null;
    }
}

// Реальная стратегия
class RealTravelService implements ItravelService {
    private DBmanager db = new DBmanager("travel_db.csv"); 

    public TravelInfo getTravelInfo(String city) {
        try { Thread.sleep(300); } catch (Exception e) {} 
        return db.getTravel(city);
    }
}

// Стратегия-заглушка
class StubTravelService implements ItravelService {
    private Map<String, TravelInfo> stubTravels = new HashMap<>(); 

    public StubTravelService() {
        stubTravels.put("Tokyo", new TravelInfo("Tokyo (Stub)", 500.0, "1s", "2026-05-14",
                "Телепорт:0;Дракон:200",
                "Замок:500:[https://picsum.photos/id/101/250/150;Пещера:10:https://picsum.photos/id/102/250/150](https://picsum.photos/id/101/250/150;Пещера:10:https://picsum.photos/id/102/250/150)",
                "[https://picsum.photos/id/200/450/200](https://picsum.photos/id/200/450/200)"));
        stubTravels.put("Moscow", new TravelInfo("Moscow (Stub)", 100.0, "1s", "2026-06-01",
                "Метро:1;Такси:20",
                "Хостел:15:[https://picsum.photos/id/111/250/150;Отель](https://picsum.photos/id/111/250/150;Отель) 5*:200:[https://picsum.photos/id/112/250/150](https://picsum.photos/id/112/250/150)",
                "[https://picsum.photos/id/122/450/200](https://picsum.photos/id/122/450/200)"));
        stubTravels.put("Paris", new TravelInfo("Paris (Stub)", 300.0, "1s", "2026-07-15",
                "Автобус:10;Самолет:150",
                "Мансарда:50:[https://picsum.photos/id/1040/250/150;Ritz:800:https://picsum.photos/id/1039/250/150](https://picsum.photos/id/1040/250/150;Ritz:800:https://picsum.photos/id/1039/250/150)",
                "[https://picsum.photos/id/1055/450/200](https://picsum.photos/id/1055/450/200)"));
        stubTravels.put("Dubai", new TravelInfo("Dubai (Stub)", 400.0, "1s", "2026-11-05",
                "Ковер-самолет:50;Вертолет:500",
                "Палатка:20:[https://picsum.photos/id/400/250/150;Burj:2000:https://picsum.photos/id/412/250/150](https://picsum.photos/id/400/250/150;Burj:2000:https://picsum.photos/id/412/250/150)",
                "[https://picsum.photos/id/380/450/200](https://picsum.photos/id/380/450/200)"));
    }

    public TravelInfo getTravelInfo(String city) {
        return stubTravels.getOrDefault(city, stubTravels.get("Tokyo"));
    }
}

// Графический интерфейс (GUI)
public class AppWithPattern extends JFrame {
    private JComboBox<String> cityPicker = new JComboBox<>(new String[]{"Moscow", "Paris", "Tokyo", "Dubai"});
    private JPanel cardPanel = new JPanel(new BorderLayout());
    private JCheckBox useStub = new JCheckBox("заглушка");

    private ItravelService realSrv = new RealTravelService();
    private ItravelService stubSrv = new StubTravelService();

    public AppWithPattern() {
        super("Pattern version");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(550, 850);

        JPanel top = new JPanel();
        top.add(new JLabel("Город:"));
        top.add(cityPicker);
        JButton btn = new JButton("Найти билеты");
        top.add(btn);
        top.add(useStub);

        add(top, BorderLayout.NORTH);
        add(new JScrollPane(cardPanel), BorderLayout.CENTER);

        btn.addActionListener(e -> startSearch());

        setLocationRelativeTo(null);
        setVisible(true);
    }

    private void startSearch() {
        cardPanel.removeAll();
        cardPanel.add(new JLabel("⏳ Загрузка данных...", SwingConstants.CENTER));
        cardPanel.revalidate(); cardPanel.repaint();

        new Thread(() -> {
            ItravelService srv = useStub.isSelected() ? stubSrv : realSrv;
            TravelInfo info = srv.getTravelInfo((String) cityPicker.getSelectedItem());
            SwingUtilities.invokeLater(() -> showInfo(info));
        }).start();
    }

    private void showInfo(TravelInfo info) {
        cardPanel.removeAll();
        if (info == null) {
            cardPanel.add(new JLabel("❌ Не найдено"), SwingConstants.CENTER);
        } else {
            JPanel p = new JPanel();
            p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
            p.setBorder(new EmptyBorder(20, 20, 20, 20));
            p.setBackground(Color.WHITE);

            JLabel title = new JLabel(info.city.toUpperCase());
            title.setFont(new Font("Arial", Font.BOLD, 24));
            p.add(title);
            p.add(Box.createVerticalStrut(10));
            p.add(getImg(info.cityPhoto, 450, 200));

            p.add(Box.createVerticalStrut(20));
            p.add(new JLabel("<html><b>⏱ Время в пути:</b> " + info.traveltime + "</html>"));
            p.add(new JLabel("<html><b>📅 Дата вылета:</b> " + info.date + "</html>"));
            p.add(Box.createVerticalStrut(20));

            p.add(new JLabel("Выберите транспорт:"));
            JComboBox<String> transBox = new JComboBox<>(info.transportsRaw.split(";"));
            transBox.setMaximumSize(new Dimension(450, 30));
            p.add(transBox);

            p.add(Box.createVerticalStrut(15));
            p.add(new JLabel("Выберите отель:"));
            JComboBox<String> hotelBox = new JComboBox<>(info.hotelsRaw.split(";"));
            hotelBox.setMaximumSize(new Dimension(450, 30));
            p.add(hotelBox);

            p.add(Box.createVerticalStrut(15));
            JLabel hotelImgLabel = new JLabel();
            p.add(hotelImgLabel);

            p.add(Box.createVerticalStrut(20));
            JLabel priceLabel = new JLabel();
            priceLabel.setFont(new Font("Arial", Font.BOLD, 20));
            priceLabel.setForeground(new Color(34, 139, 34));
            p.add(priceLabel);

            Runnable update = () -> {
                try {
                    String tStr = (String) transBox.getSelectedItem();
                    double tPrice = Double.parseDouble(tStr.split(":")[1]);

                    String hStr = (String) hotelBox.getSelectedItem();
                    String[] hParts = hStr.split(":");
                    double hPrice = Double.parseDouble(hParts[1]);
                    String hUrl = hParts[2] + ":" + hParts[3];

                    priceLabel.setText("Общая стоимость: " + (info.basePrice + tPrice + hPrice) + " $");

                    new Thread(() -> {
                        ImageIcon icon = createIcon(hUrl, 250, 150);
                        SwingUtilities.invokeLater(() -> hotelImgLabel.setIcon(icon));
                    }).start();
                } catch (Exception ex) {}
            };

            transBox.addActionListener(e -> update.run());
            hotelBox.addActionListener(e -> update.run());
            update.run();

            cardPanel.add(p, BorderLayout.NORTH);
        }
        cardPanel.revalidate(); cardPanel.repaint();
    }

    private JLabel getImg(String url, int w, int h) {
        return new JLabel(createIcon(url, w, h));
    }

    private ImageIcon createIcon(String url, int w, int h) {
        try {
            return new ImageIcon(new ImageIcon(new URL(url)).getImage().getScaledInstance(w, h, Image.SCALE_SMOOTH));
        } catch (Exception e) { return new ImageIcon(); }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(AppWithPattern::new);
    }
}
```

### 1. Интерфейс службы
* **`Itravel Service`**: Базовый интерфейс 
* **Метод**: `getTravelInfo(city: String)` метод, принимающий название города и возвращающий структурированную информацию о рейсе

### 2. Реализации
* **`RealTravelService`**: Класс, реализующий интерфейс. Он выполняет чтение базы данных
* **`StubTravelService`**: Фиктивная служба, реализующая тот же интерфейс. Она возвращает заранее определенные данные мгновенно
* **`DB`**: база данных
* **`TravelInfo`**: массив поездок для заглушки

### 3. Методы
* **`getTravelInfo(city: String)`**: Определяет абстрактный контракт для получения данных. Данный метод обязывает любую реализацию службы принимать на вход строку (название города) и возвращать сведения о поездке.

* **`getTravelInfo(city: String)`**: Реализует «тяжелую» логику взаимодействия с внешней базой данных.
    * Осуществляет подключение к файловой системе и открытие Excel-таблицы.
    * Выполняет итерационный поиск по строкам файла для сопоставления введенного города с имеющимися данными.
    * Возвращает актуальную информацию о стоимости билета, визовом режиме и доступных рейсах из файла.

* **`getTravelInfo(city: String)`**: Реализует упрощенную логику для нужд разработки и тестирования.
    * Игнорирует фактическое состояние внешних файлов.
    * Мгновенно возвращает заранее подготовленный объект с данными (например, «Токио, 65 000 руб, виза нужна»).
    * Позволяет проверять корректность отображения данных в GUI без задержек и ошибок доступа к диску.

### Вывод

Реализация StubTravelService дает возможность верстать интерфейс и проверять логику расчетов даже тогда, когда база данных еще не готова или недоступна. Можно добавлять новые способы получения данных
просто создав новый класс, реализующий ItravelService. Также отладка становится проще, так как теперь становится куда проще искать, где именно искать проблему
