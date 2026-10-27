# Escopo do Projeto DOG-IA

O DOG-IA é um robô cão-guia assistivo voltado à navegação urbana autônoma.
O sistema será desenvolvido com ROS 2, usando nós e tópicos para integrar os
componentes de percepção, navegação e controle.

## Objetivos iniciais

- Integrar sensores e componentes por meio do ROS 2.
- Explorar a simulação de física e obstáculos com Gazebo.
- Visualizar sensores, odometria e transformações TF2 no RViz2.
- Desenvolver processamento de imagens com OpenCV e `cv_bridge`.

## Primeiro marco

O pacote `dog_ia_core` fornece o nó `valida_ambiente`, que publica
periodicamente o estado inicial do sistema no tópico `dog_ia/status`.
Este marco valida a estrutura básica do pacote e a comunicação ROS 2; não
representa ainda navegação autônoma nem validação de sensores.