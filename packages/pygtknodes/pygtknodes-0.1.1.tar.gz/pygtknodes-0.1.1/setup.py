import setuptools
import subprocess
import os

if not os.path.isdir("./pygtknodes/lib"):
    print("Building gtknodes using podman ...")
    # podman build
    subprocess.run(["podman", "build", "-f", "./Dockerfile", "-t", "gtknodes"])

    # podman run -it -d --name gtknodes-container gtknodes
    subprocess.run(["podman", "run", "-it", "-d", "--name", "gtknodes-container", "gtknodes"])

    # podman cp 
    out = subprocess.run(["podman", "cp", "gtknodes-container:/gtknodes/build/.", "./pygtknodes/"])

    if out.returncode != 0:
        print("error on subprocess run podman cp.")
        exit(1)


# pip install twine
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/* --verbose

setuptools.setup(
    name='pygtknodes',
    version="0.1.1",
    author="aluntzer",
    description="",
    packages=['pygtknodes'],
    package_data={'pygtknodes':['lib/**', 'include/**', 'share/**'] }
)
