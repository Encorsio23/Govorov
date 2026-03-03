using System;
using System.IO;

namespace FurnitureCatalog
{
    // СУЩНОСТЬ: Prototype
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