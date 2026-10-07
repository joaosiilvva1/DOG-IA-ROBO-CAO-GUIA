# DOG-IA — Robô cão-guia assistivo

João Vitor da Silva Batista
RA: 97021

Riquelme Pereira Rosa 
RA: 101295

Willian Alves de Oliveria Junior
RA: 97501

Gabriel Soares Matos
RA: 99945

Kauã Xavier do Santos
RA: 94971


## Robô simulado — modelagem inicial

Primeira versão com tração diferencial, apoio traseiro, LiDAR e câmera RGB-D.
Inclui cenário de teste, inicialização integrada e configuração do RViz2.

Consulte [como abrir, movimentar e validar o robô](docs/modelagem_robo.md).
O registro do ambiente de casa está em [ambiente WSL2](docs/ambiente_casa.md).

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build --packages-select dog_ia
source install/setup.bash
ros2 launch dog_ia simulacao.launch.py
```

Navegação autônoma e percepção assistiva serão desenvolvidas nas próximas etapas.


## Aplicativo conectado e supervisão — versão 0.1.0

Interface acessível com dados da simulação, avisos por voz, pausa e emergência.
Abra http://localhost:8765 depois de iniciar o launch. Para movimentar,
use `ros2 run dog_ia teclado` em outro terminal com o workspace carregado.

O supervisor limita velocidades, bloqueia obstáculos próximos no plano do
LiDAR e para quando comandos ou sensores ficam desatualizados.

[Direção do produto, testes, acessibilidade e limitações](docs/produto_assistivo.md).
Semáforos, buracos e obstáculos suspensos ainda não possuem detectores ativos.
Esta é uma versão de pesquisa em simulação; não validada para guiamento na rua.
