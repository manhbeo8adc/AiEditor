# App Component Documentation

## Overview
Component `App` trong file `frontend/src/App.js` là main React component, cung cấp UI cho AI Video Editor application.

## Component Definition
```javascript
function App() {
    // Component logic
}
```

## State Management

### `status`
- **Type:** `string`
- **Purpose:** Lưu trữ status message từ backend
- **Initial Value:** `''` (empty string)
- **Usage:** Display backend connection status cho user

### `loading`
- **Type:** `boolean`
- **Purpose:** Track loading state khi gọi API
- **Initial Value:** `false`
- **Usage:** Disable button và show loading text

## Methods (Functions)

### `checkBackendStatus()`
**Purpose:** Kiểm tra connection đến backend server

**Parameters:** Không có

**Returns:** `Promise<void>`

**Functionality:**
- Set loading state thành `true`
- Gọi GET request đến `/api/status` endpoint
- Update status message với response
- Handle errors gracefully
- Reset loading state

**API Call:**
```javascript
const response = await axios.get('http://localhost:5000/api/status');
```

**Success Response:**
```javascript
setStatus(`Backend Status: ${response.data.message}`);
```

**Error Handling:**
```javascript
setStatus('Backend connection failed');
console.error('Error:', error);
```

**Example Usage:**
- User clicks "Check Backend Status" button
- Function được trigger
- UI updates với status message

## UI Structure

### Main Container
```javascript
<div className="App">
    <header className="App-header">
        // All content here
    </header>
</div>
```

### Header Section
- **Title:** "AI Video Editor"
- **Description:** "Merge videos with AI-generated transitions"

### Status Section
```javascript
<div className="status-section">
    <button onClick={checkBackendStatus} disabled={loading}>
        {loading ? 'Checking...' : 'Check Backend Status'}
    </button>
    {status && <p className="status-message">{status}</p>}
</div>
```

**Features:**
- Button để test backend connection
- Dynamic text: "Checking..." khi loading
- Conditional status message display
- Button disabled khi loading

### Upload Section (Placeholder)
```javascript
<div className="upload-section">
    <h2>Upload Videos</h2>
    <p>Video upload functionality will be implemented here</p>
    {/* TODO: Add video upload components */}
</div>
```

**Future Features:**
- Drag-and-drop video upload
- File validation
- Upload progress bars
- Preview thumbnails

### Processing Section (Placeholder)
```javascript
<div className="processing-section">
    <h2>Processing</h2>
    <p>Video processing controls will be implemented here</p>
    {/* TODO: Add processing controls */}
</div>
```

**Future Features:**
- Processing progress indicators
- Control buttons (start, pause, cancel)
- Real-time status updates
- Download links

## Dependencies

### Required Imports
```javascript
import React, { useState } from 'react';  // React hooks
import axios from 'axios';                // HTTP client
import './App.css';                       // Component styles
```

### External Libraries
- **React 18.2.0:** UI framework
- **Axios 1.5.0:** HTTP requests
- **CSS:** Styling

## Styling

### CSS Classes Used
- `.App`: Main container
- `.App-header`: Header section
- `.status-section`: Status check area
- `.upload-section`: Upload area
- `.processing-section`: Processing controls area
- `.status-message`: Status text styling

### Responsive Design
- Centered layout
- Mobile-friendly design
- Consistent spacing và colors

## API Integration

### Backend Endpoints Used

#### GET /api/status
**Purpose:** Health check endpoint

**URL:** `http://localhost:5000/api/status`

**Expected Response:**
```json
{
  "status": "running",
  "message": "AI Video Editor Backend is running",
  "version": "1.0.0"
}
```

**Error Handling:**
- Network errors
- Server unavailable
- Invalid responses

## User Interactions

### Button Click Flow
1. User clicks "Check Backend Status"
2. Button text changes to "Checking..."
3. Button becomes disabled
4. API request sent to backend
5. Response processed
6. Status message displayed
7. Button re-enabled với original text

### Expected User Experience
- **Success:** Green status message
- **Error:** Red error message
- **Loading:** Clear loading indicator
- **Responsive:** Immediate feedback

## Testing

### Manual Testing Steps
1. Start backend server
2. Start frontend development server
3. Open browser to http://localhost:3000
4. Verify page loads correctly
5. Click "Check Backend Status" button
6. Verify status message appears
7. Test with backend stopped (error case)

### Expected Behaviors
- **Backend Running:** "Backend Status: AI Video Editor Backend is running"
- **Backend Stopped:** "Backend connection failed"
- **Loading State:** Button shows "Checking..." và disabled

## Error Handling

### Network Errors
```javascript
catch (error) {
    setStatus('Backend connection failed');
    console.error('Error:', error);
}
```

### User Feedback
- Clear error messages
- Console logging cho debugging
- Graceful degradation

## Future Enhancements

### Planned Features
1. **File Upload:**
   - Drag-and-drop interface
   - Multiple file selection
   - File validation
   - Upload progress

2. **Video Processing:**
   - Real-time progress tracking
   - Processing controls
   - Preview functionality
   - Download management

3. **UI Improvements:**
   - Better error handling
   - Loading animations
   - Toast notifications
   - Dark mode support

### State Management Evolution
```javascript
// Future state structure
const [videos, setVideos] = useState([]);
const [processing, setProcessing] = useState(false);
const [progress, setProgress] = useState(0);
const [result, setResult] = useState(null);
```

## Component Architecture

### Current Structure
```
App (Main Component)
├── Header Section
├── Status Section
├── Upload Section (Placeholder)
└── Processing Section (Placeholder)
```

### Future Structure
```
App (Main Component)
├── Header Component
├── StatusCheck Component
├── VideoUpload Component
│   ├── DropZone Component
│   ├── FileList Component
│   └── UploadProgress Component
├── VideoProcessor Component
│   ├── ProcessingControls Component
│   ├── ProgressBar Component
│   └── PreviewPanel Component
└── ResultsPanel Component
```

## Performance Considerations
- Efficient re-rendering với React hooks
- Proper error boundaries
- Memory management cho large files
- Optimized API calls