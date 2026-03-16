# AI Study Planner 🚀

[![GitHub forks](https://img.shields.io/github/forks/govindchauhan45/AI-study-planner?style=social)](https://github.com/govindchauhan45/AI-study-planner)

[![GitHub issues](https://img.shields.io/github/issues/govindchauhan45/AI-study-planner)](https://github.com/govindchauhan45/AI-study-planner/issues)

[![License](https://img.shields.io/github/license/govindchauhan45/AI-study-planner)](https://github.com/govindchauhan45/AI-study-planner/blob/main/LICENSE)

✨ **AI Study Planner** is your personal AI-powered study assistant, designed to help you create optimized study schedules and maximize your learning efficiency. ✨

## Introduction 💡

Are you struggling to manage your study time effectively? Do you find it difficult to prioritize topics and create a balanced study plan?  AI Study Planner solves these problems by leveraging the power of large language models to generate personalized study plans based on your input.  This project is designed for students of all levels who want to improve their study habits and achieve better academic results.

## Features 🌟

*   **Personalized Study Plans:** Generate a study plan tailored to your subjects, exam dates, and available time.
*   **Topic Prioritization:**  AI intelligently prioritizes topics based on their importance and your current understanding.
*   **Time Management:** Breaks down study sessions into manageable chunks with suggested durations.
*   **Flask Backend:** Robust backend built with Flask for handling requests and interacting with the AI model.
*   **Frontend Interface:** User-friendly interface for inputting study details.
*   **OpenRouter Integration:** Integrates with OpenRouter for accessing powerful language models.
*   **Cross-Origin Resource Sharing (CORS):** Enabled for seamless communication between frontend and backend.
* **Simple and clean design** Easy to use and understand.

## Installation ⚙️

Before running the project, make sure you have Python installed (version 3.7 or higher).

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/govindchauhan15/AI-study-planner.git
    cd AI-study-planner
    ```

2.  **Create a `.env` file:**  In the project's root directory, create a file named `.env` and add your OpenRouter API key:

    ```
    OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
    OPENROUTER_MODEL=optional-model-name  # e.g., "openai/gpt-3.5-turbo"
    ```

    **Note:** Replace `YOUR_OPENROUTER_API_KEY` with your actual OpenRouter API key. You can get an API key from [OpenRouter](https://openrouter.ai/).

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage 🚀

1.  **Run the Backend:**
    ```bash
    cd backend
    python app.py
    ```
    This will start the Flask server, typically on `http://127.0.0.1:5000/`.

2.  **Run the Frontend:**
    Open the `frontend/index.html` file in your web browser.

3. **Interact with the Interface:**
   Fill the form on the frontend with your subjects, exam dates, and study preferences.

4.  **Get Your Study Plan:**
    Submit the form, and the AI Study Planner will generate a personalized study plan. <br>
    You can even redirect to a specific link that shows the study plan.

## Contributing 🤝

We welcome contributions from the community!  Here's how you can contribute:

*   **Fork the repository.**
*   **Create a new branch** for your feature or bug fix.
*   **Make your changes** and commit them with descriptive messages.
*   **Submit a pull request** to the `main` branch.

Please ensure your code follows the project's existing style and that you've added tests for any new functionality.

**Looking for good first issues?** Check out the [Issues tab](https://github.com/govindchauhan45/AI-study-planner/issues) for tasks labeled "good first issue".

## License 📝

This project is licensed under the [MIT License](https://github.com/govindchauhan45/AI-study-planner/blob/main/LICENSE) - see the [LICENSE](https://github.com/govindchauhan45/AI-study-planner/blob/main/LICENSE) file for details.

Let's build the ultimate AI Study Planner together! 🌟

---
🔗 GitHub Repo: https://github.com/govindchauhan45/AI-study-planner