# DOG-IA

Robô cão-guia urbano de inteligência assistiva. Este repositório contém o
workspace ROS 2 e o pacote inicial `dog_ia_core`.

## Requisitos

- Ubuntu 22.04 LTS
- ROS 2 Humble
- `colcon` e as dependências ROS declaradas em `src/dog_ia_core/package.xml`

Consulte [docs/escopo_dog-ia_robo.md](docs/escopo_dog-ia_robo.md) para o escopo
inicial do projeto.

## Compilar e executar

Com ROS 2 Humble e as dependências instaladas, execute na raiz deste repositório:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run dog_ia_core valida_ambiente
```

O nó publica uma mensagem de status a cada dois segundos no tópico
`dog_ia/status`.