using System;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace FurnitureCatalog
{
    public partial class Form1 : Form
    {
        // Поле prototype согласно схеме
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