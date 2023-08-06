import setuptools

setuptools.setup(
    name="streamlit-firebase-remote-config-component",
    version="0.0.1",
    author="Granit Luzhnica",
    author_email="granit.luzhnica@gmail.com",
    description="Firebase Remote Config and Google Analytics for Streamlit",
    long_description="""
        A streamlit component which enables fatching remote config variables from firebase and also enables google analytics.
        Usage:
        
        from fbrc import fbrc
        configParams:dict = fbrc(FirebaseConfig)
        """,
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.1",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
