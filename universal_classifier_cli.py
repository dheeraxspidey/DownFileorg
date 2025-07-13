#!/usr/bin/env python3
"""
Universal File Classifier CLI
A flexible command-line interface for testing different file classification models.
Supports Random Forest and can be easily extended for CNN and other classifiers.
"""

import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile

# Import Random Forest classifier
try:
    from random_forest_classifier import RandomForestFileClassifier
except ImportError:
    print("Warning: RandomForestFileClassifier not available")
    RandomForestFileClassifier = None


class BaseClassifier:
    """Base class for all classifiers."""
    
    def __init__(self):
        self.name = "Base"
        self.is_loaded = False
    
    def load_model(self, model_path: str = None):
        """Load the trained model."""
        raise NotImplementedError
    
    def predict(self, filename: str, size_mb: float) -> Dict[str, Any]:
        """Predict category for given filename and size."""
        raise NotImplementedError
    
    def get_categories(self) -> list:
        """Return list of possible categories (Finance removed as it's treated as Education)."""
        return ['Education and Finance', 'Movies', 'Games', 'Apps', 'Entertainment', 'Career', 'Others']


class RandomForestClassifierWrapper(BaseClassifier):
    """Wrapper for Random Forest classifier."""
    
    def __init__(self):
        super().__init__()
        self.name = "Random Forest"
        self.classifier = None
    
    def load_model(self, model_path: str = "rf_file_classifier.joblib"):
        """Load the Random Forest model."""
        if RandomForestFileClassifier is None:
            raise ImportError("RandomForestFileClassifier not available")
        
        try:
            self.classifier = RandomForestFileClassifier()
            if os.path.exists(model_path):
                self.classifier.load_model(model_path)
                self.is_loaded = True
                print(f"✅ {self.name} model loaded from {model_path}")
            else:
                raise FileNotFoundError(f"Model file not found: {model_path}")
        except Exception as e:
            raise Exception(f"Failed to load {self.name} model: {e}")
    
    def predict(self, filename: str, size_mb: float) -> Dict[str, Any]:
        """Predict using Random Forest classifier."""
        if not self.is_loaded:
            raise Exception(f"{self.name} model not loaded")
        
        # Create a temporary file for prediction
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, filename)
        
        try:
            # Create file with specified size
            size_bytes = int(size_mb * 1024 * 1024)
            with open(temp_file, 'wb') as f:
                # Write some realistic content based on extension
                content = self._generate_content(filename, size_bytes)
                f.write(content)
                
                # Pad to reach target size
                remaining = size_bytes - len(content)
                if remaining > 0:
                    chunk_size = min(remaining, 1024 * 1024)
                    while remaining > 0:
                        write_size = min(chunk_size, remaining)
                        f.write(b'\0' * write_size)
                        remaining -= write_size
            
            # Get prediction
            result = self.classifier.predict(temp_file)
            
            return {
                'classifier': self.name,
                'filename': filename,
                'size_mb': size_mb,
                'predicted_category': result['predicted_category'],
                'folder_name': result.get('folder_name', result['predicted_category']),
                'confidence': result['confidence'],
                'all_probabilities': result['all_probabilities']
            }
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            os.rmdir(temp_dir)
    
    def _generate_content(self, filename: str, size_bytes: int) -> bytes:
        """Generate realistic file content based on extension."""
        ext = os.path.splitext(filename)[1].lower()
        
        # Generate appropriate content based on file type
        if ext == '.pdf':
            return b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        elif ext in ['.docx', '.doc']:
            return b'PK\x03\x04\x14\x00\x06\x00\x08\x00' + b'document content'
        elif ext in ['.mp4', '.mkv', '.avi']:
            return b'\x00\x00\x00\x20ftypmp4\x00' + b'movie content'
        elif ext in ['.mp3', '.wav']:
            return b'ID3\x03\x00\x00\x00' + b'audio content'
        elif ext in ['.exe', '.msi']:
            return b'MZ\x90\x00\x03\x00\x00\x00' + b'executable content'
        elif ext in ['.zip', '.rar']:
            return b'PK\x03\x04\x14\x00\x00\x00' + b'archive content'
        elif ext in ['.jpg', '.png']:
            return b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'image content'
        else:
            return b'generic file content'


class EnhancedRandomForestWrapper(RandomForestClassifierWrapper):
    """Enhanced Random Forest with rule-based post-processing for better Education vs Finance distinction."""
    
    def __init__(self):
        super().__init__()
        self.name = "Enhanced Random Forest"
    
    def predict(self, filename: str, size_mb: float) -> Dict[str, Any]:
        """Predict with enhanced rules for Education vs Finance."""
        # Get base prediction
        result = super().predict(filename, size_mb)
        
        # Apply enhancement rules only for PDFs
        if filename.lower().endswith('.pdf') and size_mb < 50:  # Small PDFs
            predicted = result['predicted_category']
            confidence = result['confidence']
            
            # Check if top 2 predictions are Education and Finance
            sorted_probs = sorted(result['all_probabilities'].items(), 
                                key=lambda x: x[1], reverse=True)
            top1, top2 = sorted_probs[0], sorted_probs[1]
            
            # If Education and Finance are top 2 and close in probability
            if {top1[0], top2[0]} == {'Education', 'Finance'} and abs(top1[1] - top2[1]) < 0.3:
                filename_lower = filename.lower()
                
                # Strong education indicators
                edu_indicators = [
                    'assignment', 'homework', 'notes', 'lecture', 'class', 'unit', 
                    'chapter', 'lesson', 'tutorial', 'exercise', 'quiz', 'test',
                    'exam', 'study', 'course', 'syllabus', 'lab', 'report',
                    'math', 'science', 'biology', 'chemistry', 'physics',
                    'computer', 'programming', 'calculus', 'algebra'
                ]
                
                # Strong finance indicators  
                finance_indicators = [
                    'tax', 'invoice', 'bill', 'receipt', 'statement', 'bank',
                    'salary', 'payroll', 'budget', 'expense', 'income',
                    'investment', 'loan', 'mortgage', 'insurance', 'audit'
                ]
                
                edu_score = sum(1 for indicator in edu_indicators if indicator in filename_lower)
                finance_score = sum(1 for indicator in finance_indicators if indicator in filename_lower)
                
                # Apply rules
                if edu_score > finance_score:
                    # Boost education probability
                    result['predicted_category'] = 'Education'
                    result['confidence'] = max(result['all_probabilities']['Education'] + 0.2, 0.7)
                    result['enhancement_applied'] = 'Education boosted due to educational keywords'
                elif finance_score > edu_score:
                    # Boost finance probability
                    result['predicted_category'] = 'Finance'
                    result['confidence'] = max(result['all_probabilities']['Finance'] + 0.2, 0.7)
                    result['enhancement_applied'] = 'Finance boosted due to financial keywords'
                elif size_mb < 5:  # Very small PDFs likely educational
                    if result['all_probabilities']['Education'] > 0.15:  # Has some education probability
                        result['predicted_category'] = 'Education'
                        result['confidence'] = max(result['all_probabilities']['Education'] + 0.15, 0.6)
                        result['enhancement_applied'] = 'Education boosted - small PDF likely educational'
        
        return result


class CNNClassifierWrapper(BaseClassifier):
    """Placeholder for CNN classifier - can be implemented later."""
    
    def __init__(self):
        super().__init__()
        self.name = "CNN"
        # CNN implementation would go here
    
    def load_model(self, model_path: str = "cnn_file_classifier.h5"):
        """Load CNN model (placeholder)."""
        # For now, just return a mock implementation
        print(f"🚧 {self.name} classifier not implemented yet")
        self.is_loaded = False
        raise NotImplementedError(f"{self.name} classifier not implemented")
    
    def predict(self, filename: str, size_mb: float) -> Dict[str, Any]:
        """CNN prediction (placeholder)."""
        # Mock prediction for testing
        return {
            'classifier': self.name,
            'filename': filename,
            'size_mb': size_mb,
            'predicted_category': 'Others',
            'confidence': 0.5,
            'all_probabilities': {cat: 0.125 for cat in self.get_categories()}
        }


class NaiveBayesClassifierWrapper(BaseClassifier):
    """Placeholder for Naive Bayes classifier - can be implemented later."""
    
    def __init__(self):
        super().__init__()
        self.name = "Naive Bayes"
    
    def load_model(self, model_path: str = "nb_file_classifier.pkl"):
        """Load Naive Bayes model (placeholder)."""
        print(f"🚧 {self.name} classifier not implemented yet")
        self.is_loaded = False
        raise NotImplementedError(f"{self.name} classifier not implemented")
    
    def predict(self, filename: str, size_mb: float) -> Dict[str, Any]:
        """Naive Bayes prediction (placeholder)."""
        return {
            'classifier': self.name,
            'filename': filename,
            'size_mb': size_mb,
            'predicted_category': 'Others',
            'confidence': 0.3,
            'all_probabilities': {cat: 0.125 for cat in self.get_categories()}
        }


def get_classifier(classifier_name: str) -> BaseClassifier:
    """Factory function to get classifier by name."""
    classifiers = {
        'rf': RandomForestClassifierWrapper,
        'random-forest': RandomForestClassifierWrapper,
        'cnn': CNNClassifierWrapper,
        'nb': NaiveBayesClassifierWrapper,
        'naive-bayes': NaiveBayesClassifierWrapper
    }
    
    classifier_name = classifier_name.lower()
    if classifier_name not in classifiers:
        available = ', '.join(classifiers.keys())
        raise ValueError(f"Unknown classifier: {classifier_name}. Available: {available}")
    
    return classifiers[classifier_name]()


def format_output(result: Dict[str, Any], format_type: str = 'pretty') -> str:
    """Format prediction result for output."""
    if format_type == 'json':
        return json.dumps(result, indent=2)
    
    elif format_type == 'csv':
        return f"{result['filename']},{result['size_mb']},{result['predicted_category']},{result['confidence']:.3f}"
    
    else:  # pretty format
        output = []
        output.append(f"📄 File Analysis")
        output.append(f"=" * 50)
        output.append(f"Classifier:    {result['classifier']}")
        output.append(f"Filename:      {result['filename']}")
        output.append(f"Size:          {result['size_mb']} MB")
        output.append(f"Folder:        {result.get('folder_name', result['predicted_category'])}")
        output.append(f"Confidence:    {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        
        # Show confidence bar
        bar_length = 20
        filled = int(result['confidence'] * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        output.append(f"               {bar}")
        
        output.append(f"\n📊 All Probabilities:")
        sorted_probs = sorted(result['all_probabilities'].items(), 
                            key=lambda x: x[1], reverse=True)
        
        for i, (category, prob) in enumerate(sorted_probs):
            marker = "→" if category == result['predicted_category'] else " "
            output.append(f"  {marker} {category:<12} {prob:.3f} ({prob*100:.1f}%)")
        
        return "\n".join(output)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Universal File Classifier CLI - Test different ML models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf 2.5                    # Use default Random Forest
  %(prog)s movie.mp4 1500 -c cnn               # Use CNN classifier
  %(prog)s -f files.txt -c rf -o results.json  # Batch process with JSON output
  %(prog)s game.exe 500 --format csv           # CSV output format

Available Classifiers:
  rf, random-forest    - Random Forest (default)
  cnn                  - Convolutional Neural Network (planned)
  nb, naive-bayes      - Naive Bayes (planned)
        """
    )
    
    # Input arguments
    parser.add_argument('filename', nargs='?', help='Name of the file to classify')
    parser.add_argument('size_mb', nargs='?', type=float, help='Size of file in MB')
    
    # Classifier selection
    parser.add_argument('-c', '--classifier', default='rf',
                       help='Classifier to use (default: rf)')
    
    # Model path
    parser.add_argument('-m', '--model', help='Path to model file (optional)')
    
    # Batch processing
    parser.add_argument('-f', '--file', help='File containing filename,size_mb pairs')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--format', choices=['pretty', 'json', 'csv'], 
                       default='pretty', help='Output format')
    
    # Other options
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Verbose output')
    parser.add_argument('--list-classifiers', action='store_true',
                       help='List available classifiers and exit')
    
    args = parser.parse_args()
    
    # List classifiers
    if args.list_classifiers:
        print("Available Classifiers:")
        print("  rf, random-forest    - Random Forest")
        print("  cnn                  - CNN (not implemented)")
        print("  nb, naive-bayes      - Naive Bayes (not implemented)")
        return
    
    # Validate input
    if not args.file and (not args.filename or args.size_mb is None):
        parser.error("Either provide filename and size_mb, or use --file for batch processing")
    
    try:
        # Initialize classifier
        classifier = get_classifier(args.classifier)
        
        # Load model
        if args.model:
            classifier.load_model(args.model)
        else:
            classifier.load_model()  # Use default path
        
        results = []
        
        if args.file:
            # Batch processing
            if not os.path.exists(args.file):
                print(f"❌ Input file not found: {args.file}")
                return 1
            
            with open(args.file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    try:
                        parts = line.split(',')
                        if len(parts) != 2:
                            print(f"⚠️  Line {line_num}: Invalid format: {line}")
                            continue
                        
                        filename = parts[0].strip()
                        size_mb = float(parts[1].strip())
                        
                        result = classifier.predict(filename, size_mb)
                        results.append(result)
                        
                        if args.verbose:
                            print(f"✅ Processed: {filename}")
                        
                    except ValueError as e:
                        print(f"⚠️  Line {line_num}: {e}")
                        continue
        else:
            # Single file processing
            result = classifier.predict(args.filename, args.size_mb)
            results.append(result)
        
        # Format and output results
        if args.format == 'csv' and len(results) > 1:
            output_lines = ["filename,size_mb,predicted_category,confidence"]
            for result in results:
                output_lines.append(format_output(result, 'csv'))
            output = "\n".join(output_lines)
        elif args.format == 'json':
            if len(results) == 1:
                output = format_output(results[0], 'json')
            else:
                output = json.dumps(results, indent=2)
        else:
            output_lines = []
            for i, result in enumerate(results):
                if i > 0:
                    output_lines.append("\n" + "="*50 + "\n")
                output_lines.append(format_output(result, 'pretty'))
            output = "\n".join(output_lines)
        
        # Write output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"📝 Results written to {args.output}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
