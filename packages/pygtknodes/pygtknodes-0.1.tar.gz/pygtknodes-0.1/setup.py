import setuptools
import subprocess

# podman build
subprocess.run(["podman", "build", "-f", "./Dockerfile", "-t", "gtknodes"])

# podman run -it -d --name gtknodes-container gtknodes
subprocess.run(["podman", "run", "-it", "-d", "--name", "gtknodes-container", "gtknodes"])

# podman cp 
out = subprocess.run(["podman", "cp", "gtknodes-container:/gtknodes/build/.", "./pygtknodes/"])

if out.returncode != 0:
    print("error on subprocess run podman cp.")
    exit(1)

setuptools.setup(
    name='pygtknodes',
    version="0.1",
    author="aluntzer",
    description="",
    packages=['pygtknodes'],
    package_data={'pygtknodes':['lib/**', 'include/**', 'share/**'] }
)
