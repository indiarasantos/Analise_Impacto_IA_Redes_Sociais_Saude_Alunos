import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar o ficheiro CSV
df = pd.read_csv("C:\\Users\\dialuan.lima\\Documents\\CursoAnalistaDadosBigData2026\\estatistica_projeto\\impacto_ia_redes_sociais_estudantes.csv")

# Lista com os nomes exatos das colunas numéricas do CSV
colunas_numericas = [
    'idade',
    'horas_redes_sociais',
    'horas_ia',
    'horas_sono',
    'horas_atividade_fisica',
    'pontuacao_mental',
    'pontuação_fisica'
]

# ==============================================================================
# PARTE 1: CÁLCULO DAS MÉTRICAS ESTATÍSTICAS DO QUADRO
# ==============================================================================
tabela_estatisticas = []

for col in colunas_numericas:
    dados = df[col].dropna()
    
    # 1. Média e Mediana
    media = dados.mean()
    mediana = dados.median()
    
    # 2. Quartis (Q1, Q2, Q3)
    q1 = dados.quantile(0.25)
    q2 = dados.quantile(0.50)
    q3 = dados.quantile(0.75)
    
    # 3. IQR, Limite Inferior (LI), Limite Superior (LS) e Outliers
    iqr = q3 - q1
    li = q1 - (1.5 * iqr)
    ls = q3 + (1.5 * iqr)
    outliers_inf = dados[dados < li]
    outliers_sup = dados[dados > ls]
    total_outliers = len(outliers_inf) + len(outliers_sup)
    
    # 4. Amplitude Total, Variância e Desvio-Padrão
    minimo = dados.min()
    maximo = dados.max()
    amplitude_total = maximo - minimo
    variancia = dados.var()
    desvio_padrao = dados.std()
    
    # 5. Assimetria e Curtose (Excesso e Real)
    assimetria = dados.skew()
    curtose_excesso = dados.kurt()       # Padrão Fisher (Normal = 0)
    curtose_real = curtose_excesso + 3   # Padrão Pearson (Normal = 3)
    
    # Imprimir o relatório detalhado de cada variável no terminal
    print(f"\n==================== {col.upper()} ====================")
    print(f"Média: {media:.2f} | Mediana (Q2): {mediana:.2f}")
    print(f"Q1 (25%): {q1:.2f} | Q2 (50%): {q2:.2f} | Q3 (75%): {q3:.2f}")
    print(f"IQR: {iqr:.2f} | Limite Inf. (LI): {li:.2f} | Limite Sup. (LS): {ls:.2f}")
    print(f"Outliers Totais: {total_outliers} (Abaixo de LI: {len(outliers_inf)} | Acima de LS: {len(outliers_sup)})")
    print(f"Amplitude Total: {amplitude_total:.2f} (Mín: {minimo:.2f} | Máx: {maximo:.2f})")
    print(f"Variância: {variancia:.2f} | Desvio-Padrão: {desvio_padrao:.2f}")
    print(f"Assimetria: {assimetria:.4f}")
    print(f"Curtose (Excesso): {curtose_excesso:.4f} | Curtose (Real): {curtose_real:.4f}")
    
    tabela_estatisticas.append({
        'Coluna': col,
        'Média': round(media, 2),
        'Mediana (Q2)': round(mediana, 2),
        'Q1': round(q1, 2),
        'Q3': round(q3, 2),
        'IQR': round(iqr, 2),
        'LI': round(li, 2),
        'LS': round(ls, 2),
        'Outliers': total_outliers,
        'Amplitude': round(amplitude_total, 2),
        'Variância': round(variancia, 2),
        'Desvio-Padrão': round(desvio_padrao, 2),
        'Assimetria': round(assimetria, 4),
        'Curtose_Excesso': round(curtose_excesso, 4),
        'Curtose_Real': round(curtose_real, 4)
    })

# Exibir tabela resumo consolidada
df_resumo = pd.DataFrame(tabela_estatisticas)
print("\n=== TABELA RESUMO CONSOLIDADA ===")
print(df_resumo.to_string(index=False))

# ==============================================================================
# PARTE 2: GERAÇÃO DOS GRÁFICOS (HISTOGRAMA, BOXPLOT, BARRAS E LINHAS)
# ==============================================================================
sns.set_theme(style="whitegrid")

# --- GRÁFICO 1: HISTOGRAMAS ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('1. Histogramas: Distribuição, Média, Mediana e Assimetria', fontsize=15, fontweight='bold')

vars_hist = [
    ('horas_redes_sociais', 'Horas Diárias nas Redes Sociais', '#3498db'),
    ('horas_ia', 'Horas Diárias em Ferramentas de IA', '#9b59b6'),
    ('horas_sono', 'Horas Diárias de Sono', '#2ecc71'),
    ('pontuacao_mental', 'Pontuação de Saúde Mental', '#e74c3c')
]

for ax, (col, titulo, cor) in zip(axes.flatten(), vars_hist):
    sns.histplot(df[col], kde=True, ax=ax, color=cor, bins=30, alpha=0.5, edgecolor='white')
    ax.axvline(df[col].mean(), color='#c0392b', linestyle='--', linewidth=2, label=f'Média: {df[col].mean():.2f}')
    ax.axvline(df[col].median(), color='#111111', linestyle='-', linewidth=2, label=f'Mediana: {df[col].median():.2f}')
    ax.set_title(f'{titulo}\n(Assimetria = {df[col].skew():.2f} | Curtose Exc. = {df[col].kurt():.2f})', fontweight='bold')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequência (Nº de Estudantes)')
    ax.legend()

plt.tight_layout()
plt.show()

# --- GRÁFICO 2: BOXPLOTS ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('2. Boxplots: Quartis (Q1, Q2, Q3), Limites (LI, LS) e Outliers', fontsize=15, fontweight='bold')

# Boxplot de Hábitos (Horas)
habitos_cols = ['horas_redes_sociais', 'horas_ia', 'horas_sono', 'horas_atividade_fisica']
df_hab_melted = df[habitos_cols].melt(var_name='Coluna', value_name='Horas Diárias')
sns.boxplot(data=df_hab_melted, x='Coluna', y='Horas Diárias', ax=axes[0], palette='Set2', width=0.5)
axes[0].set_title('Hábitos Diários (em Horas)', fontweight='bold')

# Boxplot de Saúde (Pontuação 0 a 100)
saude_cols = ['pontuacao_mental', 'pontuação_fisica']
df_saude_melted = df[saude_cols].melt(var_name='Coluna', value_name='Pontuação (0 a 100)')
sns.boxplot(data=df_saude_melted, x='Coluna', y='Pontuação (0 a 100)', ax=axes[1], palette=['#ff7675', '#74b9ff'], width=0.4)
axes[1].set_title('Indicadores de Saúde (Escala 0 a 100)', fontweight='bold')

plt.tight_layout()
plt.show()

# --- GRÁFICO 3: BARRAS E LINHAS ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('3. Gráficos de Barras e de Linhas: Impacto das Redes Sociais e IA na Saúde', fontsize=15, fontweight='bold')

# Barras: Média de Saúde por Faixa de Redes Sociais
df['faixa_redes'] = pd.cut(df['horas_redes_sociais'], bins=[-1, 3, 6, 20], labels=['Baixo (<3h)', 'Moderado (3h-6h)', 'Alto (>6h)'])
bar_data = df.groupby('faixa_redes', observed=True)[['pontuacao_mental', 'pontuação_fisica']].mean().reset_index()
bar_melted = bar_data.melt(id_vars='faixa_redes', var_name='Indicador', value_name='Média de Pontuação')

sns.barplot(data=bar_melted, x='faixa_redes', y='Média de Pontuação', hue='Indicador', ax=axes[0], palette=['#e74c3c', '#2980b9'])
axes[0].set_title('Gráfico de Barras: Saúde por Faixa de Redes Sociais', fontweight='bold')
axes[0].set_ylim(50, 100)
for container in axes[0].containers:
    axes[0].bar_label(container, fmt='%.1f', padding=3, fontweight='bold')

# Linhas: Evolução da Saúde Mental por Horas de Uso (Redes Sociais vs IA)
df['horas_redes_int'] = df['horas_redes_sociais'].round().clip(0, 10)
df['horas_ia_int'] = df['horas_ia'].round().clip(0, 8)

line_redes = df.groupby('horas_redes_int')['pontuacao_mental'].mean()
line_ia = df.groupby('horas_ia_int')['pontuacao_mental'].mean()

axes[1].plot(line_redes.index, line_redes.values, marker='o', linewidth=2.5, color='#e74c3c', label='horas_redes_sociais (r = -0,40)')
axes[1].plot(line_ia.index, line_ia.values, marker='s', linewidth=2.5, color='#8e44ad', linestyle='--', label='horas_ia (r = -0,11)')
axes[1].set_title('Gráfico de Linhas: pontuacao_mental vs. Horas de Uso', fontweight='bold')
axes[1].set_xlabel('Horas Diárias')
axes[1].set_ylabel('Média de pontuacao_mental')
axes[1].set_xticks(range(0, 11))
axes[1].set_ylim(60, 80)
axes[1].legend()

plt.tight_layout()
plt.show()