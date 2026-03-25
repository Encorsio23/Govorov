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