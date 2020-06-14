#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <regex>
#include <chrono>

namespace fs = std::filesystem;

int main (int argc, char *argv[]) {

    bool prints = true;

    int argc_wanted = 4;

    if (argc < argc_wanted) {
        std::cout << "Missing Arguments! (" << argc - 1 << " provided, " <<  argc_wanted - 1 << " needed)" << std::endl;
        std::cout << "Provide the path to a folder with images, corresponding text files and the output." << std::endl;
        return 1;
    }

    // Initiate Tesseract
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    auto inPath_img = fs::absolute(fs::path(argv[1])).lexically_normal();
    auto inPath_txt = fs::absolute(fs::path(argv[2])).lexically_normal();
    auto outDir = fs::absolute(fs::path(argv[3])).lexically_normal();

    int left, top, width, height;

    std::vector<std::string> imgs = {};

    // Get the paths to the images
    for (const auto & entry : fs::recursive_directory_iterator(inPath_img)) {
        auto currentPath = fs::path(entry);
        if (currentPath.extension() == ".png")
            imgs.push_back(fs::absolute(entry.path()));
    }

    // OCR per image and corresponding boxes
    for (const auto & imgPath : imgs) {
        if (prints) std::cout << "Loading (png): " << imgPath << std::endl;

        // Get coordinates path
        auto extIndex  = imgPath.find(".png");
        auto txtPath = imgPath;
        txtPath.replace(extIndex, txtPath.length() - 1, ".txt");
        auto endOfPath = txtPath.erase(0, inPath_img.string().size());
        txtPath = inPath_txt.string() + endOfPath;
        if (prints) std::cout << "Loading (txt): " << txtPath << std::endl;

        // Extract coordinates
        std::ifstream coordinateFile(txtPath);
        std::string line = "";
        std::vector<int> coordinates = {};
        std::smatch match;
        std::regex rgx("([0-9]+),([0-9]+),([0-9]+),([0-9]+)");

        while (std::getline(coordinateFile, line)) {
            if (line.find("file://") != std::string::npos && line.find("% Time") != std::string::npos)
                continue;
            if (std::regex_search(line, match, rgx)) {
                for (int i = 1; i < match.size(); i++)
                    coordinates.push_back(std::stoi(match[i].str()));
            }
        }

        // Output file
        std::vector<std::string> outLines;
        std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

        if (!coordinates.empty()) {
            // Read Image
            Pix *image = pixRead(imgPath.c_str());
            api->SetImage(image);

            for (int i = 0; i < coordinates.size() - 4; i += 4) {
                int left = coordinates[i];
                int top = coordinates[i+1];
                int width = coordinates[i+2];
                int height = coordinates[i+3];
                
                //  Set the Rectangles that need to be checked
                api->SetRectangle(left, top, width, height);
                
                // Get OCR result
                char* result = api->GetUTF8Text();
                std::string outText(result);
                delete[] result;

                // Create Output
                outText.erase(std::remove(outText.begin(), outText.end(), '\n'), outText.end());
                std::string outLine = outText + "\t" + "(" + std::to_string(left) + "," + std::to_string(top) + "," + std::to_string(width) + "," + std::to_string(height) + ")";
                outLines.push_back(outLine);
            }
            pixDestroy(&image);
        }
        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        std::string time = "% Time (in microseconds):  " + std::to_string(std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count());

        // Write found words in file
        // auto endOfPath = txtPath.erase(0, inPath_img.string().size());
        auto outPath = outDir.string() + endOfPath;
        if (prints) std::cout << "Writing (txt): " << outPath << std::endl;
        fs::create_directories(fs::path(outPath).parent_path());
        std::ofstream outFile(outPath);
        std::ostream_iterator<std::string> output_iterator(outFile);
        outFile << time << "\n";
        for (const auto & line : outLines) outFile << line << "\n";
    }

    // Destroy used object and release memory
    api->End();

    return 0;
}
