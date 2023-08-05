# 🔒 locksey 🔒

Personal CLI utility tool to easily encrypt and decrypt files in a directory. Can be used to 
encrypt secrets in a repo, MFA recovery codes, password text files, your journal/diary entries or any text file with personal or confidential information.

## How does it work?

- If you want a file in a directory to work with locksey, you name the file with ending with `.unlocked.*` extension.
When you run `locksey lock <password>`, it will recursively find all `.unlocked.*` files, encrypt them and rename them to `.locked.*`.

- Similarly when you run `locksey unlock <password>`, it will recursively find all `.locked.*` files, decrypt them and rename them to `.unlocked.*`.

- You can also tell locksey to store the password in you home folder so you don't have to type it again.

- Files are encrypted as described in [this](https://stackoverflow.com/a/55147077/5516481) stackoverflow post.

## Install

```
python3 -m pip install locksey
```

## Usage

```
python3 -m locksey [-h] action [password]
```

*Actions*

| Name      | Description                                                                                               |
|-----------|-----------------------------------------------------------------------------------------------------------|
| lock      | Recursively go through the directory encrypt and rename files matching glob `./**/*.unlocked.*`                      |
| unlock    | Recursively go through the directory and decrypt and rename files matching glob `./**/*.locked.*`                    |
| setpasswd | Store password for current directory in home folder (`~/.locksey`), base64 encoded so you don't have to provide it again |
| rmpasswd  | Remove stored password for current directory                                                              |

### Changing password 

For changing the password in you current directory, run

1. `unlock`
2. `rmpasswd` if needed 
3. `lock` with new password
4. `setpasswd` with new password if needed