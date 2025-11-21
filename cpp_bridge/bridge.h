#ifndef STUDYBOARD_BRIDGE_H
#define STUDYBOARD_BRIDGE_H

#include <string>
#include <vector>
#include <memory>

namespace studyboard {

/**
 * Communication Bridge between Python backend and C++ optimization layer
 * Handles high-performance operations like model quantization and inference acceleration
 */
class CppBridge {
public:
    CppBridge();
    ~CppBridge();

    // Initialize the bridge
    bool initialize();

    // Text processing optimization
    std::string optimizeTextInference(
        const std::string& input,
        const std::vector<float>& embeddings
    );

    // Image processing optimization
    std::vector<uint8_t> optimizeImageGeneration(
        const std::vector<float>& latents,
        int width,
        int height
    );

    // Memory management
    void clearCache();
    size_t getMemoryUsage() const;

    // Model quantization helpers
    std::vector<int8_t> quantizeWeights(
        const std::vector<float>& weights
    );

    std::vector<float> dequantizeWeights(
        const std::vector<int8_t>& quantized_weights
    );

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

// Factory function for Python binding
extern "C" {
    CppBridge* createBridge();
    void destroyBridge(CppBridge* bridge);
}

} // namespace studyboard

#endif // STUDYBOARD_BRIDGE_H