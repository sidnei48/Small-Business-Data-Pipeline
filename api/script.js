async function carregarIndicadores() {
    const resposta = await fetch("http://127.0.0.1:8000/indicadores");

    const dados = await resposta.json();

    document.getElementById("matriculas-ativas").textContent =
        dados.matriculas_ativas;

    document.getElementById("matriculas-canceladas").textContent =
        dados.matriculas_canceladas;

    document.getElementById("alunos-ativos").textContent =
        dados.alunos_ativos;

    document.getElementById("media-alunos").textContent =
        dados.media_alunos_turma;
}

carregarIndicadores();