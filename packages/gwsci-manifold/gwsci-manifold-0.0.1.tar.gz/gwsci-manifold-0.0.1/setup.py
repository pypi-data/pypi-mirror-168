import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="gwsci-manifold",
	version="0.0.1",
	author="Chad Hanna",
	author_email="crh184@psu.edu",
	description="Geometric tools for gravitational wave data analysis",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://git.ligo.org/chad-hanna/manifold",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		# "License :: OSI Approved :: GPLv2",
		"Operating System :: OS Independent",
	],
	scripts=["bin/manifold_cbc_bank.py",
			 "bin/manifold_plot_test_cbc_bank.py",
			 "bin/manifold_cbc_bank_trim.py",
			 "bin/manifold_cbc_bank_to_xml.py",
			 "bin/manifold_cbc_bank_salpeter_mass_model.py",
			 "bin/manifold_plot_mass_model.py",
			 "bin/manifold_test_cbc_bank.py",
			 "bin/manifold_add_test_cbc_bank.py",
			 "bin/manifold_cbc_bank_refine.py"],
	python_requires='>=3.6',
)
