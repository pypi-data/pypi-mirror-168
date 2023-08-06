import setuptools

PACKAGE_NAME = "onelogin_aws_login"

setuptools.setup(
    name=PACKAGE_NAME,
    version="1.3",
    author="",
    author_email="",
    description="",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    py_modules=[PACKAGE_NAME],
    install_requires=[
        "boto3",
        "onelogin",
        "keyring",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            f"onelogin-aws-login = {PACKAGE_NAME}.cli:login"
        ]
    },
    zip_safe=False,
)
