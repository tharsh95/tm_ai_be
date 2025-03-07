# Taskym - Task Management Application

A full-stack task management application with FastAPI backend and React frontend.

## Docker Setup

### Docker Compose Configuration
```yaml
version: '3'

services:
  client:
    build:
      context: ./client
    image: tharsh95/taskym-client:latest
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000

  server:
    build:
      context: ./server
    image: tharsh95/taskym-server:latest
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - DATABASE_NAME=taskym
      - JWT_SECRET=your-super-secret-key-here-replace-in-production
      - JWT_ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=90
      - OPENAI_API_KEY=your-openai-api-key

  mongodb:
    build:
      context: ./mongodb
    image: tharsh95/taskym-mongodb:latest
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"

volumes:
  mongodb_data:
```

## Getting Started

### Running the Application

1. Make sure you have Docker and Docker Compose installed
3. Run the following command by creating a docker-compose.yml and pasting the above yml file :
```bash
docker compose up 
```

### Accessing the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Application Flow

### 1. User Registration & Authentication
- Navigate to http://localhost:5173
- Click "Register" to create a new account
- Provide email and password
- After registration, you'll be redirected to login
- Login with your credentials

### 2. Dashboard
After successful login, you'll see the main dashboard with:
- Header with search functionality and user menu
- Project information section
- Four task columns:
  - To Do
  - In Progress
  - Closed
  - Frozen

### 3. Task Management
#### Creating Tasks
- Click "+" in todo column
- Fill in task details:
  - Title
  - Description
  - Priority (Low/Medium/High)
  - Add Participants
  - Brief (AI-generated task summary)

#### Managing Tasks
- **View**: Click on any task to see details
- **Edit**: Click edit icon to modify task details
- **Delete**: Remove tasks using delete icon
- **Status Change**: Update task status from task modal

### 4. Search Functionality
- Use the search bar in the header
- Real-time filtering of tasks across all columns
- Search by task title & status

### 5. User Features
- Logout functionality

### 6. AI Integration
- Automatic task description generation
- Smart task descriptions
- Priority suggestions

## Security Features
- JWT-based authentication
- Secure password hashing
- Protected API endpoints
- Environment variable configuration

## Additional Features
- Responsive design for mobile and desktop
- Real-time updates
- Persistent data storage with MongoDB
- OpenAI integration for task enhancement 