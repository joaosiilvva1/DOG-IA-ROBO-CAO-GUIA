# Percepção e voz: protótipos controlados da AC-4

Implementação inicial em 06/10/2026, conforme o guia oficial da Aula 06.
Não constitui validação de guiamento em ruas nem a missão final completa.

## Semáforo pela câmera

Feche a simulação anterior e execute no Ubuntu:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build --packages-select dog_ia
source install/setup.bash
ros2 launch dog_ia semaforo.launch.py
```

O mundo inclui faixa pintada e uma lâmpada de teste. O detector recebe imagem
RGB real do Gazebo via cv_bridge/OpenCV; HSV e contornos circulares reconhecem
vermelho, amarelo e verde na região calibrada. Não consulta o estado do mundo
para decidir a cor. Verde exige três imagens consecutivas; vermelho e amarelo
bloqueiam imediatamente após identificação. Sem leitura, ambiguidade ou imagem
antiga: estado desconhecido e movimento bloqueado.

O supervisor mantém a parada após mudança para verde. Retomar exige leitura
verde recente; ainda assim não comprova que uma travessia real está livre.
O bloqueio cobre todo o movimento neste laboratório e não estima distância
até a faixa. O cenário não contém outros sinais concorrentes nem um detector
treinado para associar sinal de pedestres a uma travessia urbana real.

Teste visual/motor automático, alterando as lâmpadas no Gazebo:

```bash
python3 ~/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA/dog_ia/scripts/validar_semaforo.py
```

Resultado: vermelho/amarelo bloqueados, verde retido até retomada, deslocamento
após confirmação de 0,147 m, retorno ao vermelho parando e ausência de luz
mantendo bloqueio. Recebido evento real do nó de áudio. A imagem vermelha está
em `docs/evidencias/semaforo-camera.png`.

## Profundidade: chão e obstáculos suspensos

```bash
ros2 launch dog_ia riscos.launch.py
```

Mantida a câmera superior e acrescentada câmera RGB-D inclinada para o piso,
com TF independente. O nó transforma pontos para `base_footprint` usando o TF
no instante de captura. Descarta pontos não finitos e imagens antigas.

O chão é observado num corredor entre 0,45 e 1,50 m à frente, largura 0,60 m.
Pontos abaixo de -0,10 m ou acima de 0,12 m indicam possível buraco/degrau.
Chão livre exige cobertura de nove células e quantidade mínima de pontos.
Ausência de cobertura nunca equivale a chão livre.

A câmera superior procura pontos entre 0,55 e 1,90 m de altura, até 1,80 m
à frente e dentro de uma largura de 0,70 m. Isso é uma hipótese geométrica de
laboratório; não modela pessoa/guia, curvas ou obstáculos fora do campo de visão.
A visão superior livre no campo observado não comprova todo o espaço livre.
Thresholds, inclinações, frequências e margens exigem calibração e validação.

```bash
python3 ~/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA/dog_ia/scripts/validar_terreno.py
```

Teste real passou com piso plano, placa suspensa movida para a região de
passagem e depressão física de 0,40 m no piso. Placa e desnível geraram comando
zero. Suspensão do processo de percepção por 1,3 segundo também gerou estado
`terrain_unknown` e saída zero; processo restaurado ao final do teste.
O teste posiciona o robô para observar o buraco; não demonstra exploração
urbana nem aproximação a todos os tipos de desnível.

## Nó de voz em Python

`assistive_audio` recebe `/dog_ia/status`, publica o texto em `/dog_ia/audio_text`
e reproduz mudanças de estado numa thread separada, sem bloquear sensores.
Fila limitada mantém o aviso mais recente; mensagens não se repetem a cada tick.

No WSL usa o sintetizador nativo do Windows (System.Speech, voz pt-BR quando
instalada). Em Ubuntu nativo precisa de `espeak-ng` ou `espeak` instalado.
O backend não depende da janela do navegador. Teste direto do sintetizador do
Windows concluiu com sucesso; ainda falta confirmar volume/inteligibilidade
com usuários e testar latência dos avisos. Reprodução em curso não é interrompida
por um evento novo; não usar a voz como único mecanismo de parada.

## Arquitetura acrescentada

- `signal_detector`: Image → `/dog_ia/signal`.
- `terrain_detector`: duas PointCloud2 + TF → `/dog_ia/terrain`.
- `motion_supervisor`: sensores, comandos e bloqueios de percepção → comando.
- `assistive_audio`: estado → texto/voz, execução independente.
- Watchdog permanece como único publicador no tópico do motor.

Os detectores são ativados explicitamente por cenário; o launch simples e o
laboratório Nav2 não afirmam possuir esses bloqueios. Testes de navegação,
semáforo e terreno são separados. Falta integrar e validar a missão final,
ensaios adicionais, vídeo 2–3 min e relatório com análise estatística.

## Testes de regras

17 testes aprovados: 13 do supervisor de movimento e quatro de classificação,
ambiguidade, retomada com verde recente e bloqueio por leitura desconhecida/vencida.

```bash
python3 -m pytest ~/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA/dog_ia/test/test_signal.py ~/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA/dog_ia/test/test_motion_guard.py -q
```
