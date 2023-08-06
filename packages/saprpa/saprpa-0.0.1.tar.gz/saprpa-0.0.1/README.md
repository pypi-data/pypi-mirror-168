# saprpa

<p style="text-align: justify">Este pacote  é usado para criação da interface usada na automação de processos do SAP.</p>


## Instalação

---

Execute o seguinte para instalar:

```python
pip install saprpa
```

## Uso

---
```python
from saprpa import SessaoSap

with SessaoSap(
    ambiente="PRD - ECC BR Produção",
    path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
    mult_thread=True,
) as sessao:
    sessao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
    sessao.cria_nova_sessao_sap(1)
    sessao.sessao[0].findById("wnd[0]/tbar[0]/okcd").text = "YSRLDESCARGA"
    sessao.sessao[1].findById("wnd[0]/tbar[0]/okcd").text = "YSRLDESCARGA"
```
## Desenvolvimento
---

<p style="text-align: justify">Para instalar saprpa junto com as ferramentas para desenvolver e realizar testes,
use o seguinte comando:</p>

```python
pip install -e .[dev]
```