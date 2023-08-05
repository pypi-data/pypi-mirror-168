############################################################################################
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
############################################################################################
from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        README = f.read()
    return README


#with open("requirements.txt") as f:
#    required = f.read().splitlines()

#with open("requirements-optional.txt") as f:
#    optional_required = f.read().splitlines()

base_packages = ['pandas', 'preprocessor', 'numpy', 'sentence_transformers']

setup(
    name="embed_clustering",
    version="0.0.2",
    description="Clustering using different non-parameteric models with the combination of word Embedding",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/masumeazee/Embedding_Crp_Clustering_Pro",
    author="Masume Azizyan, Deepak John Reji",
    author_email="masume.azee@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    license_files=("LICENSE",),
    install_requires=base_packages,
    #extras_require={"full": optional_required,},
)