
# KYDS (Keep Your Data Safe)

KYDS é uma ferramenta de backup em Python que permite a criação de backups incrementais e completos de forma fácil e intuitiva, utilizando uma interface gráfica moderna baseada em PyQt5.

## Funcionalidades

- **Backup Completo**: Realiza uma cópia completa dos diretórios de origem especificados.
- **Backup Incremental**: Realiza uma cópia apenas dos arquivos que foram modificados desde o último backup.
- **Gestão de Grupos de Backup**: Permite a criação, edição, ativação/desativação e remoção de grupos de backup.
- **Interface Gráfica**: Interface gráfica moderna para gerenciar as configurações de backup.

## Requisitos

- Python 3.x
- PyQt5
- 7-Zip

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/KYDS.git
   cd KYDS
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instale o 7-Zip:**
   - Baixe e instale o 7-Zip a partir do [site oficial](https://www.7-zip.org/).
   - Atualize o caminho para o executável do 7-Zip no arquivo `backup.py` se necessário:
     ```python
     SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"
     ```

## Utilização

### Executando a Aplicação

Para iniciar a aplicação, execute o seguinte comando no terminal:
```bash
python gui.py
```

### Interface Gráfica

1. **Adicionar Grupo de Backup:**
   - Insira o nome do grupo no campo "Group Name".
   - Marque ou desmarque a opção "Active" para ativar ou desativar o grupo.
   - Marque ou desmarque a opção "Incremental Backup" para definir o tipo de backup.
   - Clique em "Add Group".

2. **Selecionar Diretórios de Origem:**
   - Selecione um grupo na lista "Backup Groups".
   - Clique em "Add Source" e escolha os diretórios que deseja incluir no backup.
   - Para remover diretórios, selecione-os na lista e clique em "Remove Selected".

3. **Definir Diretório de Destino:**
   - Selecione um grupo na lista "Backup Groups".
   - Clique em "Browse" e escolha o diretório de destino onde os backups serão armazenados.

4. **Iniciar Backup:**
   - Selecione um grupo na lista "Backup Groups".
   - Clique em "Start Backup" para iniciar o backup.

5. **Remover Grupo de Backup:**
   - Selecione um grupo na lista "Backup Groups".
   - Clique em "Remove Group".

### Configurações

As configurações dos grupos de backup são salvas no arquivo `config.json`. As informações sobre o último backup são salvas no arquivo `last_backup.json`.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para mais informações, entre em contato através de [Francisco Barboza](mailto:jose.f.barboza@outlook.com).
