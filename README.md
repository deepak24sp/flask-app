# Flask Application

This is a simple Flask application that serves as a starting point for building web applications using the Flask framework.

## Project Structure

```
flask-app
├── app.py                # Main entry point of the Flask application
├── requirements.txt      # Python dependencies required for the project
├── Dockerfile            # Instructions to build a Docker image for the application
├── setup.sh              # Script for setting up AWS infrastructure
├── test_local.py         # Scripts for local testing of the application
├── deploy_manual.sh      # Script for manual deployment of the application
├── .github
│   └── workflows
│       └── deploy.yml    # GitHub Actions workflow for CI/CD
├── .gitignore            # Files and directories to be ignored by Git
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-app
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python app.py
   ```

4. **Run tests:**
   ```
   python test_local.py
   ```

5. **Deploy the application:**
   - For manual deployment, run:
     ```
     ./deploy_manual.sh
     ```

## Usage

- Access the application in your web browser at `http://localhost:5000`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.