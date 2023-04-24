import hashlib
import sys

import numpy
import os
import re
import glob
import numpy as np
import tifffile
import argparse
from pathlib import Path

class Reader(object):
    """
    The superclass containing those functions that
    are common to reading a STORM movie file.
    Subclasses should implement:
     1. __init__(self, filename, verbose = False)
        This function should open the file and extract the
        various key bits of meta-data such as the size in XY
        and the length of the movie.
     2. loadAFrame(self, frame_number)
        Load the requested frame and return it as numpy array.
    """

    def __init__(self, filename, verbose=False):
        super(Reader, self).__init__()
        self.filename = filename
        self.fileptr = None
        self.verbose = verbose

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.close()

    def averageFrames(self, start=None, end=None):
        """
        Average multiple frames in a movie.
        """
        length = 0
        average = numpy.zeros((self.image_height, self.image_width), numpy.float)
        for [i, frame] in self.frameIterator(start, end):
            if self.verbose and ((i % 10) == 0):
                print(" processing frame:", i, " of", self.number_frames)
            length += 1
            average += frame

        if (length > 0):
            average = average / float(length)

        return average

    def close(self):
        if self.fileptr is not None:
            self.fileptr.close()
            self.fileptr = None

    def filmFilename(self):
        """
        Returns the film name.
        """
        return self.filename

    def filmSize(self):
        """
        Returns the film size.
        """
        return [self.image_width, self.image_height, self.number_frames]

    def filmLocation(self):
        """
        Returns the picture x,y location, if available.
        """
        if hasattr(self, "stage_x"):
            return [self.stage_x, self.stage_y]
        else:
            return [0.0, 0.0]

    def filmScale(self):
        """
        Returns the scale used to display the film when
        the picture was taken.
        """
        if hasattr(self, "scalemin") and hasattr(self, "scalemax"):
            return [self.scalemin, self.scalemax]
        else:
            return [100, 2000]

    def frameIterator(self, start=None, end=None):
        """
        Iterator for going through the frames of a movie.
        """
        if start is None:
            start = 0
        if end is None:
            end = self.number_frames

        for i in range(start, end):
            yield [i, self.loadAFrame(i)]

    def hashID(self):
        """
        A (hopefully) unique string that identifies this movie.
        """
        return hashlib.md5(self.loadAFrame(0).tobytes()).hexdigest()

    def loadAFrame(self, frame_number):
        assert frame_number >= 0, "Frame_number must be greater than or equal to 0, it is " + str(frame_number)
        assert frame_number < self.number_frames, "Frame number must be less than " + str(self.number_frames)

    def lockTarget(self):
        """
        Returns the film focus lock target.
        """
        if hasattr(self, "lock_target"):
            return self.lock_target
        else:
            return 0.0


class DaxReader(Reader):
    """
    Dax reader class. This is a Zhuang lab custom format.
    """

    def __init__(self, filename, verbose=False):
        super(DaxReader, self).__init__(filename, verbose=verbose)

        # save the filenames
        dirname = os.path.dirname(filename)
        if (len(dirname) > 0):
            dirname = dirname + "/"
        self.inf_filename = dirname + os.path.splitext(os.path.basename(filename))[0] + ".inf"

        # defaults
        self.image_height = None
        self.image_width = None

        # extract the movie information from the associated inf file
        size_re = re.compile(r'frame dimensions = ([\d]+) x ([\d]+)')
        length_re = re.compile(r'number of frames = ([\d]+)')
        endian_re = re.compile(r' (big|little) endian')
        stagex_re = re.compile(r'Stage X = ([\d\.\-]+)')
        stagey_re = re.compile(r'Stage Y = ([\d\.\-]+)')
        lock_target_re = re.compile(r'Lock Target = ([\d\.\-]+)')
        scalemax_re = re.compile(r'scalemax = ([\d\.\-]+)')
        scalemin_re = re.compile(r'scalemin = ([\d\.\-]+)')

        inf_file = open(self.inf_filename, "r")
        while 1:
            line = inf_file.readline()
            if not line: break
            m = size_re.match(line)
            if m:
                self.image_height = int(m.group(2))
                self.image_width = int(m.group(1))
            m = length_re.match(line)
            if m:
                self.number_frames = int(m.group(1))
            m = endian_re.search(line)
            if m:
                if m.group(1) == "big":
                    self.bigendian = 1
                else:
                    self.bigendian = 0
            m = stagex_re.match(line)
            if m:
                self.stage_x = float(m.group(1))
            m = stagey_re.match(line)
            if m:
                self.stage_y = float(m.group(1))
            m = lock_target_re.match(line)
            if m:
                self.lock_target = float(m.group(1))
            m = scalemax_re.match(line)
            if m:
                self.scalemax = int(m.group(1))
            m = scalemin_re.match(line)
            if m:
                self.scalemin = int(m.group(1))

        inf_file.close()

        # set defaults, probably correct, but warn the user
        # that they couldn't be determined from the inf file.
        if not self.image_height:
            print("Could not determine image size, assuming 256x256.")
            self.image_height = 256
            self.image_width = 256

        # open the dax file
        if os.path.exists(filename):
            self.fileptr = open(filename, "rb")
        else:
            if self.verbose:
                print("dax data not found", filename)

    def loadAFrame(self, frame_number):
        """
        Load a frame & return it as a numpy array.
        """
        super(DaxReader, self).loadAFrame(frame_number)

        self.fileptr.seek(frame_number * self.image_height * self.image_width * 2)
        image_data = numpy.fromfile(self.fileptr, dtype='uint16', count=self.image_height * self.image_width)
        image_data = numpy.reshape(image_data, [self.image_height, self.image_width])
        if self.bigendian:
            image_data.byteswap(True)
        return image_data


parser = argparse.ArgumentParser()

parser.add_argument("input_path")
#parser.add_argument("output path")

args = parser.parse_args()

print(args.input_path)



if os.path.exists(args.input_path):
    os.chdir(args.input_path)
else:
    print("Cannot access target directory. Exiting...")
    sys.exit()


for index, file in enumerate(glob.glob("*.dax"), start=1):
    print(f"Converting file {index} of ")
    daxfile = DaxReader(file, verbose=True)
    frames_list = []
    for frame in range(daxfile.number_frames):
        frame_array = daxfile.loadAFrame(frame)
        frames_list.append(frame_array)
    frame_stack = np.stack(frames_list)
    tiff_name = os.path.splitext(daxfile.filename)[0] + '.tif'
    tifffile.imwrite(tiff_name, frame_stack)







