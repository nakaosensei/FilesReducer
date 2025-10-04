# 🗺️ GPS Files Reducer

Ferramenta em Python para **redução automática de coleções de imagens georreferenciadas (com dados GPS)**.  
Seu objetivo é **eliminar fotos muito próximas entre si**, com base na distância geográfica, preservando apenas as mais relevantes.

---

## 📖 Visão Geral

O sistema lê as coordenadas GPS armazenadas nos metadados EXIF das imagens, calcula as distâncias entre elas e cria uma nova coleção contendo apenas uma foto a cada intervalo mínimo configurado (em metros).

Ideal para:
- Pesquisadores que coletam dados de campo;
- Fotógrafos de natureza ou mapeamento;
- Usuários que tiram muitas fotos com GPS e desejam reduzir redundâncias.

---

## ⚙️ Estrutura do Projeto

```
.
├── ArrayUtils.py
├── filesReducerGPSMT.py
├── view.py
└── README.md
```

### Componentes principais

- **`view.py`** — Interface gráfica (Tkinter) para seleção da pasta e execução da redução.
- **`filesReducerGPSMT.py`** — Núcleo lógico responsável por processar as imagens e gerar os resultados.
- **`ArrayUtils.py`** — Funções auxiliares usadas para dividir listas em blocos e otimizar o carregamento de dados.

---

## 🧩 Funcionalidades Principais

✅ Leitura automática de coordenadas GPS das imagens.  
✅ Comparação geográfica entre fotos (usando distância em metros).  
✅ Agrupamento e classificação por “classes” de latitude/longitude.  
✅ Geração automática de relatórios (arquivos `.txt`).  
✅ Interface gráfica simples e funcional.  
✅ Processamento em múltiplas threads para melhor desempenho.

---

## 🧰 Dependências

Instale as bibliotecas necessárias com:

```bash
pip install GPSPhoto geopy
```

Tkinter já vem incluído na maioria das instalações do Python.  
Se desejar instalar via arquivo de requisitos:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Como Usar (Interface Gráfica)

1. Execute o programa:

   ```bash
   python3 view.py
   ```

2. Na janela que abrir:
   - Escolha o **diretório com as imagens** (botão “Selecionar pasta”);
   - Informe a **distância mínima entre fotos** (em metros);
   - Clique em **“Iniciar redução”**.

3. O sistema criará automaticamente uma pasta chamada **`resultsFileReducer`** dentro do diretório escolhido, contendo:
   - As fotos selecionadas;
   - Relatórios de distâncias, rejeições e mapeamentos.

---

## 🧪 Como Usar (modo programático)

Também é possível rodar diretamente a função principal do módulo:

```bash
python3 -c "from filesReducerGPSMT import reduceFiles; reduceFiles('/caminho/para/imagens', 10)"
```

O segundo parâmetro (`10`) define a distância mínima em **metros** entre fotos.

---

## 📁 Estrutura da Saída

Após o processamento, será criada a pasta:

```
resultsFileReducer/
├── 0.jpg
├── 1.jpg
├── mapping.txt
├── distances.txt
├── rejecteds.txt
├── picturesDict.txt
└── ...
```

### Arquivos gerados

| Arquivo | Descrição |
|----------|------------|
| `mapping.txt` | Mapeia o nome original de cada foto para o novo nome. |
| `distances.txt` | Distâncias entre fotos consecutivas mantidas. |
| `rejecteds.txt` | Lista de fotos descartadas e o motivo. |
| `picturesDict.txt` | Coordenadas GPS de cada imagem. |
| `classes.txt` / `classesOrdenadas.txt` | Agrupamentos por prefixo de nome. |
| `consoleOut.txt` | Log detalhado do processo. |

---

## ⚙️ Como Funciona

1. **Leitura GPS**  
   Cada imagem é analisada com a biblioteca `GPSPhoto` para obter `(latitude, longitude)`.

2. **Classificação espacial**  
   A função `mountLatLongClass()` agrupa as imagens com coordenadas semelhantes (três casas decimais após o ponto).

3. **Comparação de distâncias**  
   As fotos são percorridas sequencialmente. Quando a distância entre duas é menor que o limite configurado, a segunda é rejeitada.

4. **Cópia e logs**  
   As fotos aceitas são copiadas para `resultsFileReducer` preservando metadados.  
   O processo gera vários relatórios `.txt` para auditoria e conferência.

---

## ⚠️ Observações Importantes

- As imagens devem conter **metadados GPS válidos**.  
  (Fotos sem coordenadas serão ignoradas ou registradas como falhas no console.)
- O algoritmo faz **cópias reais** dos arquivos (não apenas links).
- Caso existam arquivos corrompidos, será gerado um log indicando os nomes.

---

## 📸 Exemplo de Funcionamento

Suponha uma pasta com 5 fotos próximas:

| Foto | Coordenadas GPS | Distância para anterior | Mantida? |
|------|------------------|--------------------------|-----------|
| A.jpg | (-23.1234, -46.5678) | — | ✅ |
| B.jpg | (-23.1235, -46.5678) | 11 m | ❌ (muito próxima) |
| C.jpg | (-23.1240, -46.5680) | 63 m | ✅ |
| D.jpg | (-23.1241, -46.5681) | 9 m | ❌ |
| E.jpg | (-23.1250, -46.5690) | 130 m | ✅ |

Se o parâmetro de distância for `50 metros`, apenas as fotos **A**, **C** e **E** serão mantidas.

---

## 👨‍💻 Autor

Desenvolvido por **Thiago Alexandre Nakao França**  
Projeto acadêmico para otimização e análise de conjuntos de imagens com dados GPS.

---

## 🧾 Licença

Uso livre para fins acadêmicos e pessoais.  
Melhorias e contribuições são bem-vindas.
