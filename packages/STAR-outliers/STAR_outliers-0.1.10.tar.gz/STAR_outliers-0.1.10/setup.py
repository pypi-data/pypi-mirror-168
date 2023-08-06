from setuptools import setup
from setuptools import find_packages

summary = "STAR_outliers (Skew and Tail-heaviness "
summary += "Adjusted Removal of outliers) is an open "
summary += "source python package that determines "
summary += "which points are outliers relative to their "
summary += "distributions shapes. Please visit the "
summary += "[github page](https://github.com/Epistasis"
summary += "Lab/STAR_outliers) for more information."

ep_val = {"console_scripts": ["STAR_outliers = STAR_outliers:main"]}
setup(
    long_description = summary,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    version = "0.1.10",
    python_requires = ">=3.6,<=3.9",
    name = "STAR_outliers",
    entry_points = ep_val,
    py_modules=["STAR_outliers", "STAR_outliers_library",
                "STAR_outliers_plotting_library",
                "STAR_outliers_polishing_library",
                "STAR_outliers_testing_library"],
    setup_requires=["matplotlib"],
    install_requires=["numpy",
                      "pandas",
                      "tqdm",
                      "scipy",
                      "mock"]
)
