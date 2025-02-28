import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import matplotlib.pyplot as plt
import seaborn as sns

# Function to extract features from audio files
def extract_features(file_path, mfcc, chroma, mel):
    audio_data, _ = librosa.load(file_path, sr=22050)
    if mfcc:
        result = np.mean(librosa.feature.mfcc(y=audio_data, sr=22050, n_mfcc=40).T, axis=0)
    if chroma:
        result = np.mean(librosa.feature.chroma_stft(y=audio_data, sr=22050).T, axis=0)
    if mel:
        result = np.mean(librosa.feature.melspectrogram(y=audio_data, sr=22050).T, axis=0)
    return result

# Define the main function for loading data and training the model
def main(data_dir):
    # Constants
    MFCC = True
    CHROMA = False
    MEL = False
    LABELS = ['Abnormal', 'Normal']
    NUM_CLASSES = len(LABELS)
    # Load data
    data = []
    labels = []
    for i, label in enumerate(LABELS):
        folder_path = os.path.join(data_dir, label)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            features = extract_features(file_path, MFCC, CHROMA, MEL)
            data.append(features)
            labels.append(i)
    # Convert to numpy arrays
    data = np.array(data)
    labels = np.array(labels)
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    # Reshape data for VGG19 input
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    # Build the VGG19 model
    model = models.Sequential([
        layers.Conv1D(64, 3, activation='relu', input_shape=(X_train.shape[1], 1)),
        layers.Conv1D(64, 3, activation='relu', padding='same'),
        layers.MaxPooling1D(2, strides=2),
        layers.Conv1D(128, 3, activation='relu', padding='same'),
        layers.Conv1D(128, 3, activation='relu', padding='same'),
        layers.MaxPooling1D(2, strides=2),
        layers.Conv1D(256, 3, activation='relu', padding='same'),
        layers.Conv1D(256, 3, activation='relu', padding='same'),
        layers.Conv1D(256, 3, activation='relu', padding='same'),
        layers.MaxPooling1D(2, strides=2),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.MaxPooling1D(2, strides=2),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.Conv1D(512, 3, activation='relu', padding='same'),
        layers.MaxPooling1D(2, strides=2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dense(4096, activation='relu'),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # Display model summary
    model.summary()
    # Train the model
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))
    # Save the model
    model.save('2class_vgg19_model.h5')
    
    # Plot training history
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Generate confusion matrix
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    cm = confusion_matrix(y_test, y_pred_classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=LABELS, yticklabels=LABELS)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == "__main__":
    main('C:\\Users\\guhan\\OneDrive\\Desktop\\HeartSound\HeartSound\\Dataset')
