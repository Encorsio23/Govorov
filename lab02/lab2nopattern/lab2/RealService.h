#pragma once
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <windows.h>
#include <shellapi.h>
#include <filesystem>
#include "Config.h" 

namespace fs = std::filesystem;

class RealService {
public:
    std::vector<std::string> listVideos() {
        std::vector<std::string> videos;
        // Имитация задержки "сети"
        std::this_thread::sleep_for(std::chrono::seconds(2));

        try {
            fs::path serverPath(AppConfig::SERVER);
            if (fs::exists(serverPath)) {
                for (const auto& entry : fs::directory_iterator(serverPath)) {
                    if (entry.is_regular_file()) {
                        videos.push_back(entry.path().filename().string());
                    }
                }
            }
        }
        catch (...) {
            videos.push_back("Ошибка доступа к папке");
        }
        return videos;
    }

    void downloadVideo(std::string fileName) {
        std::string source = AppConfig::SERVER + fileName;
        std::string destination = AppConfig::CACHE + fileName;

        // Имитация долгой загрузки
        std::this_thread::sleep_for(std::chrono::seconds(3));

        // Копируем всегда (без проверки кэша)
        if (CopyFileA(source.c_str(), destination.c_str(), FALSE)) {
            // Обертываем в кавычки для корректного запуска пути с пробелами
            std::string quotedPath = "\"" + destination + "\"";
            ShellExecuteA(NULL, "open", quotedPath.c_str(), NULL, NULL, SW_SHOWNORMAL);
        }
        else {
            MessageBoxA(NULL, ("Не удалось найти файл: " + fileName).c_str(), "Ошибка сервера", MB_OK);
        }
    }
};