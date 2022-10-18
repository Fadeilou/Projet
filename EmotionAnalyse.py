import face_recognition
import numpy as np
import cv2
import csv
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import LeakyReLU
import pandas as pd


class EmotionAnalyse:
    def build_model(input_shape=(48, 48, 3)):
        i = tf.keras.layers.Input(input_shape, dtype=tf.uint8)
        x = tf.cast(i, tf.float32)
        x = tf.keras.applications.vgg16.preprocess_input(x)

        backbone = tf.keras.applications.vgg16.VGG16(
            include_top=False, weights='imagenet',
            input_tensor=x
        )
        output_layer = backbone.get_layer("block5_conv3").output

        def build_age_branch(input_tensor):
            x = tf.keras.layers.Dense(1024, activation=LeakyReLU(alpha=0.3))(input_tensor)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            x = tf.keras.layers.Dense(1, activation=None, name='age_output')(x)

            return x

        def build_etchnicity_branch(input_tensor):
            x = tf.keras.layers.Dense(500, activation=LeakyReLU(alpha=0.3))(input_tensor)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            x = tf.keras.layers.Dense(5, activation='softmax', name='ethnicity_output')(x)

            return x

        def build_gender_branch(input_tensor):
            x = tf.keras.layers.Dense(500, activation=LeakyReLU(alpha=0.3))(input_tensor)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            x = tf.keras.layers.Dense(1, activation='sigmoid', name='gender_output')(x)

            return x

        x = tf.keras.layers.Flatten()(output_layer)
        output_age = build_age_branch(x)
        output_ethnicity = build_etchnicity_branch(x)
        output_gender = build_gender_branch(x)
        model = tf.keras.Model(i, [output_age, output_ethnicity, output_gender])

        model.compile(tf.keras.optimizers.Adam(learning_rate=1e-4),
                      loss=['mse', 'categorical_crossentropy', 'binary_crossentropy'], loss_weights=[0.001, 0.5, 0.5],
                      metrics={'age_output': 'mean_absolute_error', 'ethnicity_output': 'accuracy',
                               'gender_output': 'accuracy'})

        plateau = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.3, patience=2, verbose=1
        )
        es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1,
                                              patience=5)  # Early stopping (stops training when validation doesn't improve for {patience} epochs)
        save_best = tf.keras.callbacks.ModelCheckpoint('weights.h5', monitor='val_loss', save_best_only=True,
                                                       mode='min',
                                                       save_weights_only=True)  # Saves the best version of the model to disk (as measured on the validation data set)
        remote_monitor_callback = tf.keras.callbacks.RemoteMonitor(
            root='https://dweet.io', path='/dweet/for/multitask',
            send_as_json=False, field='data'
        )

        Models = {}

        emotion_model = keras.models.load_model("ml_models/ferNet.h5")
        model.load_weights("ml_models/model.h5")
        Models["emotion_model"] = emotion_model
        Models["age_model"] = model
        print(Models)

        return Models

    def video_analyse(path, models):
        known_face_encodings = []
        known_face_names = []
        process_this_frame = True

        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        names_ethnicity = ['white', 'black', 'asian', 'indian', 'other']
        name_genders = ['male', 'female']
        ageList = ['(0-2)', '(3-7)', '(8-15)', '(16-30)', '(30-45)', '(46-60)', '(61-75)', '(76-100)']
        currentframe = 0
        data_path = "public/data.csv"

        with open(data_path, 'w', newline='') as fichiercsv:
            writer = csv.writer(fichiercsv)
            writer.writerow(['id', 'emotion', 'age', 'genre', 'race'])

        video_capture = cv2.VideoCapture(path)
        ret, frame = video_capture.read()
        frame_height, frame_width, _ = frame.shape
        out = cv2.VideoWriter('output6.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                              (frame_width, frame_height))
        print("Processing Video...")

        while video_capture.isOpened():
            face_names = []
            face_locations = []
            face_encodings = []

            ret, frame = video_capture.read()
            if ret:
                face_locations = face_recognition.api.face_locations(frame)

                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for face_encoding in face_encodings:

                    if not known_face_encodings:
                        known_face_encodings.append(face_encoding)

                        new_name = 1
                        known_face_names.append(new_name)

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        face_names.append(name)
                    else:
                        known_face_encodings.append(face_encoding)
                        new_name = len(known_face_names) + 1
                        known_face_names.append(new_name)
                        face_names.append(new_name)

                for (top, right, bottom, left), name, face_encoding in zip(face_locations, face_names, face_encodings):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray_frame1 = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

                    roi_frame = gray_frame[top + 50:bottom + 10, left:right]
                    roi_frame1 = gray_frame1[top + 50:bottom + 10, left:right]

                    font = cv2.FONT_HERSHEY_DUPLEX

                    try:
                        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_frame, (48, 48)), -1), 0)
                    except:
                        continue
                    try:
                        cropped_img1 = np.expand_dims(cv2.resize(roi_frame1, (48, 48)), 0)
                    except:
                        continue

                    emotion_prediction = models["emotion_model"].predict(cropped_img)
                    maxindex = int(np.argmax(emotion_prediction))
                    emotion = emotion_dict[maxindex]

                    p = models["age_model"].predict(cropped_img1)
                    index = 0

                    gender_predictions = tf.where(p[2] > 0.5, 1, 0)
                    race = names_ethnicity[p[1][index].argmax()]
                    gender = name_genders[gender_predictions[index][0]]
                    age = p[0][index].astype(np.int)[0]

                    if 0 <= age <= 2:
                        age_interval = "(0-2)"
                    elif 3 <= age <= 7:
                        age_interval = "(3-7)"
                    elif 8 <= age <= 15:
                        age_interval = "(8-15)"
                    elif 16 <= age <= 30:
                        age_interval = "(16-30)"
                    elif 30 <= age <= 45:
                        age_interval = "(30-45)"
                    elif 46 <= age <= 60:
                        age_interval = "(46-60)"
                    elif 61 <= age <= 75:
                        age_interval = "(61-75)"
                    elif 76 <= age <= 100:
                        age_interval = "(76-100)"
                    print(emotion)
                    label = "{},{},{},{},{}".format(str(name), emotion, race, gender, age_interval)

                    with open(data_path, 'a', newline='') as fichiercsv:
                        writer = csv.writer(fichiercsv)
                        writer.writerow([str(name), emotion, age_interval, gender, race])

                    cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 215, 0), 1)

                out.write(frame)
            else:
                break

        out.release()
        print("Done processing video")

    def emotion_proportion(path):
        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        df = pd.read_csv(path)
        emotion_proportion = ""
        total_emotion = df['emotion'].count()
        print(total_emotion)

        for emotion in emotion_dict:
            count = 0
            for indice, ligne in df.iterrows():
                if ligne['emotion'] == emotion_dict[emotion]:
                    count = count + 1
                proportions = (count * 100) / total_emotion
                x = emotion_dict[emotion] + ":" + str(proportions) + "-"
            emotion_proportion = emotion_proportion + x

        return emotion_proportion

    def age_proportion(path):
        ageList = ['(0-2)', '(3-7)', '(8-15)', '(16-30)', '(30-45)', '(46-60)', '(61-75)', '(76-100)']

        df = pd.read_csv(path)
        age_proportion = ""
        total_age = df['age'].count()
        print(total_age)

        for age in ageList:
            count = 0
            for indice, ligne in df.iterrows():
                if ligne['age'] == age:
                    count = count + 1
                proportions = (count * 100) / total_age
                x = age + ":" + str(proportions) + "-"
            age_proportion = age_proportion + x
        return age_proportion

    def gender_proportion(path):
        name_genders = ['male', 'female']

        df = pd.read_csv(path)
        gender_proportion = ""
        total_gender = df['age'].count()
        print(total_gender)

        for gender in name_genders:
            count = 0
            for indice, ligne in df.iterrows():
                if ligne['genre'] == gender:
                    count = count + 1
                proportions = (count * 100) / total_gender
                x = gender + ":" + str(proportions) + "-"
            gender_proportion = gender_proportion + x
        return gender_proportion

    def race_proportion(path):
        names_ethnicity = ['white', 'black', 'asian', 'indian', 'other']

        df = pd.read_csv(path)
        race_proportion = ""
        total_race = df['age'].count()
        print(total_race)

        for race in names_ethnicity:
            count = 0
            for indice, ligne in df.iterrows():
                if ligne['race'] == race:
                    count = count + 1
                proportions = (count * 100) / total_race
                x = race + ":" + str(proportions) + "-"
            race_proportion = race_proportion + x
        return race_proportion

    def emotion_proportion_according_paramater(path):
        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        names_ethnicity = ['white', 'black', 'asian', 'indian', 'other']
        name_genders = ['male', 'female']
        ageList = ['(0-2)', '(3-7)', '(8-15)', '(16-30)', '(30-45)', '(46-60)', '(61-75)', '(76-100)']

        df = pd.read_csv(path)
        multipe_proportions = ""
        total_emotion = df['emotion'].count()

        for gender in name_genders:
            for race in names_ethnicity:
                for age in ageList:
                    for emotion in emotion_dict:
                        count = 0
                        for indice, ligne in df.iterrows():
                            if ligne['genre'] == gender and ligne['race'] == race and ligne['age'] == age and ligne[
                                'emotion'] == emotion_dict[emotion]:
                                count = count + 1
                        proportion = (count * 100) / total_emotion

                        if proportion <= 0:
                            continue
                        x = str(gender) + ":" + str(race) + ":" + str(age) + ":" + emotion_dict[emotion] + ":" + str(
                            proportion) + "-"
                        multipe_proportions = multipe_proportions + x
        return multipe_proportions

    def count_people(path):
        df = pd.read_csv(path)
        identifiants = df['id']
        idTab = []
        for id in identifiants:
            if not id in idTab:
                idTab.append(id)

        return len(idTab)

