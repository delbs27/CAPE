# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.cuckoo.common.abstracts import Signature

class UsesWindowsUtilities(Signature):
    name = "uses_windows_utilities"
    description = "Uses Windows utilities for basic functionality"
    severity = 2
    confidence = 80
    categories = ["commands", "lateral"]
    authors = ["Cuckoo Technologies", "Kevin Ross"]
    minimum = "1.3"
    evented = True

    def run(self):
        utilities = [
            "at ",
            "at.exe",
            "attrib",
            "copy",
            "dir ",
            "dir.exe",
            "echo"
            "erase",
            "fsutil",
            "getmac",
            "ipconfig",
            "md ",
            "md.exe",
            "mkdir",
            "move ",
            "move.exe",
            "nbtstat",
            "net ",
            "net.exe",
            "netsh",
            "netstat",
            "nslookup",
            "ping",
            "powercfg"
            "qprocess",
            "query ",
            "query.exe",
            "quser",
            "qwinsta",
            "reg ",
            "reg.exe",
            "regsrv32",
            "ren ",
            "ren.exe",
            "rename",
            "route",
            "runas",
            "rwinsta",
            "sc ",
            "sc.exe",
            "schtasks",
            "set ",
            "set.exe",
            "shutdown",
            "systeminfo",
            "tasklist",
            "telnet",
            "tracert",
            "tree ",
            "tree.exe",
            "type",
            "ver ",
            "ver.exe",
            "whoami",
            "wmic",
            "wusa",
        ]

        ret = False
        cmdlines = self.results["behavior"]["summary"]["executed_commands"]
        for cmdline in cmdlines:
            lower = cmdline.lower()
            for utility in utilities:
                if utility in lower:
                    ret = True
                    self.data.append({"command" : cmdline})

        return ret

class SuspiciousCommandTools(Signature):
    name = "suspicious_command_tools"
    description = "Uses suspicious command line tools or Windows utilities"
    severity = 3
    confidence = 80
    categories = ["commands", "lateral"]
    authors = ["Cuckoo Technologies", "Kevin Ross"]
    minimum = "1.3"
    evented = True

    def run(self):
        utilities = [
            "accesschk",
            "accessenum",
            "adexplorer",
            "adinsight",
            "adrestore",
            "autologon",
            "autoruns",
            "bcdedit",
            "bitsadmin",
            "bginfo",
            "cacls",
            "csvde",
            "del ",
            "del.exe",
            "dsquery",
            "icacls",
            "klist",
            "psexec",        
            "psfile",
            "psgetsid",
            "psinfo",
            "psping",
            "pskill",
            "pslist",
            "psloggedon",
            "psloglist",
            "pspasswd",
            "psservice",
            "psshutdown",
            "pssuspend",
            "rd ",
            "rd.exe",
            "rexec",
            "shareenum",
            "shellrunas",
            "taskkill",
            "volumeid",
            "vssadmin",
            "wbadmin",
            "wevtutil",
            "whois",
            "xcacls",
        ]

        ret = False
        cmdlines = self.results["behavior"]["summary"]["executed_commands"]
        for cmdline in cmdlines:
            lower = cmdline.lower()
            for utility in utilities:
                if utility in lower:
                    ret = True
                    self.data.append({"command" : cmdline})

        return ret

class ScriptToolExecuted(Signature):
    name = "script_tool_executed"
    description = "A scripting utility was executed"
    severity = 2
    confidence = 80
    categories = ["commands"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True

    def run(self):
        utilities = [
            "cscript",
            "powershell",
            "wscript",
        ]

        ret = False
        cmdlines = self.results["behavior"]["summary"]["executed_commands"]
        for cmdline in cmdlines:
            lower = cmdline.lower()
            for utility in utilities:
                if utility in lower:
                    ret = True
                    self.data.append({"command" : cmdline})

        return ret

class SuspiciousPingUse(Signature):
    name = "suspicious_ping_use"
    description = "A ping command was executed with the -n argument possibly to delay analysis"
    severity = 2
    confidence = 100
    categories = ["commands"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True

    def run(self):

        ret = False
        cmdlines = self.results["behavior"]["summary"]["executed_commands"]
        for cmdline in cmdlines:
            lower = cmdline.lower()
            if "ping" in lower and ("-n" in lower or "/n" in lower):
                ret = True
                self.data.append({"command" : cmdline})

        return ret

class WMICCommandSuspicious(Signature):
    name = "wmic_command_suspicious"
    description = "Suspicious wmic.exe use was detected"
    severity = 3
    confidence = 80
    categories = ["commands", "wmi"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True

    def run(self):
        arguments = [
            "antivirusproduct",
            "baseboard",
            "bios",
            "compuersystem",
            "datafile",
            "diskdrive",
            "group",
            "fsdir",
            "logicaldisk",
            "memcache",
            "memorychip",
            "nicconfig",
            "nteventlog",
            "onboarddevice",
            "os get",
            "process",
            "product",
            "qfe",
            "service",
            "startup",
            "sysdriver",
            "useraccount",
        ]

        ret = False
        cmdlines = self.results["behavior"]["summary"]["executed_commands"]
        for cmdline in cmdlines:
            lower = cmdline.lower()
            if "wmic" in lower:
                for argument in self.arguments:
                    if argument in lower:
                        ret = True
                        self.data.append({"command" : cmdline})

        return ret

class AltersWindowsUtility(Signature):
    name = "alters_windows_utility"
    description = "Attempts to move, copy or rename a command line or scripting utility likely for evasion"
    severity = 3
    categories = ["commands", "stealth", "evasion"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.ret = False
        self.utilities = [
            "at.exe",
            "cmd.exe",
            "cscript.exe",
            "net.exe",
            "powershell.exe",
            "regsrv32.exe",
            "sc.exe",
            "vssadmin.exe",
            "wevutil.exe",
            "wmic.exe",
            "wscript.exe",
            ]

    filter_apinames = set(["CopyFileExA","CopyFileExW","MoveFileWithProgressW","MoveFileWithProgressTransactedW"])

    def on_call(self, call, process):
        self.ret = False
        origfile = self.get_argument(call, "ExistingFileName")
        destfile = self.get_argument(call, "NewFileName")
        for utility in self.utilities:
            lower = origfile.lower()
            if lower.endswith(utility):
                self.ret = True
                self.data.append({"utility" : "source file %s destination file %s" % (origfile,destfile)})

    def on_complete(self):
        return self.ret
