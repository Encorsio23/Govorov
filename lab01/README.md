Проблема: Создание каждого нового предмета мебели требует многократного выполнения однотипных действий: задания всех характеристик
(название, размеры, материал, цвет, цена), каких-либо вычислений, обращений к базе данных, ссылок и так далее.
Создание таких объектов через базовый конструктор может быть ресурсо-затратным.

Цель: Разработать интерактивный конструктор мебели для клиентов онлайн магазина, для визуализации и просто прикольно кнопки потыкать

Применение паттерна Prototype:
1. Client (класс Form1) — управляет процессом подбора мебели. Вместо прямого создания объектов через конструктор, он использует метод клонирования существующего прототипа.
2. IFurniturePrototype — интерфейс прототипа. Определяет обязательный для всех видов мебели метод Clone().
3. ConcretePrototype (Furniture) — конкретная реализация мебели. Содержит метод Clone(), использующий системный механизм MemberwiseClone() для создания точной копии объекта.
4. Продукт (Furniture экземпляр) — содержит имя, тип мебели, цвет, материал и метод GetImagePath(), который динамически формирует путь к изображению на основе текущего состояния клонированного объекта.

Реализация без прототипа:

![5 лаба-Классы лаб 2-1-2](https://github.com/user-attachments/assets/ec170539-9847-4d64-8ca5-792892d0e631)

    namespace FurnitureCatalog
    {
        // Типы мебели для выбора
        public enum FurnitureType { Chair, Table, Sofa, Armchair }

        public class Furniture
        {
            public string Name { get; set; }
            public FurnitureType Type { get; set; } // Тип
            public int Width { get; set; }
            public int Height { get; set; }
            public int Depth { get; set; }
            public string Material { get; set; }
            public string Color { get; set; }
            public decimal Price { get; set; }
            public string ImagePath { get; set; } // Путь к картинке

            public Furniture(string name, FurnitureType type, int w, int h, int d, string mat, string col, decimal price)
            {
                Name = name; Type = type; Width = w; Height = h;
                Depth = d; Material = mat; Color = col; Price = price;
                UpdateImage();
            }
    
            // Логика выбора картинки в зависимости от типа
            public void UpdateImage()
            {
                ImagePath = $"{Type.ToString().ToLower()}.png";
            }
    
            public override string ToString() => $"{Name} ({Color}) - {Price}₽";
        }
    }

//

    using System;
    using System.Drawing;
    using System.IO;
    using System.Windows.Forms;
    
    namespace FurnitureCatalog
    {
        public partial class Form1 : Form
        {
            public Form1()
            {
                InitializeComponent();
    
                comboBox1.Items.AddRange(new string[] { "Стул", "Стол", "Диван" });
                comboBox2.Items.AddRange(new string[] { "Бордовый", "Синий" });
                comboBox3.Items.AddRange(new string[] { "Дерево", "Пластмасс" });
    
                comboBox1.SelectedIndex = 0;
                comboBox2.SelectedIndex = 0;
                comboBox3.SelectedIndex = 0;
    
                UpdatePreview();
            }
    
            private void UpdatePreview()
            {
                if (comboBox1.SelectedItem == null || comboBox2.SelectedItem == null) return;
    
                string type = comboBox1.SelectedItem.ToString()!;
                string color = comboBox2.SelectedItem.ToString()!;
    
                string typeEng = type == "Стол" ? "table" : (type == "Диван" ? "sofa" : "chair");
                string colorEng = color == "Бордовый" ? "bordo" : "blue";
    
                string fileName = $"{typeEng}_{colorEng}.jpg";
                string path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "images", fileName);
    
                if (File.Exists(path))
                {
    
                    if (pictureBox1.Image != null) // перед загрузкой новой джпег освобождаем старую
                    {
                        var oldImage = pictureBox1.Image;
                        pictureBox1.Image = null;
                        oldImage.Dispose();
                    }
    
                    try
                    {
                        pictureBox1.Image = Image.FromFile(path);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка загрузки файла {fileName}: {ex.Message}");
                    }
                }
            }
    
            private void comboBox1_SelectedIndexChanged(object sender, EventArgs e) => UpdatePreview();
            private void comboBox2_SelectedIndexChanged(object sender, EventArgs e) => UpdatePreview();
    
            private void comboBox3_SelectedIndexChanged(object sender, EventArgs e) { }
    
            private void button1_Click(object sender, EventArgs e)
            {
                ConfirmLabel confirm = new ConfirmLabel();
                confirm.ShowDialog();
            }
        }
    }

С прототипом:

![5 лаба-Классы лаб 2-1-1](https://github.com/user-attachments/assets/99c9ef89-a8e3-49da-8d90-4343f2f35a65)


    using System;
    using System.IO;
    
    namespace FurnitureCatalog
    {
    
        public interface IFurniturePrototype
        {
            IFurniturePrototype Clone();
        }
    
        public class Furniture : IFurniturePrototype
        {
            public string Name { get; set; } = string.Empty;
            public string Type { get; set; } = "Стул";
            public string Color { get; set; } = "Бордовый";
            public string Material { get; set; } = "Дерево";
    
            public Furniture(string name, string type, string color, string material)
            {
                Name = name;
                Type = type;
                Color = color;
                Material = material;
            }
    
            // Реализация паттерна: return copy of this
            public IFurniturePrototype Clone()
            {
                return (Furniture)this.MemberwiseClone();
            }
    
            public string GetImagePath()
            {
                string typeEng = Type == "Стол" ? "table" : (Type == "Диван" ? "sofa" : "chair");
                string colorEng = Color == "Бордовый" ? "bordo" : "blue";
                return Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "images", $"{typeEng}_{colorEng}.jpg");
            }
        }
    }

//

    using System;
    using System.Drawing;
    using System.IO;
    using System.Windows.Forms;
    
    namespace FurnitureCatalog
    {
        public partial class Form1 : Form
        {
            // Поле prototype
            private Furniture _prototype = new Furniture("Прототип", "Стул", "Бордовый", "Дерево");
    
            public Form1()
            {
                InitializeComponent();
    
                pictureBox1.SizeMode = PictureBoxSizeMode.Zoom;
    
                comboBox1.Items.AddRange(new string[] { "Стул", "Стол", "Диван" });
                comboBox2.Items.AddRange(new string[] { "Бордовый", "Синий" });
                comboBox3.Items.AddRange(new string[] { "Дерево", "Пластмасс" });
    
                comboBox1.SelectedIndex = 0;
                comboBox2.SelectedIndex = 0;
                comboBox3.SelectedIndex = 0;
    
                comboBox1.SelectedIndexChanged += (s, e) => UpdatePreview();
                comboBox2.SelectedIndexChanged += (s, e) => UpdatePreview();
                button1.Click += button1_Click;
    
                this.Load += (s, e) => UpdatePreview();
            }
    
            private void UpdatePreview()
            {
                if (comboBox1.SelectedItem == null || comboBox2.SelectedItem == null) return;
    
                // p = prototype.Clone()
                Furniture currentSelection = (Furniture)_prototype.Clone();
    
                currentSelection.Type = comboBox1.SelectedItem.ToString()!;
                currentSelection.Color = comboBox2.SelectedItem.ToString()!;
    
                string path = currentSelection.GetImagePath();
    
                if (File.Exists(path))
                {
                    if (pictureBox1.Image != null)
                    {
                        var img = pictureBox1.Image;
                        pictureBox1.Image = null;
                        img.Dispose();
                    }
    
                    try
                    {
                        using (FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read))
                        {
                            pictureBox1.Image = Image.FromStream(fs);
                        }
                    }
                    catch (Exception) { /* Ошибка формата WebP или доступа */ }
                }
            }
    
            private void button1_Click(object sender, EventArgs e)
            {
                ConfirmLabel confirm = new ConfirmLabel();
                confirm.ShowDialog();
            }
        }
    }


Выводы:

В реализации с паттерном Prototype работа строится через клонирование существующего эталона. Client (Form1) просто запрашивает копию через интерфейс IFurniturePrototype. Это делает код расширяемым, если появится столешница или кресло, то не потребуется переписывать логику формы — достаточно создать новый класс, реализующий интерфейс, и он будет клонироваться как и базовый стул.

В реализации без паттерна форма сама создаёт объекты через new Furniture(), из-за чего возникает жесткая зависимость. Если мы решим изменить конструктор мебели добавив новые поля, проект просто перестанет собираться, пока мы вручную не исправим каждый вызов new во всех частях программы. В такой архитектуре легко допустить ошибку или передать параметры не в том порядке.

Но для работы такого масштаба паттерн избыточен.


