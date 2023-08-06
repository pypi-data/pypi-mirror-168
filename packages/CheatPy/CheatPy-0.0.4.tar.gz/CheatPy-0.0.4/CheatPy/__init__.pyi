#
# AUTOMATICALLY GENERATED FILE, DO NOT EDIT!
#

"""Cheat.py"""
from __future__ import annotations
import CheatPy
import typing

__all__ = [
    "AddressView",
    "Alert",
    "AllocationType",
    "Cheat",
    "GetKey",
    "GetProcess",
    "GetProcessFromID",
    "GetProcesses",
    "KeyCode",
    "MemoryFreeType",
    "MemoryProtection",
    "Module",
    "Process"
]


class AddressView():
    def GetViewOffset(self, arg0: int) -> AddressView: ...
    def SetByte(self, arg0: int) -> bool: ...
    def SetBytes(self, arg0: list) -> bool: ...
    def SetChar(self, arg0: str) -> bool: ...
    def SetDouble(self, arg0: float) -> bool: ...
    def SetFloat(self, arg0: float) -> bool: ...
    def SetInt(self, arg0: int) -> bool: ...
    def SetLong(self, arg0: int) -> bool: ...
    def SetSByte(self, arg0: int) -> bool: ...
    def SetShort(self, arg0: int) -> bool: ...
    def SetStr(self, arg0: str) -> bool: ...
    def SetUInt(self, arg0: int) -> bool: ...
    def SetULong(self, arg0: int) -> bool: ...
    def SetUShort(self, arg0: int) -> bool: ...
    def SetWChar(self, arg0: str) -> bool: ...
    def ToByte(self) -> int: ...
    def ToBytes(self, arg0: int) -> list: ...
    def ToChar(self, arg0: int) -> str: ...
    def ToDouble(self) -> float: ...
    def ToFloat(self) -> float: ...
    def ToInt(self) -> int: ...
    def ToLong(self) -> int: ...
    def ToSByte(self) -> int: ...
    def ToShort(self) -> int: ...
    def ToString(self, arg0: int) -> str: ...
    def ToUInt(self) -> int: ...
    def ToULong(self) -> int: ...
    def ToUShort(self) -> int: ...
    def ToWChar(self) -> str: ...
    def __add__(self, arg0: int) -> AddressView: ...
    def __iadd__(self, arg0: int) -> AddressView: ...
    def __imul__(self, arg0: int) -> AddressView: ...
    def __isub__(self, arg0: int) -> AddressView: ...
    def __itruediv__(self, arg0: int) -> AddressView: ...
    def __mul__(self, arg0: int) -> AddressView: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __sub__(self, arg0: int) -> AddressView: ...
    def __truediv__(self, arg0: int) -> AddressView: ...
    @property
    def Address(self) -> int:
        """
        :type: int
        """
    pass
class AllocationType():
    """
    Members:

      COMMIT

      LARGE_PAGES

      PHYSICAL

      RESERVE

      RESET

      RESET_UNDO

      TOP_DOWN
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    COMMIT: CheatPy.AllocationType # value = <AllocationType.COMMIT: 4096>
    LARGE_PAGES: CheatPy.AllocationType # value = <AllocationType.LARGE_PAGES: 536870912>
    PHYSICAL: CheatPy.AllocationType # value = <AllocationType.PHYSICAL: 4194304>
    RESERVE: CheatPy.AllocationType # value = <AllocationType.RESERVE: 8192>
    RESET: CheatPy.AllocationType # value = <AllocationType.RESET: 524288>
    RESET_UNDO: CheatPy.AllocationType # value = <AllocationType.RESET_UNDO: 16777216>
    TOP_DOWN: CheatPy.AllocationType # value = <AllocationType.TOP_DOWN: 1048576>
    __members__: dict # value = {'COMMIT': <AllocationType.COMMIT: 4096>, 'LARGE_PAGES': <AllocationType.LARGE_PAGES: 536870912>, 'PHYSICAL': <AllocationType.PHYSICAL: 4194304>, 'RESERVE': <AllocationType.RESERVE: 8192>, 'RESET': <AllocationType.RESET: 524288>, 'RESET_UNDO': <AllocationType.RESET_UNDO: 16777216>, 'TOP_DOWN': <AllocationType.TOP_DOWN: 1048576>}
    pass
class Cheat():
    def AllocMemory(self, arg0: int, arg1: AllocationType, arg2: MemoryProtection) -> int: ...
    def Close(self) -> bool: ...
    def CreateThread(self, arg0: int, arg1: int) -> bool: ...
    def Execute(self, arg0: int, arg1: int) -> int: ...
    def FreeMemory(self, arg0: int, arg1: int, arg2: MemoryFreeType) -> bool: ...
    @typing.overload
    def GetAddressView(self, arg0: int) -> AddressView: ...
    @typing.overload
    def GetAddressView(self, arg0: int, arg1: list) -> AddressView: ...
    def GetModule(self, arg0: str) -> Module: ...
    def GetModules(self) -> list: ...
    def Inject(self, arg0: str) -> Module: ...
    def IsEmpty(self) -> bool: ...
    def Scanner(self, arg0: list, arg1: int) -> list: ...
    def ScannerModule(self, arg0: list, arg1: Module, arg2: int) -> list: ...
    def ScannerRegion(self, arg0: list, arg1: int, arg2: int, arg3: int) -> list: ...
    def __bool__(self) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @property
    def ID(self) -> int:
        """
        :type: int
        """
    @property
    def Name(self) -> str:
        """
        :type: str
        """
    pass
class KeyCode():
    """
    Members:

      Mouse0

      Mouse1

      Mouse2

      Mouse3

      Mouse4

      Keypad0

      Keypad1

      Keypad2

      Keypad3

      Keypad4

      Keypad5

      Keypad6

      Keypad7

      Keypad8

      Keypad9

      A

      B

      C

      D

      E

      F

      G

      H

      I

      J

      K

      L

      M

      N

      O

      P

      Q

      R

      S

      T

      U

      V

      W

      X

      Y

      Z

      Tab

      Space

      Backspace

      Delete

      Esc

      Shift

      LeftShift

      RightShift

      Control

      RightControl

      LeftControl

      Alt

      LeftAlt

      RightAlt

      Enter

      KeypadPeriod

      KeypadComma

      KeypadDivide

      KeypadMultiply

      KeypadMinus

      KeypadPlus

      UpArrow

      DownArrow

      RightArrow

      LeftArrow

      F1

      F2

      F3

      F4

      F5

      F6

      F7

      F8

      F9

      F10

      F11

      F12

      F13

      F14

      F15

      Alpha0

      Alpha1

      Alpha2

      Alpha3

      Alpha4

      Alpha5

      Alpha6

      Alpha7

      Alpha8

      Alpha9

      DoubleQuote

      KeypadEqual

      Add

      Subtract

      Decimal
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    A: CheatPy.KeyCode # value = <KeyCode.A: 65>
    Add: CheatPy.KeyCode # value = <KeyCode.Add: 107>
    Alpha0: CheatPy.KeyCode # value = <KeyCode.Alpha0: 96>
    Alpha1: CheatPy.KeyCode # value = <KeyCode.Alpha1: 97>
    Alpha2: CheatPy.KeyCode # value = <KeyCode.Alpha2: 98>
    Alpha3: CheatPy.KeyCode # value = <KeyCode.Alpha3: 99>
    Alpha4: CheatPy.KeyCode # value = <KeyCode.Alpha4: 100>
    Alpha5: CheatPy.KeyCode # value = <KeyCode.Alpha5: 101>
    Alpha6: CheatPy.KeyCode # value = <KeyCode.Alpha6: 102>
    Alpha7: CheatPy.KeyCode # value = <KeyCode.Alpha7: 103>
    Alpha8: CheatPy.KeyCode # value = <KeyCode.Alpha8: 104>
    Alpha9: CheatPy.KeyCode # value = <KeyCode.Alpha9: 105>
    Alt: CheatPy.KeyCode # value = <KeyCode.Alt: 18>
    B: CheatPy.KeyCode # value = <KeyCode.B: 66>
    Backspace: CheatPy.KeyCode # value = <KeyCode.Backspace: 8>
    C: CheatPy.KeyCode # value = <KeyCode.C: 67>
    Control: CheatPy.KeyCode # value = <KeyCode.Control: 17>
    D: CheatPy.KeyCode # value = <KeyCode.D: 68>
    Decimal: CheatPy.KeyCode # value = <KeyCode.Decimal: 110>
    Delete: CheatPy.KeyCode # value = <KeyCode.Delete: 46>
    DoubleQuote: CheatPy.KeyCode # value = <KeyCode.DoubleQuote: 222>
    DownArrow: CheatPy.KeyCode # value = <KeyCode.DownArrow: 40>
    E: CheatPy.KeyCode # value = <KeyCode.E: 69>
    Enter: CheatPy.KeyCode # value = <KeyCode.Enter: 13>
    Esc: CheatPy.KeyCode # value = <KeyCode.Esc: 27>
    F: CheatPy.KeyCode # value = <KeyCode.F: 70>
    F1: CheatPy.KeyCode # value = <KeyCode.F1: 112>
    F10: CheatPy.KeyCode # value = <KeyCode.F10: 121>
    F11: CheatPy.KeyCode # value = <KeyCode.F11: 122>
    F12: CheatPy.KeyCode # value = <KeyCode.F12: 123>
    F13: CheatPy.KeyCode # value = <KeyCode.F13: 124>
    F14: CheatPy.KeyCode # value = <KeyCode.F14: 125>
    F15: CheatPy.KeyCode # value = <KeyCode.F15: 126>
    F2: CheatPy.KeyCode # value = <KeyCode.F2: 113>
    F3: CheatPy.KeyCode # value = <KeyCode.F3: 114>
    F4: CheatPy.KeyCode # value = <KeyCode.F4: 115>
    F5: CheatPy.KeyCode # value = <KeyCode.F5: 116>
    F6: CheatPy.KeyCode # value = <KeyCode.F6: 117>
    F7: CheatPy.KeyCode # value = <KeyCode.F7: 118>
    F8: CheatPy.KeyCode # value = <KeyCode.F8: 119>
    F9: CheatPy.KeyCode # value = <KeyCode.F9: 120>
    G: CheatPy.KeyCode # value = <KeyCode.G: 71>
    H: CheatPy.KeyCode # value = <KeyCode.H: 72>
    I: CheatPy.KeyCode # value = <KeyCode.I: 73>
    J: CheatPy.KeyCode # value = <KeyCode.J: 74>
    K: CheatPy.KeyCode # value = <KeyCode.K: 75>
    Keypad0: CheatPy.KeyCode # value = <KeyCode.Keypad0: 48>
    Keypad1: CheatPy.KeyCode # value = <KeyCode.Keypad1: 49>
    Keypad2: CheatPy.KeyCode # value = <KeyCode.Keypad2: 50>
    Keypad3: CheatPy.KeyCode # value = <KeyCode.Keypad3: 51>
    Keypad4: CheatPy.KeyCode # value = <KeyCode.Keypad4: 52>
    Keypad5: CheatPy.KeyCode # value = <KeyCode.Keypad5: 53>
    Keypad6: CheatPy.KeyCode # value = <KeyCode.Keypad6: 54>
    Keypad7: CheatPy.KeyCode # value = <KeyCode.Keypad7: 55>
    Keypad8: CheatPy.KeyCode # value = <KeyCode.Keypad8: 56>
    Keypad9: CheatPy.KeyCode # value = <KeyCode.Keypad9: 57>
    KeypadComma: CheatPy.KeyCode # value = <KeyCode.KeypadComma: 188>
    KeypadDivide: CheatPy.KeyCode # value = <KeyCode.KeypadDivide: 111>
    KeypadEqual: CheatPy.KeyCode # value = <KeyCode.KeypadEqual: 146>
    KeypadMinus: CheatPy.KeyCode # value = <KeyCode.KeypadMinus: 189>
    KeypadMultiply: CheatPy.KeyCode # value = <KeyCode.KeypadMultiply: 106>
    KeypadPeriod: CheatPy.KeyCode # value = <KeyCode.KeypadPeriod: 190>
    KeypadPlus: CheatPy.KeyCode # value = <KeyCode.KeypadPlus: 187>
    L: CheatPy.KeyCode # value = <KeyCode.L: 76>
    LeftAlt: CheatPy.KeyCode # value = <KeyCode.LeftAlt: 164>
    LeftArrow: CheatPy.KeyCode # value = <KeyCode.LeftArrow: 37>
    LeftControl: CheatPy.KeyCode # value = <KeyCode.LeftControl: 162>
    LeftShift: CheatPy.KeyCode # value = <KeyCode.LeftShift: 160>
    M: CheatPy.KeyCode # value = <KeyCode.M: 77>
    Mouse0: CheatPy.KeyCode # value = <KeyCode.Mouse0: 1>
    Mouse1: CheatPy.KeyCode # value = <KeyCode.Mouse1: 2>
    Mouse2: CheatPy.KeyCode # value = <KeyCode.Mouse2: 4>
    Mouse3: CheatPy.KeyCode # value = <KeyCode.Mouse3: 5>
    Mouse4: CheatPy.KeyCode # value = <KeyCode.Mouse4: 6>
    N: CheatPy.KeyCode # value = <KeyCode.N: 78>
    O: CheatPy.KeyCode # value = <KeyCode.O: 79>
    P: CheatPy.KeyCode # value = <KeyCode.P: 80>
    Q: CheatPy.KeyCode # value = <KeyCode.Q: 81>
    R: CheatPy.KeyCode # value = <KeyCode.R: 82>
    RightAlt: CheatPy.KeyCode # value = <KeyCode.RightAlt: 165>
    RightArrow: CheatPy.KeyCode # value = <KeyCode.RightArrow: 39>
    RightControl: CheatPy.KeyCode # value = <KeyCode.RightControl: 163>
    RightShift: CheatPy.KeyCode # value = <KeyCode.RightShift: 161>
    S: CheatPy.KeyCode # value = <KeyCode.S: 83>
    Shift: CheatPy.KeyCode # value = <KeyCode.Shift: 16>
    Space: CheatPy.KeyCode # value = <KeyCode.Space: 32>
    Subtract: CheatPy.KeyCode # value = <KeyCode.Subtract: 109>
    T: CheatPy.KeyCode # value = <KeyCode.T: 84>
    Tab: CheatPy.KeyCode # value = <KeyCode.Tab: 9>
    U: CheatPy.KeyCode # value = <KeyCode.U: 85>
    UpArrow: CheatPy.KeyCode # value = <KeyCode.UpArrow: 38>
    V: CheatPy.KeyCode # value = <KeyCode.V: 86>
    W: CheatPy.KeyCode # value = <KeyCode.W: 87>
    X: CheatPy.KeyCode # value = <KeyCode.X: 88>
    Y: CheatPy.KeyCode # value = <KeyCode.Y: 89>
    Z: CheatPy.KeyCode # value = <KeyCode.Z: 90>
    __members__: dict # value = {'Mouse0': <KeyCode.Mouse0: 1>, 'Mouse1': <KeyCode.Mouse1: 2>, 'Mouse2': <KeyCode.Mouse2: 4>, 'Mouse3': <KeyCode.Mouse3: 5>, 'Mouse4': <KeyCode.Mouse4: 6>, 'Keypad0': <KeyCode.Keypad0: 48>, 'Keypad1': <KeyCode.Keypad1: 49>, 'Keypad2': <KeyCode.Keypad2: 50>, 'Keypad3': <KeyCode.Keypad3: 51>, 'Keypad4': <KeyCode.Keypad4: 52>, 'Keypad5': <KeyCode.Keypad5: 53>, 'Keypad6': <KeyCode.Keypad6: 54>, 'Keypad7': <KeyCode.Keypad7: 55>, 'Keypad8': <KeyCode.Keypad8: 56>, 'Keypad9': <KeyCode.Keypad9: 57>, 'A': <KeyCode.A: 65>, 'B': <KeyCode.B: 66>, 'C': <KeyCode.C: 67>, 'D': <KeyCode.D: 68>, 'E': <KeyCode.E: 69>, 'F': <KeyCode.F: 70>, 'G': <KeyCode.G: 71>, 'H': <KeyCode.H: 72>, 'I': <KeyCode.I: 73>, 'J': <KeyCode.J: 74>, 'K': <KeyCode.K: 75>, 'L': <KeyCode.L: 76>, 'M': <KeyCode.M: 77>, 'N': <KeyCode.N: 78>, 'O': <KeyCode.O: 79>, 'P': <KeyCode.P: 80>, 'Q': <KeyCode.Q: 81>, 'R': <KeyCode.R: 82>, 'S': <KeyCode.S: 83>, 'T': <KeyCode.T: 84>, 'U': <KeyCode.U: 85>, 'V': <KeyCode.V: 86>, 'W': <KeyCode.W: 87>, 'X': <KeyCode.X: 88>, 'Y': <KeyCode.Y: 89>, 'Z': <KeyCode.Z: 90>, 'Tab': <KeyCode.Tab: 9>, 'Space': <KeyCode.Space: 32>, 'Backspace': <KeyCode.Backspace: 8>, 'Delete': <KeyCode.Delete: 46>, 'Esc': <KeyCode.Esc: 27>, 'Shift': <KeyCode.Shift: 16>, 'LeftShift': <KeyCode.LeftShift: 160>, 'RightShift': <KeyCode.RightShift: 161>, 'Control': <KeyCode.Control: 17>, 'RightControl': <KeyCode.RightControl: 163>, 'LeftControl': <KeyCode.LeftControl: 162>, 'Alt': <KeyCode.Alt: 18>, 'LeftAlt': <KeyCode.LeftAlt: 164>, 'RightAlt': <KeyCode.RightAlt: 165>, 'Enter': <KeyCode.Enter: 13>, 'KeypadPeriod': <KeyCode.KeypadPeriod: 190>, 'KeypadComma': <KeyCode.KeypadComma: 188>, 'KeypadDivide': <KeyCode.KeypadDivide: 111>, 'KeypadMultiply': <KeyCode.KeypadMultiply: 106>, 'KeypadMinus': <KeyCode.KeypadMinus: 189>, 'KeypadPlus': <KeyCode.KeypadPlus: 187>, 'UpArrow': <KeyCode.UpArrow: 38>, 'DownArrow': <KeyCode.DownArrow: 40>, 'RightArrow': <KeyCode.RightArrow: 39>, 'LeftArrow': <KeyCode.LeftArrow: 37>, 'F1': <KeyCode.F1: 112>, 'F2': <KeyCode.F2: 113>, 'F3': <KeyCode.F3: 114>, 'F4': <KeyCode.F4: 115>, 'F5': <KeyCode.F5: 116>, 'F6': <KeyCode.F6: 117>, 'F7': <KeyCode.F7: 118>, 'F8': <KeyCode.F8: 119>, 'F9': <KeyCode.F9: 120>, 'F10': <KeyCode.F10: 121>, 'F11': <KeyCode.F11: 122>, 'F12': <KeyCode.F12: 123>, 'F13': <KeyCode.F13: 124>, 'F14': <KeyCode.F14: 125>, 'F15': <KeyCode.F15: 126>, 'Alpha0': <KeyCode.Alpha0: 96>, 'Alpha1': <KeyCode.Alpha1: 97>, 'Alpha2': <KeyCode.Alpha2: 98>, 'Alpha3': <KeyCode.Alpha3: 99>, 'Alpha4': <KeyCode.Alpha4: 100>, 'Alpha5': <KeyCode.Alpha5: 101>, 'Alpha6': <KeyCode.Alpha6: 102>, 'Alpha7': <KeyCode.Alpha7: 103>, 'Alpha8': <KeyCode.Alpha8: 104>, 'Alpha9': <KeyCode.Alpha9: 105>, 'DoubleQuote': <KeyCode.DoubleQuote: 222>, 'KeypadEqual': <KeyCode.KeypadEqual: 146>, 'Add': <KeyCode.Add: 107>, 'Subtract': <KeyCode.Subtract: 109>, 'Decimal': <KeyCode.Decimal: 110>}
    pass
class MemoryFreeType():
    """
    Members:

      DECOMMIT

      RELEASE
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DECOMMIT: CheatPy.MemoryFreeType # value = <MemoryFreeType.DECOMMIT: 16384>
    RELEASE: CheatPy.MemoryFreeType # value = <MemoryFreeType.RELEASE: 32768>
    __members__: dict # value = {'DECOMMIT': <MemoryFreeType.DECOMMIT: 16384>, 'RELEASE': <MemoryFreeType.RELEASE: 32768>}
    pass
class MemoryProtection():
    """
    Members:

      EXECUTE

      EXECUTE_READ

      EXECUTE_READWRITE

      EXECUTE_WRITECOPY

      NOACCESS

      READONLY

      READWRITE

      WRITECOPY

      TARGETS_INVALID

      TARGETS_NO_UPDATE

      GUARD

      NOCACHE

      WRITECOMBINE
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    EXECUTE: CheatPy.MemoryProtection # value = <MemoryProtection.EXECUTE: 16>
    EXECUTE_READ: CheatPy.MemoryProtection # value = <MemoryProtection.EXECUTE_READ: 32>
    EXECUTE_READWRITE: CheatPy.MemoryProtection # value = <MemoryProtection.EXECUTE_READWRITE: 64>
    EXECUTE_WRITECOPY: CheatPy.MemoryProtection # value = <MemoryProtection.EXECUTE_WRITECOPY: 128>
    GUARD: CheatPy.MemoryProtection # value = <MemoryProtection.GUARD: 256>
    NOACCESS: CheatPy.MemoryProtection # value = <MemoryProtection.NOACCESS: 1>
    NOCACHE: CheatPy.MemoryProtection # value = <MemoryProtection.NOCACHE: 512>
    READONLY: CheatPy.MemoryProtection # value = <MemoryProtection.READONLY: 2>
    READWRITE: CheatPy.MemoryProtection # value = <MemoryProtection.READWRITE: 4>
    TARGETS_INVALID: CheatPy.MemoryProtection # value = <MemoryProtection.TARGETS_INVALID: 1073741824>
    TARGETS_NO_UPDATE: CheatPy.MemoryProtection # value = <MemoryProtection.TARGETS_INVALID: 1073741824>
    WRITECOMBINE: CheatPy.MemoryProtection # value = <MemoryProtection.WRITECOMBINE: 1024>
    WRITECOPY: CheatPy.MemoryProtection # value = <MemoryProtection.WRITECOPY: 8>
    __members__: dict # value = {'EXECUTE': <MemoryProtection.EXECUTE: 16>, 'EXECUTE_READ': <MemoryProtection.EXECUTE_READ: 32>, 'EXECUTE_READWRITE': <MemoryProtection.EXECUTE_READWRITE: 64>, 'EXECUTE_WRITECOPY': <MemoryProtection.EXECUTE_WRITECOPY: 128>, 'NOACCESS': <MemoryProtection.NOACCESS: 1>, 'READONLY': <MemoryProtection.READONLY: 2>, 'READWRITE': <MemoryProtection.READWRITE: 4>, 'WRITECOPY': <MemoryProtection.WRITECOPY: 8>, 'TARGETS_INVALID': <MemoryProtection.TARGETS_INVALID: 1073741824>, 'TARGETS_NO_UPDATE': <MemoryProtection.TARGETS_INVALID: 1073741824>, 'GUARD': <MemoryProtection.GUARD: 256>, 'NOCACHE': <MemoryProtection.NOCACHE: 512>, 'WRITECOMBINE': <MemoryProtection.WRITECOMBINE: 1024>}
    pass
class Module():
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @property
    def Address(self) -> int:
        """
        :type: int
        """
    @property
    def Name(self) -> str:
        """
        :type: str
        """
    @property
    def Size(self) -> int:
        """
        :type: int
        """
    pass
class Process():
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @property
    def ID(self) -> int:
        """
        :type: int
        """
    @property
    def Name(self) -> str:
        """
        :type: str
        """
    pass
def Alert(arg0: str, arg1: str) -> None:
    pass
def GetKey(arg0: KeyCode) -> bool:
    pass
def GetProcess(arg0: str) -> Cheat:
    pass
def GetProcessFromID(arg0: int) -> Cheat:
    pass
def GetProcesses() -> list:
    pass
