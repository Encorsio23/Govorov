#pragma once
#include "IVideoService.h"
#include "RealYouTubeService.h"
#include <map>
#include <filesystem>

namespace fs = std::filesystem;

class CachedVideoProxy : public IVideoService {
private:
    IVideoService* realService; // Ссылка на реальный объект (ромб в UML)
    std::vector<std::string> listCache; // Кэш списка видео

public:
    CachedVideoProxy(IVideoService* s) : realService(s) {}

    std::vector<std::string> listVideos() override {
        if (listCache.empty()) {
            listCache = realService->listVideos(); // Загружаем один раз
        }
        return listCache;
    }

    void downloadVideo(std::string fileName) override {
        std::string path = "C:\\YouTube_Cache\\" + fileName;

        // ПРОВЕРКА КЭША: Если файл уже есть на диске
        if (fs::exists(path)) {
            // Мгновенный запуск БЕЗ вызова RealService
            ShellExecuteA(NULL, "open", path.c_str(), NULL, NULL, SW_SHOWNORMAL);
        }
        else {
            // Если файла нет — просим реальный сервис его скачать
            realService->downloadVideo(fileName);
        }
    }

    std::string getVideoInfo(std::string fileName) override {
        return realService->getVideoInfo(fileName) + " (Запрошено через Proxy)";
    }
};