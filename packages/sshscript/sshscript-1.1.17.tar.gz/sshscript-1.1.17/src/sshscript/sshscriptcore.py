# Copyright (C) 2022-2026  Hsin Yuan Yeh <iapyeh@gmail.com>
#
# This file is part of Sshscript.
#
# SSHScript is free software; you can redistribute it and/or modify it under the
# terms of the MIT License.
#
# SSHScript is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the MIT License for more details.
#
# You should have received a copy of the MIT License along with SSHScript;
# if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.
#
import threading
import paramiko
import asyncio
import stat
import time
import os
import sys
import re
import random
import warnings
import __main__
from io import StringIO
from logging import DEBUG
try:
    from .sshscriptdollar import SSHScriptDollar
    from .sshscripterror import SSHScriptError, SSHScriptExit, SSHScriptBreak, getLogger
except ImportError:
    from sshscriptdollar import SSHScriptDollar
    from sshscripterror import SSHScriptError, SSHScriptExit, SSHScriptBreak, getLogger

## replace @{var} in $shell-command
pvar = re.compile('(\b?)\@\{(.+)\}')
## replace $.stdout, $.stderr to _c.stdout, _c.stderr, $.host in $LINE
pstd = re.compile('\$\.([a-z]+)')
## $.stdout in string, but not {{$.stdout}} 
pstdInCurlyBracket = re.compile(r"([^{]?){((?:\\.|[^}\\])*)}([^}])",re.M) 
## looking for @include( to self.open( in Py
pAtInclude = re.compile('^( *?)\$.include\(([^\)]+)\)',re.M)
## line startswith $, such as $${, ${, $shell-command but not $.
pDollarWithoutDot = re.compile('^\$[^\.][\{\w]?')
## line startswith $shell-command , $$shell-command , $@{py-var} , $$#! , $<space>abc
## but not ${, $${
pDollarCommand = re.compile('^\$(?!\$?\{)') # will match 
## replace @open( to self.open( in Py
#pAtFuncS = re.compile('^([\t ]*?)\@(\w+\()',re.M)
## find $.stdin =
pStdinEquals = re.compile('^[\t ]*?(\$\.stdin[\t ]*=)',re.M)
## find "with $shell-command"
pWithDollar = re.compile('^[\t ]*?with +\$[^\.]',re.M)
## replace "with @open", "with @subopen"
#pAtFuncSWith = re.compile('^([\t ]*?)with([\t ]+)\@(\w+\()',re.M)
pAtFuncSWith = re.compile('^([\t ]*?)with([\t ]+)\$\.(\w+\()',re.M)
## find with ... as ...
pAsString = re.compile(' +as +([^\:]+)\:')
## find with ... } as ... ; curly brackets
pCurlyBracketsAsString = re.compile('^[\t ]*?\}( +as +([^\:]+)\:.*)$',re.M)
## find  ... }
pCurlyBrackets = re.compile('^[ \t]*?\}')
## """ , ''', f""", f''' blocks
pqoute1 = re.compile('([fr]?)("{3})(.+?)"{3}',re.S)
pqoute2 = re.compile("([fr]?)('{3})(.+?)'{3}",re.S)
## ' .. ', "...", r'..', r"..""
pqoute3 = re.compile("([fr]?)'.*?'",re.M)
pqoute4 = re.compile('([fr]?)".*?"',re.M)
pqoute5 = re.compile('#____(.+?)____#',re.M)

## replace $.stdout, $.stderr to _c.stdout, _c.stderr
## replace $.open(), $.subopen() to SSHScript.inContext.
pQuoted = re.compile('\(.*\)')
## exported to $.<func>, such as $.open, $.close, $.exit, $.sftp,
SSHScriptExportedNames = set(['sftp','client','logger']) # default to exposed properties
SSHScriptExportedNamesByAlias = {}
#SSHScriptClsExportedFuncs = set() # "include" only, now.
def pstdSub(m):
    post = m.group(1)
    if post in SSHScriptExportedNames:
        return f'SSHScript.getContext(1).{post}'
    elif post in SSHScriptDollar.exportedProperties:
        return f'_c.{post}'
    elif post in SSHScriptExportedNamesByAlias:
        return f'SSHScript.getContext(1).{SSHScriptExportedNamesByAlias[post]}'
    #elif post in SSHScriptClsExportedFuncs:
    #    return f'SSHScript.{post}'
    else:
        # SSHScript.inContext's property
        return f'SSHScript.getContext(1).{post}'
## expose to __main__ for sshdollar.py
__main__.SSHScriptExportedNames = SSHScriptExportedNames
__main__.SSHScriptExportedNamesByAlias = SSHScriptExportedNamesByAlias

global newline, bNewline
newline = os.linesep # \n
bNewline = os.linesep.encode('utf8') # b'\n'
## resolve f'''{$.stdout}''' 
def pstdInCurlyBracketSub(m):
    f= f'{m.group(1)}{{{pstd.sub(pstdSub,m.group(2))}}}{m.group(3)}'
    return f

def export2Dollar(nameOrFunc):    
    if callable(nameOrFunc):
        SSHScriptExportedNames.add(nameOrFunc.__name__)
        return nameOrFunc
    else:
        name = nameOrFunc
        def export2DollarWithName(func):
            assert callable(func)
            SSHScriptExportedNamesByAlias[name] = func.__name__
            return func
        return export2DollarWithName

class LineGenerator:
    def __init__(self,lines):
        self.lines = lines
        self.cursor = -1
        self.savedCursor = None
    def next(self):
        self.cursor += 1
        if self.cursor >= len(self.lines):
            raise StopIteration()
        return self.lines[self.cursor]
    def save(self):
        self.savedCursor = self.cursor
    def restore(self):
        assert self.savedCursor is not None
        self.cursor = self.savedCursor
    def __next__(self):
        return self.next()
    def __iter__(self):
        return self

class SSHScript(object):
    ## SSHScript is the subject of $.method in py
    context = {}
    contextLocker = threading.Lock()
    ## a lookup table of instances of SSHScript by id
    items = {}
    @classmethod
    def getContext(cls,forceOne=False):
        ## 每個thread都有一個context instance
        t = threading.current_thread()
        try:
            return cls.context[t]
        except KeyError:
            if forceOne:
                ## usually was called by SSHScriptDollar() been created in a new thread
                try:
                    pt = t.parent
                except AttributeError:
                    ## 如果不是呼叫 $.thread產生的thread一律視為從main thread分出來的
                    pt = threading.main_thread()
                pobj = cls.context.get(pt)
                obj = SSHScript(pobj)
                obj.logger.log(DEBUG,f'create {obj} for <Thread {pt.ident}>/<Thread {t.ident}>')
                cls.setContext(obj)
                return obj
            else:
                #getLogger().log(DEBUG,f'no SSHScript() in <Thread {t.ident}>')
                return None

    @classmethod
    def setContext(cls,obj):
        ## context instance 是讓$使用的，可連線可不連線，它應該是有效的，一直都在的
        assert obj is None or isinstance(obj,SSHScript),f'{obj} is not an instance of SSHScript'
        t = threading.current_thread()
        cls.contextLocker.acquire()
        if obj is None:
            try:
                del cls.context[t]
            except KeyError:
                #getLogger().log(DEBUG,f'context of <Thread {t.ident}> is already None')
                pass
        else:
            cls.context[t] = obj
            obj.logger.log(DEBUG,f'set context to {obj} in <Thread {t.ident}>')
        cls.contextLocker.release()


    @classmethod
    def connectClient(cls,host,username,password,port,policy,**kw):
        client = paramiko.SSHClient()
        ## client.load_system_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

        if policy:
            client.set_missing_host_key_policy(policy)
        client.connect(host,username=username,password=password,port=port,**kw)
        return client
    
    @classmethod
    def include(cls,prefix,abspath,alreadyIncluded=None):
        global newline
        if alreadyIncluded is None:
            alreadyIncluded = {}
        
        if not os.path.exists(abspath):
            raise SSHScriptError(f'{abspath} not fournd, @include("{abspath}") failed',401)
        
        ## prevent infinite loop
        try:
            alreadyIncluded[abspath] += 1
            maxInclude = int(os.environ.get('MAX_INCLUDE',100))
            if alreadyIncluded[abspath] > maxInclude:
                raise SSHScriptError(f'{abspath} have been included over {maxInclude} times, guessing this is infinite loop',404)
        except KeyError:
            alreadyIncluded[abspath] = 1
        
        with open(abspath,'rb') as fd:
            content = fd.read().decode('utf8')

        ## find prefix
        prefixLen = 0
        for c in content:
            if c == ' ': prefixLen += 1
            elif c == '\t': prefixLen += 1
            else: break
        
        ## omit leading prefix
        rows = []
        for line in content.splitlines():
            ## skip "__export__ = [ "line
            if line.replace(' ','').startswith('__export__=['):
                continue
            rows.append(prefix + line[prefixLen:])
        script =  newline.join(rows)
        
        if pAtInclude.search(script):
            ## do include again (nested @include)
            scriptPath = abspath
            def pAtIncludeSub(m):
                prefix, path = m.groups()
                abspath = os.path.join(os.path.dirname(scriptPath),eval(path))
                content = SSHScript.include(prefix,abspath,alreadyIncluded)
                return content
            script = pAtInclude.sub(pAtIncludeSub,script)

        return script

    def __init__(self,parent=None):

        ## initial properties
        self._host = None
        self._port = None
        self._username = None

        self.logger = getLogger()

        ## homony i/o of this thread
        self._lastIOTime = 0
        self.lock = threading.Lock()
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        
        ## 1659910734.660772  = 2200/8/8 06:10
        self.id = f'{int(time.time()) - 1659910734}{int(1000*random.random())}'
        SSHScript.items[self.id] = self
        self._client = None
        self._shell = None
        self._sftp = None

        self.blocksOfScript = None

        ## nested sessions
        self._sock = None

        ## this is the instance in the chain of "thread"
        self.parentSession = None
        self.subSessions = set() #目前只用在exit時關閉
        ## this is the instance in the chain of "connection"
        self._previousSshscriptInContext = None

        ## parent is an SSHScript() in the parent-thread, or parent-connection
        if parent:
            assert isinstance(parent,SSHScript)
            self.parentSession = parent
            self._previousSshscriptInContext = parent
            parent.subSessions.add(self)
        else:
            pass
            ## 其次的SSHScript instance，只有在open之後才會成為SSHScript.inContext

        if threading.current_thread() == threading.main_thread():
            ## 讓第一個於main thread 創建的instance作為當下的context
            ## Caution: 如果是import使用的（不是呼叫sshscript)，第一個instance有可能不是在main thread創建的
            if SSHScript.getContext() is None:
                SSHScript.setContext(self)
       

        ## 這兩個可能有bug on threading
        # settings when exec command (see client.exec_command)
        self._careful = parent._careful if parent else False
        self._timeout = parent._timeout if parent else None #blocking
        
        ## 累積的行號(多檔案showScript時使用)
        ## v1.1.13起若有--debug時，顯示個別檔案的行號，這樣比較適合debug使用
        self.lineNumberCount = 0

        self.mute = os.environ.get('MUTE_WARNING')
    
    @property
    def host(self):
        ## 往上找一個有連線的 (in case of thread)
        return self._host or (self.parentSession and self.parentSession.host)
    
    @host.setter
    def host(self,v):
        self._host = v

    @property
    def username(self):
        ## 往上找一個有連線的 (in case of thread)
        return self._username  or (self.parentSession and self.parentSession.username)
    
    @username.setter
    def username(self,v):
        self._username = v

    @property
    def port(self):
        ## 往上找一個有連線的 (in case of thread)
        return self._port  or (self.parentSession and self.parentSession.port)
    
    @port.setter
    def port(self,v):
        self._port = v

    @property
    def connectedParent(self):
        ## for thread support
        if not self.parentSession: return None
        parentSession = self.parentSession
        while parentSession:
            if parentSession._client:
                return parentSession
            parentSession = parentSession.parentSession

    @property
    def client(self):
        return self._client or (self.parentSession and self.parentSession.client)

    @property
    def sftp(self):
        ## 先問自己
        if self._sftp is not None:
            ## 是否要確定連線還在？
            return self._sftp
        elif self._client:
            self._sftp = self._client.open_sftp()
            return self._sftp
        else:
            ## 再往上找 
            connectedParent = self.connectedParent
            if connectedParent:
                return connectedParent.sftp

    def __repr__(self):
        if self._host:
            return f'<SSHScript {self.id}:{self._host}>'
        else:
            return f'<SSHScript {self.id}>'
    
    @export2Dollar
    def log(self, level, msg, *args):
        self.logger.log(level, "[sshscript]" + msg, *args)

    def __del__(self):
        self.close(True)
        try:
            del SSHScript.items[self.id]
        except KeyError:
            ## when calls $.exit in runScript() would cause this error
            pass

    ## protocol of "with subopen as "
    def __enter__(self):
        return self

    ## protocol of "with subopen as "
    def __exit__(self,*args):
        self.close() ## close all subsession if any

    def touchIO(self):
        self.lock.acquire()
        self._lastIOTime = time.time()
        self.lock.release()

    async def waitio(self,waitingInterval,timeout=0):
        ## when timeout==0,如果io時間有更新，就一直等下去
        endtime = (time.time() + timeout) if timeout > 0 else 0
        while True:
            remain = waitingInterval - (time.time() - self._lastIOTime)
            if remain <= 0 or (endtime and time.time() >= endtime):break
            await asyncio.sleep(remain)

    async def afterio(self,waitingInterval):
        ## 不管io有沒有更新，反正就是只等一段時間
        remain = waitingInterval - (time.time() - self._lastIOTime)
        if remain > 0:
            await asyncio.sleep(remain)

    def getSocketWithProxyCommand(self,argsOfProxyCommand):
        return paramiko.ProxyCommand(argsOfProxyCommand)        

    @export2Dollar
    def thread(self,*args,**kw):
        # 主要是讓新的thread知道parent thread是誰
        self.lock.acquire()
        c = threading.current_thread()
        t = threading.Thread(*args,**kw)
        setattr(t,'parent',c)
        self.lock.release()
        return t

    @export2Dollar('break')
    def _break(self,code=0,message=''):
        raise SSHScriptBreak(message,code)

    @export2Dollar
    def exit(self,code=0,message=''):
        raise SSHScriptExit(message,code)

    @export2Dollar
    def connect(self,host,username=None,password=None,port=22,policy=None,**kw):
        ## host 可以是 username@hostname 的格式
        if '@' in host:
            username,host = host.split('@')
        
        ## 檢查是否是 subopen (讓open是subopen的alias,使用者可以都一直使用open，不使用subopen)
        if self._client is not None:
            ## 自己連接自己，可能是搞錯了
            if host == self.host:
                raise SSHScriptError(f'{host} self-connection makes no sense',502)
            else:
                return self.subconnect(host,username,password,port,**kw)
        
        ## self.host是.spy當中用來判斷有沒有ssh連線的依據（如果沒有則是subprocess)
        self._host = host
        self._port = port
        self._username = username
        
        ## user can set policy=0 to disable client.set_missing_host_key_policy
        if policy is None:
            # 允許連線不在known_hosts檔案中的主機
            policy = paramiko.AutoAddPolicy()

        ## 1. 找到目前連線的session（因為有thread時，有些thread是「中介性」的，沒有作連線，所以要
        ##    一直往回找(testing case: ex-threads-userlist2.spy)
        ## 2. 必須也檢查 self.parentSession.client，因為在同一個script中，可能上一個session已經關掉，
        ##    但是在parse時，將此段放在不同的 sshscript instance中，如unittest6()的情況
        ##    (這樣的結構在此情況下不是很漂亮，可能有未知的情況)
        connectedParentSession = self.connectedParent
        
        if connectedParentSession:
            if 'proxyCommand' in kw:
                raise NotImplementedError('proxyCommand not support in nested session')
            else:
                try:
                    self.lock.acquire()
                    self.log(DEBUG,f'nested connecting {username}@{host}:{port}')
                    ## REF: https://stackoverflow.com/questions/35304525/nested-ssh-using-python-paramiko
                    vmtransport = connectedParentSession._client.get_transport()
                    dest_addr = (host,port)
                    local_addr = (connectedParentSession._host,connectedParentSession._port)
                    self._sock = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
                    self._client = SSHScript.connectClient(host,username,password,port,policy,sock=self._sock,**kw)
                except paramiko.ChannelException as e:
                    self.log(DEBUG,f'nest connection failed ({username}@{host}:{port}), reason: {e}')    
                finally:
                    self.lock.release()
        else:
            try:
                self.lock.acquire()
                if 'proxyCommand' in kw:
                    self.log(DEBUG,f'connecting {username}@{host}:{port} by {kw["proxyCommand"]}')
                    self._sock = self.getSocketWithProxyCommand(kw['proxyCommand'])
                    del kw['proxyCommand']
                    self._client = SSHScript.connectClient(host,username,password,port,policy,sock=self._sock,**kw)
                else:
                    self.log(DEBUG,f'connecting {self.username}@{host}:{port}')
                    self._client = SSHScript.connectClient(host,username,password,port,policy,**kw)
            except paramiko.ChannelException as e:
                self.log(DEBUG,f'connection failed ({username}@{host}:{port}), reason: {e}')  
            finally:
                self.lock.release()  

        ## the parent instance of SSHScript in the same thread
        ## this could be None
        self._previousSshscriptInContext = SSHScript.getContext()
        SSHScript.setContext(self)
        self.log(DEBUG,f'{self._username}@{self._host}:{self._port} connected ')
        return self
    
    ## alias of connect, would be removed later
    @export2Dollar
    def open(self,host,username=None,password=None,port=22,**kw):
        return self.connect(host,username,password,port,**kw)
    
    @export2Dollar
    def subconnect(self,host,username=None,password=None,port=22,**kw):
        ## enter a new channel
        nestedSession = SSHScript(self)
        nestedSession.setContext(nestedSession)
        nestedSession.connect(host,username,password,port,**kw)
        return nestedSession
    
    @export2Dollar
    def paranoid(self,yes):
        warnings.warn(f'''paranoid() has renamed to careful()''',UserWarning,stacklevel=0)        
        self._careful = yes

    @export2Dollar
    def careful(self,yes=None):
        if yes is None: return self._careful
        else: self._careful = yes

    @export2Dollar
    def close(self):
        
        if len(self.subSessions):
            for s in list(self.subSessions):
                s.close()
            
        if self._sock:
            self._sock.close()
            self._sock = None
        
        if self._client:
            self.log(DEBUG,f'<SSHScript {self.id}> is closing {self.username}@{self.host}:{self.port}')
            self._client.close()
            self._client = None
        
        if self._shell:
            self._shell.close()
            self._shell = None

        if self._sftp:
            self._sftp.close()
            self._sftp = None

        self._host = None
        self._port = None
        self._username = None
        
        if self.parentSession:
            self.parentSession.lock.acquire()
            try:
                self.parentSession.subSessions.remove(self)
            except KeyError:
                pass
            self.parentSession.lock.release()

        ## restore to parent instance of SSHScript
        SSHScript.setContext(self._previousSshscriptInContext)      

    @export2Dollar
    def pkey(self,pathOfRsaPrivate):
        ## 往自己或往上找連線
        if self.client:
            try:
                self.lock.acquire()
                _,stdout,_ = self.client.exec_command(f'cat "{pathOfRsaPrivate}"')
                exitcode = stdout.channel.recv_exit_status()
                if exitcode > 0:
                    raise SSHScriptError(f'failed to get pkey from {pathOfRsaPrivate}, exitcode = {exitcode}')
                else:
                    keyfile = StringIO(stdout.read().decode('utf8'))
                    pkey = paramiko.RSAKey.from_private_key(keyfile)                
                return pkey
            finally:
                self.lock.release()
        else:
            # localhost
            with open(pathOfRsaPrivate) as fd:
                return paramiko.RSAKey.from_private_key(fd)


    @export2Dollar
    def upload(self,src,dst,makedirs=False,overwrite=True):
        """
        if dst is in an non-existing directory, FileNotFoundError will be raised.
        """        

        src = os.path.abspath(os.path.normpath(src))
        if not os.path.exists(src):
            raise FileNotFoundError(src)
        if not os.path.isfile(src):
            raise SSHScriptError(f'uploading src "{src}" must be a file',503)
        
        dst = os.path.normpath(dst)
        if sys.platform == 'win32':
            ## recorrect back, since ftp accecpt /
            dst = dst.replace('\\','/')        
        if not dst.startswith('/') and not self.mute:
            warnings.warn(f'''uploading dst "{dst}" is not absolute path''',UserWarning,stacklevel=0)
        
        self.log(DEBUG,f'upload {src} to {dst}')

        ## check exists of dst folders
        srcbasename = os.path.basename(src)
        dstbasename = os.path.basename(dst)
        if makedirs:
            ## v1.1.12
            ## 在此情形下，假設使用者給的是目錄，而非檔案名稱
            ## 如果需要產生目錄，需要全部給的目錄都產生
            ## ex. upload c0-test.txt
            ## 以下這三個沒問題
            ##  dst is  '/home/iap/sshscriptuploadtest/nonexist1/nonexist2/nonexist3/c0-test.txt'
            ##  dst is  '/home/iap/sshscriptuploadtest/nonexist1/nonexist2/nonexist3'
            ##  dst is  '/home/iap/sshscriptuploadtest/nonexist1/nonexist2/nonexist3/'
            ## 這個會有問題
            ##  dst is  '/home/iap/sshscriptuploadtest/nonexist1/nonexist2/nonexist3/test.txt'
            ## 結果會是
            ## '/home/iap/sshscriptuploadtest/nonexist1/nonexist2/nonexist3/test.txt/c0-test.txt'
            ## 所以在v1.1.13，如果最後的副檔名一樣，則最後一個為檔案，不是目錄。只是上傳之後要用不一樣的名字
            ## (see unittest/c0.spy)
            if not dstbasename == srcbasename:
                if not os.path.splitext(srcbasename)[1] == os.path.splitext(dstbasename)[1]:
                    dst = f'{dst}/{srcbasename}'

            def checking(dst,foldersToMake):
                dstDir = os.path.dirname(dst)
                try:
                    stat = self.sftp.stat(dstDir)
                except FileNotFoundError:
                    foldersToMake.append(dstDir)
                    return checking(dstDir,foldersToMake)
                return foldersToMake
            ## 由下層往上層檢查哪些目錄不存在（假設最後一層是檔案名稱）
            foldersToMake = checking(dst,[])
            if len(foldersToMake):
                foldersToMake.reverse()
                for folder in foldersToMake:
                    self.sftp.mkdir(folder)
                    self.log(DEBUG,f'mkdir {folder}')
        else:
            ## 1. basename 一樣：
            ## 2. basename 不一樣：
            ##    2.1 dst 為目錄： dst+= basename
            ##    2.2 dst 為檔案：
            if dstbasename == srcbasename:
                pass
            else:
                try:
                    dststat = self.sftp.stat(dst)
                except FileNotFoundError:
                    ## 不是，dst 視為檔案
                    pass
                else:
                    ## REF: https://stackoverflow.com/questions/18205731/how-to-check-a-remote-path-is-a-file-or-a-directory
                    if stat.S_ISDIR(dststat.st_mode):
                        # is folder，不要用os.path.join,若win32會變成倒斜線
                        dst = f'{dst}/{srcbasename}'
                        try:
                            dststat = self.sftp.stat(dst)
                        except FileNotFoundError:
                            pass
                        else:
                            if not overwrite:
                                raise FileExistsError(f'{dst} already exists')
                    else:
                        # is file
                        if not overwrite:
                            raise FileExistsError(f'{dst} already exists')
        
        self.sftp.put(src,dst)
        
        return (src,dst)

    @export2Dollar
    def download(self,src,dst=None):
        if dst is None:
            dst = os.getcwd()

        ## v1.1.13之後不必往下找self.subSession

        if not src.startswith('/') and not self.mute:
            warnings.warn(f'''downloading src "{src}" is not absolute path''',UserWarning,stacklevel=0)        
        
        dst = os.path.abspath(dst)

        ## if dst is a folder, append the filename of src to dst
        if os.path.isdir(dst):
            dst = os.path.join(dst,os.path.basename(src))

        self.log(DEBUG,f'downaloading from {src} to {dst}')            
        
        self.sftp.get(src,dst)
        
        self.log(DEBUG,f'downaloaded from {src} to {dst}')            
        return (src,dst)

    def parseScript(self,script,initLine=None,_locals=None,quotes=None):
        ## parse script at top-level session
        global newline
        scriptPath = _locals.get('__file__') if _locals else __file__
        def pAtIncludeSub(m):
            prefix, path = m.groups()
            abspath = os.path.join(os.path.abspath(os.path.dirname(scriptPath)),eval(path))
            content = SSHScript.include(prefix,abspath)
            return content
        
        def pqouteSub12(m):
            fr,quote,content = m.groups()
            key = f'#____{fr}_{hash(content)}{random.random()}____#'
            quotes[key] = m.group(0)
            return key
        def pqouteSub34(m):
            ## 只替換內容中有 $.stdout等特殊內容的字串
            fr = m.group(1)
            content = m.group(0)
            if not (pstd.search(content) or pqoute5.search(content)):
                return content
            key = f'#____{fr}_{hash(content)}{random.random()}____#'
            quotes[key] = content
            return key
        ## expend @include()
        script = pAtInclude.sub(pAtIncludeSub,script)
        
        ## store triple-quotes content 
        script = pqoute1.sub(pqouteSub12,script)
        script = pqoute2.sub(pqouteSub12,script)
        script = pqoute3.sub(pqouteSub34,script)
        script = pqoute4.sub(pqouteSub34,script)
        ## replace with @open( to "with open("
        script = pAtFuncSWith.sub('\\1with SSHScript.getContext(1).\\3',script)
        listOfLines = script.splitlines()
        ## listOfLines: [string]
        lines = LineGenerator(listOfLines)
        # lines is a generator
        self.blocksOfScript = []

        ## leadingIndent is the smallest leadingIndent of given script
        leadingIndent = -1
        rows = []

        def getShellCommandsInMultipleLines(lines):
            ## multiple lines ${
            ## ...... 此中間的格式不拘，indent也不拘，但leading space/tab 會被去掉
            ## } 必須單獨一行
            rowsInCurlyBrackets = []
            while True:
                try:
                    nextLine = next(lines)
                except StopIteration:
                    raise SSHScriptError('unclosed with ${',403)
                ## 尋找 } (必須在單獨一行的開頭；前面有space, tabOK)
                m = pCurlyBrackets.search(nextLine)
                if m:  break
                cmd = pstd.sub(pstdSub,nextLine.lstrip())
                rowsInCurlyBrackets.append(cmd)
            return self.parseScript(newline.join(rowsInCurlyBrackets),_locals=_locals,quotes=quotes)

        while True:
            try:
                if initLine:
                    line = initLine
                    initLine = None
                else:
                    line = next(lines)
            except StopIteration:
                break
            else:            
                ## i = index of the 1st no-space char of this line
                i = 0
                for idx,c in enumerate(line):
                    if c != ' ' and c != '\t':
                        i = idx
                        break

                ## initial assignment to leadingIndent
                ## at the 1st non-empty line, use its indent as top-level indent(leadingIndent)
                if leadingIndent == -1 and line.strip():
                    leadingIndent = i

                ## 這段script從去掉leadingIndent之後的那一個字元開始處理
                ## 所以若有某script全部都有indent（共同indent）,則該indent會被忽略
                ## i 在此之下是去除leadingIndent之後的index
                i -= leadingIndent 

                ## stripedLine 是去掉共同indent之後該行的內容
                stripedLine = line[leadingIndent:]
                ## indent是這一行去除共同indent之後的indent
                indent = stripedLine[:i]
                ## j 是不計with時，那一行第一個有用字元的位置
                j = i 
                
                if stripedLine.rstrip() == '':
                    rows.append(stripedLine)
                    continue
                
                
                ## 多行的${}, $${}內的內容（暫存用）
                shellCommandLines = []

                ## 檢查是否是 with 開頭的 block "with $shell-command"
                ## 不包括其他的，例如 "with @open(" 取代之後的 "with SSHScript.inContext ..."
                asPartOfWith = False
                
                ##
                ## 前處理
                ##

                ## "with $shell-command as fd", "with ${multiple lines} as fd", "with $${multiple lines} as fd"
                if pWithDollar.search(stripedLine):
                    ## find "as ..."
                    m = pAsString.search(stripedLine)
                    ## 調整 j 的位置
                    stripedLineWithoutWith = stripedLine[i+4:].lstrip()
                    j =  (len(stripedLine) - len(stripedLineWithoutWith))
                    if m:
                        asPartOfWith = m.group(0) # the " as ..." part
                        ## 把 as ... 從$指令中去掉（必須放在取得 j 值之後）
                        stripedLine = stripedLine[:m.start()].rstrip()
                    else:
                        ## multiple lines "with", for example: ${
                        ## ...... 此中間的格式不拘，indent也不拘，但leading space/tab 會被去掉
                        ## } 必須單獨一行
                        rowsInCurlyBrackets = []
                        while True:
                            ## 故意不catch StopIteration，當作找不到結束的"as ..."時候的exception
                            try:
                                nextLine = lines.next()
                            except StopIteration:
                                raise SSHScriptError('No "as" found for "with"',402)
                            ## 尋找 } as .... (必須在單獨一行的開頭；前面有space, tabOK)
                            m = pCurlyBracketsAsString.search(nextLine)
                            if not m:
                                # expand $.stdout, $.(var) etc
                                cmd = pstd.sub(pstdSub,nextLine.lstrip())
                                rowsInCurlyBrackets.append(cmd)
                                continue
                            asPartOfWith = m.group(1) # the " as ..." part
                            break
                        shellCommandLines.extend(self.parseScript(newline.join(rowsInCurlyBrackets),_locals=_locals,quotes=quotes))
                
                ##
                ## 逐行處理開始
                ##
                
                ## this is a comment line
                if stripedLine[j] == '#': 
                    rows.append(stripedLine) 

                ## support $shell-command or "with $shell-command"
                ## ＄,$$, ${, $${, $shell-command，但不是$.開頭
                elif pDollarWithoutDot.search(stripedLine[j:]) or (asPartOfWith and stripedLine[j] == '$'):
                    ## leading lines of ${} or $${} (multiple lines, and must multiple lines)
                    ## in single line is not supported ("with ${} as fd" is not supported)
                    if stripedLine[j+1:].startswith('{') or  stripedLine[j+1:].startswith('${'):
                                                
                        ## 改為只要有兩個 $$ 就是 invoke shell（不必是 $${), 但是不能是分開的 $  $
                        isTwodollars = 1 if stripedLine[j+1:].startswith('$') else 0

                        ## first line is the content after ${ or $${ , aka omitting ${ or $${ 
                        inlineScript = [stripedLine[j+3:]] if isTwodollars else [stripedLine[j+2:]]
                        
                        if len(shellCommandLines):
                            ## 已經在上面的with檢查中取得內容
                            inlineScript.extend(shellCommandLines) 
                        else:
                            try:
                                c = lines.cursor
                                shellCommandLines = getShellCommandsInMultipleLines(lines)
                            except SSHScriptError as e:
                                if e.code == 403:
                                    print('--- dump start ---')
                                    print(newline.join(lines.lines[c:lines.cursor + 1]))
                                    print('--- dump end ---')
                                    raise e
                            inlineScript.extend(shellCommandLines)
                        
                        cmd = newline.join(inlineScript)
                        ## 分成先建立SSHScriptDollar物件,再執行的2步驟。先取名為 __c 而不是 _c ，
                        ## 此__c執行之後，再指定成為 _c 
                        ## 因為命令中可能會呼叫 _c（例如 $.stdout)，係指前次執行後的_c,這樣才不會混淆。
                        ## 但是__c執行有錯的時候，_c 又必須為本次執行的__c，所以放到try:finally當中
                        ## 這樣可以在SSHScriptError丟出之前把_c設定為__c
                        indentOfTryBlock = '    '
                        rows.append(f'{indent}try:')
                        if cmd.startswith('#____'):
                            ## #____r, #____f,#____
                            fr = 1 if cmd[5] == 'f' else (2 if cmd[5] == 'r' else 0)
                            rows.append(f'{indent}{indentOfTryBlock}__b = {cmd}')
                        elif (cmd.startswith('f"') or cmd.startswith("f'")):
                            fr = 1
                            rows.append(f'{indent}{indentOfTryBlock}__b = f""" {cmd[2:-1]} """')
                        elif (cmd.startswith('r"') or cmd.startswith("r'")):
                            fr = 2
                            rows.append(f'{indent}{indentOfTryBlock}__b = r""" {cmd[2:-1]} """')
                        else:
                            fr = 0
                            rows.append(f'{indent}{indentOfTryBlock}__b = """ {cmd} """')
                        # 前後要留空白，避免 "與"""混在一起
                        rows.append(f'{indent}{indentOfTryBlock}__c = SSHScriptDollar(None,__b,locals(),globals(),inWith={bool(asPartOfWith)},fr={fr})')
                        rows.append(f'{indent}{indentOfTryBlock}__ret = __c({isTwodollars})')
                        rows.append(f'{indent}finally:')
                        rows.append(f'{indent}{indentOfTryBlock}_c = __c')
                        if asPartOfWith:
                            rows.append(f'{indent}with __ret {asPartOfWith}')

                    ## single line $shell-comand or $$shell-command
                    ## this is always run by SSHScript.inContext (an instance of SSHScript)
                    elif pDollarCommand.search(stripedLine[j:]):
                        try:
                            isTwodollars = stripedLine[j+1] == '$'
                        except IndexError:
                            ## stripedLine[j+1] does not exist
                            isTwodollars = False
                            cmd = ''
                        else:
                            ## 要有lstrip()，讓 $<space>''' 可用
                            cmd = (stripedLine[j+2:] if isTwodollars else stripedLine[j+1:]).lstrip()
                        
                        ## expand $.stdout, $.(var) etc in cmd
                        if pvar.search(stripedLine):
                            cmd = pstd.sub(pstdSub,cmd.lstrip())
                        
                        indentOfTryBlock = '    '
                        rows.append(f'{indent}try:')
                        if cmd.startswith('#____'):
                            fr = 1 if cmd[5] == 'f' else (2 if cmd[5] == 'r' else 0)
                            rows.append(f'{indent}{indentOfTryBlock}__b = {cmd}')
                        elif (cmd.startswith('f"') or cmd.startswith("f'")):
                            fr = 1
                            rows.append(f'{indent}{indentOfTryBlock}__b = f""" {cmd[2:-1]} """')
                        elif (cmd.startswith('r"') or cmd.startswith("r'")):
                            fr = 2
                            rows.append(f'{indent}{indentOfTryBlock}__b = r""" {cmd[2:-1]} """')
                        else:
                            fr = 0
                            rows.append(f'{indent}{indentOfTryBlock}__b = """ {cmd} """')
                        ## 前後要留空白，避免 "與"""混在一起
                        rows.append(f'{indent}{indentOfTryBlock}__c = SSHScriptDollar(None,__b,locals(),globals(),inWith={bool(asPartOfWith)},fr={fr})')
                        rows.append(f'{indent}{indentOfTryBlock}__ret = __c({isTwodollars})')
                        rows.append(f'{indent}finally:')
                        rows.append(f'{indent}{indentOfTryBlock}_c = __c')

                        if asPartOfWith:
                            ## 注意：此處還沒寫完，因為moreIndent必須是下一行的indent才行??
                            rows.append(f'{indent}with __ret {asPartOfWith}')
                    else:
                        raise SyntaxError(f'failed to parse "{stripedLine}" from "{[stripedLine[j:]]}"')
                else:
                    ## expand $.stdout, $.(var) etc
                    rows.append(pstd.sub(pstdSub,stripedLine))

        return rows

    
    def run(self,script,varLocals=None,varGlobals=None,showScript=False):
        global newline
        _locals = locals()
        if varLocals is not None:
            _locals.update(varLocals)

        _globals = globals()
        if varGlobals is not None:
            _globals.update(varGlobals)

        quotes = {}
        if isinstance(script, str):
            ## self.parseScript will reset self.blocksOfScript
            rows = self.parseScript(script,_locals=_locals,quotes=quotes)
            if len(rows):
                ## close this block
                self.blocksOfScript.append(newline.join(rows))        
        
        assert  self.blocksOfScript is not None
        
        ## efficiently restore key to content in quotes
        global skipedKey,replacedKey
        replacedKey = set()
        skipedKey = []
        def iterKey():
            global skipedKey,replacedKey
            ## reverse key list is faster than using set()
            try:
                allKeys = reversed(quotes.keys())
            except TypeError:
                ## python 3.6
                allKeys = reversed(list(quotes.keys()))
            while True:
                for key in allKeys:
                    if key in replacedKey: continue
                    yield key
                if len(skipedKey) == 0: break
                allKeys = skipedKey
                skipedKey = []
        def pqoute5Sub(m):
            key = m.group(0)
            replacedKey.add(key)
            return quotes[key]
        for scriptChunk in self.blocksOfScript:
            if isinstance(scriptChunk, str):
                ## restore triple-quotes content
                keygen = iterKey()
                while True:
                    try:
                        key = next(keygen)
                    except StopIteration:
                        break
                    else:
                        ## 被保留下來的字串中，如果有f-string則eval當中的{$.stdout}
                        if scriptChunk.find(key) == -1:
                            skipedKey.append(key)
                        else:
                            replacedKey.add(key)
                            c = quotes[key]
                            if c.startswith('f"') or c.startswith("f'"):
                                c = pstdInCurlyBracket.sub(pstdInCurlyBracketSub,c)
                                ## 把#4.4#換為雙引號字串
                                c = pqoute5.sub(pqoute5Sub,c)
                                ## 再掃一次，把{$.stdout}換成_c.stdout
                                c = pstdInCurlyBracket.sub(pstdInCurlyBracketSub,c)
                            scriptChunk = scriptChunk.replace(key,c)
                if showScript:
                    if os.environ.get('DEBUG'):
                        self.lineNumberCount = 0
                    lines = scriptChunk.splitlines()
                    digits = len(str(len(lines)+1))
                    for line in lines:
                        self.lineNumberCount += 1
                        print(f'{str(self.lineNumberCount).zfill(digits)}:{line}')
                    print()
                    continue
                try:
                    exec(scriptChunk,_globals,_locals)
                except SyntaxError:
                    raise
                except (SSHScriptExit, SystemExit):
                    ## 找到最上層的session，全部關掉
                    topSession = SSHScript.getContext()
                    if topSession is not None:
                        while topSession.parentSession:
                            topSession = topSession.parentSession
                        topSession.close()
                    raise
                ## other execptions did not trigger auto-close
            elif isinstance(scriptChunk, self.__class__):
                try:
                    scriptChunk.run(None,_locals,_globals,showScript=showScript)
                except (SSHScriptExit, SystemExit):
                    ## 找到最上層的session，全部關掉
                    topSession = SSHScript.getContext()
                    if topSession is not None:
                        while topSession.parentSession:
                            topSession = topSession.parentSession
                        topSession.close()
                    raise
                ## other execptions did not trigger auto-close
        return _locals