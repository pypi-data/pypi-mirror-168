from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="moodbot",
    version="1.0.3",
    author="walker",
    description="Mood adaptive chatbot",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['moodbot'],
    url="https://github.com/wa1ker38552/moodbot",
    install_requires=["requests", "nltk~=3.7", "datetime"],
    python_requires=">=3.7",
    mode='random',
)