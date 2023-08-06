from pandas import DataFrame
from pandas import concat
from numpy import array,hstack
from keras.models import Sequential
from keras.layers import LSTM , Dense , Bidirectional,TimeDistributed,Flatten,ConvLSTM2D,RepeatVector
from keras.layers.convolutional import Conv1D,MaxPooling1D
from keras.models import Model
from keras.layers import Input
from keras.layers import concatenate
def UVL(train_list,pred_list):
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
 
    raw_seq = train_list
    n_steps = 3
    X, y = split_sequence(raw_seq, n_steps)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=200, verbose=0)
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def USL(train_list,pred_list):
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
 
    raw_seq = train_list
    n_steps = 3
    X, y = split_sequence(raw_seq, n_steps)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=200, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def UBL(train_list,pred_list): 
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
 
    raw_seq = train_list
    n_steps = 3
    X, y = split_sequence(raw_seq, n_steps)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=200, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def UCNNL(train_list,pred_list):
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
 
    raw_seq = train_list
    n_steps = 4
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    # reshape from [samples, timesteps] into [samples, subsequences, timesteps, features]
    n_features = 1
    n_seq = 2
    n_steps = 2
    X = X.reshape((X.shape[0], n_seq, n_steps, n_features))
    # define model
    model = Sequential()
    model.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation='relu'), input_shape=(None, n_steps, n_features)))
    model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model.add(TimeDistributed(Flatten()))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=500, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_seq, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def UCONVL(train_list,pred_list):
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
 
    raw_seq = train_list
    n_steps = 4
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    # reshape from [samples, timesteps] into [samples, timesteps, rows, columns, features]
    n_features = 1
    n_seq = 2
    n_steps = 2
    X = X.reshape((X.shape[0], n_seq, 1, n_steps, n_features))
    # define model
    model = Sequential()
    model.add(ConvLSTM2D(filters=64, kernel_size=(1,2), activation='relu', input_shape=(n_seq, 1, n_steps, n_features)))
    model.add(Flatten())
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=500, verbose=0)
    # demonstrate prediction
    x_input = array([60, 70, 80, 90])
    x_input = x_input.reshape((1, n_seq, 1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def MIS(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences):
                break
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = X.shape[2]
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=200, verbose=0)
    x_input = array([pred_list1,pred_list2,pred_list3])
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def MPS(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences)-1:
                break
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = X.shape[2]
    model = Sequential()
    model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(100, activation='relu'))
    model.add(Dense(n_features))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=400, verbose=0)
    x_input = array([pred_list1, pred_list2,pred_list3])
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def VOM (train_list,pred_list):
    def split_sequence(sequence, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the sequence
            if out_end_ix > len(sequence):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
     
    # define input sequence
    raw_seq = train_list
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # split into samples
    X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    # define model
    model = Sequential()
    model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
    model.add(LSTM(100, activation='relu'))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=100, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def EDM (train_list,pred_list):
    def split_sequence(sequence, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the sequence
            if out_end_ix > len(sequence):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
     
    # define input sequence
    raw_seq = train_list
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # split into samples
    X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    y = y.reshape((y.shape[0], y.shape[1], n_features))
    # define model
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(100, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(1)))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=100, verbose=0)
    # demonstrate prediction
    x_input = array([70, 80, 90])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
def MIMS(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out-1
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1:out_end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # covert into input/output
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    n_features = X.shape[2]
    # define model
    model = Sequential()
    model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
    model.add(LSTM(100, activation='relu'))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=200, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1, pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def MPIMS(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)  
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # covert into input/output
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    n_features = X.shape[2]
    # define model
    model = Sequential()
    model.add(LSTM(200, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(200, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(n_features)))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=300, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1, pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
def Steps_Univariate_Forecasting(values_list, n_in=1, n_out=1):
    values = values_list
    data = series_to_supervised(values,n_in,n_out)
    print(data)
def Multivariate_Forecasting(list_1,list_2,n_in,n_out):
    raw = DataFrame()
    raw['ob1'] = list_1
    raw['ob2'] = list_2
    values = raw.values
    data = series_to_supervised(values,n_in,n_out)
    print(data)
        
def Univariate_MLP_Models(train_list,pred_list):
    # split a univariate sequence into samples
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the sequence
            if end_ix > len(sequence)-1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
    # define input sequence
    raw_seq = train_list
    # choose a number of time steps
    n_steps = 3
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_steps))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def Multiple_Input_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps = 3
    # convert into input/output
    X, y = split_sequences(dataset, n_steps)
    # flatten input
    n_input = X.shape[1] * X.shape[2]
    X = X.reshape((X.shape[0], n_input))
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_input))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_input))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def multi_headed_input_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps = 3
    # convert into input/output
    X, y = split_sequences(dataset, n_steps)
    # separate input data
    X1 = X[:, :, 0]
    X2 = X[:, :, 1]
    # first input model
    visible1 = Input(shape=(n_steps,))
    dense1 = Dense(100, activation='relu')(visible1)
    # second input model
    visible2 = Input(shape=(n_steps,))
    dense2 = Dense(100, activation='relu')(visible2)
    # merge input models
    merge = concatenate([dense1, dense2])
    output = Dense(1)(merge)
    model = Model(inputs=[visible1, visible2], outputs=output)
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit([X1, X2], y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2, pred_list3])
    x1 = x_input[:, 0].reshape((1, n_steps))
    x2 = x_input[:, 1].reshape((1, n_steps))
    yhat = model.predict([x1, x2], verbose=0)
    print(yhat)   
    
def Multiple_Parallel_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences)-1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps = 3
    # convert into input/output
    X, y = split_sequences(dataset, n_steps)
    # flatten input
    n_input = X.shape[1] * X.shape[2]
    X = X.reshape((X.shape[0], n_input))
    n_output = y.shape[1]
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_input))
    model.add(Dense(n_output))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_input))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def multi_output_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    # split a multivariate sequence into samples
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences)-1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps = 3
    # convert into input/output
    X, y = split_sequences(dataset, n_steps)
    # flatten input
    n_input = X.shape[1] * X.shape[2]
    X = X.reshape((X.shape[0], n_input))
    # separate output
    y1 = y[:, 0].reshape((y.shape[0], 1))
    y2 = y[:, 1].reshape((y.shape[0], 1))
    y3 = y[:, 2].reshape((y.shape[0], 1))
    # define model
    visible = Input(shape=(n_input,))
    dense = Dense(100, activation='relu')(visible)
    # define output 1
    output1 = Dense(1)(dense)
    # define output 2
    output2 = Dense(1)(dense)
    # define output 2
    output3 = Dense(1)(dense)
    # tie together
    model = Model(inputs=visible, outputs=[output1, output2, output3])
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, [y1,y2,y3], epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_input))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def Multi_Step_MLP(train_list,pred_list):
    # split a univariate sequence into samples
    def split_sequence(sequence, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the sequence
            if out_end_ix > len(sequence):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    raw_seq = train_list
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # split into samples
    X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_steps_in))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array(pred_list)
    x_input = x_input.reshape((1, n_steps_in))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def MIMS_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    # split a multivariate sequence into samples
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out-1
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1:out_end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # convert into input/output
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    # flatten input
    n_input = X.shape[1] * X.shape[2]
    X = X.reshape((X.shape[0], n_input))
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_input))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2,pred_list3])
    x_input = x_input.reshape((1, n_input))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
        
def MPIMS_MLP(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    # convert to [rows, columns] structure
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    # horizontally stack columns
    dataset = hstack((in_seq1, in_seq2, out_seq))
    # choose a number of time steps
    n_steps_in, n_steps_out = 3, 2
    # convert into input/output
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    # flatten input
    n_input = X.shape[1] * X.shape[2]
    X = X.reshape((X.shape[0], n_input))
    # flatten output
    n_output = y.shape[1] * y.shape[2]
    y = y.reshape((y.shape[0], n_output))
    # define model
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=n_input))
    model.add(Dense(n_output))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X, y, epochs=2000, verbose=0)
    # demonstrate prediction
    x_input = array([pred_list1,pred_list2,pred_list3])
    x_input = x_input.reshape((1, n_input))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def Univariate_CNN(train_list,pred_list):
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
    raw_seq = train_list

    n_steps = 3
    n_features = 1
    
    X, y = split_sequence(raw_seq, n_steps)
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=1000, verbose=0)
    
    x_input = array(pred_list)
    
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def MIS_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences):
                break
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = X.shape[2]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=1000, verbose=0)
    
    x_input = array([pred_list1,pred_list2,pred_list3])
    
    x_input = x_input.reshape((1, n_steps, n_features))
    
    yhat = model.predict(x_input, verbose=0)
    print(yhat)
    
def multi_headed_input_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences):
                break
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = 1
    X1 = X[:, :, 0].reshape(X.shape[0], X.shape[1], n_features)
    X2 = X[:, :, 1].reshape(X.shape[0], X.shape[1], n_features)
    visible1 = Input(shape=(n_steps, n_features))
    cnn1 = Conv1D(filters=64, kernel_size=2, activation='relu')(visible1)
    cnn1 = MaxPooling1D(pool_size=2)(cnn1)
    cnn1 = Flatten()(cnn1)
    visible2 = Input(shape=(n_steps, n_features))
    cnn2 = Conv1D(filters=64, kernel_size=2, activation='relu')(visible2)
    cnn2 = MaxPooling1D(pool_size=2)(cnn2)
    cnn2 = Flatten()(cnn2)
    merge = concatenate([cnn1, cnn2])
    dense = Dense(50, activation='relu')(merge)
    output = Dense(1)(dense)
    model = Model(inputs=[visible1, visible2], outputs=output)
    model.compile(optimizer='adam', loss='mse')
    model.fit([X1, X2], y, epochs=1000, verbose=0)
    x_input = array([pred_list1,pred_list2, pred_list3])
    x1 = x_input[:, 0].reshape((1, n_steps, n_features))
    x2 = x_input[:, 1].reshape((1, n_steps, n_features))
    yhat = model.predict([x1, x2], verbose=0)
    print(yhat)


def MPS_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences)-1:
                break
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)
    
    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = X.shape[2]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_features))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=3000, verbose=0)
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)


def multi_output_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences)-1:
                break
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)

    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps = 3
    X, y = split_sequences(dataset, n_steps)
    n_features = X.shape[2]
    y1 = y[:, 0].reshape((y.shape[0], 1))
    y2 = y[:, 1].reshape((y.shape[0], 1))
    y3 = y[:, 2].reshape((y.shape[0], 1))
    visible = Input(shape=(n_steps, n_features))
    cnn = Conv1D(filters=64, kernel_size=2, activation='relu')(visible)
    cnn = MaxPooling1D(pool_size=2)(cnn)
    cnn = Flatten()(cnn)
    cnn = Dense(50, activation='relu')(cnn)
    output1 = Dense(1)(cnn)
    output2 = Dense(1)(cnn)
    output3 = Dense(1)(cnn)
    model = Model(inputs=visible, outputs=[output1, output2, output3])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, [y1,y2,y3], epochs=2000, verbose=0)
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def vector_output_model_CNN(train_list,pred_list):
    def split_sequence(sequence, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            if out_end_ix > len(sequence):
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    raw_seq = train_list
    n_steps_in, n_steps_out = 3, 2
    X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=2000, verbose=0)
    x_input = array(pred_list) 
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def MIMS_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out-1
            if out_end_ix > len(sequences):
                break
            seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1:out_end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
   
    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)

    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps_in, n_steps_out = 3, 2
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    n_features = X.shape[2]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=2000, verbose=0)
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

def MPIMS_CNN(train_list1,train_list2,pred_list1,pred_list2,pred_list3):
    def split_sequences(sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            if out_end_ix > len(sequences):
                break
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    in_seq1 = array(train_list1)
    in_seq2 = array(train_list2)

    out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    out_seq = out_seq.reshape((len(out_seq), 1))
    dataset = hstack((in_seq1, in_seq2, out_seq))
    n_steps_in, n_steps_out = 3, 2
    X, y = split_sequences(dataset, n_steps_in, n_steps_out)
    n_output = y.shape[1] * y.shape[2]
    y = y.reshape((y.shape[0], n_output))
    n_features = X.shape[2]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_output))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=7000, verbose=0)
    x_input = array([pred_list1,pred_list2, pred_list3])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    print(yhat)

    

    
