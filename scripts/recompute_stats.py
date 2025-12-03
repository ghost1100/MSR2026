import json
from math import sqrt
with open('outputs/comprehensive_full_dataset_analysis.json','r') as f:
    res=json.load(f)
beh=res['test_behavior']['agent_behavior']
# All agents
agents_all=['OpenAI_Codex','Copilot','Claude_Code','Devin','Cursor']
cont_all=[[beh[a]['test_prs'], beh[a]['total_prs']-beh[a]['test_prs']] for a in agents_all]
def chi2_from_table(table):
    # table: list of [a,b] rows
    r=len(table)
    c=2
    row_sums=[sum(row) for row in table]
    col_sums=[sum(table[i][j] for i in range(r)) for j in range(c)]
    n=sum(row_sums)
    chi2=0.0
    for i in range(r):
        for j in range(c):
            expected=row_sums[i]*col_sums[j]/n if n else 0
            observed=table[i][j]
            if expected>0:
                chi2 += (observed-expected)**2/expected
    df=(r-1)*(c-1)
    return chi2, df, n

chi_all=chi2_from_table(cont_all)
n_all=chi_all[2]
v_all=sqrt(chi_all[0]/(n_all*1)) if n_all>0 else float('nan')
# Excluding Devin
agents_ex=['OpenAI_Codex','Copilot','Claude_Code','Cursor']
cont_ex=[[beh[a]['test_prs'], beh[a]['total_prs']-beh[a]['test_prs']] for a in agents_ex]
chi_ex=chi2_from_table(cont_ex)
n_ex=chi_ex[2]
v_ex=sqrt(chi_ex[0]/(n_ex*1)) if n_ex>0 else float('nan')
print('ALL: chi2=%.1f df=%d V=%.6f n=%d' % (chi_all[0], chi_all[1], v_all, n_all))
print('EXCL_DEVIN: chi2=%.1f df=%d V=%.6f n=%d' % (chi_ex[0], chi_ex[1], v_ex, n_ex))
