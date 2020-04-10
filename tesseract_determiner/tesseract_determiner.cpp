#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <regex>
namespace fs = std::filesystem;

int main (int argc, char *argv[]) {

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
        std::cout << "Loading (png): " << imgPath << std::endl;

        // Get coordinates path
        auto extIndex  = imgPath.find(".png");
        auto txtPath = imgPath;
        txtPath.replace(extIndex, txtPath.length() - 1, ".txt");
        std::cout << "Loading (txt): " << txtPath << std::endl;

        // Extract coordinates
        std::ifstream coordinateFile(txtPath);
        std::string line;
        std::vector<int> coordinates = {};
        std::smatch match;
        std::regex rgx("[0-9]+");

        while (std::getline(coordinateFile, line)) {
            if (line.find("file://") != std::string::npos)
                continue;


            const std::regex regex("[0-9]+");
            std::smatch match;
            while (std::regex_search(line, match, regex)) {

                for (auto currCoordinate : match)
                    coordinates.push_back(std::stoi(currCoordinate.str()));

                line = match.suffix().str();
            }
        }

        // Read Image
        Pix *image = pixRead(imgPath.c_str());
        api->SetImage(image);

        // Output file
        std::vector<std::string> outLines;

        for (int i = 0; i < coordinates.size() - 4; i += 4) {
            int left = coordinates[i];
            int top = coordinates[i+1];
            int width = coordinates[i+2];
            int height = coordinates[i+3];
            
            //  Set the Rectangles that need to be checked
            api->SetRectangle(left, top, width, height);
            
            // Get OCR result
            std::string outText;
            outText = api->GetUTF8Text();

            // Create Output
            if (outText.length() > 2)
                outText = outText.erase(outText.length() - 3, outText.length() - 1);
            std::string outLine = outText + "\t" + "(" + std::to_string(left) + "," + std::to_string(top) + "," + std::to_string(width) + "," + std::to_string(height) + ")";
            outLines.push_back(outLine);
        }

        // Write found words in file
        auto endOfPath = txtPath.erase(0,inPath.string().size());
        auto outPath = outDir.string() + endOfPath;
        std::cout << "Writing (txt): " << outPath << std::endl;
        fs::create_directories(fs::path(outPath).parent_path());
        std::ofstream outFile(outPath);
        std::ostream_iterator<std::string> output_iterator(outFile);
        for (const auto & line : outLines) outFile << line << "\n";

        pixDestroy(&image);
    }


    // Destroy used object and release memory
    api->End();

    return 0;
}
