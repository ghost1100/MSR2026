"""
Claude API integration for intelligent PR analysis and classification.
Provides AI-powered insights beyond basic keyword matching for MSR research.
"""

import os
import anthropic
import pandas as pd
import json
import time
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import logging
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class ClaudeAnalyzer:
    """
    Claude API wrapper for intelligent PR analysis and classification.
    
    Provides AI-powered analysis capabilities including:
    - Intelligent PR type classification (beyond keyword matching)
    - Description-to-change consistency analysis
    - Agent quality pattern detection
    - Batch processing with caching and rate limiting
    
    Essential for research questions requiring semantic understanding
    of PR content and agent behavior patterns.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Claude API client with caching and logging.
        
        Args:
            api_key (str): Anthropic API key, defaults to environment variable
            
        Raises:
            ValueError: If API key not found in environment or parameters
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.cache_dir = Path("data/processed/claude_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging for API monitoring
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Generate file path for cache entry."""
        return self.cache_dir / f"{cache_key}.json"
    
    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """
        Load previously computed result from cache.
        
        Critical for cost optimization - avoids re-analyzing identical PRs.
        
        Args:
            cache_key (str): Unique identifier for cached result
            
        Returns:
            dict or None: Cached result or None if cache miss
        """
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load cache {cache_key}: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """
        Save analysis result to cache for future use.
        
        Args:
            cache_key (str): Unique identifier for result
            data (dict): Analysis result to cache
        """
        cache_path = self._get_cache_path(cache_key)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.warning(f"Failed to save cache {cache_key}: {e}")
    
    def classify_pr_type(self, title: str, description: str, cache_key: str = None) -> Dict:
        """
        Classify PR type using Claude's semantic understanding.
        
        Goes beyond keyword matching to understand intent and context.
        Critical for RQ2 test-to-code ratio analysis accuracy.
        
        Args:
            title (str): PR title text
            description (str): PR description/body text
            cache_key (str): Optional cache identifier for result reuse
            
        Returns:
            dict: Classification with type, confidence, and reasoning
        """
        if cache_key:
            cached = self._load_from_cache(f"pr_type_{cache_key}")
            if cached:
                return cached
        
        prompt = f"""
        Analyze this pull request and classify its type. Be concise and accurate.

        Title: {title}
        Description: {description[:1000]}...

        Classify this PR into one of these categories:
        - feature: New functionality or enhancement
        - bugfix: Fixing bugs or issues
        - test: Adding or updating tests
        - refactor: Code restructuring without changing functionality
        - docs: Documentation updates
        - other: Anything else

        Respond in JSON format:
        {{
            "type": "category",
            "confidence": 0.95,
            "reasoning": "Brief explanation"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Cost-effective model for classification
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            
            if cache_key:
                self._save_to_cache(f"pr_type_{cache_key}", result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Claude API error in classify_pr_type: {e}")
            return {
                "type": "other",
                "confidence": 0.0,
                "reasoning": f"API Error: {str(e)}"
            }
    
    def analyze_description_consistency(self, title: str, description: str, files_changed: List[str] = None) -> Dict:
        """
        Analyze consistency between PR description and claimed changes.
        
        Supports RQ4 description consistency analysis by evaluating
        alignment between stated intent and implementation scope.
        
        Args:
            title (str): PR title
            description (str): PR description text
            files_changed (list): Optional list of modified files
            
        Returns:
            dict: Consistency analysis with score and reasoning
        """
        files_info = f"Files changed: {', '.join(files_changed[:10])}" if files_changed else "Files info not available"
        
        prompt = f"""
        Analyze the consistency between this PR's description and the changes it claims to make.

        Title: {title}
        Description: {description[:1500]}...
        {files_info}

        Rate the consistency on a scale of 1-10 where:
        - 10: Perfect match between description and expected changes
        - 7-9: Good consistency with minor discrepancies
        - 4-6: Moderate consistency, some unclear areas
        - 1-3: Poor consistency, description doesn't match expected changes

        Respond in JSON format:
        {{
            "consistency_score": 8,
            "reasoning": "Brief explanation of score",
            "potential_issues": ["issue1", "issue2"],
            "quality_indicators": ["indicator1", "indicator2"]
        }}
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content[0].text)
            
        except Exception as e:
            self.logger.error(f"Claude API error in analyze_description_consistency: {e}")
            return {
                "consistency_score": 5,
                "reasoning": f"API Error: {str(e)}",
                "potential_issues": ["API_ERROR"],
                "quality_indicators": []
            }
    
    def batch_classify_prs(self, df: pd.DataFrame, sample_size: int = 1000, batch_size: int = 10) -> pd.DataFrame:
        """
        Batch classify PRs with intelligent rate limiting and caching.
        
        Processes large datasets efficiently while respecting API limits.
        Critical for 900K+ dataset analysis with cost optimization.
        
        Args:
            df (pd.DataFrame): Full dataset of PRs
            sample_size (int): Maximum PRs to analyze (cost control)
            batch_size (int): PRs processed per batch (rate limiting)
            
        Returns:
            pd.DataFrame: Sample with Claude classification results
        """
        # Sample data for cost-effective analysis
        if len(df) > sample_size:
            df_sample = df.sample(n=sample_size, random_state=42)
            self.logger.info(f"Analyzing sample of {sample_size} PRs from {len(df)} total")
        else:
            df_sample = df.copy()
        
        results = []
        
        for i in range(0, len(df_sample), batch_size):
            batch = df_sample.iloc[i:i+batch_size]
            self.logger.info(f"Processing batch {i//batch_size + 1}/{(len(df_sample)-1)//batch_size + 1}")
            
            for idx, row in batch.iterrows():
                # Create deterministic cache key from content
                cache_key = f"{hash(str(row['title']) + str(row['body']))}"
                
                result = self.classify_pr_type(
                    title=str(row['title']),
                    description=str(row['body']),
                    cache_key=cache_key
                )
                
                results.append({
                    'index': idx,
                    'pr_type': result['type'],
                    'confidence': result['confidence'],
                    'reasoning': result['reasoning']
                })
                
                # Rate limiting between individual requests
                time.sleep(0.1)
            
            # Longer delay between batches for API stability
            if i + batch_size < len(df_sample):
                time.sleep(1)
        
        # Merge results back to original dataframe
        results_df = pd.DataFrame(results).set_index('index')
        df_sample = df_sample.join(results_df)
        
        return df_sample
    
    def analyze_agent_quality_patterns(self, df: pd.DataFrame) -> Dict:
        """
        Analyze quality patterns across different AI agents using semantic analysis.
        
        Identifies agent-specific behaviors, naming conventions, and quality
        indicators for RQ1 agent distribution analysis.
        
        Args:
            df (pd.DataFrame): Dataset with 'agent' column and PR metadata
            
        Returns:
            dict: Agent-specific quality analysis results
        """
        agent_summaries = {}
        
        for agent in df['agent'].unique():
            agent_data = df[df['agent'] == agent]
            
            # Sample for cost-effective analysis
            sample_size = min(100, len(agent_data))
            agent_sample = agent_data.sample(n=sample_size, random_state=42)
            
            # Extract representative titles for pattern analysis
            titles_sample = agent_sample['title'].head(10).tolist()
            
            prompt = f"""
            Analyze the patterns in these PR titles from AI agent '{agent}':

            Sample titles:
            {chr(10).join([f"- {title}" for title in titles_sample])}

            Total PRs by this agent: {len(agent_data)}
            
            Analyze and provide insights about:
            1. Common patterns or themes
            2. Quality indicators
            3. Potential strengths/weaknesses
            4. Consistency in naming conventions

            Respond in JSON format:
            {{
                "patterns": ["pattern1", "pattern2"],
                "quality_score": 7.5,
                "strengths": ["strength1", "strength2"],
                "improvements": ["improvement1", "improvement2"],
                "consistency_score": 8.0
            }}
            """
            
            try:
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                agent_summaries[agent] = json.loads(response.content[0].text)
                
            except Exception as e:
                self.logger.error(f"Error analyzing agent {agent}: {e}")
                agent_summaries[agent] = {
                    "patterns": [],
                    "quality_score": 5.0,
                    "strengths": [],
                    "improvements": [f"API Error: {str(e)}"],
                    "consistency_score": 5.0
                }
            
            # Rate limiting between agent analyses
            time.sleep(0.5)
        
        return agent_summaries

def create_claude_enhanced_analysis(df: pd.DataFrame, sample_size: int = 2000) -> Dict:
    """
    Main function to run comprehensive Claude-enhanced analysis.
    
    Orchestrates the complete AI-powered analysis pipeline including
    PR classification, agent pattern analysis, and enhanced statistics.
    
    Critical for research questions requiring semantic understanding
    beyond traditional keyword-based analysis methods.
    
    Args:
        df (pd.DataFrame): Complete AIDev dataset
        sample_size (int): Maximum PRs to analyze (cost optimization)
        
    Returns:
        dict: Comprehensive analysis results with all components
    """
    analyzer = ClaudeAnalyzer()
    
    print("Starting Claude-Enhanced Analysis...")
    print(f"Analyzing sample of {min(sample_size, len(df))} PRs from {len(df)} total")
    
    # Step 1: Intelligent PR classification
    print("\nStep 1: Classifying PR types...")
    classified_df = analyzer.batch_classify_prs(df, sample_size=sample_size)
    
    # Step 2: Agent behavior pattern analysis
    print("\nStep 2: Analyzing agent quality patterns...")
    agent_analysis = analyzer.analyze_agent_quality_patterns(classified_df)
    
    # Step 3: Generate enhanced summary statistics
    print("\nStep 3: Generating enhanced statistics...")
    
    type_distribution = classified_df['pr_type'].value_counts().to_dict()
    confidence_stats = {
        'mean_confidence': classified_df['confidence'].mean(),
        'high_confidence_rate': (classified_df['confidence'] > 0.8).mean()
    }
    
    results = {
        'classified_data': classified_df,
        'type_distribution': type_distribution,
        'confidence_stats': confidence_stats,
        'agent_analysis': agent_analysis,
        'sample_size': len(classified_df),
        'total_size': len(df)
    }
    
    print("Claude-Enhanced Analysis Complete!")
    return results