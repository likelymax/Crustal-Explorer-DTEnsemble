# Crustal-Explorer-DTEnsemble
Ensemble-based Decision Tree algorithms for investigating crustal thickness and velocities. This project applies machine learning techniques to geophysical data, enhancing our understanding of Earth's subsurface structure

## XGBoost training testing

Welcome to this branch! This branch is dedicated to an implementation of the XGBoost model, used for estimating crustal thickness and lower crustal and upper mantle velocities.

### Structure

This branch contains:

1. Code to train the XGBoost model with your data.  
2. Testing code to estimate crustal thickness and velocities.  

### Getting Started

Before using the code, make sure to adjust the paths for your input data, the location for the output of the trained model, and the labeled values as needed.

### Input

The input to the XGBoost model should be your receiver functions, labeled with features such as crustal thickness, lower crustal velocity, and upper mantle velocity.

### Output

The output will be the trained XGBoost model saved to your specified location, as well as estimates of crustal thickness and velocities based on the testing code.

### Running the Code

Once you have adjusted the paths for input, output, and labels, you can run the training script to train the XGBoost model. After training, you can run the testing code to get estimates of crustal thickness and velocities. Check the results at your specified output location.

### Dependencies

This project requires a Unix-like environment and Python with the XGBoost library installed.

### Contact

Should you encounter any issues or have any questions, please don't hesitate to reach out. You can contact me at yitanwang@ufl.edu

### License

This code is licensed under the MIT license. Please use it responsibly.
