import sys
import time
import frida

def on_message(message, data):
    print("[%s] => %s" % (message, data))

def main():
    device = frida.get_usb_device(timeout=1)
    pid = device.spawn('com.YoStarEN.Arknights')
    device.resume(pid)
    time.sleep(5)
    session = device.attach(pid, realm='emulated')
    script = session.create_script("""
    var proc = Module.findBaseAddress("libil2cpp.so")
    console.log("Initiating!")

    Interceptor.attach(proc.add(0xE97830), {
        onEnter: function (args) {
            console.log("Enter Crisis Battle!")
        },
        onLeave: function (retval) {
            retval.replace(0x1)
        }
    })

""")
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    main()