Проблема: В приложении с загрузкой тяжелых файлов, как видео, возникает проблема стоимости ресурсов и больших затрат трафика на загрузку

Цель: Разработать видеоплеер (мини ютуб)

Применение паттерна Proxy:

GUI (Client) — Класс графического интерфейса
«interface» IVideoService (Subject) — Интерфейс
RealService (Real Subject) — Класс, выполняющий реальную работу. Содержит логику прямых сетевых запросов и скачивания видеофайлов.
CachedVideoProxy (Proxy) — Класс-заместитель, контролирующий доступ к реальному сервису.

listVideos(): String[*] — возвращает список доступных видео.
getVideoInfo(id: String): String — возвращает метаданные ролика.
downloadVideo(id: String): void — инициирует загрузку контента.
Метод listVideos() — проверяет наличие данных в локальной памяти. Если кэш пуст, запрашивает список у RealService и сохраняет его.
Метод downloadVideo(id) — проверяет, было ли видео загружено ранее, предотвращая избыточный расход трафика.

Поле - service: IVideoService — хранит ссылку на объект реального сервиса для делегирования запросов.

![1 лаба-Классы лаб 2-2](https://github.com/user-attachments/assets/f826a688-7763-44a3-b2ef-d153b53bdf62)

Класс-заместитель (Proxy)
Прокси-объект перехватывает вызовы клиента. Если данные уже есть в кэше или на диске, он возвращает их мгновенно, не беспокоя реальный сервис.

    class CachedVideoProxy : public IVideoService {
    private:
        IVideoService* realService; // Ссылка на реальный объект
        std::vector<std::string> listCache; // Кэш списка видео в памяти
    
    public:
        CachedVideoProxy(IVideoService* s) : realService(s) {}
    
        // Кэширование данных в оперативной памяти
        std::vector<std::string> listVideos() override {
            if (listCache.empty()) {
                listCache = realService->listVideos(); // Запрос к "сети" только 1 раз
            }
            return listCache;
        }
    
        // Кэширование файлов на локальном диске
        void downloadVideo(std::string fileName) override {
            std::string cachePath = AppConfig::CACHE + fileName;
    
            if (std::filesystem::exists(cachePath)) {
                // Мгновенный запуск из локального хранилища
                ShellExecuteA(NULL, "open", cachePath.c_str(), NULL, NULL, SW_SHOWNORMAL);
            } else {
                // Если файла нет в кэше — делегируем загрузку реальному сервису
                realService->downloadVideo(fileName);
            }
        }
    };

Интерфейс:

      #pragma once
      #include <string>
      #include <vector>
      
      class IVideoService {
      public:
          virtual std::vector<std::string> listVideos() = 0;
          virtual void downloadVideo(std::string fileName) = 0;
          virtual std::string getVideoInfo(std::string fileName) = 0;
          virtual ~IVideoService() {} 
      };

класс RealYouTubeService:

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
      
  Вывод
  
  В версии без паттерна каждое взаимодействие с приложением приводило к ожиданию и избыточным операциям ввода-вывода, так как программа заново обращалась к "серверу". Это делало интерфейс отзывчивым лишь наполовину и приводило к бесполезному дублированию данных.

С паттерном Proxy запросы обрабатываются мгновенно, так как объект-заместитель перехватывает их и отдает данные из оперативной памяти или локального кэша. Таким образом, паттерн эффективно работает с ресурсами, не перегружая систему.
