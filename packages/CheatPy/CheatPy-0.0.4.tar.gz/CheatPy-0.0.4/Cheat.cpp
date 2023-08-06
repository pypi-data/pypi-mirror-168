// dllmain.cpp : Define o ponto de entrada para o aplicativo DLL.

#include <pybind11/pybind11.h>
#pragma comment(lib, "user32.lib")
#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#define DllExport   __declspec( dllexport )


namespace py = pybind11;


template<typename T>
struct ObjectFree
{
    void operator()(T* v)
    {
        v->Free();
    }
};

struct AddressView
{
    HANDLE process;
    UINT64 Address;
    std::wstring __str__()
    {
        return  std::to_wstring(Address);
    }
    std::wstring __repr__()
    {

        return __str__();
    }
    AddressView __add__(UINT64 offset)
    {
        AddressView ret = { process,Address + offset };
        return ret;
    }
    AddressView __sub__(UINT64 offset)
    {
        AddressView ret = { process,Address - offset };
        return ret;
    }
    AddressView __mul__(UINT64 offset)
    {
        AddressView ret = { process,Address * offset };
        return ret;
    }
    AddressView __truediv__(UINT64 offset)
    {
        AddressView ret = { process,Address / offset };
        return ret;
    }
    AddressView __iadd__(UINT64 offset)
    {
        this->Address += offset;
        return *this;
    }
    AddressView __isub__(UINT64 offset)
    {
        this->Address -= offset;
        return *this;
    }
    AddressView __imul__(UINT64 offset)
    {
        this->Address *= offset;
        return *this;
    }
    AddressView __itruediv__(UINT64 offset)
    {
        this->Address /= offset;
        return *this;
    }
    AddressView GetViewOffset(UINT64 offset)
    {

        AddressView ret = { process,Address + offset };
        return ret;
    }
    void Read(LPVOID result, int size)
    {
        SIZE_T numbersbyte = 0;
        ReadProcessMemory(process, (LPCVOID)Address, result, size, &numbersbyte);
    }
    void Read(LPVOID result, int size,UINT64 offset)
    {
        SIZE_T numbersbyte = 0;
        ReadProcessMemory(process, (LPCVOID)(Address + offset), result, size, &numbersbyte);
    }
    int ToInt()
    {
        int v = 0;
        Read(&v, sizeof(int));
        return v;
    }
    UINT ToUInt()
    {
        UINT v = 0;
        Read(&v, sizeof(UINT));
        return v;
    }

    char ToChar(UINT64 address)
    {
        char v = 0;
        Read(&v, sizeof(char));
        return v;
    }
    wchar_t ToWChar()
    {
        wchar_t v = 0;
        Read(&v, sizeof(wchar_t));
        return v;
    }
    int ToByte()
    {
        BYTE v;
        Read(&v, sizeof(BYTE));
        return v;
    }
    int ToSByte()
    {
        INT8 v;
        Read(&v, sizeof(INT8));
        return v;
    }
    double ToDouble()
    {
        double v;
        Read(&v, sizeof(double));
        return v;
    }
    float ToFloat()
    {
        float v;
        Read(&v, sizeof(float));
        return v;
    }
    int ToUShort()
    {
        UINT16 v;
        Read(&v, sizeof(UINT16));
        return v;
    }
    int ToShort()
    {
        INT16 v;
        Read(&v, sizeof(INT16));
        return v;
    }
    int ToLong()
    {
        INT64 v;
        Read(&v, sizeof(INT64));
        return v;
    }
    UINT64 ToULong()
    {
        UINT64 v;
        Read(&v, sizeof(UINT64));
        return v;
    }
    py::str ToString(int maxlen)
    {
        if (maxlen > 0)
        {
            int size = 0;
            uint8_t* buff = (uint8_t*)malloc(maxlen);
            Read(buff, maxlen);
            auto val = buff[0];
            while (val != 0 && size < maxlen)
            {
                size++;
                val = buff[size];
            }
            auto str = py::str((const char*)buff,size);
            free(buff);
            return str;
        }
        return py::str("");
    }
    py::list ToBytes(int numbytes)
    {        
        py::list arr(numbytes);
        int val = 0;
        uint8_t* buff = (uint8_t*)malloc(numbytes);
        Read(buff, numbytes);
        for (size_t i = 0; i < numbytes; i++)
        {
            arr[i] = buff[i];
        }
        free(buff);
        return arr;
    }
    bool Write(LPVOID value, int size)
    {
        SIZE_T numbersbyte = 0;

        WriteProcessMemory(process, (LPVOID)Address, value, size, &numbersbyte);
        return numbersbyte != 0;
    }
    bool Write(LPVOID value, int size,UINT64 offset)
    {
        SIZE_T numbersbyte = 0;

        WriteProcessMemory(process, (LPVOID)(Address + offset), value, size, &numbersbyte);
        return numbersbyte != 0;
    }
    bool SetInt(int value)
    {
        return Write(&value, sizeof(int));
    }
    bool SetUInt(UINT32 value)
    {
        return Write(&value, sizeof(UINT32));
    }
    bool SetByte(uint8_t value)
    {
        return Write(&value, sizeof(uint8_t));
    }
    bool SetSByte(int8_t value)
    {
        return Write(&value, sizeof(int8_t));
    }
    bool SetChar(char value)
    {
        return Write(&value, sizeof(char));
    }
    bool SetWChar(wchar_t value)
    {
        return Write(&value, sizeof(wchar_t));
    }
    bool SetShort(int16_t value)
    {
        return Write(&value, sizeof(int16_t));
    }
    bool SetUShort(uint16_t value)
    {
        return Write(&value, sizeof(uint16_t));
    }
    bool SetLong(INT64 value)
    {
        return Write(&value, sizeof(INT64));
    }
    bool SetULong(UINT64 value)
    {
        return Write(&value, sizeof(UINT64));
    }
    bool SetFloat(float value)
    {
        return Write(&value, sizeof(float));
    }
    bool SetDouble(double value)
    {
        return Write(&value, sizeof(double));
    }
    bool SetStr(py::str value)
    {
        
        auto len = py::len(value);
        auto getitem = value.attr("__getitem__");
        uint8_t* buff = (uint8_t*)malloc(len);
        auto flag = true;
        for (size_t i = 0; i < len; i++)
        {
            auto v = getitem(i).cast<int>();
            buff[i] = v;
        }
        Write(buff, len);
        free(buff);
        return flag;
    }
    bool SetBytes(py::list& lt)
    {
        auto len = lt.size();
        auto flag = true;
        uint8_t* buff = (uint8_t*)malloc(len);
        for (size_t i = 0; i < len; i++)
        {
            auto v = lt[i].cast<uint8_t>();
           
            buff[i] = v;
        }
        Write(buff, len);
        free(buff);
        return flag;
    }
};
struct Module
{
    UINT64 Address;
    wchar_t* name;
    UINT64 size;
    std::wstring __str__()
    {
        std::wstring str;
        str.reserve(50);
        str = name;
        str += L" - ";
        str += std::to_wstring(Address);
        return str;
    }
    std::wstring __repr__()
    {

        return __str__();
    }
    void Free()
    {
        free(name);
    }
};
struct Process
{
    UINT64 ID;
    wchar_t* name;
    void Free()
    {
        free(name);
    }
    std::wstring __str__()
    {
        std::wstring str;
        str.reserve(50);
        str = name;
        str += L" - ";
        str += std::to_wstring(ID);
        return str;
    }
    std::wstring __repr__()
    {

        return __str__();
    }
};
enum class KeyCode
{
    LBUTTON = 0x01,
    RBUTTON = 0x02,
    CANCEL = 0x03,
    MBUTTON = 0x04,
    XBUTTON1_ = 0x05,
    XBUTTON2_ = 0x06,
    BACK = 0x08,
    TAB = 0x09,
    CLEAR = 0x0C,
    RETURN = 0x0D,
    SHIFT = 0x10,
    CONTROL = 0x11,
    MENU = 0x12,
    PAUSE = 0x13,
    CAPITAL = 0x14,
    ESCAPE = 0x1B,
    CONVERT = 0x1C,
    NONCONVERT = 0x1D,
    ACCEPT = 0x1E,
    MODECHANGE = 0x1F,
    SPACE = 0x20,
    PRIOR = 0x21,
    NEXT = 0x22,
    END = 0x23,
    HOME = 0x24,
    LEFT = 0x25,
    UP = 0x26,
    RIGHT = 0x27,
    DOWN = 0x28,
    SELECT = 0x29,
    PRINT = 0x2A,
    EXECUTE = 0x2B,
    SNAPSHOT = 0x2C,
    INSERT = 0x2D,
    DELETE_ = 0x2E,
    HELP = 0x2F,
    Keypad0 = 0x30,
    Keypad1 = 0x31,
    Keypad2 = 0x32,
    Keypad3 = 0x33,
    Keypad4 = 0x34,
    Keypad5 = 0x35,
    Keypad6 = 0x36,
    Keypad7 = 0x37,
    Keypad8 = 0x38,
    Keypad9 = 0x39,
    A = 0x41,
    B = 0x42,
    C = 0x43,
    D = 0x44,
    E = 0x45,
    F = 0x46,
    G = 0x47,
    H = 0x48,
    I = 0x49,
    J = 0x4A,
    K = 0x4B,
    L = 0x4C,
    M = 0x4D,
    N = 0x4E,
    O = 0x4F,
    P = 0x50,
    Q = 0x51,
    R = 0x52,
    S = 0x53,
    T = 0x54,
    U = 0x55,
    V = 0x56,
    W = 0x57,
    X = 0x58,
    Y = 0x59,
    Z = 0x5A,
    LWIN = 0x5B,
    RWIN = 0x5C,
    APPS = 0x5D,
    SLEEP = 0x5F,
    NUMPAD0 = 0x60,
    NUMPAD1 = 0x61,
    NUMPAD2 = 0x62,
    NUMPAD3 = 0x63,
    NUMPAD4 = 0x64,
    NUMPAD5 = 0x65,
    NUMPAD6 = 0x66,
    NUMPAD7 = 0x67,
    NUMPAD8 = 0x68,
    NUMPAD9 = 0x69,
    MULTIPLY = 0x6A,
    ADD = 0x6B,
    SEPARATOR = 0x6C,
    SUBTRACT = 0x6D,
    DECIMAL = 0x6E,
    DIVIDE = 0x6F,
    F1 = 0x70,
    F2 = 0x71,
    F3 = 0x72,
    F4 = 0x73,
    F5 = 0x74,
    F6 = 0x75,
    F7 = 0x76,
    F8 = 0x77,
    F9 = 0x78,
    F10 = 0x79,
    F11 = 0x7A,
    F12 = 0x7B,
    F13 = 0x7C,
    F14 = 0x7D,
    F15 = 0x7E,
    F16 = 0x7F,
    F17 = 0x80,
    F18 = 0x81,
    F19 = 0x82,
    F20 = 0x83,
    F21 = 0x84,
    F22 = 0x85,
    F23 = 0x86,
    F24 = 0x87,
    NUMLOCK = 0x90,
    SCROLL = 0x91,
    OEM_NEC_EQUAL = 0x92,
    LSHIFT = 0xA0,
    RSHIFT = 0xA1,
    LCONTROL = 0xA2,
    RCONTROL = 0xA3,
    LMENU = 0xA4,
    RMENU = 0xA5,
    BROWSER_BACK = 0xA6,
    BROWSER_FORWARD = 0xA7,
    BROWSER_REFRESH = 0xA8,
    BROWSER_STOP = 0xA9,
    BROWSER_SEARCH = 0xAA,
    BROWSER_FAVORITES = 0xAB,
    BROWSER_HOME = 0xAC,
    VOLUME_MUTE = 0xAD,
    VOLUME_DOWN = 0xAE,
    VOLUME_UP = 0xAF,
    MEDIA_NEXT_TRACK = 0xB0,
    MEDIA_PREV_TRACK = 0xB1,
    MEDIA_STOP = 0xB2,
    MEDIA_PLAY_PAUSE = 0xB3,
    LAUNCH_MAIL = 0xB4,
    LAUNCH_MEDIA_SELECT = 0xB5,
    LAUNCH_APP1 = 0xB6,
    LAUNCH_APP2 = 0xB7,
    OEM_1 = 0xBA,
    OEM_PLUS = 0xBB,
    OEM_COMMA = 0xBC,
    OEM_MINUS = 0xBD,
    OEM_PERIOD = 0xBE,
    OEM_2 = 0xBF,
    OEM_3 = 0xC0,
    OEM_4 = 0xDB,
    OEM_5 = 0xDC,
    OEM_6 = 0xDD,
    OEM_7 = 0xDE,
    OEM_8 = 0xDF,
    OEM = 0xE1,
    OEM_102 = 0xE2,
    PROCESSKEY = 0xE5,
    PACKET = 0xE7,
    ATTN = 0xF6,
    CRSEL = 0xF7,
    EXSEL = 0xF8,
    EREOF = 0xF9,
    PLAY = 0xFA,
    ZOOM = 0xFB,
    NONAME = 0xFC,
    PA1 = 0xFD,
    OEM_CLEAR = 0xFE
};
enum class AllocationType
{
    COMMIT = 4096,
    RESERVE = 8192,
    RESET = 524288,
    RESET_UNDO = 16777216,
    LARGE_PAGES = 536870912,
    PHYSICAL = 4194304,
    TOP_DOWN = 1048576
};
enum class MemoryProtection
{
    EXECUTE = 16,
    EXECUTE_READ = 32,
    EXECUTE_READWRITE = 64,
    EXECUTE_WRITECOPY = 128,
    NOACCESS = 1,
    READONLY = 2,
    READWRITE = 4,
    WRITECOPY = 8,
    TARGETS_INVALID = 1073741824,
    TARGETS_NO_UPDATE = 1073741824,
    GUARD = 256,
    NOCACHE = 512,
    WRITECOMBINE = 1024
};
enum class MemoryFreeType
{
    DECOMMIT = 16384,
    RELEASE = 32768
};
struct Cheat
{
    HANDLE process;
    DWORD id;
    wchar_t* name;
    void Free()
    {
        free(name);
    }
    AddressView GetAddressView(UINT64 address)
    {
        AddressView v = { process,address };
        return v;
    }
    AddressView GetAddressView(UINT64 address,py::list& offsets)
    {
        AddressView v = { process,address };
        int len = py::len(offsets);
        for (size_t i = 0; i < len; i++)
        {
            auto _value = v.ToULong() + offsets[i].cast<UINT64>();
            v.Address = _value;
        }
        return v;
    }
    bool __bool__()
    {
        return process != NULL;
    }
    std::wstring __str__()
    {
        std::wstring str;
        str.reserve(50);
        str = name;
        str += L" - ";
        str += std::to_wstring(id);
        return str;
    }
    std::wstring __repr__()
    {
        
        return __str__();
    }
    bool IsEmpty()
    {
        return process == NULL;
    }
    bool Close()
    {
        bool ret = CloseHandle(process);
        process = NULL;
        return ret;
    }
    UINT64 AllocMemory(int size, AllocationType allocationtype, MemoryProtection protectiontype)
    {
        auto address = VirtualAllocEx(process, NULL, size, (DWORD)allocationtype, (DWORD)protectiontype);
        return (UINT64)address;
    }
    bool FreeMemory(UINT64 address,int size, MemoryFreeType freetype)
    {
        return (bool)VirtualFreeEx(process, (LPVOID)address, size, (DWORD)freetype);
    }
    Module GetModule(const wchar_t* modulename)
    {
        Module module = {0,nullptr};
        MODULEENTRY32W ModuleEntry = { 0 };
        HANDLE SnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, id);

        if (!SnapShot) return module;

        ModuleEntry.dwSize = sizeof(ModuleEntry);

        if (!Module32FirstW(SnapShot, &ModuleEntry)) return module;

        do
        {
            if (!lstrcmpW(ModuleEntry.szModule, modulename))
            {
                auto szModule = ModuleEntry.szModule;
                auto len = lstrlenW(szModule);
                wchar_t* str = new wchar_t[(UINT64)len + 1];
                for (size_t i = 0; i < len; i++)
                {
                    str[i] = szModule[i];
                }
                str[len] = L'\0';
                module.Address = (UINT64)ModuleEntry.modBaseAddr;
                module.name = str;
                module.size = ModuleEntry.modBaseSize;

                break;
            }
        } while (Module32NextW(SnapShot, &ModuleEntry));

        CloseHandle(SnapShot);
        return module;
    }
    bool CreateThread(UINT64 address,UINT64 arg)
    {
        return CreateRemoteThread(process, NULL, 0, (LPTHREAD_START_ROUTINE)address, (LPVOID)arg, NULL, NULL) != NULL;
    }
    UINT64 Execute(UINT64 address, UINT64 arg)
    {

        auto thread = CreateRemoteThread(process, NULL, 0, (LPTHREAD_START_ROUTINE)address, (LPVOID)arg, NULL, NULL);
        if (thread == NULL)
        {
            return NULL;
        }
        if (WaitForSingleObject(thread, -1) == WAIT_FAILED)
        {
            return NULL;
        }

        DWORD exitcode;
        GetExitCodeThread(thread, &exitcode);
        CloseHandle(thread);
        return exitcode;
    }
    Module Inject(const WCHAR* dll_file_)
    {
        Module ret = { 0,nullptr };
        // get the full path of the dll file
        WCHAR full_dll_path[MAX_PATH];
        GetFullPathNameW(dll_file_, MAX_PATH, full_dll_path, NULL);
        // get the function LoadLibraryA
        HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
        if (kernel32 != NULL)
        {
            LPVOID load_library = GetProcAddress(kernel32, "LoadLibraryW");
            if (load_library != NULL)
            {
                auto len = (UINT64)lstrlenW(full_dll_path) * 2 + 1;
                // allocate space to write the dll location
                LPVOID dll_parameter_address = VirtualAllocEx(process, 0, len, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
                if (dll_parameter_address != NULL)
                {
                    // write the dll location to the space we previously allocated
                    BOOL wrote_memory = WriteProcessMemory(process, dll_parameter_address, full_dll_path, len, NULL);
                    if (wrote_memory != false)
                    {
                        // launch the dll using LoadLibraryA
                        HANDLE dll_thread_handle = CreateRemoteThread(process, 0, 0, (LPTHREAD_START_ROUTINE)load_library, dll_parameter_address, 0, 0);
                        if (dll_thread_handle != NULL)
                        {
                            if (WaitForSingleObject(dll_thread_handle, -1) == WAIT_IO_COMPLETION)
                            {
                                DWORD V;
                                GetExitCodeThread(dll_thread_handle, &V);
                                CloseHandle(dll_thread_handle);
                                Sleep(10);
                                ret = GetModule(dll_file_);
                            }
              
                        }
                        
                    }
                    VirtualFreeEx(process, dll_parameter_address, 0, (DWORD)MemoryFreeType::RELEASE);
                }

                
            }
            
        }

        
        return ret;
    }
    py::list GetModules()
    {
        py::list values;
        MODULEENTRY32W ModuleEntry = { 0 };
        HANDLE SnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, id);

        if (!SnapShot) return values;

        ModuleEntry.dwSize = sizeof(ModuleEntry);

        if (!Module32FirstW(SnapShot, &ModuleEntry)) return values;

        do
        {
            auto szModule = ModuleEntry.szModule;
            auto len = lstrlenW(szModule);
            wchar_t* str = new wchar_t[(UINT64)len + 1];
            for (size_t i = 0; i < len; i++)
            {
                str[i] = szModule[i];
            }
            str[len] = L'\0';
            
            Module module = { (UINT64)ModuleEntry.modBaseAddr,str,ModuleEntry.modBaseSize };

            values.append(module);
        } while (Module32NextW(SnapShot, &ModuleEntry));

        CloseHandle(SnapShot);
        return values;
    }
    py::list ScannerModule(py::list& lt, Module module_, UINT64 maxlen)
    {
        return ScannerRegion(lt, module_.Address, module_.Address + module_.size, maxlen);
    }
    py::list ScannerRegion(py::list& lt, UINT64 start, UINT64 end, UINT64 maxlen)
    {
        SIZE_T lpNumberOfBytesRead;
        auto lenregion = end - start;
        auto lt_size = lt.size();

        uint8_t* bytes = (uint8_t*)malloc(lt_size);
        py::list ret;
        int len = 0;
        for (size_t i = 0; i < lt_size; i++)
        {
            bytes[i] = lt[i].cast<uint8_t>();
        }
        auto buffer = (uint8_t*)malloc(lenregion);

        if (buffer != NULL)
        {
            ReadProcessMemory(process, (LPCVOID)start, buffer, lenregion, &lpNumberOfBytesRead);
            for (size_t i = 0; i < lpNumberOfBytesRead - lt_size; i++)
            {
                bool flag = true;
                for (size_t i2 = 0; i2 < lt_size; i2++)
                {
                    if (bytes[i2] != buffer[i + i2])
                    {
                        flag = false;
                        break;
                    }
                }
                if (flag)
                {

                    ret.append(GetAddressView(start + i));
                    len++;

                    if (len >= maxlen)
                    {
                        break;
                    }
                }

            }
            free(buffer);
        }
        free(bytes);
        return ret;
    }

    py::list Scanner(py::list& lt, UINT64 maxlen)
    {
        PBYTE pb = NULL;
        uint8_t* buffer;
        MEMORY_BASIC_INFORMATION mbi;
        SIZE_T lpNumberOfBytesRead;
        auto lt_size = lt.size();

        uint8_t* bytes = (uint8_t*)malloc(lt_size);
        py::list ret;
        int len = 0;
        for (size_t i = 0; i < lt_size; i++)
        {
            bytes[i] = lt[i].cast<uint8_t>();
        }
        while (VirtualQueryEx(process, pb, &mbi, sizeof(mbi)) == sizeof(mbi))
        {
            if (len >= maxlen)
            {
                break;
            }
            bool valid = mbi.State == MEM_COMMIT;
            
            valid &= ((mbi.Protect & PAGE_GUARD) == 0);
            valid &= ((mbi.Protect & PAGE_NOACCESS) == 0);
            valid &= (mbi.Type == MEM_PRIVATE) || (mbi.Type == MEM_IMAGE);
            if (!valid) 
            {
                pb = ((uint8_t*)mbi.BaseAddress + mbi.RegionSize);
                continue;
            }

            buffer = (uint8_t*)malloc(mbi.RegionSize);
            if (buffer != NULL)
            {
                ReadProcessMemory(process, mbi.BaseAddress, buffer, mbi.RegionSize, &lpNumberOfBytesRead);
                
                for (size_t i = 0; i < lpNumberOfBytesRead - lt_size; i++)
                {
                    bool flag = true;
                    for (size_t i2 = 0; i2 < lt_size; i2++)
                    {
                        if (bytes[i2] != buffer[i+i2])
                        {
                            flag = false;
                            break;
                        }
                    }
                    if (flag)
                    {
                        
                        ret.append(GetAddressView((UINT64)mbi.BaseAddress + i));
                        len++;

                        if (len >= maxlen)
                        {
                            break;
                        }
                    }

                }
                
                free(buffer);

            }
            pb = ((uint8_t*)mbi.BaseAddress + mbi.RegionSize);
        }
        free(bytes);
        return ret;
    }
    
};
Cheat GetProcess(WCHAR* processname)
{
    Cheat ret = { nullptr,0 ,nullptr};
    
    PROCESSENTRY32W entry;
    
    entry.dwSize = sizeof(PROCESSENTRY32W);
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);
    if (Process32FirstW(snapshot, &entry) == TRUE)
    {
        while (Process32NextW(snapshot, &entry) == TRUE)
        {
            auto szExeFile = entry.szExeFile;
            if (!lstrcmpW(szExeFile, processname))
            {
                
                HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
                auto len = lstrlenW(szExeFile);
                wchar_t* str = new wchar_t[(UINT64)len + 1];
                for (size_t i = 0; i < len; i++)
                {
                    str[i] = entry.szExeFile[i];
                }
                str[len] = L'\0';
                ret = { hProcess,entry.th32ProcessID,str };
                break;
            }
        }
    }

    CloseHandle(snapshot);
    return ret;
}
Cheat GetProcessFromID(UINT64 id)
{
    Cheat ret = { nullptr,0 ,nullptr };

    PROCESSENTRY32W entry;

    entry.dwSize = sizeof(PROCESSENTRY32W);
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);
    if (Process32FirstW(snapshot, &entry) == TRUE)
    {
        while (Process32NextW(snapshot, &entry) == TRUE)
        {
            auto th32ProcessID = entry.th32ProcessID;
            if (th32ProcessID == id)
            {
                auto szExeFile = entry.szExeFile;
                HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, entry.th32ProcessID);
                auto len = lstrlenW(szExeFile);
                wchar_t* str = new wchar_t[(UINT64)len + 1];
                for (size_t i = 0; i < len; i++)
                {
                    str[i] = entry.szExeFile[i];
                }
                str[len] = L'\0';
                ret = { hProcess,th32ProcessID,str };
                break;
            }
        }
    }

    CloseHandle(snapshot);
    return ret;
}
py::list GetProcesses()
{
    py::list values;

    PROCESSENTRY32W entry;

    entry.dwSize = sizeof(PROCESSENTRY32W);
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);
    if (Process32FirstW(snapshot, &entry) == TRUE)
    {
        while (Process32NextW(snapshot, &entry) == TRUE)
        {
            auto szExeFile = entry.szExeFile;
            auto len = lstrlenW(szExeFile);
            wchar_t* str = new wchar_t[(UINT64)len + 1];
            for (size_t i = 0; i < len; i++)
            {
                str[i] = entry.szExeFile[i];
            }
            str[len] = L'\0';
            Process ret = { entry.th32ProcessID,str };
            values.append(ret);
        }
    }

    CloseHandle(snapshot);
    return values;
}
bool GetKey(KeyCode _code)
{
    return GetAsyncKeyState((int)_code) != 0;
}
void MessageBox_(const wchar_t* text,const wchar_t* caption)
{
    MessageBoxW(NULL, text, caption, MB_OK);
}
PYBIND11_MODULE(CheatPy, m) {
	m.doc() = "Cheat.py";
    m.def("GetProcess", &GetProcess);
    m.def("GetProcessFromID", &GetProcessFromID);
    m.def("GetProcesses", &GetProcesses);
    m.def("GetKey", &GetKey);
    m.def("Alert", &MessageBox_);

    auto cheat = py::class_<Cheat, std::unique_ptr<Cheat, ObjectFree<Cheat>>>(m, "Cheat");
    
    cheat.def("__bool__", &Cheat::__bool__);
    cheat.def("__repr__", &Cheat::__repr__);
    cheat.def("__str__", &Cheat::__str__);

    cheat.def("IsEmpty", &Cheat::IsEmpty);
    cheat.def("Close", &Cheat::Close);
    cheat.def("AllocMemory", &Cheat::AllocMemory);
    cheat.def("FreeMemory", &Cheat::FreeMemory);
    cheat.def("GetModule", &Cheat::GetModule);
    cheat.def("CreateThread", &Cheat::CreateThread);
    cheat.def("Execute", &Cheat::Execute);
    cheat.def("Inject", &Cheat::Inject);
    cheat.def("GetModules", &Cheat::GetModules);
    cheat.def("GetAddressView",py::overload_cast<UINT64>(&Cheat::GetAddressView));
    cheat.def("GetAddressView", py::overload_cast<UINT64,py::list&>(&Cheat::GetAddressView));
    cheat.def("Scanner",&Cheat::Scanner);
    cheat.def("ScannerModule",&Cheat::ScannerModule);
    cheat.def("ScannerRegion",&Cheat::ScannerRegion);

    cheat.def_readonly("ID", &Cheat::id);
    cheat.def_readonly("Name", &Cheat::name);

    auto allocationType = py::enum_<AllocationType>(m, "AllocationType");
    allocationType.value("COMMIT", AllocationType::COMMIT);
    allocationType.value("LARGE_PAGES", AllocationType::LARGE_PAGES);
    allocationType.value("PHYSICAL", AllocationType::PHYSICAL);
    allocationType.value("RESERVE", AllocationType::RESERVE);
    allocationType.value("RESET", AllocationType::RESET);
    allocationType.value("RESET_UNDO", AllocationType::RESET_UNDO);
    allocationType.value("TOP_DOWN", AllocationType::TOP_DOWN);

    auto memoryProtection = py::enum_<MemoryProtection>(m, "MemoryProtection");
    memoryProtection.value("EXECUTE", MemoryProtection::EXECUTE);
    memoryProtection.value("EXECUTE_READ", MemoryProtection::EXECUTE_READ);
    memoryProtection.value("EXECUTE_READWRITE", MemoryProtection::EXECUTE_READWRITE);
    memoryProtection.value("EXECUTE_WRITECOPY", MemoryProtection::EXECUTE_WRITECOPY);
    memoryProtection.value("NOACCESS", MemoryProtection::NOACCESS);
    memoryProtection.value("READONLY", MemoryProtection::READONLY);
    memoryProtection.value("READWRITE", MemoryProtection::READWRITE);
    memoryProtection.value("WRITECOPY", MemoryProtection::WRITECOPY);
    memoryProtection.value("TARGETS_INVALID", MemoryProtection::TARGETS_INVALID);
    memoryProtection.value("TARGETS_NO_UPDATE", MemoryProtection::TARGETS_NO_UPDATE);
    memoryProtection.value("GUARD", MemoryProtection::GUARD);
    memoryProtection.value("NOCACHE", MemoryProtection::NOCACHE);
    memoryProtection.value("WRITECOMBINE", MemoryProtection::WRITECOMBINE);
    
    auto memoryFreeType = py::enum_<MemoryFreeType>(m, "MemoryFreeType");
    memoryFreeType.value("DECOMMIT", MemoryFreeType::DECOMMIT);
    memoryFreeType.value("RELEASE", MemoryFreeType::RELEASE);
    
    auto module = py::class_<Module,std::unique_ptr<Module, ObjectFree<Module>>>(m, "Module");
    module.def_readonly("Address", &Module::Address);
    module.def_readonly("Name", &Module::name);
    module.def_readonly("Size", &Module::size);
    module.def("__repr__", &Module::__repr__);
    module.def("__str__", &Module::__str__);

    auto process = py::class_<Process, std::unique_ptr<Process, ObjectFree<Process>>>(m, "Process");
    process.def_readonly("ID", &Process::ID);
    process.def_readonly("Name", &Process::name);
    process.def("__repr__", &Process::__repr__);
    process.def("__str__", &Process::__str__);

    auto addressView = py::class_<AddressView >(m, "AddressView");
    addressView.def_readonly("Address", &AddressView::Address);
    addressView.def("__str__", &AddressView::__str__);
    addressView.def("__repr__", &AddressView::__repr__);
    addressView.def("__add__", &AddressView::__add__);
    addressView.def("__sub__", &AddressView::__sub__);
    addressView.def("__mul__", &AddressView::__mul__);
    addressView.def("__truediv__", &AddressView::__truediv__);
    addressView.def("__iadd__", &AddressView::__iadd__);
    addressView.def("__isub__", &AddressView::__isub__);
    addressView.def("__imul__", &AddressView::__imul__);
    addressView.def("__itruediv__", &AddressView::__itruediv__);

    addressView.def("GetViewOffset", &AddressView::GetViewOffset);

    addressView.def("ToByte", &AddressView::ToByte);
    addressView.def("ToBytes", &AddressView::ToBytes);
    addressView.def("ToChar", &AddressView::ToChar);
    addressView.def("ToDouble", &AddressView::ToDouble);
    addressView.def("ToFloat", &AddressView::ToFloat);
    addressView.def("ToInt", &AddressView::ToInt);
    addressView.def("ToLong", &AddressView::ToLong);
    addressView.def("ToSByte", &AddressView::ToSByte);
    addressView.def("ToShort", &AddressView::ToShort);
    addressView.def("ToString", &AddressView::ToString);
    addressView.def("ToUInt", &AddressView::ToUInt);
    addressView.def("ToULong", &AddressView::ToULong);
    addressView.def("ToUShort", &AddressView::ToUShort);
    addressView.def("ToWChar", &AddressView::ToWChar);
    addressView.def("SetByte", &AddressView::SetByte);
    addressView.def("SetBytes", &AddressView::SetBytes);
    addressView.def("SetChar", &AddressView::SetChar);
    addressView.def("SetDouble", &AddressView::SetDouble);
    addressView.def("SetFloat", &AddressView::SetFloat);
    addressView.def("SetInt", &AddressView::SetInt);
    addressView.def("SetLong", &AddressView::SetLong);
    addressView.def("SetSByte", &AddressView::SetSByte);
    addressView.def("SetShort", &AddressView::SetShort);
    addressView.def("SetStr", &AddressView::SetStr);
    addressView.def("SetUInt", &AddressView::SetUInt);
    addressView.def("SetULong", &AddressView::SetULong);
    addressView.def("SetUShort", &AddressView::SetUShort);
    addressView.def("SetWChar", &AddressView::SetWChar);

    auto keyCode = py::enum_<KeyCode>(m, "KeyCode");
    keyCode.value("Mouse0", KeyCode::LBUTTON);
    keyCode.value("Mouse1", KeyCode::RBUTTON);
    keyCode.value("Mouse2", KeyCode::MBUTTON);
    keyCode.value("Mouse3", KeyCode::XBUTTON1_);
    keyCode.value("Mouse4", KeyCode::XBUTTON2_);

    keyCode.value("Keypad0", KeyCode::Keypad0);
    keyCode.value("Keypad1", KeyCode::Keypad1);
    keyCode.value("Keypad2", KeyCode::Keypad2);
    keyCode.value("Keypad3", KeyCode::Keypad3);
    keyCode.value("Keypad4", KeyCode::Keypad4);
    keyCode.value("Keypad5", KeyCode::Keypad5);
    keyCode.value("Keypad6", KeyCode::Keypad6);
    keyCode.value("Keypad7", KeyCode::Keypad7);
    keyCode.value("Keypad8", KeyCode::Keypad8);
    keyCode.value("Keypad9", KeyCode::Keypad9);

    keyCode.value("A", KeyCode::A);
    keyCode.value("B", KeyCode::B);
    keyCode.value("C", KeyCode::C);
    keyCode.value("D", KeyCode::D);
    keyCode.value("E", KeyCode::E);
    keyCode.value("F", KeyCode::F);
    keyCode.value("G", KeyCode::G);
    keyCode.value("H", KeyCode::H);
    keyCode.value("I", KeyCode::I);
    keyCode.value("J", KeyCode::J);
    keyCode.value("K", KeyCode::K);
    keyCode.value("L", KeyCode::L);
    keyCode.value("M", KeyCode::M);
    keyCode.value("N", KeyCode::N);
    keyCode.value("O", KeyCode::O);
    keyCode.value("P", KeyCode::P);
    keyCode.value("Q", KeyCode::Q);
    keyCode.value("R", KeyCode::R);
    keyCode.value("S", KeyCode::S);
    keyCode.value("T", KeyCode::T);
    keyCode.value("U", KeyCode::U);
    keyCode.value("V", KeyCode::V);
    keyCode.value("W", KeyCode::W);
    keyCode.value("X", KeyCode::X);
    keyCode.value("Y", KeyCode::Y);
    keyCode.value("Z", KeyCode::Z);
    keyCode.value("Tab", KeyCode::TAB);
    keyCode.value("Space", KeyCode::SPACE);
    keyCode.value("Backspace", KeyCode::BACK);
    keyCode.value("Delete", KeyCode::DELETE_);
    keyCode.value("Esc", KeyCode::ESCAPE);
    keyCode.value("Shift", KeyCode::SHIFT);
    keyCode.value("LeftShift", KeyCode::LSHIFT);
    keyCode.value("RightShift", KeyCode::RSHIFT);
    keyCode.value("Control", KeyCode::CONTROL);
    keyCode.value("RightControl", KeyCode::RCONTROL);
    keyCode.value("LeftControl", KeyCode::LCONTROL);
    keyCode.value("Alt", KeyCode::MENU);
    keyCode.value("LeftAlt", KeyCode::LMENU);
    keyCode.value("RightAlt", KeyCode::RMENU);
    keyCode.value("Enter", KeyCode::RETURN);

    keyCode.value("KeypadPeriod", KeyCode::OEM_PERIOD);
    keyCode.value("KeypadComma", KeyCode::OEM_COMMA);

    keyCode.value("KeypadDivide", KeyCode::DIVIDE);
    keyCode.value("KeypadMultiply", KeyCode::MULTIPLY);
    keyCode.value("KeypadMinus", KeyCode::OEM_MINUS);
    keyCode.value("KeypadPlus", KeyCode::OEM_PLUS);
    keyCode.value("UpArrow", KeyCode::UP);
    keyCode.value("DownArrow", KeyCode::DOWN);
    keyCode.value("RightArrow", KeyCode::RIGHT);
    keyCode.value("LeftArrow", KeyCode::LEFT);

    keyCode.value("F1", KeyCode::F1);
    keyCode.value("F2", KeyCode::F2);
    keyCode.value("F3", KeyCode::F3);
    keyCode.value("F4", KeyCode::F4);
    keyCode.value("F5", KeyCode::F5);
    keyCode.value("F6", KeyCode::F6);
    keyCode.value("F7", KeyCode::F7);
    keyCode.value("F8", KeyCode::F8);
    keyCode.value("F9", KeyCode::F9);
    keyCode.value("F10", KeyCode::F10);
    keyCode.value("F11", KeyCode::F11);
    keyCode.value("F12", KeyCode::F12);
    keyCode.value("F13", KeyCode::F13);
    keyCode.value("F14", KeyCode::F14);
    keyCode.value("F15", KeyCode::F15);
    keyCode.value("Alpha0", KeyCode::NUMPAD0);
    keyCode.value("Alpha1", KeyCode::NUMPAD1);
    keyCode.value("Alpha2", KeyCode::NUMPAD2);
    keyCode.value("Alpha3", KeyCode::NUMPAD3);
    keyCode.value("Alpha4", KeyCode::NUMPAD4);
    keyCode.value("Alpha5", KeyCode::NUMPAD5);
    keyCode.value("Alpha6", KeyCode::NUMPAD6);
    keyCode.value("Alpha7", KeyCode::NUMPAD7);
    keyCode.value("Alpha8", KeyCode::NUMPAD8);
    keyCode.value("Alpha9", KeyCode::NUMPAD9);
    keyCode.value("DoubleQuote", KeyCode::OEM_7);
    keyCode.value("KeypadEqual", KeyCode::OEM_NEC_EQUAL);
    keyCode.value("Add", KeyCode::ADD);
    keyCode.value("Subtract", KeyCode::SUBTRACT);
    keyCode.value("Decimal", KeyCode::DECIMAL);


}


