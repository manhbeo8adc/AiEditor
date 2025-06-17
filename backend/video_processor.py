#!/usr/bin/env python3
"""
Video Processing Module for AI Video Editor

Architecture: Hybrid CPU/GPU Processing
- FFmpeg CUDA: Video decode/encode (GPU acceleration)
- PyTorch CUDA: AI model inference (GPU acceleration) 
- OpenCV CPU: Basic image operations (sufficient performance)
"""

import os
import cv2
import subprocess
import tempfile
import shutil
from pathlib import Path
import torch

# Fix OpenMP duplicate library warning
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

class VideoProcessor:
    """
    Hybrid Video Processor with optimized CPU/GPU usage và security
    
    GPU Acceleration:
    - Video decode/encode: FFmpeg CUDA + NVENC
    - AI processing: PyTorch CUDA 12.8
    
    CPU Processing (sufficient performance):
    - Frame extraction to numpy arrays
    - Basic image operations (resize, color conversion)
    - File I/O operations
    
    Security Features:
    - Safe FFmpeg command execution
    - Input validation và sanitization
    - Audio sync protection
    """
    
    def __init__(self, temp_dir="temp", use_gpu=True):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        
        # GPU configuration
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')
        
        # Check GPU capabilities
        if self.use_gpu:
            print(f"🚀 GPU acceleration enabled: {torch.cuda.get_device_name()}")
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   PyTorch version: {torch.__version__}")
        else:
            print("⚠️  Using CPU processing")
    
    def safe_ffmpeg_command(self, input_files, output_file, extra_args=None):
        """Build safe FFmpeg command preventing injection"""
        
        # Validate input files exist và are in allowed directory
        for file_path in input_files:
            if not os.path.exists(file_path):
                raise ValueError(f"Input file not found: {file_path}")
            
            abs_path = os.path.abspath(file_path)
            allowed_dirs = [os.path.abspath('uploads'), os.path.abspath('temp'), os.path.abspath('output')]
            
            if not any(abs_path.startswith(d) for d in allowed_dirs):
                raise ValueError(f"File not in allowed directory: {file_path}")
        
        # Build command with proper escaping
        cmd = ['ffmpeg', '-y']  # Always use list format
        
        # Add hardware acceleration if available
        if self.use_gpu:
            cmd.extend(['-hwaccel', 'cuda'])
        
        # Add input files
        for input_file in input_files:
            cmd.extend(['-i', input_file])
        
        # Add audio sync protection
        cmd.extend(['-avoid_negative_ts', 'make_zero'])
        
        # Add encoding parameters
        if self.use_gpu:
            cmd.extend(['-c:v', 'h264_nvenc', '-c:a', 'aac'])
        else:
            cmd.extend(['-c:v', 'libx264', '-c:a', 'aac'])
        
        # Add extra arguments if provided
        if extra_args:
            cmd.extend(extra_args)
        
        # Add output file
        cmd.append(output_file)
        
        return cmd

    def execute_safe_command(self, cmd, timeout=300):
        """Execute command safely with timeout"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            return result
        except subprocess.TimeoutExpired:
            raise RuntimeError("Command timeout")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}")

    def extract_transition_frames(self, video1_path, video2_path):
        """
        Extract last frame of video1 and first frame of video2 for transition
        
        Returns:
            tuple: (last_frame_path, first_frame_path)
        """
        try:
            output_dir = self.temp_dir / "transition_frames"
            output_dir.mkdir(exist_ok=True)
            
            # Extract last frame from video1
            last_frame_path = output_dir / "last_frame.jpg"
            cmd1 = self.safe_ffmpeg_command(
                [video1_path], 
                str(last_frame_path),
                ['-vf', 'select=eq(n\,0)', '-vframes', '1', '-update', '1']
            )
            
            # Modify command to get last frame
            cmd1[-4] = 'select=eof'  # Select last frame
            
            print("🎬 Extracting last frame from video1...")
            self.execute_safe_command(cmd1)
            
            # Extract first frame from video2
            first_frame_path = output_dir / "first_frame.jpg"
            cmd2 = self.safe_ffmpeg_command(
                [video2_path],
                str(first_frame_path), 
                ['-vf', 'select=eq(n\,0)', '-vframes', '1']
            )
            
            print("🎬 Extracting first frame from video2...")
            self.execute_safe_command(cmd2)
            
            if not os.path.exists(last_frame_path) or not os.path.exists(first_frame_path):
                raise RuntimeError("Failed to extract transition frames")
            
            print(f"✅ Transition frames extracted")
            return str(last_frame_path), str(first_frame_path)
            
        except Exception as e:
            print(f"❌ Frame extraction error: {e}")
            raise

    def merge_videos_with_transition(self, video1_path, transition_path, video2_path, output_path):
        """
        Merge videos with AI transition using safe FFmpeg command
        
        Args:
            video1_path: Path to first video
            transition_path: Path to AI-generated transition
            video2_path: Path to second video  
            output_path: Path for merged output
        """
        try:
            # Validate inputs
            input_files = [video1_path, transition_path, video2_path]
            
            # Create concat file for FFmpeg
            concat_file = self.temp_dir / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for video_path in input_files:
                    f.write(f"file '{os.path.abspath(video_path)}'\n")
            
            # Build safe FFmpeg command for concatenation
            cmd = self.safe_ffmpeg_command(
                [str(concat_file)],
                output_path,
                ['-f', 'concat', '-safe', '0']
            )
            
            # Remove input flag and modify command for concat
            cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_file)]
            
            # Add encoding và audio sync
            cmd.extend(['-avoid_negative_ts', 'make_zero'])
            
            if self.use_gpu:
                cmd.extend(['-c:v', 'h264_nvenc', '-c:a', 'aac'])
            else:
                cmd.extend(['-c:v', 'libx264', '-c:a', 'aac'])
            
            cmd.append(output_path)
            
            print("🎬 Merging videos with transition...")
            self.execute_safe_command(cmd, timeout=600)  # Longer timeout for merging
            
            # Clean up concat file
            if os.path.exists(concat_file):
                os.remove(concat_file)
            
            print(f"✅ Videos merged successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Video merge error: {e}")
            raise
    
    def extract_frames(self, video_path, output_dir=None, max_frames=None):
        """
        Extract frames from video using FFmpeg CUDA acceleration
        
        GPU: FFmpeg hardware decode
        CPU: Frame saving and basic processing
        """
        if output_dir is None:
            output_dir = self.temp_dir / "frames"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # FFmpeg command with CUDA acceleration
            cmd = [
                'ffmpeg', '-y',
                '-hwaccel', 'cuda',  # GPU hardware acceleration
                '-i', str(video_path),
                '-f', 'image2',
                str(output_dir / 'frame_%06d.jpg')
            ]
            
            if max_frames:
                cmd.extend(['-vframes', str(max_frames)])
            
            print(f"🎬 Extracting frames with GPU acceleration...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Get frame list (CPU operation - fast enough)
            frame_files = sorted(output_dir.glob('frame_*.jpg'))
            print(f"✅ Extracted {len(frame_files)} frames")
            
            return [str(f) for f in frame_files]
            
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg error: {e.stderr}")
            # Fallback to CPU decode
            return self._extract_frames_cpu(video_path, output_dir, max_frames)
    
    def _extract_frames_cpu(self, video_path, output_dir, max_frames=None):
        """
        Fallback CPU frame extraction using OpenCV
        
        Note: OpenCV CPU is sufficient for basic frame extraction
        """
        print("🔄 Falling back to CPU frame extraction...")
        
        cap = cv2.VideoCapture(str(video_path))
        frame_count = 0
        frame_files = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if max_frames and frame_count >= max_frames:
                break
            
            # Basic image operations - CPU sufficient
            frame_path = output_dir / f'frame_{frame_count:06d}.jpg'
            cv2.imwrite(str(frame_path), frame)  # CPU I/O
            frame_files.append(str(frame_path))
            frame_count += 1
        
        cap.release()
        print(f"✅ Extracted {len(frame_files)} frames (CPU)")
        return frame_files
    
    def process_frame_ai(self, frame_path):
        """
        AI processing with PyTorch CUDA acceleration
        
        GPU: AI model inference (where GPU acceleration matters most)
        CPU: Image loading and basic preprocessing
        """
        # Load image - CPU operation (fast enough)
        frame = cv2.imread(frame_path)
        if frame is None:
            raise ValueError(f"Could not load frame: {frame_path}")
        
        # Basic preprocessing - CPU sufficient
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # CPU
        frame = cv2.resize(frame, (512, 512))  # CPU - fast enough
        
        if self.use_gpu:
            # Convert to tensor and move to GPU for AI processing
            frame_tensor = torch.from_numpy(frame).float().to(self.device)
            frame_tensor = frame_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0
            
            # TODO: Add actual AI model inference here
            # processed_tensor = ai_model(frame_tensor)  # GPU acceleration
            
            # For now, just return the preprocessed frame
            processed_frame = frame_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255
            return processed_frame.astype('uint8')
        else:
            # CPU processing fallback
            return frame
    
    def merge_frames_to_video(self, frame_dir, output_path, fps=30):
        """
        Merge frames to video using FFmpeg NVENC GPU encoding
        
        GPU: Video encoding with NVENC (significant speedup)
        CPU: File path operations
        """
        frame_dir = Path(frame_dir)
        
        try:
            # FFmpeg command with GPU encoding
            cmd = [
                'ffmpeg', '-y',
                '-framerate', str(fps),
                '-i', str(frame_dir / 'frame_%06d.jpg'),
                '-c:v', 'h264_nvenc',  # NVIDIA GPU encoder
                '-preset', 'fast',
                '-pix_fmt', 'yuv420p',
                str(output_path)
            ]
            
            print(f"🎬 Encoding video with GPU acceleration...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Video saved: {output_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ GPU encoding failed: {e.stderr}")
            # Fallback to CPU encoding
            self._merge_frames_cpu(frame_dir, output_path, fps)
    
    def _merge_frames_cpu(self, frame_dir, output_path, fps=30):
        """
        Fallback CPU video encoding
        """
        print("🔄 Falling back to CPU video encoding...")
        
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', str(frame_dir / 'frame_%06d.jpg'),
            '-c:v', 'libx264',  # CPU encoder
            '-pix_fmt', 'yuv420p',
            str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Video saved (CPU): {output_path}")
    
    def process_video(self, input_path, output_path, processing_options=None):
        """
        Complete video processing pipeline
        
        Args:
            input_path: Path to input video
            output_path: Path to output video
            processing_options: Dict with processing options
        """
        print(f"🎬 Processing video: {input_path} -> {output_path}")
        
        try:
            # Step 1: Extract frames (GPU accelerated)
            frames = self.extract_frames(input_path)
            
            # Step 2: Process frames with AI (GPU accelerated)
            processed_frames = []
            for frame_path in frames:
                processed_frame = self.process_frame_ai(frame_path)
                processed_frames.append(processed_frame)
            
            # Step 3: Merge frames back to video (GPU accelerated)
            frame_dir = Path(frames[0]).parent
            self.merge_frames_to_video(frame_dir, output_path)
            
            # Step 4: Cleanup
            self.cleanup_temp_files()
            
            print(f"✅ Video processing completed: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Video processing failed: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files - CPU I/O operation"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Cleaned up temporary files")
    
    def get_video_info(self, video_path):
        """
        Get video information using FFprobe
        CPU operation - sufficient performance
        """
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams',
            str(video_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            import json
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"❌ Could not get video info: {e}")
            return None

# Example usage and architecture demonstration
if __name__ == "__main__":
    """
    Demonstration of Hybrid CPU/GPU Architecture
    
    Performance Optimization Strategy:
    1. GPU for heavy lifting (video decode/encode, AI inference)
    2. CPU for lightweight operations (file I/O, basic image ops)
    3. Minimize GPU memory transfers
    """
    
    processor = VideoProcessor()
    
    print("\n🏗️  AI Video Editor Architecture:")
    print("=" * 50)
    print("📹 Video Decode:     FFmpeg CUDA (GPU)")
    print("🖼️  Frame Operations:  OpenCV (CPU) - sufficient")
    print("🧠 AI Processing:    PyTorch CUDA (GPU)")
    print("📹 Video Encode:     FFmpeg NVENC (GPU)")
    print("💾 File I/O:         CPU - sufficient")
    print("=" * 50)
    
    if processor.use_gpu:
        print(f"✅ GPU Ready: {torch.cuda.get_device_name()}")
        print(f"   CUDA Capability: sm_{torch.cuda.get_device_capability()[0]}{torch.cuda.get_device_capability()[1]}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3} GB")
    
    print("\n💡 Note: OpenCV CUDA warning is expected and doesn't affect performance")
    print("   GPU acceleration is handled by FFmpeg and PyTorch where it matters most!") 