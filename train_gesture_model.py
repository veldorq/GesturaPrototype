"""
Gesture CNN Training Module for Gestura
========================================
Author: Senior Python Accessibility Engineer & ML Training Specialist
Date: February 8, 2026

Purpose:
    Train a lightweight CNN for real-time gesture classification.
    Based on DataFlair OpenCV + CNN approach, adapted for accessibility.

Model Architecture:
    Lightweight CNN optimized for real-time inference
    Input: 64x64 grayscale images
    Output: (gesture_label, confidence_score)

Training Strategy:
    - Small, non-overlapping gesture set
    - Data augmentation for robustness
    - Class weighting for balance
    - Early stopping to prevent overfitting
"""

import numpy as np
import cv2
import os
from pathlib import Path
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# TensorFlow/Keras imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    print("✅ TensorFlow imported successfully")
except ImportError:
    print("❌ TensorFlow not found. Install with: pip install tensorflow")
    exit(1)


class GestureModelConfig:
    """Configuration for gesture model training"""
    
    # Dataset settings
    DATASET_ROOT = "dataset"
    IMAGE_SIZE = (64, 64)
    
    # Gestures (must match dataset folders)
    GESTURES = [
        'scroll_up',
        'scroll_down',
        'swipe_left',
        'swipe_right',
        'pinch_zoom',
        'thumb_down_close',
        'mute_toggle'
    ]
    
    # Training hyperparameters
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 0.001
    VALIDATION_SPLIT = 0.2
    TEST_SPLIT = 0.1
    
    # Model settings
    INPUT_SHAPE = (64, 64, 1)  # Grayscale
    NUM_CLASSES = len(GESTURES)
    
    # Output paths
    MODEL_PATH = "models/gesture_cnn_model.h5"
    LABEL_ENCODER_PATH = "models/label_encoder.pkl"
    TRAINING_HISTORY_PATH = "models/training_history.pkl"
    
    # Early stopping patience
    EARLY_STOPPING_PATIENCE = 10
    
    # Random seed for reproducibility
    RANDOM_SEED = 42


class GestureDataLoader:
    """Load and preprocess gesture dataset"""
    
    def __init__(self):
        """Initialize data loader"""
        self.X_train = None
        self.X_val = None
        self.X_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.label_encoder = {}
    
    def load_dataset(self):
        """
        Load images from dataset folders.
        
        Returns:
            X: Images as numpy array (N, 64, 64, 1)
            y: Labels as numpy array (N,)
        """
        print("📂 Loading dataset from:", GestureModelConfig.DATASET_ROOT)
        
        images = []
        labels = []
        
        for label_idx, gesture in enumerate(GestureModelConfig.GESTURES):
            gesture_path = Path(GestureModelConfig.DATASET_ROOT) / gesture
            
            if not gesture_path.exists():
                print(f"⚠️  Warning: {gesture} folder not found")
                continue
            
            image_files = list(gesture_path.glob('*.jpg'))
            print(f"  Loading {gesture}: {len(image_files)} images")
            
            for img_path in image_files:
                try:
                    # Read image (already grayscale and normalized from collection)
                    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                    
                    if img is None:
                        continue
                    
                    # Ensure correct size
                    if img.shape != GestureModelConfig.IMAGE_SIZE:
                        img = cv2.resize(img, GestureModelConfig.IMAGE_SIZE)
                    
                    images.append(img)
                    labels.append(label_idx)
                
                except Exception as e:
                    print(f"⚠️  Error loading {img_path.name}: {e}")
        
        # Convert to numpy arrays
        X = np.array(images, dtype='float32')
        y = np.array(labels, dtype='int32')
        
        # Normalize pixel values to [0, 1]
        X = X / 255.0
        
        # Reshape for CNN: (N, 64, 64, 1)
        X = X.reshape(-1, 64, 64, 1)
        
        # Create label encoder mapping
        self.label_encoder = {i: gesture for i, gesture in enumerate(GestureModelConfig.GESTURES)}
        
        print(f"✅ Loaded {len(X)} images across {len(GestureModelConfig.GESTURES)} gestures")
        print(f"   Dataset shape: {X.shape}")
        
        return X, y
    
    def split_dataset(self, X, y):
        """
        Split dataset into train, validation, and test sets.
        
        Strategy:
            - First split: separate test set (10%)
            - Second split: train/val from remaining (80/20)
        """
        print("\n📊 Splitting dataset...")
        
        # First split: train+val (90%) and test (10%)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=GestureModelConfig.TEST_SPLIT,
            random_state=GestureModelConfig.RANDOM_SEED,
            stratify=y
        )
        
        # Second split: train (80%) and val (20%) from temp
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=GestureModelConfig.VALIDATION_SPLIT,
            random_state=GestureModelConfig.RANDOM_SEED,
            stratify=y_temp
        )
        
        self.X_train = X_train
        self.X_val = X_val
        self.X_test = X_test
        self.y_train = y_train
        self.y_val = y_val
        self.y_test = y_test
        
        print(f"  Train set: {len(X_train)} samples")
        print(f"  Validation set: {len(X_val)} samples")
        print(f"  Test set: {len(X_test)} samples")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def create_data_augmentation(self):
        """
        Create data augmentation generator for training robustness.
        
        Augmentations:
            - Rotation (±15°) - for shaky hands
            - Width/height shift (±10%) - for camera movement
            - Brightness adjustment - for lighting variations
            - Zoom (±10%) - for distance variations
        """
        datagen = ImageDataGenerator(
            rotation_range=15,  # Slight rotation for hand shakiness
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            brightness_range=[0.8, 1.2],  # Lighting variations
            fill_mode='nearest'
        )
        
        return datagen
    
    def save_label_encoder(self):
        """Save label encoder for inference"""
        Path("models").mkdir(exist_ok=True)
        
        with open(GestureModelConfig.LABEL_ENCODER_PATH, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print(f"💾 Label encoder saved: {GestureModelConfig.LABEL_ENCODER_PATH}")


class GestureCNNModel:
    """Lightweight CNN model for gesture classification"""
    
    def __init__(self):
        """Initialize model"""
        self.model = None
        self.history = None
    
    def build_model(self):
        """
        Build lightweight CNN architecture.
        
        Architecture (DataFlair-inspired, optimized for real-time):
            Conv2D(32, 3x3) -> ReLU -> MaxPool -> Dropout
            Conv2D(64, 3x3) -> ReLU -> MaxPool -> Dropout
            Conv2D(128, 3x3) -> ReLU -> MaxPool -> Dropout
            Flatten
            Dense(128) -> ReLU -> Dropout
            Dense(num_classes) -> Softmax
        
        Design principles:
            - Small kernel sizes for efficiency
            - Dropout for regularization (prevent overfitting to noisy data)
            - Batch normalization for training stability
            - Lightweight for real-time inference
        """
        print("\n🏗️  Building CNN model...")
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=GestureModelConfig.INPUT_SHAPE),
            
            # Conv Block 1
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Conv Block 2
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Conv Block 3
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Fully connected layers
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output layer
            layers.Dense(GestureModelConfig.NUM_CLASSES, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=GestureModelConfig.LEARNING_RATE),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        
        print("✅ Model built successfully")
        print(f"   Total parameters: {model.count_params():,}")
        model.summary()
        
        return model
    
    def train(self, X_train, y_train, X_val, y_val, datagen=None):
        """
        Train the CNN model with early stopping and learning rate scheduling.
        
        Safety mechanisms:
            - Early stopping: prevents overfitting
            - Model checkpointing: saves best model only
            - Learning rate reduction: adapts to training plateau
        """
        print("\n🚀 Starting training...")
        
        # Create models directory
        Path("models").mkdir(exist_ok=True)
        
        # Callbacks
        callbacks = [
            # Early stopping: stop if val_loss doesn't improve
            EarlyStopping(
                monitor='val_loss',
                patience=GestureModelConfig.EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Save best model only
            ModelCheckpoint(
                GestureModelConfig.MODEL_PATH,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            
            # Reduce learning rate on plateau
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train with or without data augmentation
        if datagen is not None:
            print("  Using data augmentation for robustness")
            history = self.model.fit(
                datagen.flow(X_train, y_train, batch_size=GestureModelConfig.BATCH_SIZE),
                epochs=GestureModelConfig.EPOCHS,
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                verbose=1
            )
        else:
            history = self.model.fit(
                X_train, y_train,
                batch_size=GestureModelConfig.BATCH_SIZE,
                epochs=GestureModelConfig.EPOCHS,
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                verbose=1
            )
        
        self.history = history
        print("\n✅ Training complete!")
        
        return history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        print("\n📊 Evaluating model on test set...")
        
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"  Test Loss: {test_loss:.4f}")
        print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        # Generate predictions
        y_pred_probs = self.model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_pred_probs, axis=1)
        
        # Classification report
        print("\n📋 Classification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=GestureModelConfig.GESTURES,
            digits=4
        ))
        
        return test_accuracy, y_pred
    
    def save_training_history(self):
        """Save training history for analysis"""
        if self.history is not None:
            with open(GestureModelConfig.TRAINING_HISTORY_PATH, 'wb') as f:
                pickle.dump(self.history.history, f)
            print(f"💾 Training history saved: {GestureModelConfig.TRAINING_HISTORY_PATH}")
    
    def plot_training_history(self):
        """Plot training curves"""
        if self.history is None:
            print("⚠️  No training history available")
            return
        
        history = self.history.history
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy plot
        ax1.plot(history['accuracy'], label='Train Accuracy')
        ax1.plot(history['val_accuracy'], label='Val Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(history['loss'], label='Train Loss')
        ax2.plot(history['val_loss'], label='Val Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('models/training_curves.png', dpi=150)
        print("📊 Training curves saved: models/training_curves.png")
        plt.close()
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=GestureModelConfig.GESTURES,
            yticklabels=GestureModelConfig.GESTURES
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('models/confusion_matrix.png', dpi=150)
        print("📊 Confusion matrix saved: models/confusion_matrix.png")
        plt.close()


def main():
    """Main training pipeline"""
    print("\n" + "="*70)
    print("  GESTURA CNN TRAINING PIPELINE")
    print("="*70 + "\n")
    
    # Set random seeds for reproducibility
    np.random.seed(GestureModelConfig.RANDOM_SEED)
    tf.random.set_seed(GestureModelConfig.RANDOM_SEED)
    
    # Step 1: Load dataset
    data_loader = GestureDataLoader()
    X, y = data_loader.load_dataset()
    
    # Check if dataset is sufficient
    if len(X) < 100:
        print("❌ Error: Insufficient data. Collect more images using collect_gesture_dataset.py")
        return
    
    # Step 2: Split dataset
    X_train, X_val, X_test, y_train, y_val, y_test = data_loader.split_dataset(X, y)
    
    # Step 3: Create data augmentation
    datagen = data_loader.create_data_augmentation()
    datagen.fit(X_train)
    
    # Step 4: Build model
    cnn_model = GestureCNNModel()
    cnn_model.build_model()
    
    # Step 5: Train model
    cnn_model.train(X_train, y_train, X_val, y_val, datagen=datagen)
    
    # Step 6: Evaluate model
    test_accuracy, y_pred = cnn_model.evaluate(X_test, y_test)
    
    # Step 7: Save artifacts
    data_loader.save_label_encoder()
    cnn_model.save_training_history()
    
    # Step 8: Generate plots
    cnn_model.plot_training_history()
    cnn_model.plot_confusion_matrix(y_test, y_pred)
    
    # Summary
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)
    print(f"✅ Model saved: {GestureModelConfig.MODEL_PATH}")
    print(f"✅ Label encoder saved: {GestureModelConfig.LABEL_ENCODER_PATH}")
    print(f"✅ Test accuracy: {test_accuracy*100:.2f}%")
    print("\nNext steps:")
    print("  1. Review training curves: models/training_curves.png")
    print("  2. Check confusion matrix: models/confusion_matrix.png")
    print("  3. Integrate model into Gestura using gesture_model_inference.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
