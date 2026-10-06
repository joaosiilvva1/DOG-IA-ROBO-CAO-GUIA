# Ambiente de desenvolvimento em casa

Data da validação: 06/10/2026.

## Configuração
- Windows com WSL2 e Ubuntu 22.04.5 LTS.
- Usuário Linux: najoao.
- ROS 2 Humble Desktop e ros-dev-tools.
- Gazebo Classic 11.10.2.
- RViz2, Xacro, joint-state-publisher-gui e teleoperação.
- Nav2, SLAM Toolbox, cv_bridge e OpenCV.
- GPU Intel Iris Xe via D3D12, com aceleração ativa e OpenGL 4.1.

## Testes aprovados
- ros2 --help.
- Importações Python: rclpy, cv2 e CvBridge.
- Gazebo aberto, renderizando e com simulação avançando.
- RViz2 aberto e renderizando.
- Pacote dog_ia criado com ament_python.
- colcon build --packages-select dog_ia concluído.
- ros2 pkg prefix dog_ia encontrou o pacote instalado.

## Organização
- Workspace: ~/ros2_ws.
- Repositório: ~/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA.
- ROS e overlay configurados no ~/.bashrc.
- build/, install/ e log/ excluídos do controle de versão.

## Observação
O aviso de Fixed Frame no RViz2 ocorreu antes da criação do
modelo do robô e da publicação das transformações.
