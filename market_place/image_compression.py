from PIL import Image
import threading


class Compression:
    origin = None
    compressed_dir = 'img/compressed/'
    image_dir = 'img/'
    data = None

    def __init__(self, origin='', data=None, destination=''):
        """

        :param origin
            -> raw uncompressed file name:
        :param data
             data from request.FILES['']
        :param destination
            where to save the file corresponds to a db field

        """
        self.origin = origin
        self.data = data
        self.destination = destination

    def compress(self):
        threading.Thread(target=self.__create_compressed_thread).start()

    def __create_compressed_thread(self):
        with open(self.image_dir + self.origin, 'wb') as infile:
            for chunks in self.data.chunks():
                infile.write(chunks)

        img = Image.open(self.image_dir + self.origin)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img.save(self.compressed_dir+self.destination, 'JPEG', quality=75, optimize=True)
