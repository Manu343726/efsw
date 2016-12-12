from conans import ConanFile, CMake
from conans.tools import download, untargz
import os, glob

class Efsw(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    name = 'efsw'
    url = 'https://github.com/Manu343726/efsw'
    license = 'MIT'
    version = '1.0.0'
    options = {
        'shared': [True, False],
        'fPIC': [True, False]
    }
    default_options = (
        'shared=False',
        'fPIC=False'
    )
    generators = 'cmake'

    @property
    def sourcedir(self):
        return os.path.join(os.getcwd(), self.name)

    def source(self):
        downloaded_tar = '{}.tar.gz'.format(self.name)
        url = 'https://bitbucket.org/SpartanJ/efsw/get/{}.tar.gz'.format(self.version)
        self.output.info('Downloading efsw {} from {} ...'.format(self.version, url))
        download(url, downloaded_tar)

        self.output.info('Extracting {} ...'.format(downloaded_tar))
        untargz(downloaded_tar)
        globstring = os.path.join(self.conanfile_directory, 'SpartanJ-efsw-*')
        self.output.info(' - src: {}'.format(os.path.join(os.getcwd(), downloaded_tar)))
        globlist = glob.glob(os.path.join(os.getcwd(), 'SpartanJ-efsw*'))

        if len(globlist) == 1:
            self.output.info(' - dst: {}'.format(globlist[0]))
            os.rename(globlist[0], self.sourcedir)
        else:
            raise RuntimeError('No extracted efsw folder (\'SpartanJ-efsw-<commit hash>\') found!')

    def build(self):
        cmake = CMake(self.settings)
        self.output.info('Configure and build...'.format(self.options.shared))
        options  = ' -DSTATIC_LIB=' + ('OFF' if self.options.shared else 'ON')
        options += ' -DCMAKE_POSITION_INDEPENDENT_CODE=' + ('ON' if self.options.fPIC else 'OFF')
        self.output.info(' - cmake options: {}'.format(options))
        self.run('cmake {} {} {}'.format(self.sourcedir, cmake.command_line, options))
        self.run('cmake --build . {}'.format(cmake.build_config))

    def package(self):
        includedir = os.path.join('include', 'efsw')
        src_includedir = os.path.join('efsw', includedir)

        self.copy(os.path.join(src_includedir, '*.h'), dst=includedir, keep_path=False)
        self.copy(os.path.join(src_includedir, '*.hpp'), dst=includedir, keep_path=False)
        self.copy('*.a', dst='lib')
        self.copy('*.so', dst='lib')
        self.copy('*.lib', dst='lib')
        self.copy('*.dll', dst='lib')

    def package_info(self):
        self.cpp_info.libs = ['efsw']

        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
