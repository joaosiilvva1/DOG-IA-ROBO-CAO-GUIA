# DOG-IA — ROBÔ CÃO-GUIA URBANO DE INTELIGÊNCIA ASSISTIVA

## DOCUMENTO DE ESCOPO DO PROJETO

Disciplina: Robótica Móvel InteligenteProjeto: DOG-IA — Robô Cão-Guia Urbano de Inteligência AssistivaFase: 1 — Configuração do Ambiente e ValidaçãoEtapa: 1 — Setup e InfraestruturaData: 05/10/2026

# 1. VISÃO GERAL DO PROJETO

O DOG-IA — Robô Cão-Guia Urbano de Inteligência Assistiva é um projeto acadêmico desenvolvido na disciplina de Robótica Móvel Inteligente.

O projeto tem como proposta o desenvolvimento de um robô móvel inspirado em um cão-guia, utilizando tecnologias de robótica, inteligência assistiva, visão computacional, navegação e simulação.

O objetivo é desenvolver, de maneira gradual, uma solução capaz de auxiliar a mobilidade em ambientes urbanos, utilizando ferramentas de software e simulação para desenvolver e testar as funcionalidades do robô.

Nesta primeira etapa do projeto, o foco principal está na configuração, padronização e validação do ambiente de desenvolvimento que será utilizado pelo grupo durante as próximas etapas.

# 2. OBJETIVO GERAL

Desenvolver um robô móvel de assistência inspirado em um cão-guia, utilizando o ecossistema ROS 2 Humble, ferramentas de simulação, navegação e visão computacional.

O desenvolvimento será realizado de maneira incremental, permitindo que as funcionalidades sejam desenvolvidas, testadas e integradas ao longo das próximas etapas do projeto.

# 3. OBJETIVOS ESPECÍFICOS

Os principais objetivos do projeto são:

Preparar um ambiente de desenvolvimento padronizado para todos os integrantes do grupo;

Utilizar o Ubuntu 22.04 LTS como sistema base;

Utilizar o WSL2 e WSLg nos computadores Windows compatíveis;

Instalar e configurar o ROS 2 Humble;

Criar e configurar um workspace ROS 2 denominado ros2_ws;

Utilizar o Gazebo para simulação de ambientes e do robô;

Utilizar o RViz2 para visualização das informações do sistema robótico;

Utilizar OpenCV para recursos relacionados à visão computacional;

Utilizar cv_bridge para realizar a integração entre ROS 2 e OpenCV;

Utilizar ferramentas relacionadas à navegação e localização;

Utilizar ferramentas de mapeamento e SLAM;

Permitir o desenvolvimento e teste de funcionalidades sem depender inicialmente de um robô físico;

Manter o projeto organizado e versionado utilizando Git e GitHub;

Documentar o desenvolvimento e a evolução do projeto.

# 4. ESCOPO DO PROJETO

O projeto DOG-IA terá como base o desenvolvimento de um sistema robótico móvel voltado à inteligência assistiva.

O escopo inicial contempla a preparação da infraestrutura de software necessária para o desenvolvimento, simulação, navegação e integração de recursos de visão computacional.

## 4.1 Ambiente de Desenvolvimento

O ambiente de desenvolvimento deverá utilizar:

Ubuntu 22.04 LTS;

WSL2 e WSLg para computadores Windows compatíveis;

ROS 2 Humble;

Python 3;

Git;

Ferramentas de desenvolvimento e compilação;

OpenCV;

cv_bridge.

## 4.2 Simulação

A simulação será utilizada como uma das principais ferramentas para desenvolvimento e validação do projeto.

O ambiente deverá possuir suporte para:

Gazebo;

RViz2;

Integração entre Gazebo e ROS 2;

Visualização dos estados do robô;

Testes de movimentação e comportamento.

A utilização da simulação permitirá que o grupo desenvolva e teste funcionalidades antes de uma possível implementação em hardware físico.

## 4.3 Navegação e Robótica Móvel

O projeto deverá possuir infraestrutura para desenvolvimento de funcionalidades relacionadas à robótica móvel.

Entre os recursos previstos estão:

Controle de movimentação;

Teleoperação;

Navegação;

Localização;

Mapeamento;

Integração com sensores;

Visualização de transformações e informações do robô.

Para isso, o ambiente deverá possuir ferramentas como:

Navigation2 (Nav2);

nav2_bringup;

SLAM Toolbox;

teleop_twist_keyboard;

Joint State Publisher GUI;

Xacro.

## 4.4 Visão Computacional

O projeto deverá possuir suporte à utilização de visão computacional.

Nesta primeira etapa será validada a integração entre:

ROS 2;

Python;

rclpy;

OpenCV;

cv_bridge.

As funcionalidades específicas relacionadas à visão computacional serão definidas e desenvolvidas nas etapas posteriores do projeto.

# 5. ARQUITETURA INICIAL DO PROJETO

A arquitetura inicial do DOG-IA será baseada no ROS 2, utilizando diferentes componentes e nós responsáveis pelas funcionalidades do sistema.

A estrutura inicial será organizada da seguinte maneira:

DOG-IA

│

├── ROS 2 Humble

│ ├── Nós do robô

│ ├── Controle de movimento

│ ├── Navegação

│ ├── Localização

│ ├── SLAM

│ └── Integração com sensores

│

├── Visão Computacional

│ ├── OpenCV

│ └── cv_bridge

│

├── Simulação

│ ├── Gazebo

│ └── RViz2

│

└── Workspace

└── ros2_ws/

└── src/

Essa arquitetura representa a estrutura inicial do projeto e poderá ser ampliada conforme novas funcionalidades forem desenvolvidas.

# 6. ESTRUTURA DO REPOSITÓRIO

O projeto deverá ser armazenado em um repositório GitHub com o nome exato:

DOG-IA_ROBO_CAO-GUIA

A estrutura inicial recomendada será:

DOG-IA_ROBO_CAO-GUIA/

│

├── README.md

│

├── docs/

│ └── escopo_dog-ia_robo.md

│

├── src/

│ └── [pacotes ROS 2 do projeto]

│

└── .gitignore

Conforme o projeto evoluir, novas pastas e arquivos poderão ser adicionados de acordo com as necessidades do desenvolvimento.

# 7. REQUISITOS DA ETAPA 1

Para que o ambiente de desenvolvimento seja considerado preparado e validado, deverão ser cumpridos os seguintes requisitos.

## 7.1 Sistema Operacional

O grupo deverá possuir o Ubuntu 22.04 LTS funcionando.

Nos computadores com Windows, deverá ser utilizado o WSL2 com suporte ao WSLg.

## 7.2 ROS 2 Humble

O ROS 2 Humble deverá estar instalado e funcionando corretamente.

## 7.3 Dependências

Deverão ser instalados os pacotes necessários para:

Simulação;

Navegação;

Mapeamento;

Teleoperação;

Visão computacional;

Integração entre ROS 2 e OpenCV.

## 7.4 Workspace

Deverá ser criado o workspace:

ros2_ws

O workspace deverá possuir a estrutura:

ros2_ws/

└── src/

Além disso, deverá ser realizada a compilação utilizando o colcon.

## 7.5 Validação do Python

O ambiente Python deverá conseguir importar corretamente:

rclpy;

cv2;

CvBridge.

O teste deverá confirmar que o ROS 2, o OpenCV e a ponte ROS-OpenCV estão funcionando.

## 7.6 Gazebo

O Gazebo deverá ser aberto corretamente para validar a renderização do simulador de física 3D.

## 7.7 RViz2

O RViz2 deverá ser aberto corretamente para validar a interface gráfica de visualização do ROS 2.

# 8. CRITÉRIOS DE ACEITAÇÃO

A Etapa 1 será considerada concluída quando os seguintes pontos forem atendidos:

Ubuntu 22.04 LTS funcionando corretamente;

ROS 2 Humble instalado;

Dependências necessárias instaladas;

Workspace ros2_ws criado;

Workspace compilado utilizando colcon;

Configuração automática do ROS 2 realizada;

Script de validação Python executado sem erros;

rclpy funcionando;

OpenCV funcionando;

cv_bridge funcionando;

Gazebo aberto e funcionando;

RViz2 aberto e funcionando;

Repositório GitHub criado;

Repositório utilizando o nome solicitado pelo professor;

README.md preenchido com os integrantes e respectivos R.A.;

Professor adicionado como colaborador;

Documento de escopo salvo em:

docs/escopo_dog-ia_robo.md

Evidências dos testes realizadas por meio de capturas de tela ou validação presencial.

Esses critérios seguem o checklist oficial apresentado pelo professor para a conclusão da Etapa 1.

# 9. FORA DO ESCOPO DA ETAPA 1

A primeira etapa possui como objetivo principal a preparação e validação da infraestrutura.

Portanto, não fazem parte da implementação obrigatória desta etapa:

Construção física do robô;

Definição definitiva do hardware;

Implementação completa da navegação autônoma;

Implementação definitiva do reconhecimento de obstáculos;

Implementação definitiva de reconhecimento de pessoas;

Integração definitiva de sensores físicos;

Testes em ambientes urbanos reais;

Operação autônoma completa;

Implementação final de todas as funcionalidades de inteligência assistiva.

Essas funcionalidades poderão ser desenvolvidas e detalhadas nas próximas etapas do projeto.

# 10. ORGANIZAÇÃO E VERSIONAMENTO

O desenvolvimento do DOG-IA será realizado utilizando Git e GitHub para controle de versão.

As alterações realizadas no projeto deverão ser registradas por meio de commits, permitindo acompanhar a evolução do sistema.

Os arquivos deverão permanecer organizados de acordo com sua finalidade, mantendo uma estrutura que facilite a manutenção e o desenvolvimento por todos os integrantes do grupo.

Documentações técnicas deverão ser armazenadas na pasta docs/.

Os códigos relacionados ao ROS 2 deverão ser organizados dentro da estrutura de desenvolvimento do projeto.

# 11. VALIDAÇÃO DO AMBIENTE

A validação técnica da infraestrutura será realizada por meio dos testes definidos na Etapa 1.

Primeiramente, será realizada a validação das bibliotecas Python e da integração entre ROS 2 e OpenCV.

O teste deverá confirmar:

ROS 2 Humble (rclpy): OK

Visão Computacional (OpenCV): OK

Ponte ROS-OpenCV (cv_bridge): OK

Em seguida, deverão ser realizados os testes gráficos utilizando:

Gazebo: deverá abrir a janela do simulador 3D sem apresentar erros de crash.

RViz2: deverá abrir sua interface gráfica de visualização corretamente.

Esses testes fazem parte da validação técnica obrigatória da Etapa 1.

# 12. EVOLUÇÃO DO ESCOPO

Este documento representa o escopo inicial do projeto DOG-IA.

Conforme o desenvolvimento avançar, novas funcionalidades e requisitos poderão ser adicionados ao projeto.

As alterações deverão ser discutidas pelo grupo e documentadas de forma adequada para manter a organização e o acompanhamento da evolução do sistema.

O escopo inicial servirá como base para as próximas etapas de desenvolvimento.

# 13. INTEGRANTES DO GRUPO

Os dados abaixo deverão ser preenchidos com as informações oficiais dos integrantes:

Integrantes

R.A.

Riquelmy Pereira Rosa

101295

William Alves de Oliveira Junior

97501

Kauã Xavier dos Santos

94971

João Vitor da Silva Batista

97021

Gabriel Soares Matos

99945
