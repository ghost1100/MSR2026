import pandas as pd
import numpy as np
import random

def create_comprehensive_pr_dataset():
    """
    Create a comprehensive dataset with 77 PRs from each agent
    Including all user data, PR details, and framework information
    """
    
    # Load the main dataset
    print("Loading main dataset...")
    df = pd.read_csv('data/raw/aidata.csv')
    
    print(f"Total dataset size: {len(df):,} PRs")
    print("Agent distribution:")
    agent_counts = df['agent'].value_counts()
    for agent, count in agent_counts.items():
        print(f"  {agent}: {count:,}")
    
    # Sample 77 PRs from each agent
    target_per_agent = 77
    sampled_data = []
    
    for agent in df['agent'].unique():
        agent_data = df[df['agent'] == agent].copy()
        
        if len(agent_data) >= target_per_agent:
            # Sample 77 random PRs from this agent
            sampled = agent_data.sample(n=target_per_agent, random_state=42)
            sampled_data.append(sampled)
            print(f"✓ Sampled {target_per_agent} PRs from {agent}")
        else:
            # Take all available if less than 77
            sampled_data.append(agent_data)
            print(f"⚠ Only {len(agent_data)} PRs available from {agent}")
    
    # Combine all sampled data
    final_sample = pd.concat(sampled_data, ignore_index=True)
    
    print(f"\nFinal sample size: {len(final_sample)} PRs")
    print("Final distribution:")
    final_counts = final_sample['agent'].value_counts()
    for agent, count in final_counts.items():
        print(f"  {agent}: {count}")
    
    # Create comprehensive analysis columns
    comprehensive_data = []
    
    for idx, row in final_sample.iterrows():
        # Extract all available information
        pr_record = {
            # Basic PR Information
            'pr_id': row.get('id', ''),
            'agent': row.get('agent', ''),
            'pr_number': row.get('number', ''),
            'pr_title': row.get('title', ''),
            'pr_body': row.get('body', ''),
            'html_url': row.get('html_url', ''),
            'api_url': row.get('url', ''),
            
            # User Information
            'user_id': row.get('user_id', ''),
            'username': row.get('user_login', ''),
            'user_avatar_url': row.get('user_avatar_url', ''),
            'user_type': row.get('user_type', ''),
            'user_site_admin': row.get('user_site_admin', ''),
            
            # Repository Information
            'repo_id': row.get('repo_id', ''),
            'repo_name': row.get('repo_name', ''),
            'repo_full_name': row.get('repo_full_name', ''),
            'repo_owner': row.get('repo_owner_login', ''),
            'repo_private': row.get('repo_private', ''),
            'repo_language': row.get('repo_language', ''),
            'repo_size': row.get('repo_size', ''),
            'repo_stargazers_count': row.get('repo_stargazers_count', ''),
            'repo_watchers_count': row.get('repo_watchers_count', ''),
            'repo_forks_count': row.get('repo_forks_count', ''),
            
            # PR Status and Timing
            'pr_state': row.get('state', ''),
            'pr_merged': row.get('merged', ''),
            'pr_mergeable': row.get('mergeable', ''),
            'pr_created_at': row.get('created_at', ''),
            'pr_updated_at': row.get('updated_at', ''),
            'pr_closed_at': row.get('closed_at', ''),
            'pr_merged_at': row.get('merged_at', ''),
            
            # PR Content Analysis
            'pr_additions': row.get('additions', ''),
            'pr_deletions': row.get('deletions', ''),
            'pr_changed_files': row.get('changed_files', ''),
            'pr_commits': row.get('commits', ''),
            'pr_comments': row.get('comments', ''),
            'pr_review_comments': row.get('review_comments', ''),
            
            # Branch Information
            'head_ref': row.get('head_ref', ''),
            'head_sha': row.get('head_sha', ''),
            'base_ref': row.get('base_ref', ''),
            'base_sha': row.get('base_sha', ''),
            
            # Manual Verification Fields (to be filled)
            'manual_testing_present': '',  # Yes/No/Partial
            'manual_test_types': '',  # unit/integration/e2e/etc
            'manual_test_frameworks': '',  # pytest/junit/jest/etc
            'manual_language_detected': '',  # Python/JavaScript/Java/etc
            'manual_framework_mentioned': '',  # React/Django/Spring/etc
            'manual_testing_keywords': '',  # List of testing keywords found
            'manual_code_quality_focus': '',  # Yes/No
            'manual_ci_cd_mentioned': '',  # Yes/No
            'manual_documentation_updated': '',  # Yes/No
            
            # Automatic Detection Results
            'auto_testing_keywords_count': 0,
            'auto_detected_language': '',
            'auto_framework_indicators': '',
            'auto_testing_confidence': '',
            
            # Reviewer Assessment
            'reviewer_name': '',
            'review_date': '',
            'review_confidence': '',  # High/Medium/Low
            'review_notes': '',
            'needs_second_review': '',  # Yes/No
            
            # Classification Results
            'final_testing_classification': '',  # Testing/Non-Testing/Ambiguous
            'final_language': '',
            'final_frameworks': '',
            'classification_rationale': ''
        }
        
        # Perform automatic keyword detection
        title_body = f"{str(row.get('title', ''))} {str(row.get('body', ''))}".lower()
        
        # Test-related keywords
        testing_keywords = [
            'test', 'testing', 'tests', 'unit test', 'integration test', 'e2e test',
            'pytest', 'junit', 'jest', 'mocha', 'jasmine', 'rspec', 'minitest',
            'assert', 'expect', 'should', 'mock', 'stub', 'spy',
            'coverage', 'tdd', 'bdd', 'spec', 'describe', 'it(',
            'test case', 'test suite', 'test file', 'test directory'
        ]
        
        found_keywords = [kw for kw in testing_keywords if kw in title_body]
        pr_record['auto_testing_keywords_count'] = len(found_keywords)
        pr_record['auto_testing_keywords_found'] = ', '.join(found_keywords) if found_keywords else ''
        
        # Language detection from repository
        repo_lang = str(row.get('repo_language', '')).lower()
        if repo_lang and repo_lang != 'nan':
            pr_record['auto_detected_language'] = repo_lang
        
        # Framework detection
        framework_keywords = {
            'react': ['react', 'jsx', 'nextjs', 'gatsby'],
            'vue': ['vue', 'vuejs', 'nuxt'],
            'angular': ['angular', 'ng-', '@angular'],
            'django': ['django', 'django-', 'drf'],
            'flask': ['flask', 'flask-'],
            'fastapi': ['fastapi', 'fast-api'],
            'spring': ['spring', 'springframework', 'springboot'],
            'express': ['express', 'expressjs', 'express.js'],
            'laravel': ['laravel', 'artisan'],
            'rails': ['rails', 'ruby on rails', 'activerecord'],
            '.net': ['.net', 'dotnet', 'aspnet', 'asp.net'],
            'nodejs': ['node.js', 'nodejs', 'npm', 'yarn'],
            'docker': ['docker', 'dockerfile', 'container'],
            'kubernetes': ['kubernetes', 'k8s', 'kubectl'],
            'tensorflow': ['tensorflow', 'tf.', 'keras'],
            'pytorch': ['pytorch', 'torch', 'torchvision']
        }
        
        detected_frameworks = []
        for framework, keywords in framework_keywords.items():
            if any(kw in title_body for kw in keywords):
                detected_frameworks.append(framework)
        
        pr_record['auto_framework_indicators'] = ', '.join(detected_frameworks) if detected_frameworks else ''
        
        # Set confidence level
        if pr_record['auto_testing_keywords_count'] >= 3:
            pr_record['auto_testing_confidence'] = 'High'
        elif pr_record['auto_testing_keywords_count'] >= 1:
            pr_record['auto_testing_confidence'] = 'Medium'
        else:
            pr_record['auto_testing_confidence'] = 'Low'
        
        comprehensive_data.append(pr_record)
    
    # Create DataFrame
    comprehensive_df = pd.DataFrame(comprehensive_data)
    
    # Save to CSV
    output_filename = 'comprehensive_pr_manual_verification_dataset.csv'
    comprehensive_df.to_csv(output_filename, index=False)
    
    print(f"\n✓ Comprehensive dataset saved to: {output_filename}")
    print(f"Total records: {len(comprehensive_df)}")
    
    # Show sample of the data
    print("\n=== Sample Data Preview ===")
    preview_cols = ['pr_id', 'agent', 'username', 'pr_title', 'html_url', 'repo_language', 'auto_testing_keywords_count', 'auto_framework_indicators']
    print(comprehensive_df[preview_cols].head(3).to_string())
    
    # Show statistics
    print("\n=== Dataset Statistics ===")
    print(f"Agents: {comprehensive_df['agent'].nunique()}")
    print(f"Unique users: {comprehensive_df['username'].nunique()}")
    print(f"Unique repositories: {comprehensive_df['repo_full_name'].nunique()}")
    print(f"Languages detected: {comprehensive_df['auto_detected_language'].nunique()}")
    
    print("\nLanguage distribution:")
    lang_dist = comprehensive_df['auto_detected_language'].value_counts().head(10)
    for lang, count in lang_dist.items():
        if pd.notna(lang) and lang != '':
            print(f"  {lang}: {count}")
    
    print("\nTesting keyword distribution:")
    testing_dist = comprehensive_df['auto_testing_confidence'].value_counts()
    for conf, count in testing_dist.items():
        print(f"  {conf}: {count}")
    
    print("\n=== Manual Verification Instructions ===")
    print("1. Open the CSV file in Excel or Google Sheets")
    print("2. For each PR, click on the 'html_url' to open the GitHub PR")
    print("3. Review the PR title, description, and files changed")
    print("4. Fill in the manual verification columns:")
    print("   - manual_testing_present: Yes/No/Partial")
    print("   - manual_test_types: unit/integration/e2e/etc")
    print("   - manual_test_frameworks: pytest/junit/jest/etc")
    print("   - manual_language_detected: Primary language used")
    print("   - manual_framework_mentioned: Frameworks mentioned")
    print("5. Add your reviewer name and confidence level")
    
    return comprehensive_df

def main():
    try:
        dataset = create_comprehensive_pr_dataset()
        return dataset
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()