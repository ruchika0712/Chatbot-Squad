**README.md - Setting Up and Running the Application**

Description of your project goes here.

### Prerequisites

- Python 3.x installed on your system.
- pip package manager (usually comes with Python installations).

### Getting Started

Follow the steps below to set up and run the application locally.

1. **Create a Virtual Environment**

   Open your command prompt or terminal and navigate to the project directory. Run the following command to create a virtual environment:

   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment to ensure your project uses the isolated environment. Depending on your operating system, use one of the following commands:

   For Windows:

   ```
   venv\Scripts\activate
   ```

   For macOS and Linux:

   ```
   source venv/bin/activate
   ```

3. **Install Requirements**

   With the virtual environment activated, install the required dependencies listed in the `requirements.txt` file using pip. Run the following command:

   ```
   pip install -r requirements.txt
   ```

   This will download and install all the necessary packages for the application.

4. **Start the Application**

   Once the requirements are installed, you can start the application. In the command prompt or terminal, run the following command:

   ```
   python ./app.py
   ```

   The Flask application will now be running locally.

5. **Access the Application**

   Open your web browser and go to `http://127.0.0.1:5000/` or `http://localhost:5000/` to access the Flask application. You should see the homepage or any other routes you have defined in your Flask app.

6. **Stopping the Application**

   To stop the Flask application, go back to the command prompt or terminal where the app is running and press `Ctrl + C`. This will terminate the development server.
