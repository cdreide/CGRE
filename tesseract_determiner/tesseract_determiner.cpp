#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <iostream>
#include <sstream>

int main (int argc, char *argv[]) {

    int argc_wanted = 6;

    if (argc < argc_wanted) {
        std::cout << "Missing Arguments! (" << argc - 1 << " provided, " <<  argc_wanted - 1 << " needed)" << std::endl;
        std::cout << "Usage:" << std::endl;
        std::cout << "  img_path left top width height" << std::endl;
        return 1;
    }

    const char* img_path = argv[1];

    int left, top, width, height;

    std::istringstream leftSS(argv[2]);
    leftSS >> left;
    std::istringstream topSS(argv[3]);
    topSS >> top;
    std::istringstream widthSS(argv[4]);
    widthSS >> width;
    std::istringstream heightSS(argv[5]);
    heightSS >> height;

    char *outText;

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Read Image
    Pix *image = pixRead(img_path);
    api->SetImage(image);
    //  Set the Rectangles that need to be checked
    api->SetRectangle(left, top, width, height);
    // Get OCR result
    outText = api->GetUTF8Text();
    printf("OCR output:\n%s", outText);

    // Destroy used object and release memory
    api->End();
    delete [] outText;
    pixDestroy(&image);

    return 0;
}
