import subprocess


def copy(string, target=None):
    extra_args = []

    if target:
        extra_args.append('-target')
        extra_args.append(target)

    return subprocess.run(
        ['xclip', '-selection', 'c'] + extra_args,
        universal_newlines=True,
        input=string
    )


def get(target=None):
    extra_args = []

    if target:
        extra_args.append('-target')
        extra_args.append(target)

    result = subprocess.run(
        ['xclip', '-selection', 'c', '-o'] + extra_args,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    return result.stdout.strip()
