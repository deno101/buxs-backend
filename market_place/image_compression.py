from PIL import Image
import threading


class Compression:
    MARKETPLACE = 1
    FASTFOOD = 2

    origin = None
    image_dir_marketplace = 'img/marketplace/'
    image_dir_fastfood = 'img/fastfood/'
    data = None

    def __init__(self, origin='', data=None, destination='', const=MARKETPLACE):
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

        if const == self.MARKETPLACE:
            self.image_dir = self.image_dir_marketplace
        elif const == self.FASTFOOD:
            self.image_dir = self.image_dir_fastfood

        if destination is None:
            self.destination = origin

    def compress(self):
        threading.Thread(target=self.__create_compressed_thread).start()

    def __create_compressed_thread(self):
        with open(self.image_dir + self.origin, 'wb') as infile:
            try:
                for chunks in self.data.chunks():
                    infile.write(chunks)
            except AttributeError:
                infile.write(self.data)

        img = Image.open(self.image_dir + self.origin)
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = img.convert('RGB')
        img.save(self.image_dir + "compressed/" + self.destination, 'JPEG', quality=75, optimize=True)
