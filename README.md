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
- Parâmetro da aleta $m = \sqrt{hP/(kA_c)}$, com cálculo da taxa de calor, da **eficiência** ($\eta$) e da **efetividade** ($\varepsilon$).
- Discretização espacial interativa (geração de nós da base, $x = 0$, até a ponta, $x = L$) com condutividade térmica ($k$) e coeficiente de convecção ($h$, em W/m².K) personalizáveis.
- Mapeamento de gradiente térmico em tempo real utilizando escala de cores (*colormap* `coolwarm`).

### 2. Condução em Parede Plana Composta `[Implementado]`
- Modelagem de redes de resistência térmica para paredes multicamadas em regime permanente, com camadas em **série** ou em **paralelo**.
- Cálculo da resistência total, taxa e fluxo de calor, calor trocado no intervalo de tempo e temperaturas nas interfaces (arranjo em série) ou taxa de calor por ramo (arranjo em paralelo).
- Banco de materiais com metais (aço carbono, alumínio, cobre, latão, ferro fundido), materiais de construção (tijolo comum, concreto, madeira) e isolantes (lã de vidro, EPS).
- Desenho da parede com camadas proporcionais à espessura (série) ou à área (paralelo) e mapa de cores de temperatura.

### 3. Convecção Forçada Interna `[Implementado]`
- Simulação de escoamento interno em tubo circular, com cálculo de Reynolds, Prandtl, Nusselt e coeficiente convectivo.
- Estimativa da temperatura de saída e da taxa de calor para temperatura de parede constante, com perfil térmico ao longo do tubo.
- Correlação laminar com região de entrada térmica (Edwards et al., apresentada no Çengel), que tende a Nu = 3,66 em tubos longos, e correlação de Gnielinski para escoamento turbulento.
- Aviso quando o tubo é mais curto que o comprimento de entrada térmica ($L < L_t$) e indicação da temperatura média do fluido, na qual as propriedades devem ser avaliadas.

---

## 🛠️ Tecnologias e Bibliotecas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** [Dear PyGui](https://github.com/hoffstadt/DearPyGui)
- **Análise Numérica e Gráficos:** NumPy, Matplotlib
- **Testes:** pytest
- **Padrão de Projeto:** Model-View-Controller (MVC) + Programação Orientada a Objetos (POO)

---

## 🏗️ Estrutura do Projeto

```text
.
├── controller/          # Intermedeia os inputs da interface e os modelos físicos
├── model/               # Solvers (FinSolver, ConductionSolver, ForcedConvectionSolver),
│   ├── chart_adapters/  #   adaptadores de gráfico,
│   ├── data_serializers/#   serializadores de exportação CSV
│   └── utils/           #   e utilitários (fontes, imagens, caminhos)
├── view/                # Telas, painéis de análise, canvas e componentes Dear PyGui
├── data/                # Banco de materiais (materials_properties.pkl e script gerador)
├── fonts/               # Fontes da interface
├── tests/               # Testes automatizados (pytest)
└── main.py              # Ponto de entrada da aplicação
```

## ▶️ Como executar

```bash
pip install -r requirements.txt
python main.py        # inicia a aplicação
python -m pytest      # roda os testes
```

Para alterar o banco de materiais, edite `data/generate_material_property.py` e execute-o para regenerar `data/materials_properties.pkl`.
