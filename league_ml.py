import league_helper
from collections import defaultdict
import cassiopeia as cass
import dill
import numpy as np
import matplotlib.pyplot as plt
import os
import random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras
import pandas as pd
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


team = ["Zyra","Singed","Evelynn","Kai'Sa","Renekton"]
random.shuffle(team)

champs = {'Aatrox': 0, 'Ahri': 1, 'Akali': 2, 'Alistar': 3, 'Amumu': 4, 'Anivia': 5, 'Annie': 6, 'Aphelios': 7, 'Ashe': 8, 'Aurelion Sol': 9, 'Azir': 10, 'Bard': 11, 'Blitzcrank': 12, 'Brand': 13, 'Braum': 14, 'Caitlyn': 15, 'Camille': 16, 'Cassiopeia': 17, "Cho'Gath": 18, 'Corki': 19, 'Darius': 20, 'Diana': 21, 'Dr. Mundo': 22, 'Draven': 23, 'Ekko': 24, 'Elise': 25, 'Evelynn': 26, 'Ezreal': 27, 'Fiddlesticks': 28, 'Fiora': 29, 'Fizz': 30, 'Galio': 31, 'Gangplank': 32, 'Garen': 33, 'Gnar': 34, 'Gragas': 35, 'Graves': 36, 'Hecarim': 37, 'Heimerdinger': 38, 'Illaoi': 39, 'Irelia': 40, 'Ivern': 41, 'Janna': 42, 'Jarvan IV': 43, 'Jax': 44, 'Jayce': 45, 'Jhin': 46, 'Jinx': 47, "Kai'Sa": 48, 'Kalista': 49, 'Karma': 50, 'Karthus': 51, 'Kassadin': 52, 'Katarina': 53, 'Kayle': 54, 'Kayn': 55, 'Kennen': 56, "Kha'Zix": 57, 'Kindred': 58, 'Kled': 59, "Kog'Maw": 60, 'LeBlanc': 61, 'Lee Sin': 62, 'Leona': 63, 'Lillia': 64, 'Lissandra': 65, 'Lucian': 66, 'Lulu': 67, 'Lux': 68, 'Malphite': 69, 'Malzahar': 70, 'Maokai': 71, 'Master Yi': 72, 'Miss Fortune': 73, 'Mordekaiser': 74, 'Morgana': 75, 'Nami': 76, 'Nasus': 77, 'Nautilus': 78, 'Neeko': 79, 'Nidalee': 80, 'Nocturne': 81, 'Nunu &amp; Willump': 82, 'Olaf': 83, 'Orianna': 84, 'Ornn': 85, 'Pantheon': 86, 'Poppy': 87, 'Pyke': 88, 'Qiyana': 89, 'Quinn': 90, 'Rakan': 91, 'Rammus': 92, "Rek'Sai": 93, 'Renekton': 94, 'Rengar': 95, 'Riven': 96, 'Rumble': 97, 'Ryze': 98, 'Samira': 99, 'Sejuani': 100, 'Senna': 101, 'Seraphine': 102, 'Sett': 103, 'Shaco': 104, 'Shen': 105, 'Shyvana': 106, 'Singed': 107, 'Sion': 108, 'Sivir': 109, 'Skarner': 110, 'Sona': 111, 'Soraka': 112, 'Swain': 113, 'Sylas': 114, 'Syndra': 115, 'Tahm Kench': 116, 'Taliyah': 117, 'Talon': 118, 'Taric': 119, 'Teemo': 120, 'Thresh': 121, 'Tristana': 122, 'Trundle': 123, 'Tryndamere': 124, 'Twisted Fate': 125, 'Twitch': 126, 'Udyr': 127, 'Urgot': 128, 'Varus': 129, 'Vayne': 130, 'Veigar': 131, "Vel'Koz": 132, 'Vi': 133, 'Viktor': 134, 'Vladimir': 135, 'Volibear': 136, 'Warwick': 137, 'Wukong': 138, 'Xayah': 139, 'Xerath': 140, 'Xin Zhao': 141, 'Yasuo': 142, 'Yone': 143, 'Yorick': 144, 'Yuumi': 145, 'Zac': 146, 'Zed': 147, 'Ziggs': 148, 'Zilean': 149, 'Zoe': 150, 'Zyra': 151}
winrates = {"Brand":59.09,"Seraphine":58.28,"Miss Fortune":56.98,"Swain":56.86,"Morgana":55.93,"Heimerdinger":55.44,"Sion":55.37,"Amumu":55.35,"Ashe":55.3,"Graves":55.27,"Ziggs":55.14,"Leona":55.13,"Zyra":55.03,"Malzahar":54.35,"Vel'Koz":54.33,"Viktor":54.33,"Maokai":54.26,"Sett":54.16,"Alistar":54.15,"Ornn":54.13,"Neeko":53.95,"Sivir":53.75,"Jhin":53.67,"Jinx":53.6,"Trundle":53.39,"Kayle":53.31,"Lux":53.27,"Fiddlesticks":53.25,"Janna":53.06,"Nami":53.06,"Veigar":52.98,"Caitlyn":52.98,"Illaoi":52.78,"Karthus":52.78,"Ezreal":52.76,"Varus":52.74,"Galio":52.7,"Xerath":52.47,"Sona":52.35,"Kog'Maw":52.2,"Senna":52.13,"Nasus":52.08,"Yorick":52.02,"Skarner":51.97,"Urgot":51.83,"Taric":51.74,"Twisted Fate":51.5,"Annie":51.5,"Diana":51.4,"Nautilus":51.38,"Cassiopeia":51.36,"Lissandra":51.31,"Ahri":51.29,"Wukong":50.84,"Jayce":50.72,"Malphite":50.58,"Shen":50.43,"Dr. Mundo":50.41,"Xayah":50.37,"Xin Zhao":50.36,"Aphelios":50.23,"Orianna":50.14,"Cho'Gath":50.04,"Teemo":50.02,"Tristana":50,"Blitzcrank":49.94,"Rammus":49.88,"Kayn":49.85,"Rek'Sai":49.7,"Gangplank":49.51,"Kled":49.44,"Vi":49.36,"Singed":49.36,"Ivern":49.35,"Lucian":49.3,"Samira":49.3,"Corki":49.15,"Zac":48.93,"Lillia":48.92,"Warwick":48.81,"Sejuani":48.67,"Quinn":48.6,"Tryndamere":48.53,"Soraka":48.52,"Fizz":48.49,"Yuumi":48.49,"Aurelion Sol":48.42,"Jax":48.41,"Draven":48.33,"Braum":48.26,"Jarvan IV":48.22,"Volibear":48.17,"Nocturne":48.14,"Olaf":47.96,"Lulu":47.91,"Zilean":47.87,"Kalista":47.77,"Poppy":47.75,"Anivia":47.69,"Nunu &amp; Willump":47.64,"Garen":47.6,"Kennen":47.56,"Gnar":47.37,"Elise":47.23,"Irelia":47.15,"Renekton":47.07,"Rengar":46.98,"Syndra":46.96,"Rakan":46.92,"Master Yi":46.84,"Pantheon":46.77,"Kai'Sa":46.75,"Twitch":46.74,"Udyr":46.69,"Vayne":46.69,"Shyvana":46.62,"Darius":46.56,"Talon":46.57,"Zed":46.48,"Ekko":46.46,"Riven":46.42,"Mordekaiser":46.4,"Azir":46.39,"Thresh":46.32,"Lee Sin":46.22,"Fiora":46.06,"Bard":46.02,"Aatrox":45.97,"Karma":45.86,"Kassadin":45.82,"Taliyah":45.72,"Kindred":45.7,"LeBlanc":45.64,"Kha'Zix":45.43,"Camille":45.35,"Shaco":45.33,"Yone":45.23,"Rumble":45.18,"Hecarim":45.17,"Evelynn":45.11,"Pyke":45.04,"Sylas":44.98,"Akali":44.86,"Vladimir":44.83,"Gragas":44.59,"Tahm Kench":44.53,"Katarina":44.19,"Qiyana":43.99,"Ryze":43.37,"Zoe":43.14,"Yasuo":42.99,"Nidalee":42.18}

Aram_Data = []
try:
    Aram_Data = dill.load(open("Aram_Data_ML.pickle", "rb"))
except:
    pass
print(len(Aram_Data),'\n')


# URL = "/Users/rale/Desktop/ddml2.htm"
# New_Aram_Data = league_helper.parse_aram_data(URL)
# Aram_Data = New_Aram_Data + Aram_Data
# dill.dump(Aram_Data, file = open("Aram_Data_ML.pickle", "wb"))

def encode_teamcomp(teamcomp):
    encoded = np.zeros(len(champs))
    for i in teamcomp:
        encoded[champs[i]] += 1
    return encoded

x = np.empty((len(Aram_Data)*2,len(champs)), dtype=int)
y = np.empty(len(Aram_Data)*2)
for i in range(len(Aram_Data)):
    if Aram_Data[i].win:
        x[i] = encode_teamcomp(Aram_Data[i].teamcomp[0])
        y[i] = 1
    else:
        x[i] = encode_teamcomp(Aram_Data[i].teamcomp[0])
        y[i] = 0

for i in range(len(Aram_Data)):
    if Aram_Data[i].win:
        x[len(Aram_Data) + i] = encode_teamcomp(Aram_Data[i].teamcomp[1])
        y[len(Aram_Data) + i] = 0
    else:
        x[len(Aram_Data) + i] = encode_teamcomp(Aram_Data[i].teamcomp[1])
        y[len(Aram_Data) + i] = 1

N = int(0.2*len(x))
X_test, y_test = x[:N], y[:N]
X_train, y_train = x[N:], y[N:]
N = int(len(X_train)/2)

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(type(classifier).__name__+' Accuracy = '+ str(100 * accuracy_score(y_test,y_pred))+'%')


x = np.empty((1,len(champs)), dtype=int)
x[0] = encode_teamcomp(team)
out = classifier.predict(x)
if out:
    print("Win")
else:
    print("Loss")


# X_valid, X_train = X_train[:N], X_train[N:]
# y_valid, y_train = y_train[:N], y_train[N:]
#
# model = keras.models.Sequential()
# model.add(keras.layers.InputLayer(input_shape=[len(champs)]))
# model.add(keras.layers.Dense(100, activation="relu",
#             kernel_regularizer=keras.regularizers.l2(0.0001),
#             kernel_initializer=keras.initializers.GlorotUniform()))
# model.add(keras.layers.Dense(50, activation="relu",
#             kernel_regularizer=keras.regularizers.l2(0.0001),
#             kernel_initializer=keras.initializers.GlorotUniform()))
# model.add(keras.layers.Dense(10, activation="softmax"))
#
# OPT = "sgd"
# OPT = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.91, beta_2=0.998, epsilon=1e-10)
# model.compile(loss="sparse_categorical_crossentropy",
#               optimizer=OPT,
#               metrics=["accuracy"])
# history = model.fit(X_train,y_train,
#                     epochs=40,
#                     batch_size=10,
#                     validation_data=(X_valid,y_valid),verbose=0,use_multiprocessing=True)
#
# model.save("keras_example.h5")
# pd.DataFrame(history.history).plot(figsize=(8,5))
# plt.grid(True)
# plt.gca().set_ylim(0,1)
# plt.gca().set_title("Loss and Accuracy as a Function of Epoch Number")
# plt.gca().set_xlabel("Epoch Number")
# # plt.show()
#
#
#
#
# model = keras.models.load_model("keras_example.h5")
#
# y_pred = model.predict_classes(X_test)
# acc = accuracy_score(y_test,y_pred)
# acc = np.round(1000*acc)/10
# print("Neural Network Model Accuracy = " + str(acc) + "%" )


correct_prediction = 0
for i in Aram_Data:
    count = 0
    count2 = 0
    for k in i.teamcomp[0]:
        count += winrates[k]
    for k in i.teamcomp[1]:
        count2 += winrates[k]
    if count > count2:
        if i.win:
            correct_prediction += 1
    else:
        if not i.win:
            correct_prediction += 1
print("NON-ML prediction Accuracy:", correct_prediction/len(Aram_Data)*100)
