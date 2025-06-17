#!/usr/bin/env python3
"""
Environment Detection Script for AI Video Editor
Automatically detects GPU, CUDA version, and recommends setup
"""

import subprocess
import sys
import os
import platform

# Fix OpenMP duplicate library warning
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def detect_cuda():
    """Detect CUDA version and GPU availability"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            # Parse CUDA version from nvidia-smi output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'CUDA Version:' in line:
                    cuda_version = line.split('CUDA Version:')[1].strip().split()[0]
                    return float(cuda_version)
        return None
    except:
        return None

def detect_gpu_architecture():
    """Detect GPU architecture"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            gpu_name = result.stdout.strip()
            if 'RTX 50' in gpu_name or 'RTX 60' in gpu_name:
                return 'blackwell'
            elif 'RTX 40' in gpu_name:
                return 'ada_lovelace'
            elif 'RTX 30' in gpu_name:
                return 'ampere'
            elif 'RTX 20' in gpu_name:
                return 'turing'
            elif 'GTX' in gpu_name:
                return 'legacy'
            else:
                return 'other'
        return None
    except:
        return None

def detect_python_version():
    """Get current Python version"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def detect_conda():
    """Check if conda is available"""
    try:
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def recommend_setup():
    """Recommend setup based on environment"""
    print("🔍 AI Video Editor - Environment Detection")
    print("=" * 50)
    
    # System info
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {detect_python_version()}")
    print(f"Conda Available: {'✓' if detect_conda() else '❌'}")
    
    # GPU Detection
    cuda_version = detect_cuda()
    gpu_arch = detect_gpu_architecture()
    
    print(f"CUDA Version: {cuda_version if cuda_version else 'Not detected'}")
    print(f"GPU Architecture: {gpu_arch if gpu_arch else 'Not detected'}")
    
    print("\n" + "=" * 50)
    
    # Recommendations
    if cuda_version and cuda_version >= 12.4:
        if gpu_arch == 'blackwell':
            print("🚀 OPTIMAL SETUP DETECTED!")
            print("✓ Blackwell GPU with CUDA 12.4+")
            print("✓ Recommended: Use environment.yml (Blackwell optimized)")
            setup_file = 'environment.yml'
            setup_type = 'conda'
        else:
            print("⚡ GPU SETUP DETECTED!")
            print("✓ Compatible GPU with CUDA 12.4+")
            print("✓ Recommended: Use environment.yml (GPU accelerated)")
            setup_file = 'environment.yml'
            setup_type = 'conda'
    elif cuda_version and cuda_version < 12.4:
        print("⚠️  CUDA VERSION TOO OLD")
        print(f"Current CUDA: {cuda_version}, Required: 12.4+")
        print("Options:")
        print("1. Upgrade CUDA to 12.4+ (recommended)")
        print("2. Use CPU-only setup (fallback)")
        setup_file = 'requirements-cpu.txt'
        setup_type = 'pip'
    else:
        print("💻 CPU-ONLY SETUP")
        print("→ No GPU detected or CUDA not available")
        print("✓ Recommended: Use requirements-cpu.txt")
        setup_file = 'requirements-cpu.txt'
        setup_type = 'pip'
    
    print("\n" + "=" * 50)
    print("📋 SETUP COMMANDS:")
    
    if setup_type == 'conda' and detect_conda():
        print(f"conda env create -f {setup_file}")
        print("conda activate ai_video_env")
    elif setup_type == 'conda' and not detect_conda():
        print("❌ Conda not available, falling back to pip:")
        print("pip install -r requirements-cpu.txt")
    else:
        print(f"pip install -r {setup_file}")
    
    print("\n📝 NEXT STEPS:")
    print("1. Run the setup command above")
    print("2. Test backend: python backend/app.py")
    print("3. Test API: python test_api.py")
    
    return setup_file, setup_type

def test_pytorch_gpu():
    """Test PyTorch GPU availability after installation"""
    try:
        import torch
        print(f"\n🧪 PyTorch Test:")
        print(f"PyTorch Version: {torch.__version__}")
        print(f"CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU Device: {torch.cuda.get_device_name(0)}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        return True
    except ImportError:
        print("\n❌ PyTorch not installed yet")
        return False

if __name__ == "__main__":
    try:
        setup_file, setup_type = recommend_setup()
        
        # Test PyTorch if available
        test_pytorch_gpu()
        
        print(f"\n💡 For detailed deployment info, see: docs/deployment-strategy.md")
        
    except KeyboardInterrupt:
        print("\n\n👋 Detection cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during detection: {e}")
        print("Falling back to CPU-only setup:")
        print("pip install -r requirements-cpu.txt")
        sys.exit(1) 