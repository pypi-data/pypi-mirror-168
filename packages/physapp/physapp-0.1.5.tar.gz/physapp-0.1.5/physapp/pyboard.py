# David THERINCOURT - 2020
#
# This file is a modification of the original pyboard.py edit by  MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2014-2019 Damien P. George
# Copyright (c) 2017 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
pyboard interface

This module provides the Pyboard class, used to communicate with and
control a MicroPython device over a communication channel. Both real
boards and emulated devices (e.g. running in QEMU) are supported.
Various communication channels are supported, including a serial
connection, telnet-style network connection, external process
connection.

Example usage:

    import pyboard
    pyb = pyboard.Pyboard('/dev/ttyACM0')

Or:

    pyb = pyboard.Pyboard('192.168.1.1')

Then:

    pyb.enter_raw_repl()
    pyb.exec('import pyb')
    pyb.exec('pyb.LED(1).on()')
    pyb.exit_raw_repl()


"""

import sys
import time
import os
from io import StringIO

try:
    stdout = sys.stdout.buffer
except AttributeError:
    # Python2 doesn't have buffer attr
    stdout = sys.stdout


def stdout_write_bytes(b):
    b = b.replace(b"\x04", b"")
    stdout.write(b)
    stdout.flush()


class PyboardError(Exception):
    pass


class TelnetToSerial:
    def __init__(self, ip, user, password, read_timeout=None):
        self.tn = None
        import telnetlib

        self.tn = telnetlib.Telnet(ip, timeout=15)
        self.read_timeout = read_timeout
        if b"Login as:" in self.tn.read_until(b"Login as:", timeout=read_timeout):
            self.tn.write(bytes(user, "ascii") + b"\r\n")

            if b"Password:" in self.tn.read_until(b"Password:", timeout=read_timeout):
                # needed because of internal implementation details of the telnet server
                time.sleep(0.2)
                self.tn.write(bytes(password, "ascii") + b"\r\n")

                if b"for more information." in self.tn.read_until(
                    b'Type "help()" for more information.', timeout=read_timeout
                ):
                    # login successful
                    from collections import deque

                    self.fifo = deque()
                    return

        raise PyboardError("Failed to establish a telnet connection with the board")

    def __del__(self):
        self.close()

    def close(self):
        if self.tn:
            self.tn.close()

    def read(self, size=1):
        while len(self.fifo) < size:
            timeout_count = 0
            data = self.tn.read_eager()
            if len(data):
                self.fifo.extend(data)
                timeout_count = 0
            else:
                time.sleep(0.25)
                if self.read_timeout is not None and timeout_count > 4 * self.read_timeout:
                    break
                timeout_count += 1

        data = b""
        while len(data) < size and len(self.fifo) > 0:
            data += bytes([self.fifo.popleft()])
        return data

    def write(self, data):
        self.tn.write(data)
        return len(data)

    def inWaiting(self):
        n_waiting = len(self.fifo)
        if not n_waiting:
            data = self.tn.read_eager()
            self.fifo.extend(data)
            return len(data)
        else:
            return n_waiting


class ProcessToSerial:
    "Execute a process and emulate serial connection using its stdin/stdout."

    def __init__(self, cmd):
        import subprocess

        self.subp = subprocess.Popen(
            cmd,
            bufsize=0,
            shell=True,
            preexec_fn=os.setsid,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        # Initially was implemented with selectors, but that adds Python3
        # dependency. However, there can be race conditions communicating
        # with a particular child process (like QEMU), and selectors may
        # still work better in that case, so left inplace for now.
        #
        # import selectors
        # self.sel = selectors.DefaultSelector()
        # self.sel.register(self.subp.stdout, selectors.EVENT_READ)

        import select

        self.poll = select.poll()
        self.poll.register(self.subp.stdout.fileno())

    def close(self):
        import signal

        os.killpg(os.getpgid(self.subp.pid), signal.SIGTERM)

    def read(self, size=1):
        data = b""
        while len(data) < size:
            data += self.subp.stdout.read(size - len(data))
        return data

    def write(self, data):
        self.subp.stdin.write(data)
        return len(data)

    def inWaiting(self):
        # res = self.sel.select(0)
        res = self.poll.poll(0)
        if res:
            return 1
        return 0


class ProcessPtyToTerminal:
    """Execute a process which creates a PTY and prints slave PTY as
    first line of its output, and emulate serial connection using
    this PTY."""

    def __init__(self, cmd):
        import subprocess
        import re
        import serial

        self.subp = subprocess.Popen(
            cmd.split(),
            bufsize=0,
            shell=False,
            preexec_fn=os.setsid,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        pty_line = self.subp.stderr.readline().decode("utf-8")
        m = re.search(r"/dev/pts/[0-9]+", pty_line)
        if not m:
            print("Error: unable to find PTY device in startup line:", pty_line)
            self.close()
            sys.exit(1)
        pty = m.group()
        # rtscts, dsrdtr params are to workaround pyserial bug:
        # http://stackoverflow.com/questions/34831131/pyserial-does-not-play-well-with-virtual-port
        self.ser = serial.Serial(pty, interCharTimeout=1, rtscts=True, dsrdtr=True)

    def close(self):
        import signal

        os.killpg(os.getpgid(self.subp.pid), signal.SIGTERM)

    def read(self, size=1):
        return self.ser.read(size)

    def write(self, data):
        return self.ser.write(data)

    def inWaiting(self):
        return self.ser.inWaiting()


class Pyboard:
    def __init__(self, device, baudrate=115200, user="micro", password="python", wait=0):
        if device.startswith("exec:"):
            self.serial = ProcessToSerial(device[len("exec:") :])
        elif device.startswith("execpty:"):
            self.serial = ProcessPtyToTerminal(device[len("qemupty:") :])
        elif device and device[0].isdigit() and device[-1].isdigit() and device.count(".") == 3:
            # device looks like an IP address
            self.serial = TelnetToSerial(device, user, password, read_timeout=10)
        else:
            import serial

            delayed = False
            for attempt in range(wait + 1):
                try:
                    self.serial = serial.Serial(device, baudrate=baudrate, interCharTimeout=1)
                    break
                except (OSError, IOError):  # Py2 and Py3 have different errors
                    if wait == 0:
                        continue
                    if attempt == 0:
                        sys.stdout.write("Waiting {} seconds for pyboard ".format(wait))
                        delayed = True
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
            else:
                if delayed:
                    print("")
                raise PyboardError("failed to access " + device)
            if delayed:
                print("")

    def close(self):
        self.serial.close()

    def read_until(self, min_num_bytes, ending, timeout=10, data_consumer=None):
        # if data_consumer is used then data is not accumulated and the ending must be 1 byte long
        assert data_consumer is None or len(ending) == 1

        data = self.serial.read(min_num_bytes)
        if data_consumer:
            data_consumer(data)
        timeout_count = 0
        while True:
            if data.endswith(ending):
                break
            elif self.serial.inWaiting() > 0:
                new_data = self.serial.read(1)
                if data_consumer:
                    data_consumer(new_data)
                    data = new_data
                else:
                    data = data + new_data
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 100 * timeout:
                    break
                time.sleep(0.01)
        return data

    def enter_raw_repl(self):
        self.serial.write(b"\r\x03\x03")  # ctrl-C twice: interrupt any running program

        # flush input (without relying on serial.flushInput())
        n = self.serial.inWaiting()
        while n > 0:
            self.serial.read(n)
            n = self.serial.inWaiting()

        self.serial.write(b"\r\x01")  # ctrl-A: enter raw REPL
        data = self.read_until(1, b"raw REPL; CTRL-B to exit\r\n>")
        if not data.endswith(b"raw REPL; CTRL-B to exit\r\n>"):
            print(data)
            raise PyboardError("could not enter raw repl")

        self.serial.write(b"\x04")  # ctrl-D: soft reset
        data = self.read_until(1, b"soft reboot\r\n")
        if not data.endswith(b"soft reboot\r\n"):
            print(data)
            raise PyboardError("could not enter raw repl")
        # By splitting this into 2 reads, it allows boot.py to print stuff,
        # which will show up after the soft reboot and before the raw REPL.
        data = self.read_until(1, b"raw REPL; CTRL-B to exit\r\n")
        if not data.endswith(b"raw REPL; CTRL-B to exit\r\n"):
            print(data)
            raise PyboardError("could not enter raw repl")

    def exit_raw_repl(self):
        self.serial.write(b"\r\x02")  # ctrl-B: enter friendly REPL

    def follow(self, timeout, data_consumer=None):
        # wait for normal output
        data = self.read_until(1, b"\x04", timeout=timeout, data_consumer=data_consumer)
        if not data.endswith(b"\x04"):
            raise PyboardError("timeout waiting for first EOF reception")
        data = data[:-1]

        # wait for error output
        data_err = self.read_until(1, b"\x04", timeout=timeout)
        if not data_err.endswith(b"\x04"):
            raise PyboardError("timeout waiting for second EOF reception")
        data_err = data_err[:-1]

        # return normal and error output
        return data, data_err

    def exec_raw_no_follow(self, command):
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding="utf8")

        # check we have a prompt
        data = self.read_until(1, b">")
        if not data.endswith(b">"):
            raise PyboardError("could not enter raw repl")

        # write command
        for i in range(0, len(command_bytes), 256):
            self.serial.write(command_bytes[i : min(i + 256, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b"\x04")

        # check if we could exec command
        data = self.serial.read(2)
        if data != b"OK":
            raise PyboardError("could not exec command (response: %r)" % data)

    def exec_raw(self, command, timeout=10, data_consumer=None):
        self.exec_raw_no_follow(command)
        return self.follow(timeout, data_consumer)

    def eval(self, expression):
        ret = self.exec_("print({})".format(expression))
        ret = ret.strip()
        return ret

    def exec_(self, command, data_consumer=None):
        ret, ret_err = self.exec_raw(command, data_consumer=data_consumer)
        if ret_err:
            raise PyboardError("exception", ret, ret_err)
        return ret

    def execfile(self, filename):
        with open(filename, "rb") as f:
            pyfile = f.read()
        return self.exec_(pyfile)

    def get_time(self):
        t = str(self.eval("pyb.RTC().datetime()"), encoding="utf8")[1:-1].split(", ")
        return int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6])

    def fs_ls(self, src):
        cmd = (
            "import uos\nfor f in uos.ilistdir(%s):\n"
            " print('{:12} {}{}'.format(f[3]if len(f)>3 else 0,f[0],'/'if f[1]&0x4000 else ''))"
            % (("'%s'" % src) if src else "")
        )
        self.exec_(cmd, data_consumer=stdout_write_bytes)

    def fs_cat(self, src, chunk_size=256):
        cmd = (
            "with open('%s') as f:\n while 1:\n"
            "  b=f.read(%u)\n  if not b:break\n  print(b,end='')" % (src, chunk_size)
        )
        self.exec_(cmd, data_consumer=stdout_write_bytes)

    def fs_get(self, src, dest, chunk_size=256):
        self.exec_("f=open('%s','rb')\nr=f.read" % src)
        with open(dest, "wb") as f:
            while True:
                data = bytearray()
                self.exec_("print(r(%u))" % chunk_size, data_consumer=lambda d: data.extend(d))
                assert data.endswith(b"\r\n\x04")
                data = eval(str(data[:-3], "ascii"))
                if not data:
                    break
                f.write(data)
        self.exec_("f.close()")

    def fs_put(self, src, dest, chunk_size=256):
        self.exec_("f=open('%s','wb')\nw=f.write" % dest)
        with open(src, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                if sys.version_info < (3,):
                    self.exec_("w(b" + repr(data) + ")")
                else:
                    self.exec_("w(" + repr(data) + ")")
        self.exec_("f.close()")

    def fs_mkdir(self, dir):
        self.exec_("import uos\nuos.mkdir('%s')" % dir)

    def fs_rmdir(self, dir):
        self.exec_("import uos\nuos.rmdir('%s')" % dir)

    def fs_rm(self, src):
        self.exec_("import uos\nuos.remove('%s')" % src)

    def exec(self, cmd):
        """
        Exécute une commande MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.
        La fonction retourne la chaîne de caractères renvoyée par la commande

        Paramètres :
            cmd (str) : instruction MicroPython

        Retourne (str) :
            Chaîne de caractères renvoyée par la commande dans le REPL
        """
        raw_output = self.exec_(cmd)
        output = raw_output.decode()
        return output[:-2]  # Return string without last 2 character "\r\n"

    def exec_file(self, fileName):
        """
        Exécute un programme MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.
        La fonction retourne une chaine de caractères transmise par une fonction print() placée dans le script.

        Paramètres :
            fileName (str) : nom du fichier MicroPython à exécuté.

        Retourne (str) :
            Chaîne de caractères transmit par la fonction print(str) du script micropython.
        """
        self.enter_raw_repl()
        output = self.execfile(fileName)
        self.exit_raw_repl()
        return output.decode()

    def exec_file_to_data(self, fileName):
        """
        Exécute un programme MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.
        La fonction retourne un tuple transmise par une fonction print() placée dans le script.

        Paramètres :
            fileName (str) : nom du fichier MicroPython à exécuté.

        Retourne (tuple) :
            Tuple transmis par une unique fonction print(tuple) placée dans le script micropython.
            Exemple : print((x,y))
        """
        self.enter_raw_repl()
        data = self.execfile(fileName)
        self.exit_raw_repl()
        return eval(data.decode())

    def exec_file_to_csv(self, fileName, csvFileName = "data.txt", sep = ';', headerLine = '# MicroPython Data'):
        self.enter_raw_repl()
        data = self.execfile(fileName)
        self.exit_raw_repl()
        data = eval(data.decode())
        data = np.transpose(data)
        np.savetxt(csvFileName, data, delimiter = sep, header = headerLine, comments='')

    def exec_script(self, lines):
        """
        Exécute un script MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.
        La fonction retourne une chaine de caractères transmise par une fonction print() placée dans le script.

        Paramètres :
            lines (str) : script sous forme d'une chaîne de caractères sur plusieurs lignes

        Retourne (str) :
            Chaîne de caractères transmit par la fonction print(str) du script micropython.
        """
        self.enter_raw_repl()
        output = self.exec_(lines)
        self.exit_raw_repl()
        return output.decode()

    def exec_script_to_data(self, lines):
        """
        Exécute un script MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.
        La fonction retourne un tuple transmise par une fonction print() placée dans le script.

        Paramètres :
            lines (str) : script sous forme d'une chaine de caractères sur plusieurs lignes

        Retourne (tuple) :
            Tuple transmis par une unique fonction print(tuple) placée dans le script micropython.
            Exemple : print((x,y))
        """
        self.enter_raw_repl()
        data = self.exec_(lines)
        self.exit_raw_repl()
        return eval(data.decode())
