import os
import subprocess
import sys
import tkFileDialog, tkMessageBox
from Tkinter import *


class ImageConverter:

    def converter(self, path, image_path, image_name, format, quality):
        output = path+"/new/" + image_name.rpartition('.')[0] + "." + format
        subprocess.call(["convert", "-quality", quality, image_path, output])
        return output

    def get_files_num(self, path):
        total = 0

        for root, dirs, files in os.walk(path):
            if "new" in dirs:
                dirs.remove("new")
            for file in files:
                for ext in ['.jpg', '.png', '.tif', '.JPG']:
                    if file.endswith(ext):
                        total += 1
        return total



    def getImgList(self, path, format, quality):
        output = ""
        i = 0
        total = self.get_files_num(path) 
        for root, dirs, files in os.walk(path):
            if "new" in dirs:
                dirs.remove("new")
            for file in files:
                for ext in ['.jpg', '.png', '.tif', '.JPG']:
                    if file.endswith(ext):
                        i += 1
                        img_path = root+"/"+file
                        file_name = file
                        print "Processing: " + file + " img %d of %d" % (i,total)
                        output = self.converter(path, img_path, file_name, format, quality)
        return i


class GUI:
  def __init__(self, genitore):

    #------ costanti per il controllo della disposizione
    larghezza_pulsanti = 8  ### (1)

    imb_pulsantex = "2m"  ### (2)
    imb_pulsantey = "1m"  ### (2)

    imb_quadro_pulsantix = "3m"       ### (3)
    imb_quadro_pulsantiy = "2m"       ### (3)
    imb_int_quadro_pulsantix = "3m"   ### (3)
    imb_int_quadro_pulsantiy = "1m"   ### (3)
    #------------------ fine costanti -------------------

    self.mioGenitore = genitore
    self.quadro_pulsanti = Frame(genitore)

    self.quadro_pulsanti.pack(  ### (4)
      ipadx = imb_int_quadro_pulsantix,  ### (3)
      ipady = imb_int_quadro_pulsantiy,  ### (3)
      padx = imb_quadro_pulsantix,       ### (3)
      pady = imb_quadro_pulsantiy,       ### (3)
      )

    self.pulsante1 = Button(self.quadro_pulsanti,
                            command = self.pulsante1Premuto)
    self.pulsante1.configure(text = "Convert", background = "green")
    self.pulsante1.focus_force()
    self.pulsante1.configure(
      width = larghezza_pulsanti,  ### (1)
      padx = imb_pulsantex,  ### (2)
      pady = imb_pulsantey   ### (2)
      )

    self.pulsante1.pack(side = LEFT)
    self.pulsante1.bind("<Return>", self.pulsante1Premuto_a)

    self.pulsante2 = Button(self.quadro_pulsanti,
                            command = self.pulsante2Premuto)
    self.pulsante2.configure(text = "Close", background = "red")
    self.pulsante2.configure(
      width = larghezza_pulsanti,  ### (1)
      padx = imb_pulsantex,  ### (2)
      pady = imb_pulsantey   ### (2)
      )

    self.pulsante2.pack(side = RIGHT)
    self.pulsante2.bind("<Return>", self.pulsante2Premuto_a)

    optionFrame = Frame(genitore)
    optionLabel = Label(optionFrame)
    optionLabel["text"] = "Select destination format: "
    optionLabel.pack(side=LEFT)
    variable = StringVar(optionFrame)
    variable.set("jpg")  # default value
    w = OptionMenu(optionFrame, variable, "jpg", "png")
    w.pack(side=RIGHT)
    optionFrame.pack()

    optionFrame2 = Frame(genitore)
    optionLabel2 = Label(optionFrame2)
    optionLabel2["text"] = "Select quality level: "
    optionLabel2.pack(side=LEFT)
    variable2 = StringVar(optionFrame2)
    variable2.set("100%")  # default value
    q = OptionMenu(optionFrame2, variable2, '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%')
    q.pack(side=RIGHT)
    optionFrame2.pack()

    self.optionFormat = w
    self.optionQuality = q


  def pulsante1Premuto(self):
      format = self.optionFormat.cget("text")
      quality = self.optionQuality.cget("text")
      dir_path = tkFileDialog.askdirectory()
      new_path = dir_path+"/new"
      os.system("mkdir " + new_path)
      os.system("rm " + dir_path+"/new/*")
      number = ImageConverter().getImgList(dir_path, format, quality)
      if number != 0:
        message = "Conversion complete! \n "
      else:
        message = "No images found! \n "
      tkMessageBox.showinfo("Info", message + str(number) +
                            " converted images")
      self.pulsante1["background"] = "green"


  def pulsante2Premuto(self):
    self.mioGenitore.destroy()

  def pulsante1Premuto_a(self, event):
    self.pulsante1Premuto()

  def pulsante2Premuto_a(self, event):
    self.pulsante2Premuto()





def main():

    radice = Tk()
    radice.title("Image Converter")
    radice.geometry('{}x{}'.format(400, 200))
    radice.option_add('*Dialog.msg.width', 40)
    miaApp = GUI(radice)
    radice.mainloop()

    pass

if __name__ == '__main__':
    main()
