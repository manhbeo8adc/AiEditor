# Frontend Documentation

## Overview
Frontend của AI Video Editor được xây dựng bằng React, cung cấp giao diện người dùng cho việc upload và xử lý video.

## Structure
```
frontend/
├── public/
│   └── index.html      # HTML template
├── src/
│   ├── App.js          # Main React component
│   ├── App.css         # Component styles
│   ├── index.js        # React entry point
│   └── index.css       # Global styles
└── package.json        # Dependencies and scripts
```

## Files Documentation

### public/index.html
**Purpose:** HTML template cho React application

**Key Features:**
- Meta tags cho responsive design
- Root div element cho React mounting
- Basic SEO meta tags

### src/App.js
**Purpose:** Main React component với UI logic

**Key Features:**
- Backend status checking
- Video upload interface (placeholder)
- Processing controls (placeholder)
- Axios integration cho API calls

**Testing:**
```bash
# Start development server
cd frontend
npm start

# Test backend connection
# Click "Check Backend Status" button
```

### src/index.js
**Purpose:** React application entry point

**Key Features:**
- React DOM rendering
- StrictMode wrapper
- App component mounting

### Styling Files
- **App.css:** Component-specific styles
- **index.css:** Global application styles

## Components Structure

### App Component
**State Management:**
- `status`: Backend connection status
- `loading`: Loading state cho API calls

**Methods:**
- `checkBackendStatus()`: Test backend connection

**UI Sections:**
- Header với title và description
- Status section với backend check
- Upload section (placeholder)
- Processing section (placeholder)

## API Integration

### Backend Communication
```javascript
// Example API call
const response = await axios.get('http://localhost:5000/api/status');
```

**Endpoints Used:**
- `GET /api/status` - Backend health check

## Dependencies

### Production Dependencies
- React 18.2.0
- React-DOM 18.2.0
- Axios 1.5.0
- React-Dropzone 14.2.3 (for file uploads)
- React-Scripts 5.0.1

### Development Dependencies
- Electron 25.6.0 (for desktop app)
- Electron-Builder 24.6.3
- Concurrently 8.2.0

## Scripts

```bash
# Development server
npm start

# Production build
npm run build

# Run tests
npm test

# Eject configuration (not recommended)
npm run eject
```

## Testing

### Manual Testing
1. Start backend: `python backend/app.py`
2. Start frontend: `cd frontend && npm start`
3. Open http://localhost:3000
4. Click "Check Backend Status" button
5. Verify status message appears

### Expected Behavior
- Button shows "Checking..." when loading
- Success: "Backend Status: AI Video Editor Backend is running"
- Error: "Backend connection failed"

## Future Features
- File upload với drag-and-drop
- Progress bars cho processing
- Video preview
- Error handling UI
- Real-time status updates