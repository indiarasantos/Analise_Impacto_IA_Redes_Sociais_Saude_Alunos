-- Verificar se o comportamento digital ou a saúde muda conforme o nível acadêmico.








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

