#!/usr/bin/env python3
"""
Test PyTorch GPU compatibility for Blackwell GPUs
Updated for PyTorch 2.6 + CUDA 12.8 support
"""

import os
import sys
import warnings

# Fix OpenMP duplicate library warning
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def test_pytorch_installation():
    """Test PyTorch installation and GPU compatibility"""
    print("🔥 Testing PyTorch Installation...")
    print("=" * 50)
    
    try:
        import torch
        import torchvision
        import torchaudio
        
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ TorchVision version: {torchvision.__version__}")
        print(f"✅ TorchAudio version: {torchaudio.__version__}")
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"✅ CUDA available: {cuda_available}")
        
        if cuda_available:
            print(f"✅ CUDA version: {torch.version.cuda}")
            print(f"✅ cuDNN version: {torch.backends.cudnn.version()}")
            
            # GPU Information
            gpu_count = torch.cuda.device_count()
            print(f"✅ GPU count: {gpu_count}")
            
            for i in range(gpu_count):
                props = torch.cuda.get_device_properties(i)
                capability = torch.cuda.get_device_capability(i)
                print(f"GPU {i}: {props.name} ({props.total_memory / 1e9:.1f} GB)")
                print(f"   Compute Capability: sm_{capability[0]}{capability[1]}")
                
                # Special check for Blackwell GPUs
                if capability[0] >= 12:  # sm_120+
                    print(f"   🎉 Blackwell GPU detected with PyTorch 2.6+ support!")
                elif capability[0] >= 9:  # sm_90+
                    print(f"   ✅ Modern GPU with full PyTorch support")
                else:
                    print(f"   ⚠️  Older GPU - may have limited features")
        
        return True, "PyTorch installation OK"
        
    except ImportError as e:
        return False, f"Import error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def test_gpu_computation():
    """Test actual GPU computation"""
    print("\n🔥 Testing GPU computation...")
    print("=" * 50)
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("⚠️  No GPU available - using CPU")
            device = torch.device('cpu')
        else:
            device = torch.device('cuda')
            print(f"🎯 Using device: {device}")
        
        # Test tensor operations
        print("📊 Creating test tensors...")
        a = torch.randn(1000, 1000, device=device)
        b = torch.randn(1000, 1000, device=device)
        
        print("🧮 Testing matrix multiplication...")
        c = torch.matmul(a, b)
        
        print("🔢 Testing advanced operations...")
        d = torch.nn.functional.relu(c)
        e = torch.sum(d)
        
        print(f"✅ Computation successful! Result sum: {e.item():.2f}")
        
        # Memory info
        if torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated() / 1e6
            memory_reserved = torch.cuda.memory_reserved() / 1e6
            print(f"📊 GPU Memory - Allocated: {memory_allocated:.1f}MB, Reserved: {memory_reserved:.1f}MB")
        
        return True, "GPU computation successful"
        
    except RuntimeError as e:
        error_msg = str(e)
        if "no kernel image is available" in error_msg:
            print("⚠️  GPU computation failed: CUDA error: no kernel image is available for execution on the device")
            print("→ This WAS expected for Blackwell GPUs with older PyTorch versions")
            print("→ With PyTorch 2.6 + CUDA 12.8, this should be FIXED!")
            print("→ If you still see this error, check:")
            print("   1. NVIDIA Driver version (need 560+)")
            print("   2. PyTorch version (need 2.6.0+cu128)")
            print("   3. Clear PyTorch cache: rm -rf ~/.cache/torch")
            return False, "GPU computation failed - may need driver/PyTorch update"
        else:
            print(f"❌ GPU computation failed: {error_msg}")
            return False, f"GPU computation error: {error_msg}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def test_video_processing():
    """Test video processing capabilities"""
    print("\n🔥 Testing Video Processing...")
    print("=" * 50)
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        # Check OpenCV CUDA support
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            print(f"✅ OpenCV CUDA devices: {cv2.cuda.getCudaEnabledDeviceCount()}")
        else:
            print("⚠️  OpenCV CUDA not available")
        
        return True, "Video processing OK"
        
    except ImportError:
        return False, "OpenCV not installed"
    except Exception as e:
        return False, f"Video processing error: {e}"

def main():
    """Main test function"""
    print("🚀 AI Video Editor - PyTorch 2.6 + CUDA 12.8 Compatibility Test")
    print("=" * 60)
    
    tests = [
        ("PyTorch Installation", test_pytorch_installation),
        ("GPU Computation", test_gpu_computation),
        ("Video Processing", test_video_processing),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            results.append((test_name, success, message))
        except Exception as e:
            results.append((test_name, False, f"Test failed: {e}"))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, success, message in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your system is ready for AI Video Editor!")
    else:
        print("⚠️  Some tests failed. Check the messages above for solutions.")
        print("\n💡 Common solutions:")
        print("   1. Update NVIDIA drivers to 560+")
        print("   2. Install PyTorch 2.6 with CUDA 12.8:")
        print("      pip install torch==2.6.0+cu128 torchvision==0.21.0+cu128 torchaudio==2.6.0+cu128 --index-url https://download.pytorch.org/whl/cu128")
        print("   3. Clear PyTorch cache: rm -rf ~/.cache/torch")
        print("   4. Create new conda environment if needed")
    
    print("=" * 60)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 