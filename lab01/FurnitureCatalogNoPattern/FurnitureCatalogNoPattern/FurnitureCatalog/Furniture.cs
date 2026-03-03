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