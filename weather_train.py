import pandas as pd
# import numpy as np
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import *

NN_version = "version 4"

# ************* LOAD AND PREPROCESSING DATA *******************

# Load training data set from CSV file
data = pd.read_csv("wu_weather.csv")
target = data.iloc[:,0:13]
target.to_csv("target.csv")
timeline = np.asarray(target['Datestamp'])
timeline_shifted = np.around(np.add(timeline, -.04167), 5)
timeshift = pd.DataFrame(np.stack((timeline, timeline_shifted), axis = 1), columns = ['Datestamp', 'Datestamp_shifted'])
target_shifted = target.merge(timeshift, left_on = 'Datestamp', right_on = 'Datestamp', how = "inner").drop(columns = ['Datestamp'])

target_shifted.to_csv("target_shifted.csv")

training_df = data.merge(target_shifted, left_on = "Datestamp", right_on = "Datestamp_shifted", how = "inner").dropna()

training_df.to_csv("training_df.csv")

training_df = training_df.drop(columns = ['Datestamp', 'Datestamp_shifted'])

# Load testing data set from CSV file
data = pd.read_csv("wu_test.csv")
target = data.iloc[:,0:13]
timeline = np.asarray(target['Datestamp'])
timeline_shifted = np.around(np.add(timeline, -.04167), 5)
timeshift = pd.DataFrame(np.stack((timeline, timeline_shifted), axis = 1), columns = ['Datestamp', 'Datestamp_shifted'])
target_shifted = target.merge(timeshift, left_on = 'Datestamp', right_on = 'Datestamp', how = 'inner').drop(columns = ['Datestamp'])

test_df = data.merge(target_shifted, left_on = "Datestamp", right_on = "Datestamp_shifted", how = "inner").dropna()
test_df = test_df.drop(columns = ['Datestamp', 'Datestamp_shifted'])

# All data needs to be scaled to a small range like 0 to 1 for the neural
# network to work well. Create scalers for the inputs and outputs.
scaler = MinMaxScaler(feature_range = (0, 1))

# Scale both the training inputs and outputs
scaled_training = scaler.fit_transform(training_df)
scaled_testing = scaler.transform(test_df)

scaled_training_df = pd.DataFrame(scaled_training, columns=training_df.columns.values)
scaled_testing_df = pd.DataFrame(scaled_testing, columns=test_df.columns.values)

scaled_training_df.to_csv("training_scaled.csv")
scaled_testing_df.to_csv("testing_scaled.csv")

# Training data for the model
X = scaled_training_df.drop(columns=['Month_y', 'Moonlight_y', 'Moon_phase_y', '0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y',
                                     '0_Wind_Dir_y', '0_Wind_Gust_y', '0_UV_y', '0_Precipitation_y', '0_Dew_point_y']).values
Y = scaled_training_df[['0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y', '0_Wind_Dir_y',
                                '0_Wind_Gust_y', '0_UV_y', '0_Precipitation_y', '0_Dew_point_y']].values
pd.DataFrame(X).to_csv("wu_X.csv")
pd.DataFrame(Y).to_csv("wu_Y.csv")

# Testing data for the model
X_test = scaled_testing_df.drop(columns=['Month_y', 'Moonlight_y', 'Moon_phase_y', '0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y',
                                     '0_Wind_Dir_y', '0_Wind_Gust_y', '0_UV_y', '0_Precipitation_y', '0_Dew_point_y']).values
Y_test = scaled_testing_df[['0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y', '0_Wind_Dir_y',
                                '0_Wind_Gust_y', '0_UV_y', '0_Precipitation_y', '0_Dew_point_y']].values

# ************** NEURAL NETWORK MODEL ******************

# Define the model
model = Sequential()
model.add(Dense(50, input_dim = 84, activation = 'relu', name = 'layer_1'))
model.add(Dense(1600, activation = 'relu', name = 'layer_2'))
model.add(Dense(1600, activation = 'relu', name = 'layer_3'))
model.add(Dense(120, activation = 'relu', name = 'layer_4'))
model.add(Dense(9, activation = 'linear', name = 'output_layer'))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')

# Create a TesnsorBoard logger
logger = keras.callbacks.TensorBoard(
    log_dir = "logs\{Version}".format(Version = NN_version),
    write_graph = True
)

# Train the model
model.fit(
    X,
    Y,
    epochs = 100,
    shuffle = True,
    verbose = 2,
    callbacks = [logger]
)

test_error_rate = model.evaluate(X_test, Y_test, verbose = 0)
print("MSE for the test data set is {}".format(test_error_rate))

# Save the trained model
model.save("wu_weather_model.h5")
print ("Model saved to disk")
print('==================================================')
print('Normalizing coefficients:')
print(scaler.scale_[87:96])
print(scaler.min_[87:96])
print ("0_Temp_y * {:.4} + {:.4}".format(scaler.scale_[87], scaler.min_[87]))
print ("0_Pressure_y * {:.4} + {:.4}".format(scaler.scale_[88], scaler.min_[88]))
print ("0_Humidity_y * {:.4} + {:.4}".format(scaler.scale_[89], scaler.min_[89]))
print ("0_Wind_Speed_y * {:.4} + {:.4}".format(scaler.scale_[90], scaler.min_[90]))
print ("0_Wind_Dir_y * {:.4} + {:.4}".format(scaler.scale_[91], scaler.min_[91]))
print ("0_Wind_Gust_y * {:.4} + {:.4}".format(scaler.scale_[92], scaler.min_[92]))
print ("0_UV_y * {:.4} + {:.4}".format(scaler.scale_[93], scaler.min_[93]))
print ("0_Precipitation_y * {:.4} + {:.4}".format(scaler.scale_[94], scaler.min_[94]))
print ("0_Dew_point_y * {:.4} + {:.4}".format(scaler.scale_[95], scaler.min_[95]))
scaler_param = pd.DataFrame([scaler.scale_, scaler.min_], columns = training_df.columns.values, index = ['Scale', 'Min'])
scaler_param.to_csv("wu_model_scaler_param.csv")   # Save for further use to rescale results