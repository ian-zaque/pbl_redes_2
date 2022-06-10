# Coleta de lixo inteligente

## Problema 2 - Conectividade e Concorrência

### Autores
<div align="justify">
  <li><a href="https://github.com/ian-zaque">@ian-zaque</a></li>
  <li><a href="https://github.com/ozenilsoncruz">@ozenilsoncruz</a></li>
</div>

### Máquina
<div align="justify">
  <ol>
 ​    <li>  
 ​       Sistema operacional:  e 11;
        <ol> 
            <li>Windows 10; </li>
            <li>Ubuntu 22.04 LTS ; </li>
        </ol>
 ​     </li>
    <li> 
       Linguagem de programação: Python 3.10.4;
     </li>
    <li> 
       Bibliotecas nativas utilizadas:
      <ol> 
        <li>flask; </li>
        <li>json; </li>
        <li>paho_mqtt; </li>
        <li>random; </li>
        <li>string; </li>
        <li>threading; </li>
      </ol>
    </li>
  </ol>
</div>

### Instalção

This tutorial assumes you already have a valid Python instalation. If not, please check the website above for tutorials.

1. Clone o repositório.
   ```sh
   git clone https://github.com/ian-zaque/pbl_redes_2.git
   ```
2. Dentro da pasta, crie um novo ambiente.
   ```sh
   python3 -m venv venv
   ```

3. Use o novo ambiente.
   * No Windows, use:
     ```sh
     venv\Scripts\activate.bat
     ```
   * No Linux, use:
     ```sh
     source venv/bin/activate
     ```

4. Dentro da pasta, instale as bibliotecas especificadas por nós no arquivo require.txt.
   ```sh
   pip install -r requirements.txt
   ```

5. Execute os scripts seguindo a ordem:.
    1. Servidor:
        ```sh
        python3 control/setor.py
        ``` 

    2. Caminhão:
        ``` sh
        python3 model/caminhao.py
        ```

    3. Lixeras:
        ``` sh
        python3 model/lixeira.py
        ```