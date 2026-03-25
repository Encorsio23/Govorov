#pragma once
#include "IVideoService.h"
#include "Config.h"
#include <windows.h>
#include <shellapi.h>
#include <thread>
#include <vector>
#include <string>
#include <filesystem> 

namespace fs = std::filesystem;

class RealYouTubeService : public IVideoService {
public:

    std::vector<std::string> listVideos() override {
        std::vector<std::string> foundVideos;

        
        std::this_thread::sleep_for(std::chrono::seconds(1));//типо запрос к серверу

        try {
            if (fs::exists(AppConfig::SERVER) && fs::is_directory(AppConfig::SERVER)) {
                for (const auto& entry : std::filesystem::directory_iterator(AppConfig::SERVER)) {
                    std::string fileName = entry.path().filename().string();
                    foundVideos.push_back(fileName);
                }
            }
            else {
                foundVideos.push_back("Ошибка: Папка сервера не найдена");
            }
        }
        catch (const std::exception& e) {
            foundVideos.push_back("Ошибка чтения диска");
        }

        if (foundVideos.empty()) {
            foundVideos.push_back("Папка сервера пуста");
        }

        return foundVideos;
    }

    void downloadVideo(std::string fileName) override {
        std::string source = AppConfig::SERVER + fileName;
        std::string destination = AppConfig::CACHE + fileName;

        std::this_thread::sleep_for(std::chrono::seconds(3));

        // Копируем файл из сервера в кэш
        // FALSE означает, что мы всегда перезаписываем файл, если он там был
        if (CopyFileA(source.c_str(), destination.c_str(), FALSE)) {
            // Если скопировалось - запускаем плеер
            ShellExecuteA(NULL, "open", destination.c_str(), NULL, NULL, SW_SHOWNORMAL);
        }
        else {
            OutputDebugStringA("Ошибка: Не удалось скопировать файл с сервера.");
        }
    }

    // Получение информации о файле
    std::string getVideoInfo(std::string fileName) override {
        return "Файл: " + fileName + " | Источник: Удаленный сервер (C:\\YouTube_Server)";
    }
};