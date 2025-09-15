# Banco de Dados de Materiais para Transferência de Calor

Este repositório contém um arquivo `.yml` com propriedades físicas de materiais metálicos comumente usados em estudos de transferência de calor.  
Ele pode ser utilizado como base para simulações, cálculos analíticos ou integração em softwares de engenharia.

## 📂 Estrutura do Arquivo

O arquivo `materiais_transferencia_calor.yml` segue o seguinte formato:

```yaml
nome_material:
    densidade_kg_m3: valor
    condutividade_termica_W_mK: valor
    calor_especifico_J_kgK: valor
    expansao_termica_1_K: valor
```

### 🔧 Propriedades Incluídas
- **densidade_kg_m3:** massa por unidade de volume (kg/m³)
- **condutividade_termica_W_mK:** capacidade de condução de calor (W/m·K)
- **calor_especifico_J_kgK:** energia para elevar 1 kg do material em 1 K (J/kg·K)
- **expansao_termica_1_K:** coeficiente de dilatação térmica linear (1/K)

## 📑 Materiais Incluídos
- Aço carbono
- Alumínio
- Cobre
- Latão
- Ferro fundido

## 🚀 Como Usar

1. Baixe o arquivo `materiais_transferencia_calor.yml`
2. Importe-o no seu código (Python exemplo):
```python
import yaml

with open("materiais_transferencia_calor.yml", "r") as file:
    materiais = yaml.safe_load(file)

print(materiais["aco_carbono"]["condutividade_termica_W_mK"])
```

## 📌 Observações
- Os valores são típicos de materiais comerciais e podem variar conforme a liga, tratamento térmico ou pureza.
- Recomenda-se confirmar os valores em tabelas ou normas (ASTM, ISO) para aplicações críticas.

## 📅 Última Atualização
15/09/2025

## 📜 Licença
Este projeto é de uso livre sob a licença MIT.
