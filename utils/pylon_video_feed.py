from pypylon import pylon
import platform

if __name__ == '__main__':
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # demonstrate some feature access
    new_width = camera.Width.GetValue() - camera.Width.GetInc()
    if new_width >= camera.Width.GetMin():
        camera.Width.SetValue(new_width)

    numberOfImagesToGrab = 5
    camera.StartGrabbingMax(numberOfImagesToGrab)
    img = pylon.PylonImage()

    i = 1
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data.
            print("SizeX: ", grabResult.Width)
            print("SizeY: ", grabResult.Height)
            img_arr = grabResult.Array
            print("Gray value of first pixel: ", img_arr[0, 0])
        
        img.AttachGrabResultBuffer(grabResult)
        if platform.system() == 'Windows':
            # The JPEG format that is used here supports adjusting the image
            # quality (100 -> best quality, 0 -> poor quality).
            ipo = pylon.ImagePersistenceOptions()
            quality = 90 - i * 10
            ipo.SetQuality(quality)

            filename = "saved_pypylon_img_%d.jpeg" % quality
            img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
        else:
            filename = "saved_pypylon_img_%d.png" % i
            img.Save(pylon.ImageFileFormat_Png, filename)
        i += 1

        img.Release()
        grabResult.Release()
    camera.Close()