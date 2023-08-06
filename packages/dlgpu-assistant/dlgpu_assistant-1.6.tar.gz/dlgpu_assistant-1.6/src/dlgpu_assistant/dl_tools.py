import logging
import os
import sys
import tensorflow
import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn import compose


class DlAssistant:
    """
    The "DlAssistant" module has two functions:
        - tf_warnings: It permits to avoid the tensorflow warnings
        - find_gpu: It returns if your GPU has been found or not. In case your GPU is not available, the program is
        shut down.
    """

    def tf_warnings(self):
        # With this setting we can avoid to see the uncomfortable tensorflow messages
        # 0 = all messages are logged (default behavior)
        # 1 = INFO messages are not printed
        # 2 = INFO and WARNING messages are not printed
        # 3 = INFO, WARNING, and ERROR messages are not printed
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        return os.environ['TF_CPP_MIN_LOG_LEVEL']

    def find_gpu(self):
        # Check if the GPU has been found
        print("You are using TensorFlow version", tensorflow.__version__)
        gpus_available = len(tensorflow.config.list_physical_devices("GPU"))
        if gpus_available != 0:
            print("{0} GPU available\n".format(gpus_available))
        else:
            print("None GPUS available. Killing Program ...")
            sys.exit()  # If there is no GPU available we can not continue. We don't want to run our training process on CPU


class DlTools:
    """
    The "DlTools" module has two functions:
        - data_preprocessing: It returns x and y data ready for being used in the ANN. This function applied Label Encoder
        and One Hot Encoder to the features that the user gives to it.
        Parameters -> (dataset, features, label, label_encoder_list, one_hot_encoded_list)
            dataset (directory string): It must be in ".csv" format
            features (array of strings): The columns for the x data
            label (array of strings): The objective variable to predict
            label_encoder_bool (bool): Label Encoder is necessary or not
            label_encoder_list (array of strings): Label Encoder for specific columns
            one_hot_encoded_bool (bool): One-Hot Encoder is necessary or not
            one_hot_encoded_list (array of strings): One-Hot Encoder for specific columns
        - model_structure: It automates the process of create the layers of the ANN.
        Parameters -> (model, x, y, hidden_layers, neurons_hidden_layer, hidden_layer_af, output_layer_af)
            model: The object to be adjusted
            x and y: It needs to know the length of the data
            models_dir (str): Directory where the models will be saved
            hidden_layers (int): Number of Hidden Layers
            neurons_hidden_layer (array of strings): Number per Hidden Layer
            hidden_layer_af (string): Hidden Layer activation function
            output_layer_af (string): Output Layer activation function
    """

    def data_preprocessing(self, dataset, features, label, label_encoder_bool, label_encoder_list, one_hot_encoded_bool, one_hot_encoded_list):
        df = pd.read_csv(dataset).fillna(0)

        if label_encoder_bool:
            for i in label_encoder_list:
                df[i] = preprocessing.LabelEncoder().fit_transform(df[i])

        x = df[features].values

        if one_hot_encoded_bool:
            one_hot_list = [features.index(i) for i in one_hot_encoded_list]
            ct = compose.ColumnTransformer(transformers=[("encoder", preprocessing.OneHotEncoder(), one_hot_list)],
                                           remainder="passthrough")
            x = np.array(ct.fit_transform(x))

        y = df[label].values  # Labels
        return x, y

    def model_structure(self, model, x, y, models_dir, hidden_layers, neurons_hidden_layer, hidden_layer_af, output_layer_af):
        model.add(tensorflow.keras.layers.InputLayer(input_shape=len(x[0]), name="Input_Layer"))
        for i in range(0, hidden_layers):
            model.add(tensorflow.keras.layers.Dense(int(neurons_hidden_layer[i]), activation=hidden_layer_af, name=("Hidden_Layer_" + str(i + 1))))
        model.add(tensorflow.keras.layers.Dense(len(y[0]), activation=output_layer_af, name="Output_Layer"))

        if not os.path.exists(models_dir):
            os.mkdir(models_dir)

        return model


class DlLogger:
    """
    The "DlLogger" module has one functions:
        - logger_metrics: It creates a file where is registered the structure of the ANN with its results.
        Parameters -> (file_name, dataset, history, hidden_layers, neurons_per_hidden_layer, hidden_layer_af, output_layer_af,
                       optimizer, loss, metrics, batch_size, epochs, verbose)
            file_name: String variable with the name of the resultant file
            dataset (directory string): The name of the file that contain the data
            history: Data from the training process
            models_names: The name of the saved model
            hidden_layers (int): Number of Hidden Layers
            neurons_hidden_layer (array of strings): Number per Hidden Layer
            hidden_layer_af (string): Hidden Layer activation function
            output_layer_af (string): Output Layer activation function
            optimizer: The optimizer that is being used
            loss (int): The Loss value
            metrics: The metrics that are being used
            batch_size: The batch size of the model
            epochs: The number of epochs
            verbose: Yes or No has been used
    """

    def logger_metrics(self, file_name, dataset, history, model_name, hidden_layers, neurons_per_hidden_layer,
                       hidden_layer_af, output_layer_af, optimizer, loss, metrics, batch_size, epochs, verbose):
        # Save the minimum loss and the maximum accuracy values with its index
        loss_min, acc_max = [max(history["loss"]), 0], [0, 0]
        for i in range(0, len(history["loss"])):
            if loss_min[0] > history["loss"][i]:
                loss_min = [history["loss"][i], i]
            if acc_max[0] < history["accuracy"][i]:
                acc_max = [history["accuracy"][i], i]

        # Save the training results to the logger
        logging.basicConfig(filename=file_name,
                            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                            filemode="a")  # w -> overwrite  a -> append
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.debug("Model name: " + model_name)
        logger.debug("Dataset: " + dataset)
        logger.debug("Structure: " +
                     "Hidden Layers -> " + str(hidden_layers) +
                     " / Neurons per Hidden Layer -> " + ", ".join(neurons_per_hidden_layer) +
                     " / Hidden Layer Activation Function -> " + hidden_layer_af +
                     " / Output Layer Activation Function -> " + output_layer_af)
        logger.debug("Compile: " + " Optimizer -> " + optimizer + " / Loss Function -> " + loss + " / Metrics -> " + ", ".join(metrics))
        logger.debug("Training: " + " Batch Size -> " + str(batch_size) + " / Epochs -> " + str(epochs) + " / Verbose -> " + str(verbose))
        logger.debug("Minimum Loss -> " + str(round(loss_min[0], 3)) + " epoch " + str(loss_min[1]) + " / Maximum Accuracy -> " + str(round(acc_max[0], 3)) + " epoch " + str(acc_max[1]))
        logger.debug("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Metrics has been saved")
