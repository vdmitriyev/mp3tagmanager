__license__ = "MIT"
__version__ = "1.1"
__created__    = "07.02.2014"
__updated__    = "21.02.2019"
__description__ = "Assigning right tags(title, artist, album) to the MP3 files located in a specified folder."

import os
import sys
import codecs
import argparse
import artists

import mutagen
from mutagen.easyid3 import EasyID3

# helpers

from folder_iterator import FolderIterator

class ChangeMP3Tags():

    exceptional_artists = list()

    def __init__(self, folder):

        iterator = FolderIterator()
        print ('[i] Following folder will be processed: {0}'.format(folder))

        self.mp3_files_list = iterator.iterate_through_catalog(folder)
        #self.read_exeptional_artists()
        self.exceptional_artists = artists.artists

    # def read_exeptional_artists(self):
    #     _file = codecs.open('artists.txt', "r", "utf8")
    #     line = _file.readline()
    #     while line:
    #         self.exceptional_artists.append(line)
    #         line = _file.readline()
    #     _file.close()

    # def save_to_file(self, data_as_set , append = False):
    #     file_name = 'artists.txt'
    #     if append:
    #         _file = codecs.open(file_name, "a", "utf-8")
    #     else:
    #         _file = codecs.open(file_name, "w", "utf-8")
    #     for value in data_as_set:
    #         _file.write(value + '\n')
    #     _file.close()

    def split_helper_01(self, input_array, delim):
        """
            (obj, list, str) -> list

            Splitting file name of mp3 with more than one '-' delimter inside.
        """

        result = list()
        size = len(input_array)

        firt_part = ''
        firt_part = input_array[0]
        for index in range(1, size-1):
            firt_part = firt_part + delim + input_array[index]

        second_part = input_array[ size - 1]

        result.append(firt_part)
        result.append(second_part)

        return result

    def remove_dubled_delims(self, file_name, delim):
        """
            (obj, list, str) -> list

            Dealing with files names having douled (or more) number of delimters.
        """

        found = False
        result = list()
        for value in self.exceptional_artists:
            if file_name.find(value) >= 0:
                found = True
                splitted = file_name.split(delim)
                part2 = ''
                for tmp_part in splitted:
                    part2 += ' ' + tmp_part
                part2 = part2[len(value.decode("utf8"))+1:]
                result.append(value)
                result.append(part2)

        if not found:
            result = self.split_helper_01(file_name.split(delim), delim)

        return result


    def split_name(self, _input, delims=[ u'-', u'–', u'-']):
        """
            (obj, str, str) -> []

            Splits the name of the file by the given delimeter to extract title and artist.
        """

        result = ["", ""]

        try:

            file_name = _input[_input.rfind('\\')+1:]
            file_name = file_name[:file_name.rfind('.')]
            result = ["", file_name]
        except Exception as e:
            print ('[e] Exception : ' + str(e))
            file_name = 'NoName - NoName'

        found = False
        for delim in delims:
            if delim in file_name:
                try:
                    temp_split = file_name.split(delim)
                    if len(temp_split) > 2:
                        #self.save_to_file({file_name}, True)
                        result = self.remove_dubled_delims(file_name, delim)
                    else:
                        result = temp_split
                except Exception as e:
                    print ('[e] exception in mtd "split_name": ' + str(e))
                found = True
                break

        if not found:
            result = ["", file_name]
        #print (result)
        return result

    def change_tags(self, file_name):
        '''
            (obj, str) -> None

            Change the tags of the given file name.
        '''

        names = self.split_name(file_name)

        print (file_name)
        try:
            meta = EasyID3(file_name)
            meta.delete()
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(file_name, easy=True)
            meta.add_tags()

        artist, title = '', ''

        try:
            artist = names[0]#.encode('UTF-8')
            title = names[1]#.encode('UTF-8')
        except Exception as ex:
            print ('[e] exception in mtd "change_tags": ' + str(e))

        meta['artist'] = artist.strip()
        meta['title'] = title.strip()
        meta['album'] = artist.strip()
        #print (artist, title)
        meta.save(file_name, v2_version=3)

    def process(self):
        """
            (obj) -> None

            Process the whole mp3 files that are specified.
        """

        for folder in self.mp3_files_list:
            print ('\t' + folder)
            for file_name in self.mp3_files_list[folder]:
                try:
                    self.change_tags(folder + '\\' + file_name)
                except Exception as e:
                     print ('[e] exception in mtd "process": ' + str(e))

def main(folder):
    ''' Create MP3 changer and starting processing '''

    changer = ChangeMP3Tags(folder)
    changer.process()

if __name__ == '__main__':

    # setting system default encoding to the UTF-8
    #reload(sys)
    #sys.setdefaultencoding('UTF8')

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--folder", required=True, help="folder with MP3 files")
    args = vars(ap.parse_args())
    main(folder = args['folder'])

