import pandas as pd
import re
from collections import Counter

def analyze_programming_languages():
    """Analyze programming languages from the bidirectional verification sample"""
    
    # Load the sample
    df = pd.read_csv('bidirectional_verification_study.csv')
    print(f'Analyzing sample of {len(df)} PRs...\n')
    
    # Define programming language patterns
    file_extensions = {
        'Python': [r'\.py\b', r'\.pyw\b', r'\.pyi\b'],
        'JavaScript': [r'\.js\b', r'\.mjs\b', r'\.cjs\b'],
        'TypeScript': [r'\.ts\b', r'\.tsx\b', r'\.d\.ts\b'],
        'Java': [r'\.java\b', r'\.jar\b', r'\.class\b'],
        'C++': [r'\.cpp\b', r'\.cxx\b', r'\.cc\b', r'\.h\b', r'\.hpp\b'],
        'C': [r'\.c\b', r'\.h\b'],
        'C#': [r'\.cs\b', r'\.csx\b', r'\.csproj\b'],
        'PHP': [r'\.php\b', r'\.phtml\b', r'\.php3\b', r'\.php4\b', r'\.php5\b'],
        'Ruby': [r'\.rb\b', r'\.rbw\b', r'\.rake\b', r'\.gemspec\b'],
        'Go': [r'\.go\b', r'\.mod\b'],
        'Rust': [r'\.rs\b', r'\.toml\b'],
        'Swift': [r'\.swift\b'],
        'Kotlin': [r'\.kt\b', r'\.kts\b'],
        'Scala': [r'\.scala\b', r'\.sc\b'],
        'Dart': [r'\.dart\b'],
        'R': [r'\.r\b', r'\.R\b', r'\.Rmd\b'],
        'Julia': [r'\.jl\b'],
        'Perl': [r'\.pl\b', r'\.pm\b', r'\.perl\b'],
        'Shell': [r'\.sh\b', r'\.bash\b', r'\.zsh\b', r'\.fish\b'],
        'HTML': [r'\.html\b', r'\.htm\b', r'\.xhtml\b'],
        'CSS': [r'\.css\b', r'\.scss\b', r'\.sass\b', r'\.less\b'],
        'SQL': [r'\.sql\b', r'\.mysql\b', r'\.pgsql\b'],
        'YAML': [r'\.yml\b', r'\.yaml\b'],
        'JSON': [r'\.json\b', r'\.jsonl\b'],
        'XML': [r'\.xml\b', r'\.xsd\b', r'\.xsl\b'],
        'Markdown': [r'\.md\b', r'\.markdown\b', r'\.mdown\b'],
        'Docker': [r'dockerfile\b', r'\.dockerfile\b'],
        'Lua': [r'\.lua\b'],
        'Haskell': [r'\.hs\b', r'\.lhs\b'],
        'Clojure': [r'\.clj\b', r'\.cljs\b', r'\.cljc\b'],
        'F#': [r'\.fs\b', r'\.fsx\b', r'\.fsi\b'],
        'MATLAB': [r'\.m\b', r'\.mat\b'],
        'Objective-C': [r'\.m\b', r'\.mm\b', r'\.h\b']
    }
    
    # Language name patterns
    language_names = {
        'Python': [r'\bpython\b', r'\bpy\b(?!\w)', r'\bpypi\b', r'\bpip\b', r'\bconda\b', r'\bdjango\b', r'\bflask\b', r'\bfastapi\b'],
        'JavaScript': [r'\bjavascript\b', r'\bnode\.?js\b', r'\bnpm\b', r'\byarn\b', r'\breact\b', r'\bvue\b', r'\bangular\b', r'\bexpress\b'],
        'TypeScript': [r'\btypescript\b', r'\btsc\b', r'\bts\b(?!\w)'],
        'Java': [r'\bjava\b(?!script)', r'\bmaven\b', r'\bgradle\b', r'\bspring\b', r'\bhibernate\b', r'\bjunit\b'],
        'C++': [r'\bc\+\+\b', r'\bcpp\b', r'\bcmake\b', r'\bmake\b'],
        'C': [r'\bc\b(?!\+|\#)', r'\bgcc\b', r'\bclang\b'],
        'C#': [r'\bc#\b', r'\bcsharp\b', r'\b\.net\b', r'\bdotnet\b', r'\bnuget\b', r'\bmsbuild\b'],
        'PHP': [r'\bphp\b', r'\bcomposer\b', r'\blaravel\b', r'\bsymfony\b'],
        'Ruby': [r'\bruby\b', r'\bgem\b', r'\bbundle\b', r'\brails\b', r'\bsinatra\b'],
        'Go': [r'\bgolang\b', r'\bgo\b(?!\w)', r'\bgo\.mod\b', r'\bgo\.sum\b'],
        'Rust': [r'\brust\b', r'\bcargo\b', r'\bcrates\.io\b'],
        'Swift': [r'\bswift\b', r'\bxcode\b', r'\bcocoapods\b'],
        'Kotlin': [r'\bkotlin\b'],
        'Scala': [r'\bscala\b', r'\bsbt\b'],
        'Dart': [r'\bdart\b', r'\bflutter\b', r'\bpub\b'],
        'R': [r'\b[rR]\b(?!\w)', r'\bcran\b', r'\brstudio\b'],
        'Julia': [r'\bjulia\b'],
        'Perl': [r'\bperl\b', r'\bcpan\b'],
        'Shell': [r'\bbash\b', r'\bshell\b', r'\bzsh\b', r'\bfish\b'],
        'Docker': [r'\bdocker\b', r'\bcontainer\b', r'\bdockerfile\b'],
        'Lua': [r'\blua\b'],
        'Haskell': [r'\bhaskell\b', r'\bghc\b', r'\bcabal\b'],
        'Clojure': [r'\bclojure\b', r'\bleiningen\b'],
        'MATLAB': [r'\bmatlab\b', r'\boctave\b'],
        'Objective-C': [r'\bobjective.?c\b', r'\bobjc\b']
    }
    
    # Testing frameworks to identify
    testing_frameworks = {
        'pytest': r'\bpytest\b',
        'unittest': r'\bunittest\b',
        'jest': r'\bjest\b',
        'mocha': r'\bmocha\b',
        'jasmine': r'\bjasmine\b',
        'karma': r'\bkarma\b',
        'cypress': r'\bcypress\b',
        'selenium': r'\bselenium\b',
        'junit': r'\bjunit\b',
        'testng': r'\btestng\b',
        'rspec': r'\brspec\b',
        'phpunit': r'\bphpunit\b',
        'nunit': r'\bnunit\b',
        'xunit': r'\bxunit\b'
    }
    
    # Count languages by file extensions
    ext_counts = Counter()
    name_counts = Counter()
    framework_counts = Counter()
    
    for _, row in df.iterrows():
        text = f"{row['title']} {row['body']}".lower()
        
        # Check file extensions
        for lang, patterns in file_extensions.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    ext_counts[lang] += 1
                    break  # Count each language only once per PR
        
        # Check language names
        for lang, patterns in language_names.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    name_counts[lang] += 1
                    break
        
        # Check testing frameworks
        for framework, pattern in testing_frameworks.items():
            if re.search(pattern, text, re.IGNORECASE):
                framework_counts[framework] += 1
    
    print("=== PROGRAMMING LANGUAGES DETECTED ===")
    print(f"(Based on analysis of {len(df)} PRs from MSR 2026 dataset)")
    print()
    
    # Combine and sort results
    all_langs = set(ext_counts.keys()) | set(name_counts.keys())
    combined_counts = {}
    
    for lang in all_langs:
        ext_count = ext_counts.get(lang, 0)
        name_count = name_counts.get(lang, 0)
        # Take the maximum to avoid double counting
        combined_counts[lang] = max(ext_count, name_count)
    
    # Sort by frequency
    sorted_langs = sorted(combined_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("Top Programming Languages (by frequency in sample):")
    print("-" * 50)
    for i, (lang, count) in enumerate(sorted_langs[:20], 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {lang:<15} {count:4d} PRs ({percentage:4.1f}%)")
    
    if len(sorted_langs) > 20:
        print(f"... and {len(sorted_langs) - 20} more languages")
    
    print(f"\nTotal unique languages detected: {len(sorted_langs)}")
    
    print("\n=== TESTING FRAMEWORKS DETECTED ===")
    print("-" * 50)
    sorted_frameworks = sorted(framework_counts.items(), key=lambda x: x[1], reverse=True)
    for framework, count in sorted_frameworks:
        percentage = (count / len(df)) * 100
        print(f"{framework:<15} {count:4d} PRs ({percentage:4.1f}%)")
    
    print(f"\n=== SAMPLE COMPOSITION ===")
    print(f"Total PRs analyzed: {len(df):,}")
    print(f"Keyword-detected PRs: {len(df[df['sample_type'] == 'keyword_detected'])}")
    print(f"Non-keyword PRs: {len(df[df['sample_type'] == 'no_keyword'])}")
    
    # Return the full list for documentation
    return sorted_langs

if __name__ == "__main__":
    languages = analyze_programming_languages()