"""Textos narrativos (lore) exibidos em caixas de diálogo."""

INTRODUCAO = (
    "🐉  MUNDO DOS DRAGÕES  🐉\n\n"
    "Sua pacífica vila vive dias sombrios: hordas de goblins cruéis atacam "
    "sem descanso. Correm rumores de que um ancestral e tirânico Dragão Supremo "
    "escraviza a raça dracônica, semeando o caos entre os reinos.\n\n"
    "Você foi escolhido para trilhar uma jornada que decidirá o destino de "
    "dois mundos. Prepare-se, herói — os dados serão rolados."
)

CRIACAO_PERSONAGEM = (
    "Antes de partir, você precisa forjar seu destino.\n\n"
    "• Escolha uma classe (Guerreiro, Pescador ou Doutor).\n"
    "• Distribua 10 pontos entre RIGIDEZ (mitiga dano) e CARISMA "
    "(inspira aliados a se juntarem a você).\n"
    "Estes pontos são únicos: você os terá pelo resto da aventura."
)

HUB_PRIMEIRA_VEZ = (
    "A vila descansa por um instante. Antes da próxima batalha, você pode:\n"
    "• Explorar (avançar na missão atual);\n"
    "• Pescar no mar (arriscar-se por Saúde);\n"
    "• Estudar na biblioteca (arriscar-se por Inteligência);\n"
    "• Visitar a loja."
)

MISSOES = {
    "m1_floresta": {
        "inicio": (
            "MISSÃO 1 — EMBOSCADA NA FLORESTA\n\n"
            "A floresta ao redor da vila está agitada. Três goblins fracos "
            "saltam das moitas com adagas enferrujadas. É o seu primeiro "
            "combate — mostre do que é feito!"
        ),
        "fim": (
            "Os goblins tombam a seus pés. Entre folhas e cinzas, você "
            "descobre um baú misterioso: dentro dele, um OVO estranho "
            "pulsa lentamente e há uma PARTE DE UM MAPA rabiscado.\n\n"
            "+10 ouro, +1 Força."
        ),
    },
    "m2_caverna": {
        "inicio": (
            "MISSÃO 2 — EXPLORAÇÃO DA CAVERNA\n\n"
            "Seguindo o mapa, você chega a uma caverna úmida com três túneis. "
            "Instinto te leva pelo caminho do meio, onde o ar cheira a "
            "enxofre e ossos ranhem sob suas botas..."
        ),
        "fim": (
            "Um GOBLIN GIGANTE lidera a emboscada, mas cai por suas mãos. "
            "No fundo da caverna, um baú guarda a SEGUNDA PARTE DO MAPA e "
            "um APRIMORADOR DE ITENS.\n\n+20 ouro, +2 Força."
        ),
    },
    "m3_vila_goblin": {
        "inicio": (
            "MISSÃO 3 — VILA DOS GOBLINS\n\n"
            "O mapa completo revela o esconderijo dos goblins. Você invade "
            "a masmorra em três hordas ferozes. Ao final, o próprio "
            "REI GOBLIN aguarda no trono.\n\n"
            "Aldeões corajosos podem se juntar à sua causa se você tiver "
            "carisma suficiente (>3)."
        ),
        "fim": (
            "O Rei Goblin desaba. Do baú do trono, o OVO em sua mochila "
            "começa a rachar... e um pequeno DRAGÃO MASCOTE nasce! "
            "Ele te fita com olhos leais.\n\n+50 ouro, +2 Força, aprimorador de itens."
        ),
    },
    "obj1_defesa": {
        "inicio": (
            "OBJETIVO I — DEFESA DA VILA\n\n"
            "Ao voltar em triunfo, você encontra sua vila em chamas. "
            "Os goblins remanescentes atacam em massa. Um aldeão e seu "
            "dragão bebê lutam ao seu lado — se seu carisma for alto, "
            "mais aldeões se levantarão!\n\n"
            "Após esta defesa, apenas EXPLORAR estará disponível."
        ),
        "fim": (
            "A vila resiste. Você percebe que só há um caminho: seguir o "
            "mapa até o mítico MUNDO DOS DRAGÕES e libertá-los.\n\n+30 ouro, +1 Força."
        ),
    },
    "m4_mundo_dragoes": {
        "inicio": (
            "MISSÃO 4 — CHEGADA AO MUNDO DOS DRAGÕES\n\n"
            "Seu dragão, já adulto, corta os céus com você em suas costas. "
            "Ao pousar no MUNDO DOS DRAGÕES, três DRAGÕES REBELDES escravizados "
            "os recebem cuspindo fogo — precisam ser libertados pela força."
        ),
        "fim": (
            "Os rebeldes caem e, por um instante, os olhos deles clareiam antes "
            "de fugir para o horizonte. A rebelião começou.\n\n+30 ouro, +2 Força, aprimorador."
        ),
    },
    "m5_vila_dragoes": {
        "inicio": (
            "MISSÃO 5 — VILA DOS DRAGÕES\n\n"
            "Uma vila dracônica se ergue entre picos. Dois DRAGÕES DA VILA "
            "e um DRAGÃO ESPECIAL, ainda sob o jugo do Supremo, barram sua "
            "entrada. Prove seu valor."
        ),
        "fim": (
            "Os dragões vencidos se ajoelham em respeito. Você agora é bem-vindo "
            "entre eles.\n\n+40 ouro, +2 Força, aprimorador."
        ),
    },
    "obj2_supremo": {
        "inicio": (
            "OBJETIVO FINAL — O DRAGÃO SUPREMO\n\n"
            "No topo da montanha, o DRAGÃO SUPREMO aguarda. Suas hordas de "
            "dragões escravizados formam três ondas antes da batalha final. "
            "Seu dragão mascote, agora adulto, e um dragão da vila lutam ao "
            "seu lado. Se seu carisma for alto, mais dragões surgirão para "
            "a rebelião!"
        ),
        "fim": (
            "O Dragão Supremo tomba com um rugido que estremece os céus. "
            "As correntes se quebram. Sua vila humana e o Mundo dos Dragões "
            "se unem em uma nova era de harmonia.\n\n"
            "🏆  Você venceu Mundo dos Dragões!"
        ),
    },
}

ATIVIDADE = {
    "pescar_inicio": "🎣 Você lança a linha nas ondas escuras do mar da vila. O que virá?",
    "pescar_critico": "Um peixe raro dá o bote — você o traz para o barco. +2 Saúde!",
    "pescar_sucesso": "Uma boa pescaria. +1 Saúde.",
    "pescar_falha": "Nada morde a isca. A tarde escapa entre as ondas.",
    "pescar_desastre": (
        "As águas fervem! Um MONSTRO MARINHO emerge e ataca ferozmente!"
    ),
    "estudar_inicio": "📚 Você abre um tomo empoeirado. Runas antigas dançam nas páginas...",
    "estudar_critico": "Uma revelação profunda! +2 Inteligência.",
    "estudar_sucesso": "Você absorve o conhecimento. +1 Inteligência.",
    "estudar_falha": "Os símbolos se embaralham. Você não aprende nada hoje.",
    "estudar_desastre": (
        "Um farfalhar entre as prateleiras — uma ARANHA GIGANTE desperta!"
    ),
    "loja_boas_vindas": (
        "🛒 O comerciante te cumprimenta com um sorriso torto: "
        "'Ouro na mão, aventureiro? Tenho maravilhas para você.'"
    ),
}

FIM_DERROTA = (
    "💀  O grupo tombou. A escuridão engole a vila e o Mundo dos Dragões "
    "cai sob o Dragão Supremo... por enquanto. Rolem os dados novamente."
)
