# Akshara Annotation Platform

Akshara Annotation Platform is a hybrid web application designed for audio transcription and annotation workflows. It provides role-based access for Admins, Reviewers, and Annotators, allowing teams to upload datasets, transcribe audio, annotate specific segments, and review the work before exporting the finalized annotations.

## Basic Functionality

- **Role-Based Workflows**:
  - **Admin**: Has an overview of platform analytics, dataset management, and user management. Can upload ZIP datasets containing audio and transcript files, monitor progress, and export finalized annotation packages.
  - **Annotator**: Can claim annotation tasks from a queue, listen to audio files, view/edit the transcript, and submit their work for review.
  - **Reviewer**: Can review submitted tasks from annotators, leave comments, and approve or return tasks for rework.

- **Audio & Transcript Synchronization**: The platform displays a dynamic waveform for precise audio navigation alongside the text transcript.
- **RSML (Rich Semantic Markup Language) Support**: Allows annotators to tag named entities and segments within the transcript.
- **Cloudinary Integration**: Supports uploading large audio files to Cloudinary for robust storage and streaming.
- **Exporting**: Approved tasks can be exported as a ZIP containing the original audio, the original transcript, and the final RSML annotation file.

## Architecture

The platform uses a modern hybrid architecture:
- **Backend**: FastAPI (Python) serving a RESTful API and handling database operations using SQLAlchemy.
- **Frontend**: React (TypeScript) built with Vite, utilizing React Query for state management and React Router for navigation.
- **Database**: SQLite (for local development).

## Local Setup Walkthrough

### Prerequisites
- Python 3.9+
- Node.js (v16+) and npm
- A Cloudinary account (for audio storage)

### 1. Clone the repository
```bash
git clone https://github.com/ParthaKesavReddyChundi/Akshara-Annotation-Platform.git
cd Akshara-Annotation-Platform
```

### 2. Backend Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory and add your Cloudinary credentials and JWT secret:
   ```env
   CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@<your_cloud_name>
   JWT_SECRET=your_jwt_secret_key_here
   ```
3. Run the database initialization script (if necessary) to set up tables and default admin users:
   ```bash
   python -m streamlit_app.database.init_db
   ```
4. Start the FastAPI backend server:
   ```bash
   # Make sure PYTHONPATH includes streamlit_app for module resolution
   $env:PYTHONPATH="streamlit_app"
   uvicorn backend.main:app --reload --port 8000
   ```
   The API will be running at `http://localhost:8000`.

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```
3. Ensure the frontend is pointing to the correct API URL (usually `http://localhost:8000/api`). This is configured in `frontend/src/services/api.ts` or via a `.env.local` file in the frontend folder containing `VITE_API_URL=http://localhost:8000`.
4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173`.

### 4. Logging In
- Navigate to the frontend URL in your browser.
- Log in with the default Super Admin credentials created during database initialization (usually `admin` / `admin`).
- You can now start creating users and uploading datasets!
