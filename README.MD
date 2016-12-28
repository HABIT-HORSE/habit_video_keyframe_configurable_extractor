Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham

Can only open AVI video files - should work with MP4 files.

I ran into this issue using OpenCV version 2.4.11 and Python 2.7 under a Windows 7 operating system. I wasn't able to open and manipulate mp4 files, but was able to open avi files.

The solution in my case was to copy the opencv_ffmpeg2411.dll file from the build folder of my OpenCV installation, and paste it into the root folder of my Python installation. So, in my case, the DLL file is in "C:\dev\opencv\build\x86\vc12\bin", and I copied it to "C:\Program Files(x86)\Python2.7".