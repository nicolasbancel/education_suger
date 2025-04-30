# Auto-Correct Tool

This project is designed to automatically correct exams and exercises for students by processing images of book pages containing exercises. The tool crops the specified exercise area and generates a LaTeX document that includes a screenshot of the exercise along with the associated corrections.

## Project Structure

```
auto-correct-tool
├── src
│   ├── main.py                # Entry point of the application
│   ├── utils
│   │   ├── image_processing.py # Functions for image loading and cropping
│   │   ├── latex_generator.py   # Functions for LaTeX document generation
│   │   └── correction_logic.py   # Logic for automatic correction
│   └── models
│       └── __init__.py        # Initialization of models package
├── data
│   ├── input                  # Directory for input files (images)
│   └── output                 # Directory for output files (LaTeX documents)
├── tests
│   ├── test_image_processing.py # Unit tests for image processing functions
│   ├── test_latex_generator.py   # Unit tests for LaTeX generation functions
│   └── test_correction_logic.py   # Unit tests for correction logic functions
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Files and directories to ignore in version control
```

## Setup Instructions

1. **Clone the Repository**
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**
   Change into the project directory:
   ```
   cd auto-correct-tool
   ```

3. **Install Dependencies**
   Install the required Python packages listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

4. **Prepare Input Data**
   Place the images of book pages containing exercises in the `data/input` directory.

5. **Run the Application**
   Execute the main script to start the application:
   ```
   python src/main.py
   ```

## Usage

- The tool will load the specified book page, crop the exercise, and generate a LaTeX document with the exercise image and corrections.
- The generated LaTeX documents will be saved in the `data/output` directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.