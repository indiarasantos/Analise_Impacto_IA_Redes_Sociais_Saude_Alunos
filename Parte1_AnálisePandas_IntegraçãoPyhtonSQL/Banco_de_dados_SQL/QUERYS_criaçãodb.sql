-- Usando o banco de dados.
USE impacto_ia_redes_sociais;

--  Levanta o total de alunos e as faixas de idade dentro de cada nível de escolaridade e genero.
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

-- Verifica como o aumento das horas em redes sociais reduz o tempo de sono e de atividade física, enquanto o uso de IA permanece estável.
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

-- Analisa isoladamente a tabela saude para classificar os estudantes em faixas de saúde mentale comparar com a média de saúde física.
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

-- Prova de que o aumento das horas em redes sociais derruba as pontuações de saúde.
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

--  Localizar por escolaridade e genero os estudantes em situação crítica (mais de 6h de redes sociais, menos de 6h de sono e saúde mental abaixo de 65).
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