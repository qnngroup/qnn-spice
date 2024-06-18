# qnn-spice
QNN's SPICE models library

This repository sync's all of the SPICE models we use with their respective remotes
and updates the LTSpice internal directory to add a new `[qnn-spice]` folder into
LTSpice's component library that sorts the components.

- [Installation](#Installation)
- [Usage](#Usage)
- [Troubleshooting](#Troubleshooting)

## Example

<center><img src="example.png" width="350px"/></center>

The component library for the following `models.md` config:

```
- htron_behavioral: htrons
  - htron_behav_model.asc: htron_b.asc
  - htron_behav_model.asy: htron_b.asy
- JJ: JJs
  - JJ.asy: JJ_v1.asy
  - JJ.lib: JJ_v1.lib
- JJ_v2: JJs
  - JJ.asy: JJ_v2.asy
  - JJ.lib: JJ_v2.lib
- ntron: ntron
  - ntron.lib
  - ntron.asy
```


## Usage

If you are using this repo for the first time, [go to Installation](#Installation). 

#### How to sync repos and download the latest models?

Run `./update` in the root of the qnn-spice repo. This will pull
all the latest changes from all available repos and sync the
files in `models.md` to your local LTSpice directory, so you can
access all the models as in the Example.

Note, `./update` creates symlinks in Windows only if the path to the
LTSpice directory is supplied as a commandline argument. Note that if
you are using WSL instead of cygwin/minGW, then `update_helper.py`
*will not* create symlinks so whenever you modify any model files
(locally or by pulling in upstream changes), you'll need to rerun `./update`

#### How to push changes to a model?

Just like how you would push to a regular github repo, go into the repo with your 
edited file as you would normally do and commit and push your changes, then go up 
one directory to the `qnn-spice` repo and commit and push these changes too.
For example, `snspd-spice` is a repo that houses a file edited, so we can run
the following:
``` bash
$ pwd # should return .../snspd-spice
$ git add .
$ git commit -m "Updating model"
$ git push
$ cd ..
$ pwd # should return .../qnn-spice
$ git add .
$ git commit -m "Updating snspd-spice head"
$ git push
```

#### How to add a new repo?

In the repo you want to add, create a new file titled `models.md` in the base of the 
repository. This file helps locate models in your repository and present them in a 
helpful way to LTSpice. See [How to write a model file](#How_to_write_a_model_file).
Push these changes to the repository.

Now in qnn-spice, you can simply run `git submodule add [repo-you-want-to-add]`, then
running `./update` will get the latest changes for this repo and sync them with your 
local LTSpice model libraries. Then commit and push the changes to `qnn-spice` so that
everyone has these changes!

## How to write a model file

## Installation

You should be able to install this repository by cloning it 
(`git clone git@github.com:qnngroup/qnn-spice.git`) and then running the
`update` script using `./update` (or `./update [PATH-TO-LTSPICE-LIB-FILE]`) when
in the qnn-spice directory.

## Troubleshooting

- On windows, creation of symlinks by users is disabled by default, so the update
script will likely give you an `OSError` regarding permissions (e.g. OSError 1314).
In this case, either enable developer mode, or just relaunch git bash as an administrator
(Run Program as Administrator).
- If you get a permission error saying you can't run `./update`, you might need to run
`chmod +x update` in the `qnn-spice` directory to give the update script execution
permissions.
- If you experience errors setting up the submodules, try running `git submodule init`
`git submodule update` and if this doesn't work, proceed to clone the repositories in
a separate directory to make sure your git setup has the correct credentials.
- 
