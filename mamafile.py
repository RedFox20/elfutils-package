import mama
import os
from mama.utils.system import console
from mama.utils.gnu_project import BuildProduct

# Explore Mama docs at https://github.com/RedFox20/Mama
class elfutils(mama.BuildTarget):

    local_workspace = 'packages'

    def init(self):
        self.elfutils = self.gnu_project('elfutils', '0.189',
            url='https://sourceware.org/elfutils/ftp/0.189/{{project}}.tar.bz2',
            build_products=[
                BuildProduct('{{installed}}/lib/libelf.so', None),
                BuildProduct('{{installed}}/lib/libdw.so', None),
            ])

    def settings(self):
        self.config.prefer_gcc(self.name)
        if self.mips:
            self.config.set_mips_toolchain('mipsel')

    def dependencies(self):
        self.add_git('zlib', 'https://github.com/RedFox20/zlib-package.git')

    def build(self):
        if self.elfutils.should_build():
            opts = '--enable-static --disable-shared'
            opts += ' --disable-rpath' # do not hardcode runtime library paths
            opts += ' --disable-largefile' # omit support for large files
            opts += ' --disable-nls' # globalization translation (unnecessary)
            opts += ' --with-zlib' # use zlib
            opts += ' --disable-debuginfod --enable-libdebuginfod=dummy' # disable debuginfod server
            zlib = self.find_target('zlib')
            include = zlib.exported_includes[0]
            library = os.path.dirname(zlib.exported_libs[0])
            self.elfutils.extra_env['CFLAGS'] = f"-fPIC -I{include} -L{library}"
            self.elfutils.build(opts, multithreaded=True)
        else:
            console('lib/libdw.so and lib/libelf.so already built', color='green')

    def package(self):
        self.export_include('iptables-built/include', build_dir=True)
        self.export_lib('elfutils-built/lib/libelf.so', build_dir=True)
        self.export_lib('elfutils-built/lib/libdw.so', build_dir=True)
