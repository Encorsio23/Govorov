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

            // Заполняем списки, чтобы они не были пустыми
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
                // Перед загрузкой новой картинки освобождаем старую, чтобы не было ошибок доступа
                if (pictureBox1.Image != null)
                {
                    var oldImage = pictureBox1.Image;
                    pictureBox1.Image = null;
                    oldImage.Dispose();
                }

                try
                {
                    // Используем загрузку из файла
                    pictureBox1.Image = Image.FromFile(path);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка загрузки файла {fileName}: {ex.Message}");
                }
            }
        }

        // Привязываем события изменения списков
        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e) => UpdatePreview();
        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e) => UpdatePreview();

        // Метод для comboBox3 можно оставить пустым или просто не привязывать
        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e) { }

        // Кнопка ПРИМЕНИТЬ
        private void button1_Click(object sender, EventArgs e)
        {
            // Проверь, как называется твоя форма подтверждения: ConfirmLabel или ConfirmForm
            ConfirmLabel confirm = new ConfirmLabel();
            confirm.ShowDialog();
        }
    }
}