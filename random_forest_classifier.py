"""
Random Forest File Classifier
Trains a Random Forest model on file features to classify files into folders.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from typing import Dict, List, Tuple, Optional
import json

class RandomForestFileClassifier:
    """Random Forest based file classifier."""
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """
        Initialize Random Forest classifier.
        
        Args:
            n_estimators: Number of trees in forest
            random_state: Random seed for reproducibility
        """
        self.rf_model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced'  # Handle class imbalance
        )
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        self.extension_mapping = {}  # Store extension to number mapping
        self.is_trained = False
        
        # Categories mapping
        self.categories = {
            'Education': 'Education and Finance',
            'Movies': 'Movies', 
            'Games': 'Games',
            'Apps': 'Apps',
            'Entertainment': 'Entertainment',
            'Career': 'Career',
            'Finance': 'Education and Finance',
            'Others': 'Others'
        }
    
    def load_data(self, csv_path: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load training data from CSV.
        
        Args:
            csv_path: Path to training CSV file
            
        Returns:
            Features DataFrame and labels Series
        """
        print(f"📊 Loading training data from {csv_path}...")
        
        df = pd.read_csv(csv_path)
        print(f"   Loaded {len(df)} samples with {len(df.columns)} columns")
        
        # Separate features and labels
        X = df.drop(['filename', 'label'], axis=1)  # Remove filename and label
        y = df['label']
        
        # Encode categorical features
        # Extension encoding
        if 'extension' in X.columns:
            # Get unique extensions and create mapping
            unique_extensions = X['extension'].unique()
            self.extension_mapping = {ext: i for i, ext in enumerate(unique_extensions)}
            X['extension'] = X['extension'].map(self.extension_mapping)
        
        # Convert size_category to numeric if it's string
        if 'size_category' in X.columns and X['size_category'].dtype == 'object':
            size_map = {'tiny': 0, 'small': 1, 'medium': 2, 'large': 3, 'huge': 4}
            X['size_category'] = X['size_category'].map(size_map).fillna(0)
        
        # Store feature names
        self.feature_names = list(X.columns)
        
        print(f"   Features: {len(X.columns)}")
        print(f"   Classes: {list(y.unique())}")
        print(f"   Class distribution:")
        for label, count in y.value_counts().items():
            print(f"     {label}: {count}")
        
        return X, y
    
    def train(self, csv_path: str) -> Dict:
        """
        Train the Random Forest model.
        
        Args:
            csv_path: Path to training CSV file
            
        Returns:
            Training metrics dictionary
        """
        print("🌲 Training Random Forest File Classifier")
        print("=" * 50)
        
        # Load data
        X, y = self.load_data(csv_path)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        print(f"📈 Training set: {len(X_train)} samples")
        print(f"🧪 Test set: {len(X_test)} samples")
        
        # Train model
        print("🔄 Training Random Forest...")
        self.rf_model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model
        print("📋 Evaluating model...")
        
        # Training accuracy
        train_score = self.rf_model.score(X_train, y_train)
        
        # Test accuracy
        test_score = self.rf_model.score(X_test, y_test)
        
        # Cross-validation
        cv_scores = cross_val_score(self.rf_model, X, y_encoded, cv=5)
        
        # Predictions for detailed metrics
        y_pred = self.rf_model.predict(X_test)
        
        # Feature importance
        feature_importance = dict(zip(
            self.feature_names, 
            self.rf_model.feature_importances_
        ))
        
        # Sort by importance
        sorted_features = sorted(feature_importance.items(), 
                               key=lambda x: x[1], reverse=True)
        
        # Print results
        print(f"\n✅ Training completed!")
        print(f"   Training accuracy: {train_score:.3f}")
        print(f"   Test accuracy: {test_score:.3f}")
        print(f"   Cross-validation: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        print(f"\n🎯 Top 10 Most Important Features:")
        for feature, importance in sorted_features[:10]:
            print(f"   {feature}: {importance:.4f}")
        
        # Classification report
        class_names = self.label_encoder.inverse_transform(range(len(self.label_encoder.classes_)))
        print(f"\n📊 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Return metrics
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': sorted_features,
            'n_samples': len(X),
            'n_features': len(self.feature_names)
        }
    
    def extract_features_from_file(self, file_path: str) -> pd.DataFrame:
        """
        Extract features from a real file for prediction - matches training format exactly.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Feature DataFrame with proper column names
        """
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0].lower()
        extension = os.path.splitext(filename)[1].lower()
        
        try:
            size_bytes = os.path.getsize(file_path)
        except:
            size_bytes = 0
        
        # Size category - match training data exactly
        if size_bytes <= 1024:
            size_category = 0  # tiny
        elif size_bytes <= 100000:
            size_category = 1  # small
        elif size_bytes <= 10000000:
            size_category = 2  # medium
        elif size_bytes <= 100000000:
            size_category = 3  # large
        else:
            size_category = 4  # huge
        
        # Keywords for each category - match training data
        category_keywords = {
            'education': ['assignment', 'notes', 'class', 'syllabus', 'exam', 'lecture', 'worksheet', 'college', 'study', 'textbook', 'tutorial', 'course', 'homework', 'quiz', 'test', 'university', 'school', 'academic', 'research', 'thesis', 'dissertation', 'math', 'science', 'biology', 'chemistry', 'physics', 'computer', 'programming', 'algorithm', 'data', 'statistics'],
            'movies': ['movie', 'film', 'trailer', 'cinema', 'hd', 'bluray', 'dvd', '4k', 'action', 'comedy', 'drama', 'horror', 'thriller', 'adventure', 'fantasy', 'scifi', 'romance', 'animation', 'documentary', 'imax', 'extended', 'directors', 'cut', 'unrated', 'remastered'],
            'games': ['game', 'gaming', 'setup', 'install', 'launcher', 'steam', 'epic', 'origin', 'battle', 'playstation', 'xbox', 'nintendo', 'mod', 'patch', 'dlc', 'expansion', 'multiplayer', 'online', 'rpg', 'fps', 'strategy', 'puzzle', 'arcade', 'simulation', 'sports'],
            'apps': ['app', 'application', 'software', 'program', 'tool', 'utility', 'installer', 'setup', 'exe', 'dmg', 'pkg', 'deb', 'rpm', 'snap', 'flatpak', 'portable', 'professional', 'enterprise', 'business', 'productivity', 'editor', 'browser', 'client'],
            'entertainment': ['music', 'song', 'audio', 'video', 'entertainment', 'comedy', 'funny', 'viral', 'trending', 'podcast', 'stream', 'live', 'concert', 'album', 'playlist', 'mix', 'dance', 'party', 'show', 'series', 'episode', 'channel', 'youtube', 'tiktok', 'instagram'],
            'career': ['resume', 'cv', 'career', 'job', 'work', 'professional', 'interview', 'application', 'cover', 'letter', 'linkedin', 'portfolio', 'project', 'skill', 'certification', 'training', 'development', 'management', 'leadership', 'performance', 'review', 'promotion', 'salary', 'negotiation'],
            'finance': ['finance', 'financial', 'money', 'bank', 'banking', 'invoice', 'bill', 'receipt', 'statement', 'tax', 'salary', 'payroll', 'budget', 'expense', 'income', 'investment', 'stock', 'crypto', 'currency', 'loan', 'mortgage', 'insurance', 'audit', 'accounting'],
            'others': ['temp', 'temporary', 'cache', 'data', 'config', 'system', 'log', 'backup', 'archive', 'database', 'misc', 'other', 'unknown', 'file', 'document', 'folder', 'directory', 'settings', 'preferences', 'metadata', 'info', 'readme', 'license', 'changelog']
        }
        
        # Extension matches - match training data
        category_extensions = {
            'education': ['.pdf', '.docx', '.pptx', '.txt', '.doc', '.ppt', '.rtf', '.tex', '.epub', '.bib'],
            'movies': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
            'games': ['.exe', '.zip', '.rar', '.7z', '.iso', '.msi', '.apk', '.dmg', '.pkg', '.deb'],
            'apps': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.snap', '.flatpak', '.appimage', '.tar.gz'],
            'entertainment': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.mp4', '.webm', '.mkv'],
            'career': ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt'],
            'finance': ['.pdf', '.xlsx', '.xls', '.csv', '.txt', '.docx'],
            'others': ['.dat', '.bin', '.tmp', '.log', '.cfg', '.ini', '.xml', '.json', '.db', '.sqlite', '.bak', '.old']
        }
        
        # Count keywords for each category
        keyword_counts = {}
        for category, keywords in category_keywords.items():
            count = sum(1 for keyword in keywords if keyword in name_without_ext)
            keyword_counts[f'keywords_{category}'] = count
        
        # Extension matches for each category
        ext_matches = {}
        for category, extensions in category_extensions.items():
            ext_matches[f'ext_match_{category}'] = 1 if extension in extensions else 0
        
        # Create feature dictionary
        features = {
            'extension': extension,
            'name_length': len(name_without_ext),
            'size_bytes': size_bytes,
            'size_category': size_category,
            'has_numbers': 1 if any(c.isdigit() for c in name_without_ext) else 0,
            'has_underscore': name_without_ext.count('_'),
            'has_dash': name_without_ext.count('-'),
            'word_count': len([w for w in name_without_ext.replace('_', ' ').replace('-', ' ').split() if w])
        }
        
        # Add keyword and extension features
        features.update(keyword_counts)
        features.update(ext_matches)
        
        # Convert to DataFrame with proper column names
        df = pd.DataFrame([features])
        
        # Ensure all training columns are present
        for col in self.feature_names:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data
        df = df[self.feature_names]
        
        # Handle extension encoding
        if 'extension' in df.columns:
            df['extension'] = df['extension'].map(self.extension_mapping).fillna(-1)
        
        return df
    
    def predict(self, file_path: str) -> Dict:
        """
        Predict the folder category for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Prediction dictionary with category and confidence
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load_model().")
        
        # Extract features
        features_df = self.extract_features_from_file(file_path)
        
        # Get prediction probabilities
        probabilities = self.rf_model.predict_proba(features_df)[0]
        
        # Get predicted class
        predicted_class_idx = np.argmax(probabilities)
        predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]
        
        # Convert Finance to Education (simplification for better UX)
        if predicted_class == 'Finance':
            predicted_class = 'Education'
            # Find Education class index for confidence
            try:
                education_idx = list(self.label_encoder.classes_).index('Education')
                confidence = probabilities[education_idx]
            except ValueError:
                confidence = probabilities[predicted_class_idx]
        else:
            confidence = probabilities[predicted_class_idx]
        
        # Create probability dictionary
        prob_dict = {}
        for i, class_name in enumerate(self.label_encoder.classes_):
            actual_name = self.label_encoder.inverse_transform([i])[0]
            # Convert Finance probabilities to Education
            if actual_name == 'Finance':
                if 'Education' in prob_dict:
                    prob_dict['Education'] += probabilities[i]
                else:
                    prob_dict['Education'] = probabilities[i]
            else:
                prob_dict[actual_name] = probabilities[i]
        
        return {
            'filename': os.path.basename(file_path),
            'predicted_category': predicted_class,
            'folder_name': self.get_folder_name(predicted_class),
            'confidence': confidence,
            'all_probabilities': prob_dict
        }
    
    def predict_batch(self, file_paths: List[str]) -> List[Dict]:
        """
        Predict categories for multiple files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.predict(file_path)
                results.append(result)
            except Exception as e:
                results.append({
                    'filename': os.path.basename(file_path),
                    'predicted_category': 'Others',
                    'confidence': 0.0,
                    'error': str(e)
                })
        return results
    
    def save_model(self, model_path: str = 'rf_file_classifier.joblib'):
        """Save trained model to disk."""
        if not self.is_trained:
            print("❌ No trained model to save!")
            return
        
        model_data = {
            'rf_model': self.rf_model,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'extension_mapping': self.extension_mapping,
            'categories': self.categories
        }
        
        joblib.dump(model_data, model_path)
        print(f"💾 Model saved to {model_path}")
    
    def load_model(self, model_path: str = 'rf_file_classifier.joblib'):
        """Load trained model from disk."""
        try:
            model_data = joblib.load(model_path)
            
            self.rf_model = model_data['rf_model']
            self.label_encoder = model_data['label_encoder']
            self.feature_names = model_data['feature_names']
            self.extension_mapping = model_data.get('extension_mapping', {})
            self.categories = model_data['categories']
            self.is_trained = True
            
            print(f"📚 Model loaded from {model_path}")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from trained model."""
        if not self.is_trained:
            return {}
        
        importance_dict = dict(zip(
            self.feature_names,
            self.rf_model.feature_importances_
        ))
        
        return dict(sorted(importance_dict.items(), 
                          key=lambda x: x[1], reverse=True))
    
    def get_folder_name(self, predicted_category: str) -> str:
        """Get the folder name for organizing files based on predicted category."""
        # Always map Education and Finance to "Education and Finance"
        if predicted_category in ['Education', 'Finance']:
            return 'Education and Finance'
        return self.categories.get(predicted_category, predicted_category)


def main():
    """Main function to train and test the Random Forest classifier."""
    
    # Create classifier
    classifier = RandomForestFileClassifier(n_estimators=150, random_state=42)
    
    # Train model
    csv_path = 'train.csv'
    if not os.path.exists(csv_path):
        print(f"❌ Training data file not found: {csv_path}")
        return
    
    # Train the model
    metrics = classifier.train(csv_path)
    
    # Save model
    classifier.save_model()
    
    # Test with some example predictions
    print(f"\n🧪 Testing Predictions:")
    print("-" * 30)
    
    # Create some test files for demonstration
    test_examples = [
        "assignment_math_2024.pdf",
        "movie_action_hd.mp4", 
        "game_setup.exe",
        "resume_engineer.docx",
        "invoice_jan_2024.pdf",
        "music_album.mp3"
    ]
    
    for example in test_examples:
        # For demo, we'll just predict based on filename patterns
        # In real usage, these would be actual file paths
        print(f"\n📄 File: {example}")
        
        # Create a temporary file for testing
        temp_path = f"/tmp/{example}"
        try:
            with open(temp_path, 'w') as f:
                f.write("sample content")
            
            result = classifier.predict(temp_path)
            print(f"   Predicted: {result['predicted_category']}")
            print(f"   Confidence: {result['confidence']:.3f}")
            print(f"   Top 3 probabilities:")
            
            sorted_probs = sorted(result['all_probabilities'].items(), 
                                key=lambda x: x[1], reverse=True)
            for category, prob in sorted_probs[:3]:
                print(f"     {category}: {prob:.3f}")
            
            # Clean up
            os.remove(temp_path)
            
        except Exception as e:
            print(f"   Error: {e}")
    
    print(f"\n🎉 Random Forest File Classifier ready!")
    print(f"📊 Final test accuracy: {metrics['test_accuracy']:.3f}")
    print(f"🌲 Model uses {classifier.rf_model.n_estimators} trees")
    print(f"💾 Model saved and ready for use!")


if __name__ == "__main__":
    main()
