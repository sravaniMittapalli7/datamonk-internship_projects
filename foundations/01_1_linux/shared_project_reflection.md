# Reflection: Secure Shared Project Directory

## File vs. Directory Permissions
The execute (`x`) permission on a directory allows a user to **enter (cd into)** it and access its contents. Even if a file inside is readable, without `x` on the directory, the user cannot list or access its name. It's essential for navigation.

## The 777 Risk
A file with `777` on a web server can be **written and executed by anyone**. If an attacker uploads malicious PHP code to a `777` directory, they can run it remotely and **gain control** over the server, alter files, or steal data.

## Symbolic vs. Octal chmod
Using `chmod g+x a_file.txt` is **safer** because it only changes **group execute** permission without touching others. Calculating octal manually (like turning `-rwx-w-r--` into `771`) risks **overwriting existing permissions** by mistake.

## sudo’s Power
Typing `sudo rm -rf / temp_files/` would cause Linux to interpret `/` as root and **delete your entire system** recursively. `sudo` gives full root access, so it **removes system-critical files**, making the system unrecoverable.

## Ownership for Collaboration
Changing the group to `developers` allows **controlled access** for team members without exposing the project to the entire system (as `others`). It’s **secure and scalable**, ensuring only trusted users can modify files.
