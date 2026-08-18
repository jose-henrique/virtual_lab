# 🌡️ Laboratório Virtual de Transferência de Calor

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Dear%20PyGui-orange)](https://github.com/hoffstadt/DearPyGui)
[![Arquitetura](https://img.shields.io/badge/Arquitetura-MVC-green)](https://pt.wikipedia.org/wiki/MVVM)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)](#-cronograma-e-proximos-passos)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-brightgreen.svg)](LICENSE)

Uma aplicação desktop educacional desenvolvida em Python para simulação, visualização interativa e análise numérica de fenômenos de **Transferência de Calor**. O projeto visa conectar equações diferenciais aplicadas à engenharia a uma interface intuitiva, permitindo a geração de gráficos térmicos e exportação de dados em tempo real.

> 🚧 **Status do Projeto**: Em desenvolvimento ativo como Trabalho de Conclusão de Curso (TCC) em Engenharia Mecânica. O núcleo de cálculo numérico e a estrutura da interface gráfica já estão implementados.

---

## 🌟 Destaques Técnicos

Este repositório foi construído aplicando **boas práticas de engenharia de software** voltadas à modelagem científica e simulação física:

- **Arquitetura MVC (Model-View-Controller):** Separação rigorosa entre a física e os métodos numéricos (Model), a interface gráfica do utilizador (View) e a gestão de estados e eventos (Controller).
- **Interface Gráfica de Alto Desempenho:** Desenvolvida utilizando **Dear PyGui** (wrapper de C++ em modo imediato), garantindo renderização rápida e baixo consumo de memória sem depender de frameworks pesados como Electron.
- **Motor Científico Extensível:** Modelos matemáticos orientados a objetos (OOP), permitindo a adição simples de novas condições de contorno, geometrias e tipos de materiais.
- **Pipeline de Exportação de Dados:** Suporte à exportação da matriz de nós e perfis de temperatura em formatos estruturados (CSV) para validação no MATLAB/Excel, além de gráficos em alta resolução (PNG).

---

## 📐 Módulos de Simulação

### 1. Superfícies Estendidas (Aletas) `[Implementado]`
- Solução para condução e convecção unidimensional (1D) em aletas com 4 condições de contorno clássicas:
  - Aleta infinitamente longa;
  - Extremidade adiabática;
  - Extremidade com temperatura especificada;
  - Extremidade com convecção.
- Discretização espacial interativa (geração de nós) com condutividade térmica ($k$) e coeficiente de convecção ($h$) personalizáveis.
- Mapeamento de gradiente térmico em tempo real utilizando escala de cores (*colormap* `coolwarm`).

### 2. Condução em Parede Plana Composta `[Em Desenvolvimento]`
- Modelagem de redes de resistência térmica para paredes multicamadas em regime permanente.

### 3. Convecção Forçada Interna `[Planejado]`
- Visualização de escoamento e troca de calor em tubos com cálculo de taxa de transferência térmica.

---

## 🛠️ Tecnologias e Bibliotecas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** [Dear PyGui](https://github.com/hoffstadt/DearPyGui)
- **Análise Numérica e Gráficos:** NumPy, Matplotlib, Pandas
- **Padrão de Projeto:** Model-View-Controller (MVC) + Programação Orientada a Objetos (POO)

---

## 🏗️ Estrutura do Projeto

```text
src/
├── controllers/    # Intermedeia os inputs da interface e os modelos físicos
├── models/         # Motores de cálculo numérico (ex: FinSolver)
├── views/          # Componentes visuais e renderização de janelas no Dear PyGui
├── utils/          # Módulos de validação, formatação e exportação (CSV/PNG)
└── main.py         # Ponto de entrada da aplicação