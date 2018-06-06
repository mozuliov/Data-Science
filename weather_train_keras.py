import pandas as pd
# import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import *

# ************* LOAD AND PREPROCESSING DATA *******************

# Load training data set from CSV file
data = pd.read_csv("weather_data_training.csv")
factors = data.iloc[:,0:12]
factors.to_csv("factors.csv")
timeline = np.asarray(factors['Datestamp'])
timeline_shifted = np.around(np.add(timeline, -.04167), 5)
timeshift = pd.DataFrame(np.stack((timeline, timeline_shifted), axis = 1), columns = ['Datestamp', 'Datestamp_shifted'])
factors_shifted = factors.merge(timeshift, left_on = 'Datestamp', right_on = 'Datestamp', how = "inner").drop(columns = ['Datestamp'])

factors_shifted.to_csv("factors_shifted.csv")

training_data_df = data.merge(factors_shifted, left_on = "Datestamp", right_on = "Datestamp_shifted", how = "inner").dropna()

training_data_df.to_csv("training_data_df.csv")

training_data_df = training_data_df.drop(columns = ['Datestamp', 'Datestamp_shifted'])

#TODO:Fix testing dataset
# Load testing data set from CSV file
data = pd.read_csv("weather_data_test.csv")
factors = data.iloc[:,0:12]
timeline = np.asarray(factors['Datestamp'])
timeline_shifted = np.around(np.add(timeline, -.04167), 5)
timeshift = pd.DataFrame(np.stack((timeline, timeline_shifted), axis = 1), columns = ['Datestamp', 'Datestamp_shifted'])
factors_shifted = factors.merge(timeshift, left_on = 'Datestamp', right_on = 'Datestamp', how = 'inner').drop(columns = ['Datestamp'])

test_data_df = data.merge(factors_shifted, left_on = "Datestamp", right_on = "Datestamp_shifted", how = "inner").dropna()
test_data_df = test_data_df.drop(columns = ['Datestamp', 'Datestamp_shifted'])

# All data needs to be scaled to a small range like 0 to 1 for the neural
# network to work well. Create scalers for the inputs and outputs.
scaler = MinMaxScaler(feature_range = (0, 1))

# Scale both the training inputs and outputs
scaled_training = scaler.fit_transform(training_data_df)
scaled_testing = scaler.transform(test_data_df)

scaled_training_df = pd.DataFrame(scaled_training, columns=training_data_df.columns.values)
scaled_testing_df = pd.DataFrame(scaled_testing, columns=test_data_df.columns.values)

scaled_training_df.to_csv("scaled_training.csv")
scaled_testing_df.to_csv("scaled_testing.csv")

# Training data for the model
X = scaled_training_df.drop(columns=['Month_y', 'Day_Quadrant_y', '0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y',
                                     '0_Wind_Dir_y', '0_Wind_Gust_y', '0_Clouds_y', '0_Rain_y', '0_Snow_y']).values
Y = scaled_training_df[['0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y', '0_Wind_Dir_y',
                                '0_Wind_Gust_y', '0_Clouds_y', '0_Rain_y', '0_Snow_y']].values
pd.DataFrame(X).to_csv("X.csv")
pd.DataFrame(Y).to_csv("Y.csv")

# Testing data for the model
X_test = scaled_testing_df.drop(columns=['Month_y', 'Day_Quadrant_y', '0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y',
                                     '0_Wind_Dir_y', '0_Wind_Gust_y', '0_Clouds_y', '0_Rain_y', '0_Snow_y']).values
Y_test = scaled_testing_df[['0_Temp_y', '0_Pressure_y', '0_Humidity_y', '0_Wind_Speed_y', '0_Wind_Dir_y',
                                '0_Wind_Gust_y', '0_Clouds_y', '0_Rain_y', '0_Snow_y']].values

# ************** NEURAL NETWORK MODEL ******************

# Create the model
model = Sequential()
model.add(Dense(400, input_dim = 83, activation = 'relu'))
model.add(Dense(800, activation = 'relu'))
model.add(Dense(400, activation = 'relu'))
model.add(Dense(9, activation = 'linear'))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')

# Train the model
model.fit(
    X,
    Y,
    epochs = 100,
    shuffle = True,
    verbose = 2
)

test_error_rate = model.evaluate(X_test, Y_test, verbose = 0)
print("MSE for the test data set is {}".format(test_error_rate))

# Save the trained model
model.save("weather_model_trained.h5")
print ("Model saved to disk")
print(scaler.scale_[83:92])
print(scaler.min_[83:92])
print ("0_Temp_y * {:.4} + {:.4}".format(scaler.scale_[85], scaler.min_[85]))
print ("0_Pressure_y * {:.4} + {:.4}".format(scaler.scale_[86], scaler.min_[86]))
print ("0_Humidity_y * {:.4} + {:.4}".format(scaler.scale_[87], scaler.min_[87]))
print ("0_Wind_Speed_y * {:.4} + {:.4}".format(scaler.scale_[88], scaler.min_[88]))
print ("0_Wind_Dir_y * {:.4} + {:.4}".format(scaler.scale_[89], scaler.min_[89]))
print ("0_Wind_Gust_y * {:.4} + {:.4}".format(scaler.scale_[90], scaler.min_[90]))
print ("0_Clouds_y * {:.4} + {:.4}".format(scaler.scale_[91], scaler.min_[91]))
print ("0_Rain_y * {:.4} + {:.4}".format(scaler.scale_[92], scaler.min_[92]))
print ("0_Snow_y * {:.4} + {:.4}".format(scaler.scale_[93], scaler.min_[93]))
scaler_param = pd.DataFrame([scaler.scale_, scaler.min_], columns = training_data_df.columns.values, index = ['Scale', 'Min'])
# scaler_param = pd.DataFrame([scaler.scale_[83:92], scaler.min_[83:92]], columns = ['Temp', 'Pressure', 'Humidity', 'Wind_Speed', 'Wind_Dir', 'Wind_Gusp', 'Clouds', 'Rain', 'Snow'])
scaler_param.to_csv("scaler_param.csv")