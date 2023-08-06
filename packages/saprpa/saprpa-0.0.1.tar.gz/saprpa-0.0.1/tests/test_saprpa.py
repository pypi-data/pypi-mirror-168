""" Testa a classe SessaoSap"""
from saprpa.saprpa import SessaoSap, LogonError, COMError,  NumMaxSessaoError
import win32com.client
import pytest
import os


def test_erro_ambinte_returns_com_error():
    """Erro no ambiente logon"""
    with pytest.raises(COMError):
        with SessaoSap(
            ambiente="PRD - ECC BR Produção2",
            path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=False,
        ):
            pass

    with pytest.raises(COMError):
        with SessaoSap(
            ambiente="PRD - ECC BR Produção2",
            path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=True,
        ):
            pass


def test_erro_arquivo_returns_FileNotFoundError():
    """Erro no caminho do arquivo de logon"""

    with pytest.raises(FileNotFoundError):
        with SessaoSap(
            ambiente="PRD - ECC BR Produção",
            path=r"C:\Program Files2 (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=False,
        ):
            pass
    
    with pytest.raises(FileNotFoundError):
        with SessaoSap(
            ambiente="PRD - ECC BR Produção",
            path=r"C:\Program Files2 (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=True,
        ):
            pass

def test_cria_sessaosap():
    """Erro na criação da sessão"""
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        assert isinstance(sessao.sessao[0], win32com.client.CDispatch)
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as sessao:
        assert isinstance(sessao.sessao[0], win32com.client.CDispatch)

def test_erro_mandante_errado():
    """Erro na nserção do mandante no logon"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        with pytest.raises(LogonError):
            sessao.logon(mandante=401, chave=os.getlogin(), senha=os.environ.get("zcn3"))
    
def test_erro_usuario_errado():
    """Erro na inserção do usuário no logon"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        with pytest.raises(LogonError):
            sessao.logon(mandante=400, chave="zzzz", senha=os.environ.get("zcn3"))

def test_erro_senha_errada():
    """Erro na inserção da senha no logon"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        with pytest.raises(LogonError):
            sessao.logon(mandante=400, chave=os.getlogin(), senha=12345)

def test_logon():
    """Teste de logon"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        sessao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        assert sessao.sessao[0].FindById("wnd[0]/sbar/pane[1]").Text == 'SAPLSMTR_NAVIGATION'

def test_criasessao_nova():
    """Teste de criação de nova sessao"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as sessao:
        sessao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        sessao.cria_nova_sessao_sap(1)
        assert isinstance(sessao.sessao[0], win32com.client.CDispatch)

def test_num_max_sessao():
    """Teste de numero márimo de sessoes"""
    
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as sessao:
        sessao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        with pytest.raises( NumMaxSessaoError):
            sessao.cria_nova_sessao_sap(6)


if __name__ == "__main__":
    pytest.main(["test_saprpa.py", "-s"])