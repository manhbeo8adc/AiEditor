# Hướng dẫn Cài đặt GraphRAG cho Cursor

## Tổng quan
GraphRAG (Graph Retrieval-Augmented Generation) là một extension mạnh mẽ cho Cursor giúp cải thiện khả năng hiểu và phân tích codebase phức tạp thông qua knowledge graph.

## Yêu cầu hệ thống
- **Cursor IDE**: Phiên bản 0.40+ 
- **Python**: 3.10+ (có thể dùng conda environment hiện tại)
- **RAM**: Tối thiểu 8GB, khuyến nghị 16GB+
- **GPU**: Không bắt buộc nhưng tăng tốc độ xử lý

## Cài đặt GraphRAG

### 1. Cài đặt Extension trong Cursor

1. **Mở Cursor IDE**
2. **Truy cập Extensions** (Ctrl+Shift+X)
3. **Tìm kiếm "GraphRAG"** hoặc "Microsoft GraphRAG"
4. **Click Install** cho extension chính thức

### 2. Cài đặt Python Dependencies

```bash
# Kích hoạt conda environment hiện tại
conda activate ai_video_env

# Cài đặt GraphRAG
pip install graphrag

# Cài đặt dependencies bổ sung
pip install tiktoken networkx graspologic
```

### 3. Cấu hình cho AI Video Editor Project

#### 3.1 Tạo cấu hình GraphRAG

```bash
# Tạo thư mục config
mkdir -p .graphrag

# Tạo file cấu hình
cat > .graphrag/settings.yaml << 'EOF'
# GraphRAG Configuration for AI Video Editor
encoding_model: cl100k_base
skip_workflows: []
reporting:
  type: file
  base_dir: .graphrag/output
  
storage:
  type: file
  base_dir: .graphrag/storage

cache:
  type: file
  base_dir: .graphrag/cache

input:
  type: file
  file_type: text
  base_dir: .graphrag/input
  file_pattern: ".*\\.(py|md|txt|js|jsx|ts|tsx)$"

llm:
  api_key: ${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-4o-mini
  model_supports_json: true
  max_tokens: 4000
  temperature: 0.1

embeddings:
  api_key: ${OPENAI_API_KEY}
  type: openai_embedding
  model: text-embedding-3-small
  max_tokens: 8191

chunks:
  size: 1200
  overlap: 100

community_detection:
  max_cluster_size: 10

entity_extraction:
  max_gleanings: 1

summarize_descriptions:
  max_length: 500
EOF
```

#### 3.2 Chuẩn bị dữ liệu input

```bash
# Tạo script để chuẩn bị input data
cat > prepare_graphrag_input.py << 'EOF'
#!/usr/bin/env python3
"""
Chuẩn bị input data cho GraphRAG từ AI Video Editor codebase
"""

import os
import shutil
from pathlib import Path

def prepare_input_data():
    """Chuẩn bị dữ liệu input cho GraphRAG"""
    
    # Tạo thư mục input
    input_dir = Path('.graphrag/input')
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # Danh sách files và directories quan trọng
    important_files = [
        'README.md',
        'requirements.txt',
        'docs/roadmap.md',
        'docs/environment-setup.md',
        'docs/testing/step1-testing-guide.md',
        'docs/testing/step2-testing-guide.md',
        'backend/app.py',
        'backend/video_processor.py',
        'backend/wan2gp_wrapper.py',
        'frontend/src/App.js',
        'frontend/src/index.js',
        'frontend/package.json',
    ]
    
    # Copy files quan trọng
    for file_path in important_files:
        if os.path.exists(file_path):
            # Tạo tên file unique
            safe_filename = file_path.replace('/', '_').replace('\\', '_')
            target_path = input_dir / safe_filename
            
            try:
                shutil.copy2(file_path, target_path)
                print(f"✅ Copied: {file_path} -> {safe_filename}")
            except Exception as e:
                print(f"⚠️  Failed to copy {file_path}: {e}")
    
    # Tạo project overview file
    overview_content = """
# AI Video Editor Project Overview

## Architecture
- **Backend**: Python Flask with video processing capabilities
- **Frontend**: React-based user interface
- **AI Processing**: wan2GP integration for video transitions
- **Security**: Rate limiting, input validation, secure file handling

## Key Components
- VideoProcessor: Handles video processing pipeline
- Flask API: RESTful endpoints for frontend communication
- wan2GP Wrapper: AI model integration layer
- Security Layer: File validation and safe command execution

## Development Environment
- Python 3.10+ with conda environment
- GPU Blackwell compatibility (RTX 50xx series)
- FFmpeg for video processing
- PyTorch for AI model inference

## Testing Strategy
- Step 1: Environment and basic setup
- Step 2: Video processing and security features
- Step 3: wan2GP integration
- Step 4: Frontend development
- Step 5: End-to-end testing
"""
    
    with open(input_dir / 'project_overview.txt', 'w') as f:
        f.write(overview_content)
    
    print(f"\n✅ GraphRAG input data prepared in {input_dir}")
    print(f"📊 Total files: {len(list(input_dir.glob('*')))}")

if __name__ == "__main__":
    prepare_input_data()
EOF

# Chạy script chuẩn bị
python prepare_graphrag_input.py
```

#### 3.3 Cấu hình Environment Variables

```bash
# Tạo file .env cho GraphRAG (nếu chưa có)
cat > .env << 'EOF'
# OpenAI API Key for GraphRAG
OPENAI_API_KEY=your_openai_api_key_here

# GraphRAG Configuration
GRAPHRAG_API_KEY=${OPENAI_API_KEY}
GRAPHRAG_STORAGE_TYPE=file
GRAPHRAG_CACHE_TYPE=file
EOF

# Thêm vào .gitignore
echo ".graphrag/" >> .gitignore
echo ".env" >> .gitignore
```

## Sử dụng GraphRAG trong Cursor

### 1. Khởi tạo Knowledge Graph

```bash
# Trong terminal của Cursor
conda activate ai_video_env

# Khởi tạo GraphRAG index
graphrag index --config .graphrag/settings.yaml

# Kiểm tra kết quả
ls -la .graphrag/output/
```

### 2. Sử dụng GraphRAG Queries

```bash
# Query về architecture
graphrag query --config .graphrag/settings.yaml \
  --method global \
  "Explain the overall architecture of the AI Video Editor project"

# Query về specific component
graphrag query --config .graphrag/settings.yaml \
  --method local \
  "How does the VideoProcessor handle GPU acceleration?"

# Query về security features
graphrag query --config .graphrag/settings.yaml \
  --method global \
  "What security measures are implemented in the backend?"
```

### 3. Tích hợp với Cursor Workflow

#### 3.1 Tạo Cursor Commands

Tạo file `.cursor/commands.json`:

```json
{
  "commands": [
    {
      "name": "GraphRAG: Analyze Current File",
      "command": "graphrag query --config .graphrag/settings.yaml --method local \"Analyze the current file and its role in the project\"",
      "shortcut": "Ctrl+Alt+G"
    },
    {
      "name": "GraphRAG: Project Overview",
      "command": "graphrag query --config .graphrag/settings.yaml --method global \"Provide a comprehensive overview of the AI Video Editor project structure\"",
      "shortcut": "Ctrl+Alt+O"
    },
    {
      "name": "GraphRAG: Update Index",
      "command": "graphrag index --config .graphrag/settings.yaml",
      "shortcut": "Ctrl+Alt+U"
    }
  ]
}
```

#### 3.2 Cursor Settings

Cập nhật `.cursor/settings.json`:

```json
{
  "graphrag.enabled": true,
  "graphrag.configPath": ".graphrag/settings.yaml",
  "graphrag.autoIndex": false,
  "graphrag.indexOnSave": true,
  "python.defaultInterpreterPath": "./ai_video_env/bin/python"
}
```

## Troubleshooting

### Lỗi thường gặp

#### 1. OpenAI API Key không hoạt động
```bash
# Kiểm tra API key
echo $OPENAI_API_KEY

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### 2. Memory issues
```bash
# Giảm chunk size trong settings.yaml
chunks:
  size: 800
  overlap: 50

# Hoặc sử dụng model nhỏ hơn
llm:
  model: gpt-3.5-turbo
```

#### 3. Indexing quá chậm
```bash
# Sử dụng model embedding nhỏ hơn
embeddings:
  model: text-embedding-ada-002
  
# Hoặc giảm số lượng files
file_pattern: ".*\\.(py|md)$"
```

## Sử dụng nâng cao

### 1. Custom Prompts

Tạo file `.graphrag/prompts/custom_prompts.yaml`:

```yaml
entity_extraction: |
  Extract entities related to:
  - AI/ML components and models
  - Video processing functions
  - API endpoints and security measures
  - File types and data structures
  - Error handling patterns

community_detection: |
  Identify communities based on:
  - Functional modules (backend, frontend, AI)
  - Security components
  - Testing frameworks
  - Documentation patterns

summarization: |
  Summarize focusing on:
  - Technical architecture decisions
  - Security implementations
  - Performance optimizations
  - Integration patterns
```

### 2. Automated Updates

Tạo script `update_graphrag.py`:

```python
#!/usr/bin/env python3
"""
Tự động cập nhật GraphRAG index khi code thay đổi
"""

import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GraphRAGUpdater(FileSystemEventHandler):
    def __init__(self):
        self.last_update = 0
        self.update_delay = 60  # 60 seconds
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Chỉ update cho Python và MD files
        if not event.src_path.endswith(('.py', '.md', '.js', '.jsx')):
            return
        
        current_time = time.time()
        if current_time - self.last_update > self.update_delay:
            print(f"📁 File changed: {event.src_path}")
            self.update_graphrag()
            self.last_update = current_time
    
    def update_graphrag(self):
        """Update GraphRAG index"""
        try:
            print("🔄 Updating GraphRAG index...")
            subprocess.run([
                'python', 'prepare_graphrag_input.py'
            ], check=True)
            
            subprocess.run([
                'graphrag', 'index', 
                '--config', '.graphrag/settings.yaml'
            ], check=True)
            
            print("✅ GraphRAG index updated successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to update GraphRAG: {e}")

if __name__ == "__main__":
    event_handler = GraphRAGUpdater()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    
    print("👁️  Watching for file changes...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
```

## Tối ưu hóa Performance

### 1. Caching Strategy

```yaml
# Trong settings.yaml
cache:
  type: file
  base_dir: .graphrag/cache
  ttl: 3600  # 1 hour cache

# Sử dụng local cache cho development
storage:
  type: file
  base_dir: .graphrag/storage
  connection_string: "sqlite:///.graphrag/storage/graphrag.db"
```

### 2. Batch Processing

```bash
# Xử lý batch nhiều queries
cat > batch_queries.txt << 'EOF'
What is the overall architecture of the project?
How does video processing work?
What security measures are implemented?
How is the frontend connected to the backend?
EOF

# Chạy batch queries
while IFS= read -r query; do
  echo "Query: $query"
  graphrag query --config .graphrag/settings.yaml --method global "$query"
  echo "---"
done < batch_queries.txt
```

## Kết luận

GraphRAG sẽ giúp bạn:
- **Hiểu codebase nhanh hơn**: Tự động phân tích và tạo knowledge graph
- **Tìm kiếm thông tin chính xác**: Query về specific components hoặc patterns
- **Debug hiệu quả**: Hiểu relationships giữa các modules
- **Code review tốt hơn**: Phát hiện patterns và potential issues

Sau khi setup, GraphRAG sẽ tự động cập nhật và cung cấp insights về codebase AI Video Editor project của bạn.