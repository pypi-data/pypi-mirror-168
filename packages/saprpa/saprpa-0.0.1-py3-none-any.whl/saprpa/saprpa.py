from __future__ import annotations
import win32com.client
import sys
import subprocess
import psutil
import time
import os
import win32gui, win32con
import pythoncom
from typing import List, Any, Sequence
from dataclasses import dataclass, field
from typing import ClassVar, Union


class VPNnotConectedError(Exception):
    """Erro lançado quando a VPN não está ligada"""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class InstanceError(Exception):
    """Erro lançado quando não encontrada instancia do processo"""

    def __init__(self, value: Any, mensagem: str) -> None:
        self.value = value
        self.mensagem = mensagem
        super().__init__(mensagem)


class LogonError(Exception):
    """Erro lançado quando ocorre erro no LOGON"""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class LogoutError(Exception):
    """Erro lançado quando ocorre erro no LOGOUT"""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class COMError(Exception):
    """Erro lançado quando ocorre erro no LOGON"""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class NumMaxSessaoError(Exception):
    """Erro lançado quando se tenta criar mais sessões que o maximo"""

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


@dataclass()
class SessaoSap:
    """Classe que abre o sap logon e cria uma sessão do sap RPA"""

    TIMEOUT: ClassVar[int] = 15
    NUM_MAX_SES: ClassVar[int] = 6
    ambiente: str
    path: Union[
        Union[bytes, str],
        Sequence[Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]],
    ]
    mult_thread: bool = field(default=False)
    vpn: bool = field(default=True)
    sessao: List[win32com.client.CDispatch] = field(default_factory=list)
    sessao_id: List[Any] = field(default_factory=list)
    processo: Any = field(repr=False, default=None)
    shell: win32com.client.CDispatch = field(repr=False, default=None)
    sapgui_auto: win32com.client.CDispatch = field(default=None)
    application: win32com.client.CDispatch = field(default=None)
    connection: win32com.client.CDispatch = field(default=None)

    def __post_init__(self) -> None:
        self.conexao()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.terminate()

    @staticmethod
    def vpn_ligada():
        """Testa se a VPN está ligada"""
        try:
            vpn = subprocess.check_output(
                'netsh interface show interface name="Ethernet 3" | findstr de | findstr "Conectado"',
                shell=True,
            )
        except subprocess.CalledProcessError:
            raise VPNnotConectedError(
                mensagem=f"INFO:SAP-RPA: VPN desconectada"
            ) from None

    @staticmethod
    def recupera_saplogon():
        """Testa se já existe logon"""

        for proc in psutil.process_iter():
            try:
                if (
                    proc.name() == "saplogon.exe"
                    and proc.status() == psutil.STATUS_RUNNING
                ):
                    return proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    @staticmethod
    def minimiza_sap_Logon():
        """Minimiza a janela do SAP LOGON"""
        hwnd = win32gui.FindWindow(None, "SAP Logon 740")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def terminate(self):
        try:
            for i in range(len(self.sessao)):
                self.connection.CloseSession(f"ses[{i}]")
            self.processo.terminate()
        except:
            raise LogoutError(f"INFO:SAP-RPA: O LOGOUT já foi feito") from None

    def abre_sap_logon(self):
        """Abre o aplicativo SAP LOGON"""
        pid_saplogon = self.recupera_saplogon()

        try:
            if pid_saplogon is None:
                processo = subprocess.Popen(self.path)
            else:
                processo = psutil.Process(pid_saplogon)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"INFO:SAP-RPA: O caminho para o SAP LOGON não Existe"
            ) from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon: {sys.exc_info()[0]}"
            ) from None

        if not (
            isinstance(processo, subprocess.Popen)  # type: ignore
            or isinstance(processo, psutil.Process)
        ):
            raise InstanceError(
                value=processo,
                mensagem=f"INFO:SAP-RPA: Não encontrada instancia do Processo do SAP Logon",
            )
        self.processo = processo

    @classmethod
    def abre_shell(cls):
        """Abre o aplicativo WScript.Shell"""
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
        except pythoncom.com_error as e:
            hr, msg, exc, arg = e.args
            if exc is None:
                raise COMError(
                    f"INFO:SAP-RPA:Função abre_shell falhou com o código: {hr} , {msg}"
                ) from None
            else:
                wcode, source, text, helpFile, helpId, scode = exc
                raise COMError(
                    f"INFO:SAP-RPA: Erro ao na função abre_shell. a mensagem foi: {text}"
                ) from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa abre_shell: {sys.exc_info()[0]}"
            ) from None

        if not type(shell) == win32com.client.CDispatch:
            raise InstanceError(
                value=shell,
                mensagem=f"INFO:SAP-RPA: Não encontrada instancia do Processo do WScript.Shell",
            )
        while not shell.AppActivate("SAP Logon"):
            time.sleep(1)
            tempo = 0
            if tempo == cls.TIMEOUT:
                raise TimeoutError(
                    f"Tempo limite para abrir esgotado ou processo não encontrado"
                )
            tempo += 1
        return shell

    @staticmethod
    def cria_sapgui_auto():
        """Cria o SAPGUI AUTO"""
        try:
            sapgui_auto = win32com.client.GetObject("SAPGUI")
        except pythoncom.com_error as e:
            (hr, msg, exc, arg) = e.args
            if exc is None:
                raise COMError(
                    f"INFO:SAP-RPA:Erro ao criar SAPGUIAUTO com o código: {hr}, {msg}"
                ) from None
            else:
                wcode, source, text, helpFile, helpId, scode = exc
                raise COMError(f"INFO:SAP-RPA: mensagem original, {text}") from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa cria_sapgui_auto: {sys.exc_info()[0]}"
            ) from None

        if not type(sapgui_auto) == win32com.client.CDispatch:
            raise InstanceError(
                value=sapgui_auto,
                mensagem=f"INFO:SAP-RPA: Não encontrada instancia COM do do SAPGUI",
            )
        return sapgui_auto

    def cria_sap_application(self):
        """Cria a ScriptingEngine do SAPGUI AUTO"""
        try:
            sap_application = self.sapgui_auto.GetScriptingEngine
        except pythoncom.com_error as e:
            (hr, msg, exc, arg) = e.args
            if exc is None:
                raise COMError(
                    f"INFO:SAP-RPA:Erro ao criar ScriptEngine com o código: {hr}, {msg}"
                ) from None
            else:
                wcode, source, text, helpFile, helpId, scode = exc
                raise COMError(f"INFO:SAP-RPA: mensagem original: {text}") from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa cria_sap_application: {sys.exc_info()[0]}"
            ) from None

        if not type(sap_application) == win32com.client.CDispatch:
            raise InstanceError(
                value=sap_application,
                mensagem=f"INFO:SAP-RPA: Não encontrada ScriptngEngine COM do SAPGUI",
            )
        self.application = sap_application

    def abre_conexao_sap(self):
        """Cria a uma conexão com a ScriptingEngine do SAPGUI AUTO"""
        try:
            sap_conexao = self.application.OpenConnection(self.ambiente, False)
        except pythoncom.com_error as e:
            (hr, msg, exc, arg) = e.args
            if exc is None:
                self.terminate()
                raise COMError(
                    f"INFO:SAP-RPA:Erro ao abrir conexão com o código: {hr}, {msg}"
                ) from None
            else:
                self.terminate()
                wcode, source, text, helpFile, helpId, scode = exc
                raise COMError(f"INFO:SAP-RPA: mensagem original: {text}") from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa abre_conexao_sap, {sys.exc_info()[0]}"
            ) from None

        if not isinstance(sap_conexao, win32com.client.CDispatch):
            raise InstanceError(
                value=sap_conexao,
                mensagem=f"INFO:SAP-RPA: Não encontrada conexão do SAPGUI",
            )
        return sap_conexao

    def cria_sessao_sap(self):
        """Cria a uma sessão SAP"""
        try:
            sessao = self.connection.Children(0)
        except pythoncom.com_error as e:
            (hr, msg, exc, arg) = e.args
            if exc is None:
                raise COMError(
                    f"INFO:SAP-RPA:Erro ao criar sessão com o código:{hr}, {msg}"
                ) from None
            else:
                wcode, source, text, helpFile, helpId, scode = exc
                raise COMError(f"INFO:SAP-RPA: mensagem original: {text}") from None
        except Exception:
            raise Exception(
                f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa cria_sessao_sap, {sys.exc_info()[0]}"
            ) from None

        if not isinstance(sessao, win32com.client.CDispatch):
            raise InstanceError(
                value=sessao, mensagem=f"INFO:SAP-RPA: Não encontrada sessão do SAP"
            )

        self.sessao.append(sessao)

        if self.mult_thread:
            try:
                sessao_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
                    pythoncom.IID_IDispatch, sessao
                )
                self.sessao_id.append(sessao_id)
            except pythoncom.com_error as e:
                (hr, msg, exc, arg) = e.args
                if exc is None:
                    raise COMError(
                        f"INFO:SAP-RPA:Erro ao recuperar o id da sesao"
                    ) from None
                else:
                    wcode, source, text, helpFile, helpId, scode = exc
                    raise COMError(f"INFO:SAP-RPA: mensagem original: {text}") from None
            except Exception:
                raise Exception(
                    f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa cria_sessao_sap, {sys.exc_info()[0]}"
                ) from None

    def cria_nova_sessao_sap(self, num):
        """Cria a uma nova sessão SAP"""
        if len(self.sessao) + num > self.NUM_MAX_SES:
            raise NumMaxSessaoError(f"INFO:SAP-RPA: numero maximo de sessãoes superado")

        if not self.mult_thread:
            raise NumMaxSessaoError(
                f"INFO:SAP-RPA: numero maximo de sessãoes para não multhread é 1"
            )

        for _ in range(num):
            try:
                self.sessao[0].createSession()
                time.sleep(2)
                sessao = self.connection.Children(len(self.sessao))
                self.sessao.append(sessao)
                sessao_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
                    pythoncom.IID_IDispatch, sessao
                )
                self.sessao_id.append(sessao_id)
            except pythoncom.com_error as e:
                (hr, msg, exc, arg) = e.args
                if exc is None:
                    raise COMError(
                        f"INFO:SAP-RPA:Erro ao criar nova sessão com o código: {hr}, {msg}"
                    ) from None
                else:
                    wcode, source, text, helpFile, helpId, scode = exc
                    raise COMError(f"INFO:SAP-RPA: mensagem original: {text}") from None
            except Exception:
                raise Exception(
                    f"INFO:SAP-RPA: Erro ao Abrir SAP Logon na etapa cria_nova_sessao_sap, {sys.exc_info()[0]}"
                ) from None

            if not isinstance(sessao, win32com.client.CDispatch):
                raise InstanceError(
                    value=sessao, mensagem=f"INFO:SAP-RPA: Não encontrada sessão do SAP"
                )

    def conexao(self):
        """Função que abre e cria a conexão"""
        if self.vpn:
            self.vpn_ligada()  # Determina se a VPN está ligada:

        self.abre_sap_logon()

        # Abre um obejeto shell que será usado para determinar se o sap logon carregou
        self.shell = self.abre_shell()

        self.minimiza_sap_Logon()  # minimiza o SAP LOGON

        # Cria um objeto com a API para interagir com o SAP Logon
        self.sapgui_auto = self.cria_sapgui_auto()

        # Cria ScriptingEngine do sapautogui
        self.cria_sap_application()

        # Conecta com o ambiente produção do sap Logon caso não esteja aberto.
        # Caso aberto usa a conexao existente.
        if self.application.Connections.Count == 0:
            self.connection = self.abre_conexao_sap()
        else:
            self.connection = self.application.Connections(0)

        # Cria o objeto da sessaão do SAP RPA aberto pra possibilitar a interação
        self.cria_sessao_sap()

    def logon(self, mandante, chave, senha):
        """Função para fazer Logon no SAP"""
        # testa se o logon não foi feito procurando a palavra informação no tela de logon
        try:
            informacao = self.sessao[0].FindById("wnd[0]/usr/boxMESSAGE_FRAME").Text
        except pythoncom.com_error as e:
            (hr, msg, exc, arg) = e.args
            if hr == -2147352567:
                raise LogonError(f"INFO:SAP-RPA: O Logon já foi feito") from None
        except Exception:
            raise LogonError(f"INFO:SAP-RPA: Não encontrada sessão SAP ativa") from None
        if informacao == "Informação":
            self.sessao[0].FindById("wnd[0]").Maximize
            self.sessao[0].FindById("wnd[0]/usr/txtRSYST-MANDT").Text = mandante
            self.sessao[0].FindById("wnd[0]/usr/txtRSYST-BNAME").Text = chave
            self.sessao[0].FindById("wnd[0]/usr/pwdRSYST-BCODE").Text = senha
            self.sessao[0].FindById("wnd[0]").SendVKey(0)

            mensagens = [
                "Preeencher todos os campos obrigatórios",
                "O nome ou a senha não está correto (repetir o logon)",
                "O mandante 401 não existe no sistema",
            ]

            menssagem = self.sessao[0].FindById("wnd[0]/sbar/pane[0]").Text
            if menssagem in mensagens:
                raise LogonError(f"INFO:SAP-RPA: Erro no Logon, {menssagem}")

            try:
                self.sessao[0].FindById("wnd[0]/tbar[0]/btn[0]")
            except pythoncom.com_error as e:
                (hr, msg, exc, arg) = e.args
                if exc is None:
                    raise LogonError(
                        f"INFO:SAP-RPA:Erro ao fazer o logon com o código: {hr}, {msg}"
                    ) from None
                else:
                    wcode, source, text, helpFile, helpId, scode = exc
                    raise LogonError(
                        f"INFO:SAP-RPA: mensagem original: {text}"
                    ) from None
            except Exception:
                raise LogonError(
                    f"INFO:SAP-RPA: Erro ao fazer o logon, {sys.exc_info()[0]}"
                ) from None


if __name__ == "__main__":
    with SessaoSap(
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as sessao:
        sessao.logon(mandante=400, chave="zcn3", senha=os.environ.get("zcn3"))