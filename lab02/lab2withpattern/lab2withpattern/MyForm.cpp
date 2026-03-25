#include <string>
#include <vector>
#include <msclr\marshal_cppstd.h> 

#include "IVideoService.h" 
#include "RealYouTubeService.h"
#include "CachedVideoProxy.h"

#using <System.dll>
#using <System.Windows.Forms.dll>
#using <System.Drawing.dll>

using namespace System;
using namespace System::Windows::Forms;

public ref class MyForm : public Form {
private:
    IVideoService* service;
    ListBox^ listBox;
    Button^ btnLoad;
    Button^ btnDownload;
    Label^ lblStatus;

public:
    MyForm() {
        service = new CachedVideoProxy(new RealYouTubeService());
        InitComponents();
    }

    void InitComponents() {
        this->Text = "YouTube Proxy Demo";
        this->Size = System::Drawing::Size(400, 350);

        listBox = gcnew ListBox();
        listBox->Location = System::Drawing::Point(10, 10);
        listBox->Size = System::Drawing::Size(360, 150);

        btnLoad = gcnew Button();
        btnLoad->Text = "Список видео";
        btnLoad->Location = System::Drawing::Point(10, 170);
        btnLoad->Click += gcnew EventHandler(this, &MyForm::OnLoadClick);

        btnDownload = gcnew Button();
        btnDownload->Text = "Загрузить";
        btnDownload->Location = System::Drawing::Point(120, 170);
        btnDownload->Click += gcnew EventHandler(this, &MyForm::OnDownloadClick);

        lblStatus = gcnew Label();
        lblStatus->Text = "Статус: Ожидание";
        lblStatus->Location = System::Drawing::Point(10, 210);
        lblStatus->AutoSize = true;

        this->Controls->Add(listBox);
        this->Controls->Add(btnLoad);
        this->Controls->Add(btnDownload);
        this->Controls->Add(lblStatus);
    }

    void OnLoadClick(Object^ sender, EventArgs^ e) {
        lblStatus->Text = "Запрос списка...";
        this->Refresh();

        auto videos = service->listVideos();
        listBox->Items->Clear();
        for (const auto& v : videos) {
            listBox->Items->Add(gcnew String(v.c_str()));
        }
        lblStatus->Text = "Список получен.";
    }

    void OnDownloadClick(Object^ sender, EventArgs^ e) {
        if (listBox->SelectedItem == nullptr) return;

        String^ selected = listBox->SelectedItem->ToString();
        std::string fileName = msclr::interop::marshal_as<std::string>(selected);

        lblStatus->Text = "Обработка " + selected + "...";
        this->Refresh();

        service->downloadVideo(fileName);

        lblStatus->Text = "Готово: " + selected;
    }
};

[STAThreadAttribute]
int main() {
    Application::EnableVisualStyles();
    Application::Run(gcnew MyForm());
    return 0;
}