from setuptools import find_packages, setup

package_name = 'percepto_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rishabh',
    maintainer_email='rishabh@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "visual_feed=percepto_planner.visual_feed:main",
            "sorting_assigner=percepto_planner.sorting_assigner:main",
            "path_planner=percepto_planner.path_planner:main",
            "timerthreadtest=percepto_planner.timerthreadtest:main"
        ],
    },
)
