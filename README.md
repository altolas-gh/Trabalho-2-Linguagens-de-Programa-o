# 🛡️ CyberSec Brasil — Dashboard de Segurança Cibernética

**Projeto G2 · Tema 26 — Análise de Segurança Cibernética e Ataques Digitais**

---

## 📋 Sobre o Projeto

Dashboard analítico desenvolvido com **Streamlit** e **Plotly** para investigar padrões de ataques cibernéticos e incidentes de segurança digital no Brasil entre **2015 e 2024**.

O projeto responde às principais perguntas de negócio:
- Quais tipos de ataques são mais frequentes?
- Quais setores sofrem mais incidentes?
- Houve crescimento dos ataques ao longo do tempo?
- Qual o impacto financeiro médio dos ataques?
- Quais vulnerabilidades aparecem com maior frequência?
- Quais regiões apresentam maior número de incidentes?

---

## 🗂️ Estrutura do Projeto

```
projeto-ciberseguranca/
│
├── app.py                          # Dashboard principal (Streamlit)
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── index.html                      # Página GitHub Pages
│
├── dados/
│   └── simulacao_ciberseguranca_brasil.csv
│
├── notebooks/
│   └── analise_ciberseguranca.ipynb
│
├── database/                       # SQLite gerado automaticamente
└── imagens/                        # Capturas de tela do dashboard
```

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/projeto-ciberseguranca.git
cd projeto-ciberseguranca
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard
```bash
streamlit run app.py
```

---

## 📊 Funcionalidades

### KPIs
| KPI | Descrição |
|-----|-----------|
| Total de Incidentes | Soma de todos os incidentes no período |
| Impacto Financeiro | Prejuízo estimado em bilhões de reais |
| Tempo Médio de Recuperação | Média em horas |
| Ataque Predominante | Tipo de ataque com maior frequência |
| Setor Mais Afetado | Setor com mais incidentes |
| Região Crítica | Região com maior volume |

### Visualizações
- 📈 **Linha temporal** — evolução por tipo de ataque
- 📊 **Barras** — frequência de ataques e setores
- 🔥 **Heatmap mensal** — sazonalidade dos incidentes
- 💠 **Dispersão** — correlação impacto × incidentes
- 🥧 **Pizza** — distribuição de vulnerabilidades
- 📋 **Tabela dinâmica** — exploração detalhada

### Filtros Interativos
Ano, Mês, Região, Estado (UF), Setor, Tipo de Ataque e Nível de Criticidade

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python** | Linguagem principal |
| **Pandas** | Manipulação e análise de dados |
| **Plotly** | Visualizações interativas |
| **Streamlit** | Interface do dashboard |
| **SQLAlchemy** | Persistência em SQLite |
| **NumPy** | Operações numéricas |

---

## 🌐 Links

- 🔗 **GitHub:** `https://github.com/seu-usuario/projeto-ciberseguranca`
- 🌍 **GitHub Pages:** `https://seu-usuario.github.io/projeto-ciberseguranca`
- 📊 **Streamlit Cloud:** `https://seu-usuario-projeto-ciberseguranca.streamlit.app`

---

## 📦 Dataset

**Arquivo:** `dados/simulacao_ciberseguranca_brasil.csv`

| Coluna | Descrição |
|--------|-----------|
| `ano` | Ano do incidente (2015–2024) |
| `mes` | Mês do incidente (1–12) |
| `data` | Data completa da ocorrência |
| `regiao` | Região do Brasil |
| `uf` | Estado (sigla) |
| `setor` | Setor organizacional |
| `tipo_ataque` | Categoria do ataque |
| `vulnerabilidade` | Tipo de vulnerabilidade explorada |
| `incidentes` | Quantidade de incidentes |
| `impacto_financeiro` | Prejuízo estimado em R$ |
| `tempo_recuperacao` | Horas para recuperação |
| `sistemas_afetados` | Quantidade de sistemas comprometidos |
| `nivel_criticidade` | Baixo / Médio / Alto / Crítico |
| `status_resposta` | Resolvido / Em análise / Mitigado |

---

## 📝 Conclusões Analíticas

A análise dos dados revela um crescimento consistente dos ataques cibernéticos no Brasil ao longo da década, com destaque para:

- **Ransomware e Phishing** como ataques predominantes
- **Falha humana** como principal vetor de vulnerabilidade
- **Setor Financeiro e Saúde** como os mais impactados financeiramente
- **Região Sudeste** concentrando maior volume absoluto de incidentes
- Necessidade de **planos de resposta a incidentes** com foco em criticidade alta/crítica

---

*Projeto desenvolvido para fins acadêmicos com dados simulados.*
