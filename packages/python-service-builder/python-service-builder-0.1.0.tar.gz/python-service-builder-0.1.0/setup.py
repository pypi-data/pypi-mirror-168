# Copyright 2022 David Harcombe. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
    name='python-service-builder',
    version='0.1.0',
    description='Helper library for easier creation of Google services.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='David Harcombe',
    author_email='david.harcombe@gmail.com',
    license='Apache 2.0',
    zip_safe=False,
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=">=3.9",
    install_requires=[
        'absl-py>=0.12.0',
        'dataclasses-json>=0.5.2',
        'gcs-oauth2-boto-plugin>=2.7',
        'google-api-core>=1.26.1',
        'google-api-python-client>=2.0.2',
        'google-auth-httplib2>=0.1.0',
        'google-auth-oauthlib>=0.4.3',
        'google-auth>=1.28.0',
        'google-reauth>=0.1.1',
        'googleapis-common-protos>=1.53.0',
        'httplib2>=0.19.0',
        'immutabledict>=2.2.1',
        'oauth2client>=4.1.3',
        'oauthlib>=3.1.0',
    ],
)
