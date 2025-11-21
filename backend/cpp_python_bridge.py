"""Python bridge to C++ optimization layer for STUDYBOARD"""

import ctypes
import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CppBridge:
    """
    Python interface to C++ optimization bridge.
    Provides high-performance operations for model inference.
    """
    
    def __init__(self):
        self.bridge = None
        self.initialized = False
        self._load_library()
    
    def _load_library(self):
        """Load the C++ shared library"""
        try:
            # Determine library extension based on platform
            if sys.platform == 'win32':
                lib_name = 'studyboard_bridge.dll'
            elif sys.platform == 'darwin':
                lib_name = 'studyboard_bridge.dylib'
            else:
                lib_name = 'studyboard_bridge.so'
            
            # Search for library in cpp_bridge/build/
            lib_path = Path(__file__).parent.parent / 'cpp_bridge' / 'build' / lib_name
            
            if not lib_path.exists():
                logger.warning(f"C++ bridge library not found at {lib_path}")
                logger.warning("C++ optimizations will not be available")
                logger.warning("To build: cd cpp_bridge && mkdir build && cd build && cmake .. && cmake --build .")
                return
            
            # Load library
            self.bridge = ctypes.CDLL(str(lib_path))
            
            # Define function signatures
            self.bridge.createBridge.restype = ctypes.c_void_p
            self.bridge.destroyBridge.argtypes = [ctypes.c_void_p]
            
            logger.info("C++ bridge loaded successfully")
            self.initialized = True
            
        except Exception as e:
            logger.error(f"Failed to load C++ bridge: {str(e)}")
            self.bridge = None
    
    def is_available(self):
        """Check if C++ bridge is available"""
        return self.initialized and self.bridge is not None
    
    def optimize_inference(self, input_data):
        """
        Optimize model inference using C++ layer.
        Falls back to Python if C++ not available.
        
        Args:
            input_data: Input tensor or data for optimization
        
        Returns:
            Optimized output
        """
        if not self.is_available():
            logger.debug("C++ bridge not available, using Python fallback")
            return input_data  # Fallback to Python
        
        try:
            # Call C++ optimization
            # This is a placeholder - actual implementation depends on your needs
            logger.debug("Using C++ optimized inference")
            return input_data
        except Exception as e:
            logger.error(f"C++ optimization failed: {str(e)}")
            return input_data  # Fallback
    
    def quantize_model(self, weights):
        """
        Quantize model weights using C++ for speed.
        
        Args:
            weights: Model weights as numpy array
        
        Returns:
            Quantized weights
        """
        if not self.is_available():
            # Python fallback quantization
            import numpy as np
            return np.round(weights * 127).astype(np.int8)
        
        # Use C++ quantization (placeholder)
        logger.debug("Using C++ quantization")
        return weights
    
    def cleanup(self):
        """Clean up C++ resources"""
        if self.bridge and self.initialized:
            try:
                # Call cleanup if needed
                logger.info("C++ bridge cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up C++ bridge: {str(e)}")

# Global instance
_cpp_bridge = None

def get_cpp_bridge():
    """Get global C++ bridge instance"""
    global _cpp_bridge
    if _cpp_bridge is None:
        _cpp_bridge = CppBridge()
    return _cpp_bridge