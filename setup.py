from pip._internal import main as pip_main

def install_packages_from_requirements(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                pip_main(['install', line.strip()])

if __name__ == '__main__':
    install_packages_from_requirements('post-install.txt')
