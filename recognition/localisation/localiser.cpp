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

    int argc_wanted = 3;

    if (argc < argc_wanted) {
        std::cout << "Missing Arguments! (" << argc - 1 << " provided, " <<  argc_wanted - 1 << " needed)" << std::endl;
        std::cout << "Provide the path to a folder with images and corresponding text files." << std::endl;
        return 1;
    }

    // Initiate Tesseract
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    auto inPath = fs::absolute(fs::path(argv[1])).lexically_normal();
    auto outDir = fs::absolute(fs::path(argv[2])).lexically_normal();

    int left, top, width, height;

    std::vector<std::string> imgs = {};

    // Get the paths to the images
    for (const auto & entry : fs::recursive_directory_iterator(inPath)) {
        auto currentPath = fs::path(entry);
        if (currentPath.extension() == ".png")
            imgs.push_back(fs::absolute(entry.path()));
    }

    // OCR per image and corresponding boxes
    for (const auto & imgPath : imgs) {
        if (prints) std::cout << "Loading (png): " << imgPath << std::endl;
        // Get coordinates path
        auto extIndex  = imgPath.find(".png");

        // Read Image
        std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
        Pix *image = pixRead(imgPath.c_str());
        api->SetImage(image);

        // Output file
        std::vector<std::string> outLines;

        Boxa* boxes = api->GetComponentImages(tesseract::RIL_WORD, true, NULL, NULL);
        if (boxes) {
            for (int i = 0; i < boxes->n; ++i) {
                BOX* box = boxaGetBox(boxes, i, L_CLONE);
                int left = box->x;
                int top = box->y;
                int width = box->w;
                int height = box->h;

                // Create Output
                std::string outLine = "\t(" + std::to_string(left) + "," + std::to_string(top) + "," + std::to_string(width) + "," + std::to_string(height) + ")";
                outLines.push_back(outLine);
            }
        }
        pixDestroy(&image);

        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        std::string time = "% Time (in microseconds):  " + std::to_string(std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count());

        // Write found words in file
        auto endOfPath = imgPath;
        endOfPath.replace(extIndex, endOfPath.length() - 1, ".txt");
        endOfPath = endOfPath.erase(0,inPath.string().size());

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
