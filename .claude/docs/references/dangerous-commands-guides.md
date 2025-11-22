# Dangerous Commands

## Project Overview

- here is a list of dangerous bash commands, categorized by the type of threat they can pose if implemented accidentally.

## Overview

### System Modification and Data Destruction

- These commands can alter or permanently delete files, directories, and user accounts. Accidental use can lead to irreversible data loss or system instability.
- rm : Deletes files or directories. The
-rf / flag is particularly destructive as it can erase the entire filesystem.
- mv : Moves or renames files. A misplaced command, such as moving a directory to
- /dev/null, can effectively destroy data.
- useradd / userdel : Adds or deletes user accounts, which can alter system access or remove user data.
- kill / pkill / killall : Terminates running processes, which can cause system instability or data corruption if critical services are stopped.
- shutdown / reboot : Powers down or restarts the system, leading to immediate service interruption.

### Privilege and Permission Management

- These commands manage user privileges and file permissions. Incorrect use can create major security holes by granting overly broad access.
- sudo : Executes commands with superuser (root) privileges, bypassing standard user restrictions.
- chmod : Changes file permissions. An overly permissive setting like
- 777 can make sensitive files readable, writable, and executable by any user.
- setfacl : Sets fine-grained access control lists for files, which can be misconfigured to grant unintended permissions.
- chattr : Changes file attributes on a Linux file system, which can be used to make files immutable or otherwise evade standard permissions.

### Networking and Data Exfiltration

- These commands can transfer data over a network. They can be accidentally used to send sensitive information to an external, unauthorized server.
- curl : Transfers data from or to a server. Can be used to upload sensitive files to an attacker's endpoint.
- wget : Downloads files from the network. Can be used to fetch malicious scripts or tools.
- nc / netcat : A versatile networking utility that can be used to create connections, transfer files, or open backdoors.
- nmap : A network scanning tool that can be used to discover open ports and services on a network, often as a precursor to an attack.
- tftp : A simple file transfer protocol that can be used for data exfiltration.
- tcpdump : Captures and analyzes network traffic, potentially exposing sensitive data sent over the network.

### Information Gathering and Reconnaissance

- These commands are used to collect information about the system, its users, and its configuration, which can be leveraged for further attacks.
- cat : Displays the content of files. Can be used to read sensitive files like
- /etc/passwd or /etc/shadow.
- uname : Prints system information, revealing the OS version which can help identify potential vulnerabilities.
- ifconfig : Displays network interface configuration.
- netstat : Shows active network connections and listening ports.
- whoami / users / groups / last : Reveals information about current and past logged-in users.

### Persistence and Defense Evasion

- These commands can be used to maintain access to a compromised system or to hide malicious activities by disabling security tools.
- crontab : Schedules automated jobs, which can be used to run malicious scripts at regular intervals.
- history -c or modifying HISTFILESIZE : Clears the command history, erasing evidence of executed commands.
- systemctl stop <service> : Stops system services, which could include security monitoring tools like
- auditd.
- LD_PRELOAD : A mechanism that can be abused to load malicious shared libraries into a process, hijacking its execution flow

