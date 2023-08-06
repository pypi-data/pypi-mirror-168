# igm

[![PyPI](https://img.shields.io/pypi/v/igm)](https://pypi.org/project/igm/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/igm)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/99cb08da2773e37cc1338ae8be12d798/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/99cb08da2773e37cc1338ae8be12d798/raw/comments.json)

[![Docs Deploy](https://github.com/igm4ai/igm/workflows/Docs%20Deploy/badge.svg)](https://github.com/igm4ai/igm/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/igm4ai/igm/workflows/Code%20Test/badge.svg)](https://github.com/igm4ai/igm/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/igm4ai/igm/workflows/Badge%20Creation/badge.svg)](https://github.com/igm4ai/igm/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/igm4ai/igm/workflows/Package%20Release/badge.svg)](https://github.com/igm4ai/igm/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/igm4ai/igm/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/igm4ai/igm)

[![GitHub stars](https://img.shields.io/github/stars/igm4ai/igm)](https://github.com/igm4ai/igm/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/igm4ai/igm)](https://github.com/igm4ai/igm/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/igm4ai/igm)
[![GitHub issues](https://img.shields.io/github/issues/igm4ai/igm)](https://github.com/igm4ai/igm/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/igm4ai/igm)](https://github.com/igm4ai/igm/pulls)
[![Contributors](https://img.shields.io/github/contributors/igm4ai/igm)](https://github.com/igm4ai/igm/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/igm4ai/igm)](https://github.com/igm4ai/igm/blob/master/LICENSE)

IGM (Intelligence Guidance Manager for AI).

The ultimate purpose of AI is to serve science (as ai4science does), so let's call it ``sci-igm``.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install sci-igm
```

Or install from latest source code as follows:

```shell
git clone https://github.com/igm4ai/igm.git
cd igm
pip install . --user
```

## Quick Start for IGM

Here is a simple example to create a hello world project:

```shell
igm new git+https://github.com/igm4ai/template-simple helloword  # create helloworld project
cd helloword
igm run  # run the helloworld project
```

## What Happened?

After you enter the `igm new <template> <proj_dir>` command to your terminal, igm operate as the following stages:

1. **Initialization Stage** - Check the template, if remote url or repository detected, download it to local storage.
2. **Project Creation Stage**
    1. **Load Step** - Load the template's meta information.
    2. **Inquire Step** - Ask the user to provide some necessary.
    3. **Build Step** - Build the project based on the template, the project will be placed at `<proj_dir>`.
3. **Project Use Stage**
    * (Optional) **Prerequisite Installation** - run `igm run install` command to install the dependencies.
    * **Code Run** - run `igm run` command to run the main project code.
    * **What Scripts Are Provided?** - run `igm run -h` to see the list of provided scripts.
    * (Optional) Other custom scripts - you can use the other scripts provided by template, or custom the extra scripts
      in `igmeta.py`.

## How to Create A New Project Template

The detailed documentation is still preparing, but you can take a look at the following examples:

* [template-simple](https://github.com/igm4ai/template-simple), a helloworld template example
* [template-linear-regression](https://github.com/igm4ai/template-linear-regression), a more advanced example of linear
  regression problem, **with visualization example**
* [template-resnet18](https://github.com/igm4ai/template-resnet18), template for resnet18, including resource download
  and usage of tensorboard
* [IGM-di](https://github.com/PaParaZz1/IGM-di), example of usage of DI-engine, including custom complex generating of
  training code
* [Test Template](https://github.com/igm4ai/igm/tree/main/templates/test), a test template for unittest of igm tools,
  more advanced usage can be found here.

For information on template syntax, see the following:

* [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/), the template render framework we used in IGM.
* [potc](https://github.com/potc-dev/potc), transform any object to readable python object, will be useful when render
  python source code. It is integrated into IGM with a filter named `potc`.

## Contributing

We appreciate all contributions to improve `igm`, both logic and system designs. Please refer to CONTRIBUTING.md
for more guides.

## License

`igm` released under the Apache 2.0 license.
