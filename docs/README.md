# AI Video Editor - Documentation Index

## 📋 Quick Start Guide

1. **Bắt đầu development:** Đọc `roadmap.md` từ đầu đến bước cần làm
2. **Gặp lỗi:** Tìm trong `troubleshooting.md` 
3. **Setup environment:** Follow `environment-setup.md`
4. **Security concerns:** Check `security-validation.md`
5. **Ready to build:** Use `build-deployment.md`

## 📁 Documentation Structure

### 🗺️ [roadmap.md](./roadmap.md)
**Main development guide với micro-tasks và AI prompts**

**Khi nào dùng:** Đây là file chính, đọc từ đầu đến cuối theo thứ tự
**Cho AI:** Mỗi AI prompt đã có references đến docs cần đọc
**Cho Human:** Mỗi Human task có link đến docs cần tham khảo

**Key sections:**
- MVP Implementation Steps với AI Prompts
- Human validation steps với doc references  
- Phase 2 advanced features planning

---

### 🔧 [environment-setup.md](./environment-setup.md)
**System requirements, dependencies, installation guide**

**Khi nào dùng:**
- Bước 1.1 (Project Structure): sections "Project Structure Setup", "Exact Dependencies"
- Mọi lúc cần check dependencies hoặc setup clean environment
- Khi validation fails trong roadmap steps

**For AI prompts:** AI cần đọc "Exact Dependencies" cho version chính xác
**For Human tasks:** Use "Installation Verification" và "Final Verification Script"

**Key sections:**
- `System Requirements`: Hardware và software minimums
- `Exact Dependencies`: Version-locked requirements.txt và package.json  
- `Installation Verification`: Scripts để test setup
- `Performance Optimization`: GPU memory, system optimization

---

### 🛡️ [security-validation.md](./security-validation.md)
**Security best practices, validation rules, safe coding patterns**

**Khi nào dùng:**
- Bước 1.2 (Flask App): AI đọc "API Security", "Request Validation"
- Bước 2.1 (Upload Handler): AI đọc "File Upload Security"
- Bước 2.3 (Video Merger): AI đọc "Process Security"
- Mọi lúc implement user input handling

**For AI prompts:** AI phải apply security patterns từ docs này
**For Human validation:** Check security features theo checklist trong docs

**Key sections:**
- `File Upload Security`: Magic byte validation, path traversal prevention
- `API Security`: Rate limiting, CORS, request validation decorators
- `Process Security`: Safe FFmpeg commands, command injection prevention
- `Security Checklist`: Pre-deployment security audit

---

### 🔍 [troubleshooting.md](./troubleshooting.md)
**Solutions cho common issues, debugging guide, recovery procedures**

**Khi nào dùng:**
- Khi có lỗi trong bất kỳ step nào của roadmap
- Bước 3.2.3 (wan2GP Testing): "wan2GP CUDA Errors", "Performance Issues"
- Bước 5.2 (Performance Testing): "Performance Issues", "Memory Overflow"
- Backend validation fails: "Network & API Issues"

**For Human tasks:** First place to check khi có lỗi
**For AI debugging:** Reference specific solutions cho bug fixes

**Key sections:**
- `Environment Setup Issues`: FFmpeg, CUDA, dependencies problems
- `Runtime Issues`: Memory, port conflicts, permissions
- `Processing Issues`: Video formats, audio sync
- `Quick Diagnostic Commands`: System health checks
- `Emergency Recovery`: Complete reset procedures

---

### 📦 [build-deployment.md](./build-deployment.md)
**Production build, deployment, distribution guide**

**Khi nào dùng:**
- Khi ready để build MVP for testing
- Bước 5.2 (Performance Testing): Use "Testing Builds" section
- Phase 1D (Polish & Deploy): Follow complete build process
- Cross-platform deployment

**For Human tasks:** Complete build và deployment workflows  
**For AI:** Template code cho build scripts và configurations

**Key sections:**
- `Development Build`: Local development setup
- `Production Build`: PyInstaller, Electron Builder configs
- `Cross-Platform Build`: Build scripts cho Windows/Mac/Linux
- `Testing Builds`: Automated testing cho built executables
- `Distribution`: Installer creation, packaging

---

## 🚀 Development Workflow

### Starting Development (Human)
1. Read `environment-setup.md` - check system requirements
2. Follow `roadmap.md` step by step
3. Keep `troubleshooting.md` open for quick reference

### AI Assistance Workflow
1. Human gives roadmap step to AI
2. AI reads referenced docs from roadmap prompt
3. AI generates code following security-validation.md patterns
4. Human validates using human testing steps from roadmap
5. If issues → check troubleshooting.md và iterate

### Common Problem Resolution
```
Issue → troubleshooting.md → Specific solution → Apply fix → Test
```

### Security Validation Flow
```
Feature → security-validation.md → Apply patterns → Human test security → Pass
```

## 📚 Quick Reference

### Frequently Used Commands
```bash
# Environment check
python docs/environment-setup.md#verify_setup.py

# Diagnostic
python -c "import cv2, torch, flask; print('All deps OK')"
nvidia-smi  # GPU status

# Development
python backend/app.py  # Start backend
npm start  # Start frontend (in frontend/)

# Troubleshooting
ffmpeg -version  # Check FFmpeg
curl http://localhost:5000/api/status  # Test API
```

### Quick Navigation
- **Error codes** → troubleshooting.md
- **Security patterns** → security-validation.md  
- **Dependencies** → environment-setup.md
- **Build issues** → build-deployment.md
- **Development steps** → roadmap.md

### File Dependencies Map
```
roadmap.md (main)
├── References → environment-setup.md (setup)
├── References → security-validation.md (security)  
├── References → troubleshooting.md (fixes)
└── References → build-deployment.md (deployment)
```

## 🔄 Documentation Maintenance

### When to Update Docs
- New bugs found → Add to troubleshooting.md
- Security issues → Update security-validation.md
- New dependencies → Update environment-setup.md
- Build process changes → Update build-deployment.md
- Process improvements → Update roadmap.md

### Documentation Standards
- Always include code examples
- Reference between docs using relative links
- Keep troubleshooting.md solutions action-oriented
- Update version numbers trong environment-setup.md
- Maintain security-validation.md với latest threats 