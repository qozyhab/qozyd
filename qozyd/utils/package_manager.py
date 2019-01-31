import subprocess
import sys
from xmlrpc.client import ServerProxy
from pkg_resources import parse_version
import pkg_resources
import docutils.core


class PackageManager():
    PYPI_XMLRCP_ENDPOINT = "https://pypi.org/pypi"

    def get_available_plugins(self):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points('qozy.plugins')
        }

        return plugins

    def get_installed_packages(self):
        packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        packages = packages.decode()

        for package_line in packages.split():
            name, version = package_line.split("==")

            yield name, parse_version(version)

    def install_package(self, name, version):
        return subprocess.check_call([sys.executable, '-m', 'pip', 'install', '%s==%s' % (name, version)])


    def uninstall_package(self, name):
        return subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', name])


    def find_packages_by_classifier(self, classifier):
        installed_packages = dict(self.get_installed_packages())

        client = ServerProxy(self.PYPI_XMLRCP_ENDPOINT)
        packages = client.browse([classifier])

        for package, version in packages:
            release_data = client.release_data(package, version)
            
            version = parse_version(release_data["version"])

            name = release_data["name"]
            is_installed = name in installed_packages
            is_upgradable = installed_packages[name] < version if is_installed else False

            yield {
                "name": name,
                "version": release_data["version"],
                "author": release_data["author"],
                "authorEmail": release_data["author_email"],
                "summary": release_data["summary"],
                "description": docutils.core.publish_parts(release_data["description"], writer_name="html")["html_body"],
                "installed": is_installed,
                "upgradable": is_upgradable,
            }