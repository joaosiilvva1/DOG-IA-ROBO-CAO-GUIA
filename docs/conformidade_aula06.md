# Conferência dos arquivos oficiais da Aula 06

Fonte: https://github.com/PROFSANTARELLI/IMR_CDC6_2026/tree/main/AULA_06
Conferido em 06/10/2026. O guia informa que tarefas serão liberadas aula a aula;
as próximas instruções do professor podem detalhar ou alterar estes critérios.

## Arquivos lidos

- `roteiro_aula06.txt`: setup, grupo, repositório, escopo, validação e envio.
- `AULA06_IMR.pdf` (3 páginas): nós/tópicos ROS, infraestrutura, Gazebo e RViz2.
- `Guia Oficial - Projeto AC 3 e 4.pdf` (4 páginas): objetivo, entregáveis e fases.
- `guia_fase1_etapa1_aula05102026.pdf` (6 páginas): instalação e checklist inicial.

## Requisitos e situação

| Etapa | Solicitação oficial | Situação do projeto |
|---|---|---|
| 05/10 | Ambiente, workspace e entrega inicial | Ambiente validado; usuário informou entrega concluída |
| 26/10 | Rodas motrizes + roda boba, câmera RGB-D inclinada, LiDAR, plugins, odom e TF | Modelo implementado e teste de movimento realizado |
| 09/11 | SLAM Toolbox, Nav2, costmaps/inflação, meta autônoma via RViz2 e documentação | SLAM/Nav2 configurados; meta por ação validada em cenário delimitado; cidade e validação gráfica de mapa pendentes |
| 16/11 | Nó Python OpenCV/cv_bridge; semáforo verde/vermelho ou faixa; impedir cruzamento no vermelho | Detector e bloqueio específico ainda pendentes |
| 23/11 | Nó Python de voz, robustez, vídeo 2–3 min e relatório | Voz do navegador existe como extra; não substitui o nó Python obrigatório |
| 30/11 | Missão completa ao vivo; código, arquitetura, relatório e vídeo | Entrega final pendente |

O desafio geral inclui buracos e obstáculos suspensos em 3D. Publicar nuvem de
pontos não atende sozinho à detecção. A câmera inclinada atual atende à
modelagem inicial, mas a percepção de piso precisa de posição/cobertura adequadas.
O requisito específico de visão cita vermelho/verde; amarelo pode ser extensão.
Não há exigência de integrar Google Maps/Waze nem criar aplicativo comercial.

O roteiro exige nome exato `DOG-IA_ROBO_CAO-GUIA`; o repositório atual usa
`DOG-IA-ROBO-CAO-GUIA`. O usuário informou que esta pendência já foi resolvida;
este trabalho não renomeou o repositório nem repetiu a entrega administrativa.

## Ordem de implementação adotada

1. Consolidar modelo e sensores (já implementados).
2. Validar navegação SLAM/Nav2 e ampliar o cenário urbano.
3. Reconhecer sinal e interromper a trajetória no vermelho.
4. Implementar áudio Python e percepção dos riscos 3D.
5. Registrar experimentos, arquitetura completa, relatório e vídeo.

Acessibilidade sem exigir visão permanece uma diretriz do usuário para a
extensão móvel. O fluxo de destino por voz ainda está pendente; não é apresentado
como concluído pela simples existência de botões grandes ou ditagem do teclado.
