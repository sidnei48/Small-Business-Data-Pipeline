const API_URL = "";

let graficoMatriculas;
let graficoProfessores;
let graficoTiposTurma;
let graficoOcupacao;


// Pega os valores selecionados nos filtros
function obterParametrosFiltros() {
    const professor =
        document.getElementById("filtro-professor").value;

    const idioma =
        document.getElementById("filtro-idioma").value;

    const tipoTurma =
        document.getElementById("filtro-tipo").value;

    const parametros = new URLSearchParams();

    if (professor) {
        parametros.append(
            "professor",
            professor
        );
    }

    if (idioma) {
        parametros.append(
            "idioma",
            idioma
        );
    }

    if (tipoTurma) {
        parametros.append(
            "tipo_turma",
            tipoTurma
        );
    }

    return parametros;
}


// Monta a URL da API com os filtros selecionados
function montarUrl(endpoint) {
    const parametros =
        obterParametrosFiltros();

    let url = `${API_URL}${endpoint}`;

    if (parametros.toString()) {
        url += `?${parametros.toString()}`;
    }

    return url;
}


// Faz uma requisição para a API
async function buscarDados(url) {
    const resposta = await fetch(url);

    if (!resposta.ok) {
        throw new Error(
            `Erro ao buscar dados: ${resposta.status}`
        );
    }

    return resposta.json();
}


// Busca os indicadores principais
async function carregarIndicadores() {
    const url =
        montarUrl("/indicadores");

    const dados =
        await buscarDados(url);

    document
        .getElementById("matriculas-ativas")
        .textContent =
        dados.matriculas_ativas;

    document
        .getElementById("matriculas-canceladas")
        .textContent =
        dados.matriculas_canceladas;

    document
        .getElementById("alunos-ativos")
        .textContent =
        dados.alunos_ativos;

    document
        .getElementById("media-alunos")
        .textContent =
        dados.media_alunos_turma;

    atualizarGraficoMatriculas(dados);
}


// Cria ou atualiza o gráfico de matrículas
function atualizarGraficoMatriculas(dados) {
    const canvas =
        document.getElementById(
            "grafico-matriculas"
        );

    const valores = [
        dados.matriculas_ativas,
        dados.matriculas_canceladas
    ];

    if (graficoMatriculas) {
        graficoMatriculas
            .data
            .datasets[0]
            .data = valores;

        graficoMatriculas.update();

        return;
    }

    graficoMatriculas =
        new Chart(canvas, {
            type: "bar",

            data: {
                labels: [
                    "Ativas",
                    "Canceladas"
                ],

                datasets: [
                    {
                        label: "Matrículas",
                        data: valores,

                        backgroundColor: [
                            "#2563eb",
                            "#9ca3af"
                        ]
                    }
                ]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
}


// Carrega as opções dos filtros
async function carregarFiltros() {
    const dados =
        await buscarDados(
            `${API_URL}/filtros`
        );

    const filtroProfessor =
        document.getElementById(
            "filtro-professor"
        );

    const filtroIdioma =
        document.getElementById(
            "filtro-idioma"
        );

    const filtroTipo =
        document.getElementById(
            "filtro-tipo"
        );


    dados.professores.forEach(
        professor => {
            const option =
                document.createElement(
                    "option"
                );

            option.value = professor;
            option.textContent = professor;

            filtroProfessor.appendChild(
                option
            );
        }
    );


    dados.idiomas.forEach(
        idioma => {
            const option =
                document.createElement(
                    "option"
                );

            option.value = idioma;
            option.textContent = idioma;

            filtroIdioma.appendChild(
                option
            );
        }
    );


    dados.tipos_turma.forEach(
        tipo => {
            const option =
                document.createElement(
                    "option"
                );

            option.value = tipo;
            option.textContent = tipo;

            filtroTipo.appendChild(
                option
            );
        }
    );
}


// Busca alunos ativos por professor
async function carregarGraficoProfessores() {
    const url =
        montarUrl(
            "/graficos/alunos-professor"
        );

    const dados =
        await buscarDados(url);

    const canvas =
        document.getElementById(
            "grafico-professores"
        );

    if (graficoProfessores) {
        graficoProfessores.data.labels =
            dados.professores;

        graficoProfessores
            .data
            .datasets[0]
            .data =
            dados.alunos_ativos;

        graficoProfessores.update();

        return;
    }

    graficoProfessores =
        new Chart(canvas, {
            type: "bar",

            data: {
                labels:
                    dados.professores,

                datasets: [
                    {
                        label:
                            "Alunos Ativos",

                        data:
                            dados.alunos_ativos,

                        backgroundColor:
                            "#2563eb"
                    }
                ]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
}


// Busca quantidade de turmas por tipo
async function carregarGraficoTiposTurma() {
    const url =
        montarUrl(
            "/graficos/turmas-tipo"
        );

    const dados =
        await buscarDados(url);

    const canvas =
        document.getElementById(
            "grafico-tipos-turma"
        );

    if (graficoTiposTurma) {
        graficoTiposTurma.data.labels =
            dados.tipos_turma;

        graficoTiposTurma
            .data
            .datasets[0]
            .data =
            dados.quantidades;

        graficoTiposTurma.update();

        return;
    }

    graficoTiposTurma =
        new Chart(canvas, {
            type: "bar",

            data: {
                labels:
                    dados.tipos_turma,

                datasets: [
                    {
                        label:
                            "Quantidade de Turmas",

                        data:
                            dados.quantidades,

                        backgroundColor:
                            "#2563eb"
                    }
                ]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
}


// Busca as turmas com maior ocupação
async function carregarGraficoOcupacao() {
    const url =
        montarUrl(
            "/graficos/ocupacao-turmas"
        );

    const dados =
        await buscarDados(url);

    const turmas =
        dados.turmas.slice(
            0,
            15
        );

    const ocupacoes =
        dados.ocupacoes.slice(
            0,
            15
        );

    const canvas =
        document.getElementById(
            "grafico-ocupacao"
        );

    if (graficoOcupacao) {
        graficoOcupacao.data.labels =
            turmas;

        graficoOcupacao
            .data
            .datasets[0]
            .data =
            ocupacoes;

        graficoOcupacao.update();

        return;
    }

    graficoOcupacao =
        new Chart(canvas, {
            type: "bar",

            data: {
                labels: turmas,

                datasets: [
                    {
                        label:
                            "Ocupação (%)",

                        data:
                            ocupacoes,

                        backgroundColor:
                            "#2563eb"
                    }
                ]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            callback:
                                function(valor) {
                                    return (
                                        valor + "%"
                                    );
                                }
                        }
                    }
                }
            }
        });
}


// Atualiza todos os indicadores e gráficos
async function atualizarDashboard() {
    try {
        await Promise.all([
            carregarIndicadores(),
            carregarGraficoProfessores(),
            carregarGraficoTiposTurma(),
            carregarGraficoOcupacao()
        ]);

    } catch (erro) {
        console.error(
            "Erro ao atualizar dashboard:",
            erro
        );
    }
}


// Configura os eventos dos filtros
function configurarEventos() {
    document
        .getElementById(
            "filtro-professor"
        )
        .addEventListener(
            "change",
            atualizarDashboard
        );

    document
        .getElementById(
            "filtro-idioma"
        )
        .addEventListener(
            "change",
            atualizarDashboard
        );

    document
        .getElementById(
            "filtro-tipo"
        )
        .addEventListener(
            "change",
            atualizarDashboard
        );
}


// Inicializa a aplicação
async function iniciarDashboard() {
    try {
        await carregarFiltros();

        configurarEventos();

        await atualizarDashboard();

    } catch (erro) {
        console.error(
            "Erro ao iniciar dashboard:",
            erro
        );
    }
}


iniciarDashboard();