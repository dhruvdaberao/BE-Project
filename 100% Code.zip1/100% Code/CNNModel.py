# def main():
#     import numpy as np
#     from keras.models import Sequential
#     from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
#     from tensorflow.keras import optimizers
#     from tensorflow.keras.preprocessing.image import ImageDataGenerator
#     import matplotlib.pyplot as plt

#     # basepath = "D:/100% Code.zip1/100% Code"
#     basepath = r"D:\BE Project\SR_BE_Project\100% Code.zip1\100% Code"


#     # Initializing the CNN
#     classifier = Sequential()

#     # Step 1 - Convolution Layer
#     classifier.add(Convolution2D(32, 1, 1, input_shape=(64, 64, 3), activation='relu'))

#     # Step 2 - Pooling
#     classifier.add(MaxPooling2D(pool_size=(2, 2)))

#     # Second convolution layer
#     classifier.add(Convolution2D(32, 1, 1, activation='relu'))
#     classifier.add(MaxPooling2D(pool_size=(2, 2)))

#     # Third convolution layer
#     classifier.add(Convolution2D(64, 1, 1, activation='relu'))
#     classifier.add(MaxPooling2D(pool_size=(2, 2)))

#     # Flattening
#     classifier.add(Flatten())

#     # Full connection
#     classifier.add(Dense(256, activation='relu'))
#     classifier.add(Dropout(0.8))
#     classifier.add(Dense(2, activation='softmax'))  # Adjust for number of classes

#     # Compiling the CNN
#     classifier.compile(
#         optimizer=optimizers.SGD(learning_rate=0.01),
#         loss='categorical_crossentropy',
#         metrics=['accuracy']
#     )

#     # Data augmentation
#     train_datagen = ImageDataGenerator(
#         rescale=1./255,
#         shear_range=0.2,
#         zoom_range=0.2,
#         horizontal_flip=True
#     )

#     test_datagen = ImageDataGenerator(rescale=1./255)

#     training_set = train_datagen.flow_from_directory(
#         basepath + '/training set',
#         target_size=(64, 64),
#         batch_size=32,
#         class_mode='categorical'
#     )

#     test_set = test_datagen.flow_from_directory(
#         basepath + '/testing set',
#         target_size=(64, 64),
#         batch_size=32,
#         class_mode='categorical'
#     )

#     steps_per_epoch = int(np.ceil(training_set.samples / 32))
#     val_steps = int(np.ceil(test_set.samples / 32))

#     # Training the model
#     model = classifier.fit(
#         training_set,
#         steps_per_epoch=steps_per_epoch,
#         epochs=50,
#         validation_data=test_set,
#         validation_steps=val_steps
#     )

#     # Saving the model
#     classifier.save(basepath + '/model1.h5')

#     # Evaluation
#     scores = classifier.evaluate(test_set, verbose=1)
#     B = "Testing Accuracy: %.2f%%" % (scores[1] * 100)
#     print(B)

#     scores = classifier.evaluate(training_set, verbose=1)
#     C = "Training Accuracy: %.2f%%" % (scores[1] * 100)
#     print(C)

#     msg = B + '\n' + C

#     # Plotting accuracy
#     plt.plot(model.history['accuracy'])
#     plt.plot(model.history['val_accuracy'])
#     plt.title('Model Accuracy')
#     plt.ylabel('Accuracy')
#     plt.xlabel('Epoch')
#     plt.legend(['Train', 'Test'], loc='upper left')
#     plt.savefig(basepath + "/accuracy.png", bbox_inches='tight')
#     plt.show()

#     # Plotting loss
#     plt.figure()
#     plt.plot(model.history['loss'])
#     plt.plot(model.history['val_loss'])
#     plt.title('Model Loss')
#     plt.ylabel('Loss')
#     plt.xlabel('Epoch')
#     plt.legend(['Train', 'Test'], loc='upper left')
#     plt.savefig(basepath + "/loss.png", bbox_inches='tight')
#     plt.show()

#     return msg


# # Entry point
# if __name__ == "__main__":
#     main()
       

def main():
    import numpy as np
    from keras.models import Sequential
    from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras import optimizers
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    import matplotlib.pyplot as plt
    from sklearn.metrics import classification_report, confusion_matrix

    basepath = r"D:\BE Project\SR_BE_Project\100% Code.zip1\100% Code"

    # Initializing the CNN
    classifier = Sequential()

    # Step 1 - Convolution Layer
    classifier.add(Convolution2D(32, 1, 1, input_shape=(64, 64, 3), activation='relu'))

    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Second convolution layer
    classifier.add(Convolution2D(32, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Third convolution layer
    classifier.add(Convolution2D(64, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Flattening
    classifier.add(Flatten())

    # Full connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.8))
    classifier.add(Dense(2, activation='softmax'))  

    # Compiling the CNN
    classifier.compile(
        optimizer=optimizers.SGD(learning_rate=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory(
        basepath + '/training set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )

    test_set = test_datagen.flow_from_directory(
        basepath + '/testing set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )

    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))

    # Training the model
    model = classifier.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=50,
        validation_data=test_set,
        validation_steps=val_steps
    )

    # Saving the model
    classifier.save(basepath + '/model1.h5')

    # Evaluation
    test_accuracy = classifier.evaluate(test_set, verbose=1)[1] * 100
    train_accuracy = classifier.evaluate(training_set, verbose=1)[1] * 100

    # --------------------------------------------------------
    #  Added Precision, Recall, F1-Score, Confusion Matrix
    # --------------------------------------------------------
    test_set.reset()

    y_true = test_set.classes
    y_pred_prob = classifier.predict(test_set)
    y_pred = np.argmax(y_pred_prob, axis=1)

    class_labels = list(test_set.class_indices.keys())

    cls_report = classification_report(y_true, y_pred, target_names=class_labels)
    cm = confusion_matrix(y_true, y_pred)

    print("\nClassification Report:\n", cls_report)
    print("\nConfusion Matrix:\n", cm)

    # --------------------------------------------------------

    # Plotting accuracy
    plt.plot(model.history['accuracy'])
    plt.plot(model.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/accuracy.png", bbox_inches='tight')
    plt.show()

    # Plotting loss
    plt.figure()
    plt.plot(model.history['loss'])
    plt.plot(model.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/loss.png", bbox_inches='tight')
    plt.show()

    # Return all results as a single string
    results = (
        f"Training Accuracy: {train_accuracy:.2f}%\n"
        f"Testing Accuracy: {test_accuracy:.2f}%\n"
        f"Classification Report:\n{cls_report}\n"
        f"Confusion Matrix:\n{cm}"
    )

    return results


if __name__ == "__main__":
    print(main())
