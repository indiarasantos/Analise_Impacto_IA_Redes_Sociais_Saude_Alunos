import pandas as pd
import mysql.connector

# ---- Conexão MySQL ---
conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="impacto_ia_redes_sociais"
        )

# --- As 5 consultas estratégicas ---
consultas = {
    "1_perfil_escolaridade_genero":"""
SELECT 
    escolaridade,
    genero,
    COUNT(id_estudante) AS total_alunos,
    MIN(idade) AS idade_minima,
    ROUND(AVG(idade), 1) AS media_idade,
    MAX(idade) AS idade_maxima
FROM estudantes
GROUP BY escolaridade, genero
ORDER BY escolaridade, total_alunos DESC;
""",
"2_faixa_rede_vs_habitos": """
SELECT
    CASE 
        WHEN horas_redes_sociais < 3 THEN '1. Baixo (<3h)'
        WHEN horas_redes_sociais BETWEEN 3 AND 6 THEN '2. Moderado (3h-6h)'
        ELSE '3. Alto (>6h)'
    END AS faixa_redes_sociais,
    COUNT(id_estudante) AS qtd_alunos,
    ROUND(AVG(horas_ia), 2) AS media_ia,
    ROUND(AVG(horas_sono), 2) AS media_sono,
    ROUND(AVG(horas_atividade_fisica), 2) AS media_exercicio
FROM habitos
GROUP BY faixa_redes_sociais
ORDER BY faixa_redes_sociais;
""",
"3_faixa_saude_mental": """
SELECT 
    CASE 
        WHEN pontuacao_mental < 65 THEN '1. Alerta / Baixa (<65)'
        WHEN pontuacao_mental BETWEEN 65 AND 75 THEN '2. Moderada (65 a 75)'
        ELSE '3. Saudavel (>75)'
    END AS faixa_saude_mental,
    COUNT(id_estudante) AS total_alunos,
    ROUND(AVG(pontuacao_mental), 2) AS media_saude_mental,
    ROUND(AVG(pontuacao_fisica), 2) AS media_saude_fisica
FROM saude
GROUP BY faixa_saude_mental
ORDER BY media_saude_mental ASC;
""",
"4_redes_sociais_x_saude": """
SELECT 
    CASE 
        WHEN h.horas_redes_sociais < 3 THEN '1. Baixo (<3h)'
        WHEN h.horas_redes_sociais BETWEEN 3 AND 6 THEN '2. Moderado (3h-6h)'
        ELSE '3. Alto (>6h)'
    END AS faixa_redes_sociais,
    COUNT(h.id_estudante) AS qtd_alunos,
    ROUND(AVG(h.horas_ia), 2) AS media_horas_ia,
    ROUND(AVG(h.horas_sono), 2) AS media_horas_sono,
    ROUND(AVG(s.pontuacao_mental), 2) AS media_saude_mental,
    ROUND(AVG(s.pontuacao_fisica), 2) AS media_saude_fisica
FROM habitos h
INNER JOIN saude s ON h.id_estudante = s.id_estudante
GROUP BY faixa_redes_sociais
ORDER BY faixa_redes_sociais;
""",
"5_alunos_em_risco": """
SELECT
    e.escolaridade,
    e.genero,
    COUNT(e.id_estudante) AS alunos_em_risco,
    ROUND(AVG(h.horas_redes_sociais), 2) AS media_redes_sociais,
    ROUND(AVG(h.horas_ia), 2) AS media_ia,
    ROUND(AVG(s.pontuacao_mental), 2) AS media_saude_mental
FROM estudantes e
INNER JOIN habitos h ON e.id_estudante = h.id_estudante
INNER JOIN saude s ON e.id_estudante = s.id_estudante
WHERE h.horas_redes_sociais > 6 
  AND h.horas_sono < 6 
  AND s.pontuacao_mental < 65
GROUP BY e.escolaridade, e.genero
ORDER BY alunos_em_risco DESC;
"""
}

# --- Execuda cada consulta e exibe o resultado ---
resultados = {}
for nome, sql in consultas.items():
    print(f"\n{'='*60}\n{nome}\n{'='*60}")
    df_resultado = pd.read_sql(sql, conexao)
    print(df_resultado)
    resultados[nome] = df_resultado

# --- Exporta cada resultado para CSV ---
for nome, df_resultado in resultados.items():
    df_resultado.to_csv(f"resultado_{nome}.csv", index=False)

# --- Fechando conexão ---
conexao.close()
print("\nConsultas finalizadas e exportadas.")