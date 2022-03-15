# PasswordManager
A simple Python Password Manager CLI application using Typer and MongoDB


# Password Manager
**Install dependencies**
```console
sudo apt install xclip xsel wl-clipboard
```
**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`
* `delete`
* `get`
* `list`
* `update`

## `add`

**Usage**:

```console
$ add [OPTIONS] KEY
```

**Arguments**:

* `KEY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `delete`

**Usage**:

```console
$ delete [OPTIONS] KEY
```

**Arguments**:

* `KEY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `get`

**Usage**:

```console
$ get [OPTIONS] KEY
```

**Arguments**:

* `KEY`: [required]

**Options**:

* `--copy / --no-copy`: [default: False]
* `--help`: Show this message and exit.

## `list`

**Usage**:

```console
$ list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `update`

**Usage**:

```console
$ update [OPTIONS] KEY
```

**Arguments**:

* `KEY`: [required]

**Options**:

* `--help`: Show this message and exit.
