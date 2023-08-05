import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-jenkins",
    "version": "0.0.57",
    "description": "Jenkins construct for CDK8s",
    "license": "Apache-2.0",
    "url": "https://github.com/cdk8s-team/cdk8s-jenkins",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdk8s-team/cdk8s-jenkins"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_jenkins",
        "cdk8s_jenkins._jsii"
    ],
    "package_data": {
        "cdk8s_jenkins._jsii": [
            "cdk8s-jenkins@0.0.57.jsii.tgz"
        ],
        "cdk8s_jenkins": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdk8s>=2.3.16, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.67.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
