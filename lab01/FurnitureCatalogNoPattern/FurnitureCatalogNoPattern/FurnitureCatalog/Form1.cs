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