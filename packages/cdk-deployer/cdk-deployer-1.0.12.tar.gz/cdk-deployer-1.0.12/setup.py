import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-deployer",
    "version": "1.0.12",
    "description": "A construct library for deploying artifacts via CodeDeploy inside of a AWS CDK application.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-deployer",
    "long_description_content_type": "text/markdown",
    "author": "Jeff Gardner",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-deployer"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_deployer",
        "cdk_deployer._jsii"
    ],
    "package_data": {
        "cdk_deployer._jsii": [
            "cdk-deployer@1.0.12.jsii.tgz"
        ],
        "cdk_deployer": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk.aws-autoscaling>=1.173.0, <2.0.0",
        "aws-cdk.aws-codedeploy>=1.173.0, <2.0.0",
        "aws-cdk.aws-ec2>=1.173.0, <2.0.0",
        "aws-cdk.aws-iam>=1.173.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.173.0, <2.0.0",
        "aws-cdk.aws-s3-assets>=1.173.0, <2.0.0",
        "aws-cdk.aws-s3>=1.173.0, <2.0.0",
        "aws-cdk.core>=1.173.0, <2.0.0",
        "aws-cdk.custom-resources>=1.173.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
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
