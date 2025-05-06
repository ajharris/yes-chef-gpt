# YesChefGPT

YesChefGPT is an AI-powered cooking assistant designed to make cooking easier and more enjoyable. Forget about last-minute grocery runs or struggling to figure out what to cook with the ingredients you have. YesChefGPT helps you create recipes based on what’s already in your kitchen and your food preferences.

## Features
- **Ingredient-Based Recipe Generation**: Input the ingredients you have, and YesChefGPT will generate recipes tailored to your pantry.
- **AI-Powered Suggestions**: Uses modern AI to provide seamless and voice-friendly recipe suggestions.
- **User-Friendly Interface**: Designed to be intuitive and accessible for all users.

## Project Structure
The project is divided into two main parts:

### Backend
- Built with Python and Flask.
- Handles API requests and integrates with AI models for recipe generation.
- Key files and directories:
  - `routes/`: Contains route handlers for authentication, recipe generation, and more.
  - `models.py`: Defines the data models.
  - `config.py`: Configuration settings for the application.

### Frontend
- Built with React and TypeScript.
- Provides a user-friendly interface for interacting with the AI assistant.
- Key files and directories:
  - `app/`: Contains the main application layout and pages.
  - `components/`: Reusable UI components.
  - `assets/`: Fonts and images used in the application.

## Installation

### Prerequisites
- Node.js and npm
- Python 3.8+
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/yes-chef-gpt.git
   cd yes-chef-gpt
   ```
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```
4. Start the development servers:
   - Backend:
     ```bash
     cd backend
     flask run
     ```
   - Frontend:
     ```bash
     cd frontend
     npm start
     ```

## Usage
1. Open the frontend in your browser (usually at `http://localhost:3000`).
2. Enter the ingredients you have and your food preferences.
3. Get AI-generated recipes and start cooking!

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
Spurred on to development by Allen R. Wazny’s [Medium article](https://medium.com/@allenwazny/creative-content-part-iii-a-recipe-to-code-1daf83f3fb17) on solving pantry puzzles. YesChefGPT takes a modern AI approach to make cooking seamless and enjoyable.