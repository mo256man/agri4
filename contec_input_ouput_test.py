import ctypes
import sys
import cdio
import time
import datetime

class Contec():
    def __ini__(self):
        self.DEV_NAME = "DIO000"
        self.dio_id = ctypes.c_short()
        self.io_data = ctypes.c_ubyte()
        self.port_no = ctypes.c_short(0)
        self.bit_no = ctypes.c_short()
        self.err_str = ctypes.create_string_buffer(256)
        lret = cdio.DioInit(DEV_NAME.encode(), ctypes.byref(dio_id))
        port_no = ctypes.c_short(0)
        if lret != cdio.DIO_ERR_SUCCESS:
            cdio.DioGetErrorString(lret, err_str)
            print(f"DioInit = {lret}: {err_str.value.decode('utf-8')}")
            sys.exit()

    def input(self):
        lret = cdio.DioInpByte(self.dio_id, self.port_no, self.ctypes.byref(io_data))
        if lret == cdio.DIO_ERR_SUCCESS:
            cdio.DioGetErrorString(lret, err_str)
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')} : 十六進数で 0x{io_data.value:02x}、二進数で 0b{format(io_data.value, '08b')}")
        else:
            cdio.DioGetErrorString(lret, err_str)
            print(f"DioInpByte = {lret}: {err_str.value.decode('utf-8')}")

def light_on(bool):
    dio_id = ctypes.c_short()
    io_data = ctypes.c_ubyte()
    port_no = ctypes.c_short()
    bit_no = ctypes.c_short()
    err_str = ctypes.create_string_buffer(256)
    DEV_NAME = "DIO000"
    port_no = ctypes.c_short(0)
    lret = cdio.DioInit(DEV_NAME.encode(), ctypes.byref(dio_id))

    buf = 0x10000000 if bool else 0b00000000
    io_data = ctypes.c_ubyte(buf)
    lret = cdio.DioOutByte(dio_id, port_no, io_data)
    if lret == cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')} : 0x{io_data.value:02x}, 0b{format(io_data.value, '08b')}")
    else:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioOutByte = {lret}: {err_str.value.decode('utf-8')}")            


def main():
    dio_id = ctypes.c_short()
    io_data = ctypes.c_ubyte()
    port_no = ctypes.c_short()
    bit_no = ctypes.c_short()
    err_str = ctypes.create_string_buffer(256)

    # ドライバ初期化
    DEV_NAME = "DIO000"
    lret = cdio.DioInit(DEV_NAME.encode(), ctypes.byref(dio_id))
    port_no = ctypes.c_short(0)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioInit = {lret}: {err_str.value.decode('utf-8')}")
        sys.exit()

    # メインループ
    try:
        while True:
            lret = cdio.DioInpByte(dio_id, port_no, ctypes.byref(io_data))
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f"{datetime.datetime.now().strftime('%H:%M:%S')} : 十六進数で 0x{io_data.value:02x}、二進数で 0b{format(io_data.value, '08b')}")
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioInpByte = {lret}: {err_str.value.decode('utf-8')}")

            cnt = bin(io_data.value).count("1")
            print(f"光センサー　点灯数＝{cnt}")
            if cnt < 2:
                print("　→　十分明るい")
                light_on(False)
            else:
                print("　→　暗いのでLED点灯する")
                light_on(True)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n終了")
        # ドライバ終了
        lret = cdio.DioExit(dio_id)
        if lret != cdio.DIO_ERR_SUCCESS:
            cdio.DioGetErrorString(lret, err_str)
            print(f"DioExit = {lret}: {err_str.value.decode('utf-8')}")
        # プログラム終了
        time.sleep(3)
        sys.exit()

if __name__ == "__main__":
    main()
