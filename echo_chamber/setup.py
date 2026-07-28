from setuptools import find_packages, setup

package_name = 'echo_chamber'

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
    maintainer='tambo',
    maintainer_email='tambo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "test_node = echo_chamber.first_node:main",
            "draw_circle = echo_chamber.draw_circle:main",
            "pose_subscriber = echo_chamber.pose_subscriber:main",
            "random_number = echo_chamber.talker:main",
            "listener = echo_chamber.listener:main"
        ],
    },
)
