# Running the Reporting Agent Locally

This guide explains how to run the Reporting Agent application locally using Docker, without needing to manually build the frontend or install Python dependencies on your host machine.

## Prerequisites

1.  **Docker:** Ensure [Docker](https://www.docker.com/products/docker-desktop/) is installed and running on your machine.

## Steps to Run

1.  **Clone/Copy the project:** Ensure you have the entire project folder on your machine.

2.  **Build the Container Image:**
    Open your terminal, navigate to the root directory of the project, and run:
    ```bash
    docker build -t reporting-agent .
    ```
    *This step will automatically build the React frontend and configure the Python backend inside the container.*

3.  **Run the Container:**
    After the build finishes, run the container with:
    ```bash
    docker run -p 8001:8001 reporting-agent
    ```

4.  **Access the Application:**
    Once the container is running, open your web browser and go to:
    [http://localhost:8001](http://localhost:8001)

## Troubleshooting
- **Build Errors:** Ensure Docker has enough resources allocated (e.g., in Docker Desktop settings).
- **Port Conflicts:** If `8001` is already in use on your machine, you can change the host port in step 3: `docker run -p 9000:8001 reporting-agent` (then access `http://localhost:9000`).
