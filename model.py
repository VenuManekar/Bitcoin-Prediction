import pandas as pd, numpy as np, matplotlib.pyplot as plt
import os

from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.models import Sequential



def predict_price():
    data_final = pd.read_csv('train.csv')
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data_final['close'].values.reshape(-1,1))
    time_intervals_to_train = 24
    prediction_interval = 12

    x_train = []
    y_train = []

    for i in range(time_intervals_to_train, len(scaled_data) - prediction_interval):
        x_train.append(scaled_data[i - time_intervals_to_train: i, 0])
        y_train.append(scaled_data[i + prediction_interval, 0])

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()

    model.add(LSTM(128, return_sequences= True, input_shape = (x_train.shape[1], 1), activation = 'relu'))
    model.add(Dropout(0.4))
    model.add(LSTM(64, return_sequences= True, activation = 'relu'))
    model.add(Dropout(0.3))
    model.add(LSTM(32, activation= 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation = 'sigmoid'))

    model.compile(loss = 'mean_squared_error', optimizer= 'adam', metrics= ['accuracy'])

    model.fit(x_train, y_train, epochs=4, batch_size= 64)

    test_data_final = pd.read_csv('test.csv')
    bitcoin_prices = pd.to_numeric(test_data_final['close'], errors = 'coerce').values

    test_inputs = test_data_final['close'].values
    test_inputs = test_inputs.reshape(-1,1)
    model_inputs = scaler.fit_transform(test_inputs)

    x_test = []

    for x in range(time_intervals_to_train, len(model_inputs)):
        x_test.append(model_inputs[x - time_intervals_to_train:x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)


    plt.clf()
    plt.plot(bitcoin_prices, label = 'Bitcoin Prices')
    plt.plot(prediction_prices, label = 'Predicted Prices')
    plt.title('Predicting Bitcoin Price')
    plt.xlabel('5min Time interval')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(r'static\graph.jpg')



    last_data = model_inputs[len(model_inputs) - time_intervals_to_train : len(model_inputs) +1, 0]
    last_data = np.array(last_data)
    last_data = np.reshape(last_data, (1, -1, 1))
    prediction = model.predict(last_data)
    prediction = scaler.inverse_transform(prediction)

    return prediction

predict_price()