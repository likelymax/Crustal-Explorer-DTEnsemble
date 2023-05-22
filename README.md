# Crustal-Explorer-DTEnsemble
Ensemble-based Decision Tree algorithms for investigating crustal thickness and velocities. This project applies machine learning techniques to geophysical data, enhancing our understanding of Earth's subsurface structure

## RF-training-synthetic

Welcome to this branch! Here, I provide a Random Forest model training for crustal thickness prediction. This model leverages receiver function data in ASCII format. The labeled features for the receiver functions can be Moho depth, lower crustal, or upper mantle vp.

### Structure

The branch primarily contains a single code file that trains the Random Forest model with your data. It also provides an example of testing data based on an offset structure.

### Getting Started

Before you run the code, ensure to adjust paths for the input data, the output location for the trained model, and the labeled values accordingly.

### Input 

The input should be receiver functions in ASCII format. They should be labeled with features such as Moho depth, lower crustal, or upper mantle vp.

### Output

The output of the model is the trained Random Forest model stored at your specified output location.

### Example

An example of testing process for an offset structure is provided in the branch for your reference.

### Running the Code

After adjusting the input, output, and label paths, run the script to train the model. Check the results at your specified output location.

### Dependencies

This project requires a Unix-like system with a Python compiler, depending on the language the code is written in.

### Contact

Please feel free to reach out if you encounter any issues or have questions. You can reach me via email at yitanwang@ufl.edu

### License

This code is licensed under the MIT license. Please use it responsibly.
