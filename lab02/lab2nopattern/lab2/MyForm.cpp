#include <string>
#include <vector>
#include <msclr\marshal_cppstd.h> // КРИТИЧНО для конвертации строк

#using <System.dll>
#using <System.Windows.Forms.dll>
#using <System.Drawing.dll>

#include "RealService.h"

using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

public ref class MyForm : public Form {
private:
    RealService* service;
    ListBox^ listBox;
    Button^ btnLoad;
    Button^ btnDownload;
    Label^ lblStatus;

public:
    MyForm() {
        service = new RealService();
        InitComponents();
    }

    void InitComponents() {
        this->Text = "YouTube - Version NO PATTERN";
        this->Size = System::Drawing::Size(450, 350);

        listBox = gcnew ListBox();
        listBox->Location = Point(10, 10);
        listBox->Size = System::Drawing::Size(400, 150);

        btnLoad = gcnew Button();
        btnLoad->Text = "Обновить список";
        btnLoad->Location = Point(10, 180);
        btnLoad->Size = System::Drawing::Size(150, 35);
        btnLoad->Click += gcnew EventHandler(this, &MyForm::OnLoadClick);

        btnDownload = gcnew Button();
        btnDownload->Text = "Скачать видео";
        btnDownload->Location = Point(170, 180);
        btnDownload->Size = System::Drawing::Size(150, 35);
        btnDownload->Click += gcnew EventHandler(this, &MyForm::OnDownloadClick);

        lblStatus = gcnew Label();
        lblStatus->Text = "Статус: Готов";
        lblStatus->Location = Point(10, 230);
        lblStatus->AutoSize = true;

        this->Controls->Add(listBox);
        this->Controls->Add(btnLoad);
        this->Controls->Add(btnDownload);
        this->Controls->Add(lblStatus);
    }

    void OnLoadClick(Object^ sender, EventArgs^ e) {
        lblStatus->Text = "Запрос к серверу";
        this->Refresh();

        std::vector<std::string> videos = service->listVideos();

        listBox->Items->Clear();
        for (const auto& v : videos) {
            listBox->Items->Add(gcnew String(v.c_str()));
        }
        lblStatus->Text = "Список получен напрямую";
    }

    void OnDownloadClick(Object^ sender, EventArgs^ e) {
        if (listBox->SelectedItem == nullptr) {
            MessageBox::Show("Сначала выберите видео из списка!");
            return;
        }

        // 1. Получаем имя из ListBox
        String^ selected = listBox->SelectedItem->ToString();

        // 2. Конвертируем в std::string для RealService
        std::string fileName = msclr::interop::marshal_as<std::string>(selected);

        lblStatus->Text = "Загрузка " + selected + "";
        this->Refresh();

        // 3. Вызываем метод с реальным именем файла
        service->downloadVideo(fileName);

        lblStatus->Text = "Статус: Видео " + selected + " открыто.";
    }
};

[STAThreadAttribute]
int main() {
    Application::EnableVisualStyles();
    Application::Run(gcnew MyForm());
    return 0;
}