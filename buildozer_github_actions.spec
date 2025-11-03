[app]

# (str) Title of your application
title = نظام السوبر ماركت

# (str) Package name
package.name = supermarket

# (str) Package domain (needed for android/ios packaging)
package.domain = com.supermarket.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,ttf,db

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,sqlite3,requests

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, portrait, all or unset)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25.2.9519653

# (str) Android SDK version to use
android.sdk = 33

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.androidx is currently only supported with Gradle plugin 3.5+
android.enable_androidx = True

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (bool) Enable AndroidX bundle. 
android.enable_androidx_bundle = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (bool) Enable Android App Bundle support (only works with buildozer >= 1.2.0)
android.enable_android_app_bundle = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternatively, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency... ios_ignore_simulator is only available for iOS 9 and above
#ios_ignore_simulator = True

# (bool) Enables or disables the "ios_ignore_simulator" option, which skips ios app build if simulator target is selected
ios_ignore_simulator = True

# (bool) Enables or disables the "ios_allow_debugging" option (only works with buildozer >= 1.2.0)
ios_allow_debugging = False

[androidx]

# enable AndroidX support
enable_androidx = True

# (list) add AndroidX package dependencies
#androidx_packages = any#pattern to match androidx packages
androidx_packages = 

# (bool) Enable AndroidX Bundle. 
enable_androidx_bundle = True

# (list) add compileSdk deps
android_compile_sdk_version = 33
android_compile_sdk_test_version = 33

# (list) add buildtools deps  
android_buildtools_version = 33.0.2

# (list) add manifest deps
android_manifest_version = 33

# (list) add minSdk deps
android_min_sdk_version = 21
android_min_sdk_test_version = 21

# (list) add ndk deps  
android_ndk_version = 25.2.9519653
android_ndk_version_alt = 25.2.9519653
android_ndk_test_version = 25.2.9519653

# (list) add cmake deps
android_cmake_version = 3.22.1

# (str) Extra cmake flags
android_extra_cmake_options = 

# (str) gradle_dependencies extra gradle deps
android_gradle_dependencies = 

# (list) gradle bundled deps
android_gradle_bundled = 

# (str) sdk deps
android_sdk_version = 33

# (str) add java compile options
android_add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

[distribution]

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternatively, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency... ios_ignore_simulator is only available for iOS 9 and above
#ios_ignore_simulator = True

# (bool) Enables or disables the "ios_ignore_simulator" option, which skips ios app build if simulator target is selected
ios_ignore_simulator = True

# (bool) Enables or disables the "ios_allow_debugging" option (only works with buildozer >= 1.2.0)
ios_allow_debugging = False

[buildozer.ios]

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternatively, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency... ios_ignore_simulator is only available for iOS 9 and above
#ios_ignore_simulator = True

# (bool) Enables or disables the "ios_ignore_simulator" option, which skips ios app build if simulator target is selected
ios_ignore_simulator = True

# (bool) Enables or disables the "ios_allow_debugging" option (only works with buildozer >= 1.2.0)
ios_allow_debugging = False