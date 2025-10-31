import sys
sys.path.append('src')
from data_loader import load_aidev

print('🔍 Agent Representation Validation')
print('=' * 40)

# Test with larger sample to ensure agent diversity
print('Loading larger sample for agent validation...')
df = load_aidev(sample_size=50000)

if df is not None:
    print(f'✅ Sample loaded: {len(df)} rows')
    agents_found = df['agent'].nunique()
    print(f'   Agents found: {agents_found}/5')
    
    agent_dist = df['agent'].value_counts()
    for agent, count in agent_dist.items():
        pct = (count / len(df)) * 100
        print(f'   {agent}: {count:,} PRs ({pct:.1f}%)')
    
    if agents_found >= 5:
        print('✅ EXCELLENT: All 5 agents represented!')
    elif agents_found >= 4:
        print('✅ GOOD: 4+ agents represented')
    else:
        print(f'⚠️  LIMITED: Only {agents_found} agents found')
        
    print(f'\n🎯 Agent diversity score: {agents_found}/5')
else:
    print('❌ Failed to load data for agent validation')