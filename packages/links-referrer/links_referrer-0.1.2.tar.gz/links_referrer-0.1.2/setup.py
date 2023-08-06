import setuptools
from links_referrer.version import Version
setuptools.setup(name='links_referrer',
                 version=Version('0.1.2').number,
                 description='Links referrer (for traffic)',
                 long_description_content_type="text/markdown",
                 long_description=open('README.md').read().strip(),
                 author='@KM8Oz (kmoz000)',
                 author_email='<kimo@oldi.dev>',
                 url='https://github.com/KM8Oz/insta_refs.git',
                 py_modules=['links_referrer'],
                 install_requires=[],
                 license='MIT License',
                 keywords=['Traffic', 'SEO', 'shortlink', 'shortner', 'referral', 'links'],
                 classifiers=['Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License', 'Topic :: Communications :: Email'])
