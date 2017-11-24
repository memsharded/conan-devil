from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, replace_in_file
import os


class DevilConan(ConanFile):
    name = "DevIL"
    version = "1.8.0"
    license = "LGPL License http://openil.sourceforge.net/license.php"
    url = "https://github.com/whitebatman2/conan-devil"
    requires = "zlib/1.2.8@lasote/stable", "libpng/1.6.21@lasote/stable", "libtiff/4.0.6@bilke/stable", "libjpeg/9a@Kaosumaru/stable"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True", "zlib:shared=True", "libpng:shared=True"
    generators = "cmake"

    def source(self):

        zip_name = "v%s.zip" % self.version
        download("https://github.com/DentonW/DevIL/archive/%s" % zip_name, zip_name, verify=True)
        unzip(zip_name)
        os.unlink(zip_name)
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("./DevIL-%s/DevIL/CMakeLists.txt" % self.version, "project(ImageLib)", '''project(TImageLib)
                                include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                                conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.run("cmake ./DevIL-%s/DevIL %s" % (self.version, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*", dst="include", src="DevIL-%s/DevIL/include" % self.version)
        self.copy("*", dst="bin", src="bin")
        		
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            elif self.settings.os == "Windows":
			    self.copy(pattern="*.lib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["DevIL"]
