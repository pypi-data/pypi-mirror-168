Example Code:

```py
from CheatPy import *
import time
            
def MENUCLI(dz:Cheat,cheat1:AddressView,cheat2:AddressView,cheat3: AddressView,cheat4: AddressView,cheat5: AddressView):
    def ToStr(v: bool):
        if v:
            return "ON"
        else:
            return "OFF"
    
    enable1 = enable2 = enable3 = enable4 = False
    event1 = event2 = event3 = event4 = event5 = event6 = False
    cheatbuff = {
        False:[0xF7, 0xDA],
        True:[0x31, 0xD2]
    }
    cheatbuff2 = {
        False:[0x29, 0xF8 ],
        True: [0x90,0x90]
    }
    cheatbuff3 = {
        False:[ 0x39, 0x83, 0x40, 0x01, 0x00, 0x00 ],
        True :[ 0x39, 0xC0, 0x90, 0x90, 0x90, 0x90 ]
    }
    offset = [0x60,0x98,0x40,0xA8]
    print("1. No Consume Tower")
    print("2. No Consume Update Tower")
    print("3. No Damage")
    print("4. Fast Update Tower")
    print("5. Add Money")
    print("6. Close")
    while True:
        event1 = GetKey(KeyCode.Keypad1)
        if event1:
            enable1 = not enable1
            cheat1.SetBytes(cheatbuff[enable1])
        event2 = GetKey(KeyCode.Keypad2)
        if event2:
            enable2 = not enable2
            cheat2.SetBytes(cheatbuff[enable2])
        event3 = GetKey(KeyCode.Keypad3)
        if event3:
            enable3 = not enable3
            cheat3.SetBytes(cheatbuff2[enable3])
        event4 = GetKey(KeyCode.Keypad4)
        if event4:
            enable4 = not enable4
            cheat4.SetBytes(cheatbuff3[enable4])
        

        event5 = GetKey(KeyCode.Keypad5)

        if event5:
            cheat6 = dz.GetAddressView(cheat5.Address,offset)
            cheat6.SetInt(cheat6.ToInt() + 1000)
        
        
        event6 = GetKey(KeyCode.Keypad6)
        if event6:
            dz.Close()
            break
        time.sleep(1)


dz = GetProcess("Defense Zone - Original.exe")


if dz:
    gameassembly = dz.GetModule("GameAssembly.dll")
    gameassembly_addr = gameassembly.Address
    unityengine = dz.GetModule("UnityPlayer.dll").Address 

    test = dz.ScannerModule([0x8B, 0x90, 0x14, 0x01, 0x00, 0x00, 0x45, 0x33, 0xC0, 0xF7, 0xDA, 0x48, 0x8B, 0xCB],gameassembly,1)
    
    if len(test) > 0:
        print(hex(test[0].Address))
    cheat5 = dz.GetAddressView(unityengine + 0x01614508)
    
    if gameassembly_addr != 0:
        cheat1 = dz.GetAddressView(gameassembly_addr + 0x18288C)
        cheat2 = dz.GetAddressView(gameassembly_addr + 0x17BCB1)
        cheat3 = dz.GetAddressView(gameassembly_addr + 0x181797)
        cheat4 = dz.GetAddressView(gameassembly_addr + 0x24EAB9)
        MENUCLI(dz,cheat1,cheat2,cheat3,cheat4,cheat5)
else:
    Alert("Not found","Maury Dev")
```