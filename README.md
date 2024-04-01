# Snarky-ML-Frontend
This project is the frontend of snarky-ml library. The current version integrates a decision tree classifier with Zero-Knowledge proofs using `o1js` from the Mina Protocol, enabling the private and verifiable prediction of classification results based on the decision tree model. This README provides an overview of the project, highlighting its core functionalities, current progress, and how to set up and test the system.

## Project Highlights

- **Decision Tree Classifier**: Utilizes a decision tree algorithm for classification tasks, making it suitable for a range of predictive modeling scenarios.
- **Zero-Knowledge Proofs with `o1js`**: Incorporates Zero-Knowledge proofs via `o1js`, ensuring that predictions can be made and verified without revealing the input data, preserving user privacy.
- **Mina Protocol Integration**: Leverages the lightweight and secure blockchain environment provided by the Mina Protocol for deploying and verifying Zero-Knowledge smart contracts.
- **Interactive Web Interface**: Features a user-friendly web interface allowing users to input data for prediction, submit it for Zero-Knowledge proof generation, and receive verifiable results.

## Current Progress

-[x] The decision tree model is implemented and capable of making predictions.

-[x] The backend (`app.py`) integrates with `o1js` to define ZK circuits for a simplified model prediction, showcasing the concept of private and verifiable computations.

-[x] A frontend (`index.html`) is provided, offering an interface for inputting data, initiating predictions, and displaying results with verification status.

-[] Preliminary integration of the decision tree model with Zero-Knowledge proof generation and verification is in place, demonstrating the feasibility of the approach.

## Setup and Testing

### Prerequisites

- [Python](https://www.python.org/): Version 3.7 or higher, required for the Flask backend. You can install all the requirements libraries with `pip install -r requirements.txt`, or install them one by one with the following script.
- Flask: Install using pip: `pip install Flask`
- Additional Python libraries: `numpy`, `pandas`, `scikit-learn`, `matplotlib`. Install these using pip: `pip install numpy pandas scikit-learn matplotlib`

### Running the Project

1. **Clone the Repository**: Clone this repository to your local machine and navigate to the project directory.
2. **Run the Flask Backend**:
   - Navigate to the directory containing `app.py`.
   - Run `python app.py` to start the Flask server.
3. **Access the Web Interface**: Open a web browser and go to `http://localhost:5000`. You should see the project's web interface.

### Testing the System

1. **Input Prediction Data**: Use the web interface to input data for prediction. The current setup assumes simplified input fields for demonstration purposes. Adjust these fields according to your decision tree model's requirements. The demo already included the iris dataset.
2. **Submit for Prediction**: Click the "Submit Prediction" button. This sends the input data to the backend, where a Zero-Knowledge proof for the prediction is generated and verified.
3. **View Results**: The prediction result and verification status will be displayed on the web interface.

## Examples

Due to the project's experimental nature and the complexity of integrating decision tree models with `o1js`, specific examples are provided in the form of commented code blocks in both the frontend and backend implementations. These examples illustrate the process of defining ZK circuits for model predictions, compiling these circuits, and interacting with them via the web interface.

## Conclusion and Next Steps

This project represents an initial exploration into combining machine learning models with Zero-Knowledge proofs for private and verifiable predictions. Future work may include:

- Compile and execute `o1js` files using the frontend.
- Enhancing the decision tree model's integration with `o1js` for more complex and realistic use cases.
- Improving the efficiency and scalability of Zero-Knowledge proof generation and verification.
- Extending the web interface for more interactive and user-friendly experiences.
- Exploring additional machine learning models and their potential applications in a Zero-Knowledge proof context.