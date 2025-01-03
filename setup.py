from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os

class SilentInstallCommand(install):
    """
    Custom install command to silently install all dependencies from the bundled dependencies folder.
    """
    def run(self):
        # Path to the bundled dependencies folder
        dependencies_path = os.path.join(os.path.dirname(__file__), "auroraai", "dependencies")

        # Install all dependencies silently from the bundled .whl files
        if os.path.exists(dependencies_path):
            print("Starting silent installation of bundled dependencies...")
            for wheel in os.listdir(dependencies_path):
                if wheel.endswith(".whl"):
                    wheel_path = os.path.join(dependencies_path, wheel)
                    try:
                        print(f"Installing: {wheel}")
                        subprocess.check_call(
                            ["pip", "install", "--quiet", "--no-deps", wheel_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        print(f"Successfully installed: {wheel}")
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to install {wheel}: {e}")
                        raise RuntimeError("Silent installation failed. Contact support.")

        else:
            print("Dependencies folder not found. Skipping silent installation.")
        
        # Proceed with the normal installation process
        super().run()

setup(
    name="auroraai",
    version="1.0.0",
    description="Advanced transcription model for audio and video files.",
    author="aurorasolutions.ai",
    author_email="aurorasolutions.ai@gmail.com",
    url="https://github.com/aurorasolutions-ai/auroraai",
    packages=find_packages(),
    package_data={
        "auroraai": ["dependencies/*.whl"]  # Include all .whl files in the dependencies folder
    },
    cmdclass={"install": SilentInstallCommand},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
