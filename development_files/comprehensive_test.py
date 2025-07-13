#!/usr/bin/env python3
"""
Comprehensive Test Suite for Random Forest File Classifier
Tests the improved classifier with various file types and shows detailed results.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pandas as pd
from random_forest_classifier import RandomForestFileClassifier

def create_test_files():
    """Create a comprehensive set of test files with realistic content."""
    
    # Create temporary directory for test files
    test_dir = tempfile.mkdtemp(prefix="file_classifier_test_")
    
    # Define test files with realistic names and sizes
    test_files = {
        # Education files
        'calculus_homework_assignment.pdf': (45000, b'%PDF-1.4 calculus assignment content'),
        'computer_science_lecture_notes.docx': (67000, b'PK computer science notes content'),
        'biology_lab_report_2024.txt': (23000, b'Biology Lab Report - Cell Division'),
        'python_programming_tutorial.py': (15000, b'# Python Tutorial\ndef main():\n    pass'),
        'machine_learning_dataset.csv': (234000, b'feature1,feature2,label\n1,2,A\n3,4,B'),
        
        # Movies files
        'avengers_endgame_4k_bluray.mkv': (8900000000, b'movie content here'),
        'the_matrix_trilogy_collection.mp4': (5600000000, b'matrix movie collection'),
        'star_wars_new_hope_remastered.avi': (4300000000, b'star wars content'),
        'lord_of_rings_extended_edition.mov': (7800000000, b'lotr extended content'),
        'inception_directors_cut_imax.mp4': (6200000000, b'inception movie content'),
        
        # Games files
        'cyberpunk_2077_goty_edition.exe': (78000000000, b'MZ cyberpunk game installer'),
        'minecraft_java_edition_mods.zip': (12000000000, b'PK minecraft mods package'),
        'call_of_duty_modern_warfare.iso': (89000000000, b'call of duty game iso'),
        'the_witcher_3_complete_edition.rar': (67000000000, b'Rar! witcher game files'),
        'fortnite_battle_royale_update.7z': (23000000000, b'7z fortnite update files'),
        
        # Apps files
        'microsoft_office_365_professional.msi': (3400000000, b'Microsoft Office installer'),
        'adobe_photoshop_2024_creative.exe': (2800000000, b'MZ adobe photoshop installer'),
        'visual_studio_code_extensions.zip': (567000000, b'PK vscode extensions package'),
        'google_chrome_enterprise_browser.pkg': (234000000, b'chrome browser package'),
        'zoom_meetings_professional.dmg': (345000000, b'zoom application package'),
        
        # Entertainment files
        'spotify_premium_music_collection.mp3': (890000000, b'ID3 music collection'),
        'netflix_series_binge_watch.mkv': (23000000000, b'netflix series content'),
        'youtube_viral_compilation.mp4': (5600000000, b'youtube compilation video'),
        'podcast_true_crime_archive.wav': (1200000000, b'RIFF podcast audio content'),
        'tiktok_trending_videos.webm': (3400000000, b'tiktok video compilation'),
        
        # Career files
        'software_engineer_resume_2024.pdf': (145000, b'%PDF-1.4 professional resume'),
        'cover_letter_tech_company.docx': (23000, b'PK cover letter content'),
        'linkedin_profile_optimization.txt': (34000, b'LinkedIn Profile Guide'),
        'job_interview_preparation.pptx': (567000, b'PK interview prep slides'),
        'portfolio_web_development.zip': (12000000, b'PK web development portfolio'),
        
        # Finance files
        'tax_returns_2024_complete.pdf': (234000, b'%PDF-1.4 tax return document'),
        'investment_portfolio_analysis.xlsx': (345000, b'PK investment analysis'),
        'monthly_budget_tracker.csv': (45000, b'date,category,amount\n2024-01-01,groceries,150'),
        'mortgage_payment_schedule.docx': (123000, b'PK mortgage payment document'),
        'cryptocurrency_trading_log.xlsx': (89000, b'PK crypto trading spreadsheet'),
        
        # Others files
        'system_backup_full_archive.tar.gz': (45000000000, b'backup archive content'),
        'server_logs_december_2024.log': (234000000, b'[2024-12-01] Server log entries'),
        'database_dump_production.sql': (12000000000, b'-- Database dump\nCREATE TABLE'),
        'configuration_settings.json': (23000, b'{"config": {"setting1": "value1"}}'),
        'api_documentation_swagger.yaml': (45000, b'swagger: "2.0"\ninfo:\n  title: API')
    }
    
    print(f"📁 Creating {len(test_files)} test files in {test_dir}")
    
    created_files = []
    for filename, (size, content) in test_files.items():
        file_path = os.path.join(test_dir, filename)
        
        # Write file with appropriate size
        with open(file_path, 'wb') as f:
            # Write actual content first
            f.write(content)
            
            # Pad with zeros to reach target size
            remaining = size - len(content)
            if remaining > 0:
                chunk_size = min(remaining, 1024 * 1024)  # 1MB chunks
                while remaining > 0:
                    write_size = min(chunk_size, remaining)
                    f.write(b'\0' * write_size)
                    remaining -= write_size
        
        created_files.append(file_path)
    
    return test_dir, created_files

def run_comprehensive_test():
    """Run comprehensive test suite."""
    
    print("🧪 COMPREHENSIVE RANDOM FOREST FILE CLASSIFIER TEST")
    print("=" * 60)
    
    # Check if model exists
    model_path = 'rf_file_classifier.joblib'
    if not os.path.exists(model_path):
        print("❌ Model file not found. Training new model...")
        
        # Train model first
        classifier = RandomForestFileClassifier(n_estimators=150, random_state=42)
        csv_path = 'train.csv'
        if os.path.exists(csv_path):
            classifier.train(csv_path)
            classifier.save_model()
        else:
            print("❌ Training data not found. Please run training first.")
            return
    
    # Load the trained model
    classifier = RandomForestFileClassifier()
    classifier.load_model(model_path)
    
    print(f"✅ Model loaded successfully!")
    print(f"📊 Model info:")
    print(f"   - Trees: {classifier.rf_model.n_estimators}")
    print(f"   - Features: {len(classifier.feature_names)}")
    print(f"   - Categories: {len(classifier.label_encoder.classes_)}")
    
    # Create test files
    test_dir, test_files = create_test_files()
    
    try:
        print(f"\n🔍 TESTING {len(test_files)} FILES")
        print("-" * 60)
        
        # Track results by category
        results_by_category = {}
        all_results = []
        
        for file_path in test_files:
            try:
                result = classifier.predict(file_path)
                
                filename = result['filename']
                predicted = result['predicted_category']
                confidence = result['confidence']
                
                # Determine expected category from filename
                expected = determine_expected_category(filename)
                
                # Store result
                result_info = {
                    'filename': filename,
                    'expected': expected,
                    'predicted': predicted,
                    'confidence': confidence,
                    'correct': expected == predicted,
                    'all_probabilities': result['all_probabilities']
                }
                
                all_results.append(result_info)
                
                if expected not in results_by_category:
                    results_by_category[expected] = []
                results_by_category[expected].append(result_info)
                
                # Print result
                status = "✅" if expected == predicted else "❌"
                confidence_bar = "█" * int(confidence * 20)
                print(f"{status} {filename[:40]:<40} | {expected:<12} → {predicted:<12} | {confidence:.3f} {confidence_bar}")
                
            except Exception as e:
                print(f"❌ Error testing {os.path.basename(file_path)}: {e}")
        
        # Calculate and display statistics
        print(f"\n📊 DETAILED RESULTS BY CATEGORY")
        print("=" * 60)
        
        total_correct = 0
        total_files = 0
        category_stats = {}
        
        for category in sorted(results_by_category.keys()):
            results = results_by_category[category]
            correct = sum(1 for r in results if r['correct'])
            total = len(results)
            accuracy = correct / total if total > 0 else 0
            avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
            
            category_stats[category] = {
                'correct': correct,
                'total': total,
                'accuracy': accuracy,
                'avg_confidence': avg_confidence
            }
            
            total_correct += correct
            total_files += total
            
            print(f"📁 {category:<12} | {correct:>2}/{total:<2} | {accuracy:>5.1%} | Conf: {avg_confidence:.3f}")
        
        overall_accuracy = total_correct / total_files if total_files > 0 else 0
        
        print(f"\n🎯 OVERALL PERFORMANCE")
        print("-" * 30)
        print(f"Total Files:     {total_files}")
        print(f"Correct:         {total_correct}")
        print(f"Accuracy:        {overall_accuracy:.1%}")
        print(f"Average Conf:    {sum(r['confidence'] for r in all_results) / len(all_results):.3f}")
        
        # Show top confusing cases
        print(f"\n🔍 ANALYSIS - MISCLASSIFIED FILES")
        print("-" * 40)
        
        incorrect_results = [r for r in all_results if not r['correct']]
        
        if incorrect_results:
            for result in sorted(incorrect_results, key=lambda x: x['confidence'], reverse=True):
                print(f"❌ {result['filename'][:35]:<35}")
                print(f"   Expected: {result['expected']:<12} | Predicted: {result['predicted']:<12} | Conf: {result['confidence']:.3f}")
                
                # Show top 3 probabilities
                sorted_probs = sorted(result['all_probabilities'].items(), key=lambda x: x[1], reverse=True)
                print(f"   Top predictions: ", end="")
                for i, (cat, prob) in enumerate(sorted_probs[:3]):
                    if i > 0:
                        print(", ", end="")
                    print(f"{cat}: {prob:.3f}", end="")
                print()
                print()
        else:
            print("🎉 No misclassified files!")
        
        # Show feature importance
        print(f"\n🎯 TOP FEATURE IMPORTANCE")
        print("-" * 30)
        
        feature_importance = classifier.get_feature_importance()
        for i, (feature, importance) in enumerate(list(feature_importance.items())[:10]):
            print(f"{i+1:>2}. {feature:<25} {importance:.4f}")
        
        print(f"\n✅ Test completed successfully!")
        print(f"📁 Test files created in: {test_dir}")
        
    finally:
        # Clean up test files
        print(f"\n🧹 Cleaning up test files...")
        shutil.rmtree(test_dir)

def determine_expected_category(filename):
    """Determine expected category based on filename patterns."""
    filename_lower = filename.lower()
    
    # Education keywords
    if any(word in filename_lower for word in ['assignment', 'homework', 'lecture', 'notes', 'tutorial', 'lab', 'report', 'calculus', 'computer', 'science', 'biology', 'python', 'programming', 'machine', 'learning']):
        return 'Education'
    
    # Movies keywords
    elif any(word in filename_lower for word in ['avengers', 'matrix', 'star', 'wars', 'lord', 'rings', 'inception', 'movie', 'bluray', '4k', 'remastered', 'directors', 'cut', 'imax', 'trilogy', 'collection']):
        return 'Movies'
    
    # Games keywords
    elif any(word in filename_lower for word in ['cyberpunk', 'minecraft', 'call', 'duty', 'witcher', 'fortnite', 'game', 'goty', 'edition', 'mods']):
        return 'Games'
    
    # Apps keywords
    elif any(word in filename_lower for word in ['microsoft', 'office', 'adobe', 'photoshop', 'visual', 'studio', 'google', 'chrome', 'zoom', 'professional', 'enterprise', 'browser']):
        return 'Apps'
    
    # Entertainment keywords
    elif any(word in filename_lower for word in ['spotify', 'netflix', 'youtube', 'podcast', 'tiktok', 'music', 'viral', 'trending', 'series', 'compilation']):
        return 'Entertainment'
    
    # Career keywords
    elif any(word in filename_lower for word in ['resume', 'cover', 'letter', 'linkedin', 'job', 'interview', 'portfolio', 'engineer', 'preparation']):
        return 'Career'
    
    # Finance keywords
    elif any(word in filename_lower for word in ['tax', 'investment', 'budget', 'mortgage', 'cryptocurrency', 'trading', 'financial', 'portfolio', 'analysis']):
        return 'Finance'
    
    # Others
    else:
        return 'Others'

if __name__ == "__main__":
    run_comprehensive_test()
